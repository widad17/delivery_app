import concurrent.futures
import itertools
import multiprocessing
import platform
from typing import List, Optional

import networkx as nx

from src.config import Config
from src.models.map import Map, Segment
from src.models.tour import (
    DeliveriesComputingResult,
    DeliveryLocation,
    DeliveryRequest,
    TourComputingResult,
    TourRequest,
)
from src.services.singleton import Singleton


class TourComputingService(Singleton):
    def compute_tour(self, tour_request: TourRequest, map: Map) -> TourComputingResult:
        """Compute tours for a list of tour requests.

        Args:
            tour_request (TourRequest): The tour request to compute the tour for.
            map (Map): The map to compute the tour on.

        Returns:
            TourComputingResult: Result of the computation
        """
        map_graph = self.create_graph_from_map(map)
        warehouse = DeliveryRequest(
            DeliveryLocation(Segment(-1, "", map.warehouse, map.warehouse, 0), 0), 8
        )

        os_name = platform.system()
        if os_name == "Linux":
            max_deliveries_brut_force = 8
        else:
            max_deliveries_brut_force = 6

        if os_name == "Linux":
            shortest_path_graph = self.compute_shortest_path_graph_parallel(
                map_graph, [warehouse] + list(tour_request.deliveries.values())
            )
        else:
            shortest_path_graph = self.compute_shortest_path_graph(
                map_graph, [warehouse] + list(tour_request.deliveries.values())
            )

        if len(tour_request.deliveries) <= max_deliveries_brut_force:
            if os_name == "Linux":
                tsp_result = self.solve_tsp_parallel(shortest_path_graph)
            else:
                tsp_result = self.solve_tsp(shortest_path_graph)

        else:
            tsp_result = self.solve_greedy_tsp(shortest_path_graph)

        return tsp_result

    def create_graph_from_map(self, map: Map) -> nx.Graph:
        """Create a directed graph from a Map object.

        Args:
            map (Map): The Map object to create the graph from.

        Returns:
            nx.Graph: The directed graph created from the Map object.
        """
        graph = nx.DiGraph()

        graph.add_node(map.warehouse.id)

        for intersection in map.intersections.values():
            graph.add_node(
                intersection.id,
                latitude=float(intersection.latitude),
                longitude=float(intersection.longitude),
            )

        for segment in map.get_all_segments():
            graph.add_edge(
                segment.origin.id, segment.destination.id, length=segment.length
            )

        return graph

    def compute_shorted_path_graph_multiprocessing(
        self,
        graph: nx.Graph,
        shortest_path_graph: nx.DiGraph,
        source_deliveries: List[DeliveryRequest],
        target_deliveries: List[DeliveryRequest],
    ) -> nx.DiGraph:
        for source in source_deliveries:
            for target in target_deliveries:
                if source != target:
                    # add time windows constraints
                    if (
                        target.time_window + 1 <= source.time_window
                        and target != target_deliveries[0]
                    ):
                        continue
                    try:
                        shortest_path_length, shortest_path = nx.single_source_dijkstra(
                            graph,
                            source.location.segment.origin.id,
                            target.location.segment.origin.id,
                            weight="length",
                        )
                    except nx.NetworkXNoPath:
                        continue
                    shortest_path_graph.add_edge(
                        source.location.segment.origin.id,
                        target.location.segment.origin.id,
                        length=shortest_path_length,
                        path=shortest_path,
                    )
        return shortest_path_graph

    def compute_shortest_path_graph_parallel(
        self, graph: nx.Graph, deliveries: List[DeliveryRequest]
    ) -> nx.DiGraph:
        """Compute the shortest path graph between delivery locations.

        Args:
            graph (nx.Graph): The graph to compute the shortest path distances and paths between delivery locations.
            deliveries (List[DeliveryRequest]): The list of delivery requests.

        Returns:
            nx.DiGraph: The directed graph with the shortest path distances and paths between delivery locations.
        """
        G = nx.DiGraph()
        # Add delivery locations as nodes
        for delivery in deliveries:
            G.add_node(
                delivery.location.segment.origin.id, timewindow=delivery.time_window
            )

        max_cpu_count = multiprocessing.cpu_count()
        if max_cpu_count > len(deliveries):
            chunks = [deliveries]
        else:
            chunk_size = len(deliveries) // max_cpu_count
            chunks = [
                deliveries[i : i + chunk_size]
                for i in range(0, len(deliveries), chunk_size)
            ]

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_cpu_count
        ) as executor:
            futures = [
                executor.submit(
                    self.compute_shorted_path_graph_multiprocessing,
                    graph,
                    G,
                    chunk,
                    deliveries,
                )
                for chunk in chunks
            ]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

        shortest_path_graph = nx.DiGraph()
        # Merge all partial results
        for partial_shortest_path_graph in results:
            shortest_path_graph = nx.compose(
                shortest_path_graph, partial_shortest_path_graph
            )

        return shortest_path_graph

    def solve_tsp_multiprocessing(
        self, permutations_chunk, warehouse_id, shortest_path_graph: nx.DiGraph
    ):
        shortest_cycle_length = float("inf")
        shortest_cycle: List[DeliveriesComputingResult] = []
        for permuted_points in permutations_chunk:
            is_valid_tuple = True
            permuted_points = list(permuted_points)
            permuted_points = [warehouse_id] + permuted_points
            cycle_length = 0
            current_time = Config.INITIAL_DEPART_TIME

            times = []

            for i in range(len(permuted_points) - 1):
                source = permuted_points[i]
                target = permuted_points[i + 1]
                if not shortest_path_graph.has_edge(source, target):
                    is_valid_tuple = False
                    break
                travel_distance = shortest_path_graph[source][target]["length"]
                cycle_length += travel_distance

                # Check if the delivery time is within the time window
                time_window = shortest_path_graph.nodes[target]["timewindow"] * 60
                travel_time = (
                    travel_distance / 15000
                ) * 60  # Convert meters to minutes based on speed (15 km/h)
                arrival_time = current_time + travel_time

                if arrival_time < time_window:
                    # Courier arrives before the time window, wait until it starts
                    current_time = (
                        time_window + Config.DELIVERY_TIME
                    )  # Add 5 minutes for delivery
                elif arrival_time <= time_window + Config.TIME_WINDOW_SIZE:
                    # Courier arrives within the time window
                    current_time = (
                        arrival_time + Config.DELIVERY_TIME
                    )  # Add 5 minutes for delivery
                else:
                    # Courier arrives after the time window, this tuple is invalid
                    is_valid_tuple = False
                    break

                times.append(current_time - Config.DELIVERY_TIME)

            if not is_valid_tuple:
                continue
            # Add the length of the last edge back to the starting point to complete the cycle
            if not shortest_path_graph.has_edge(
                permuted_points[-1], permuted_points[0]
            ):
                continue
            cycle_length += shortest_path_graph[permuted_points[-1]][
                permuted_points[0]
            ]["length"]

            if cycle_length < shortest_cycle_length:
                shortest_cycle_length = cycle_length
                shortest_cycle = list(zip(permuted_points, [0] + times))

            return shortest_cycle, shortest_cycle_length

    def solve_tsp_parallel(self, shortest_path_graph: nx.Graph) -> TourComputingResult:
        """Solves the Traveling Salesman Problem (TSP) for a given graph of delivery points and returns the shortest route.

        Args:
            shortest_path_graph (nx.Graph): A graph representing the shortest path between delivery points.

        Returns:
            TourComputingResult: The result of the computed Tour.
        """
        shortest_cycle_length = float("inf")
        shortest_cycle: List[DeliveriesComputingResult] = []
        route = []
        # Generate all permutations of delivery points to find the shortest cycle
        delivery_points = list(shortest_path_graph.nodes())
        warehouse_id = delivery_points.pop(0)
        permutations = itertools.permutations(delivery_points)
        permutations = list(permutations)

        max_cpu_count = multiprocessing.cpu_count()
        if max_cpu_count > len(permutations):
            chunks = [permutations]
        else:
            chunk_size = len(permutations) // max_cpu_count
            chunks = [
                permutations[i : i + chunk_size]
                for i in range(0, len(permutations), chunk_size)
            ]

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_cpu_count
        ) as executor:
            futures = [
                executor.submit(
                    self.solve_tsp_multiprocessing,
                    chunk,
                    warehouse_id,
                    shortest_path_graph,
                )
                for chunk in chunks
            ]
            results = [
                future.result() for future in concurrent.futures.as_completed(futures)
            ]

            for result in results:
                if result == None:
                    continue
                if result[1] < shortest_cycle_length:
                    shortest_cycle_length = result[1]
                    shortest_cycle = result[0]

        # Compute the actual route from the shortest cycle
        if shortest_cycle == []:
            return []

        for i in range(len(shortest_cycle) - 1):
            source, source_time = shortest_cycle[i]
            target, target_time = shortest_cycle[i + 1]
            dijkstra_path = shortest_path_graph[source][target]["path"]
            route = route + dijkstra_path
            route.pop()

        # Complete the route with the path from the last delivery point to the first
        dijkstra_path = shortest_path_graph[shortest_cycle[-1][0]][
            shortest_cycle[0][0]
        ]["path"]

        route = route + dijkstra_path

        return TourComputingResult(
            route=route,
            deliveries=shortest_cycle[1:],
        )

    def solve_greedy_tsp(self, shortest_path_graph: nx.Graph) -> TourComputingResult:
        delivery_points = list(shortest_path_graph.nodes())
        warehouse_id = delivery_points.pop(0)

        current_node = warehouse_id
        unvisited_nodes = set(delivery_points)
        route = [current_node]

        while unvisited_nodes:
            # Find the nearest unvisited node among valid edges
            current_time_node = min(
                unvisited_nodes,
                key=lambda node: shortest_path_graph.nodes[node]["timewindow"],
            )
            current_time = shortest_path_graph.nodes[current_time_node]["timewindow"]
            nearest_node = None
            min_length = float("inf")
            for node in unvisited_nodes:
                if shortest_path_graph.nodes[node]["timewindow"] > current_time:
                    continue
                if shortest_path_graph.has_edge(current_node, node):
                    length = shortest_path_graph[current_node][node]["length"]
                    if length < min_length:
                        min_length = length
                        nearest_node = node

            route.append(nearest_node)
            unvisited_nodes.remove(nearest_node)
            current_node = nearest_node

        return self.return_route_from_shortest_cycle(shortest_path_graph, route)

    def return_route_from_shortest_cycle(
        self, shortest_path_graph: nx.Graph, shortest_cycle: List[int]
    ) -> Optional[TourComputingResult]:
        route = []
        deliveries: List[DeliveriesComputingResult] = []
        current_time = 8 * 60  # Starting time at the warehouse (8 a.m.)

        if len(shortest_cycle) < 2:
            return []

        for i in range(len(shortest_cycle) - 1):
            source = shortest_cycle[i]
            target = shortest_cycle[i + 1]

            if not shortest_path_graph.has_edge(source, target):
                return []

            time_window = shortest_path_graph.nodes[target]["timewindow"] * 60

            travel_distance = shortest_path_graph[source][target]["length"]
            travel_time = (
                travel_distance / 15000
            ) * 60  # Convert meters to minutes based on speed (15 km/h)
            arrival_time = current_time + travel_time

            if arrival_time < time_window:
                # Courier arrives before the time window, wait until it starts
                current_time = time_window + 5  # Add 5 minutes for delivery
            elif arrival_time <= time_window + 60:
                # Courier arrives within the time window
                current_time = arrival_time + 5  # Add 5 minutes for delivery
            else:
                return None

            deliveries.append((target, current_time - 5))

            dijkstra_path = shortest_path_graph[source][target]["path"]
            route = route + dijkstra_path
            route.pop()

        # Complete the route with the path from the last delivery point to the first
        if not shortest_path_graph.has_edge(shortest_cycle[-1], shortest_cycle[0]):
            return []

        dijkstra_path = shortest_path_graph[shortest_cycle[-1]][shortest_cycle[0]][
            "path"
        ]

        route = route + dijkstra_path

        return TourComputingResult(
            route=route,
            deliveries=deliveries,
        )

    # Check arrival time constraint
    def check_arrival_time_constraint(
        self, tsp_result: TourComputingResult, shortest_path_graph: nx.Graph
    ):
        current_time = 8 * 60  # Starting time at the warehouse (8 a.m.)
        cycle_length = 0

        for i in range(len(tsp_result.route) - 1):
            source = tsp_result[i]
            target = tsp_result[i + 1]
            travel_distance = shortest_path_graph[source][target]["length"]
            cycle_length += travel_distance

            # Check if the delivery time is within the time window
            time_window = shortest_path_graph.nodes[target]["timewindow"] * 60
            travel_time = (
                travel_distance / 15000
            ) * 60  # Convert meters to minutes based on speed (15 km/h)
            arrival_time = current_time + travel_time

            if arrival_time < time_window:
                # Courier arrives before the time window, wait until it starts
                current_time = time_window + 5  # Add 5 minutes for delivery
            elif arrival_time <= time_window + 60:
                # Courier arrives within the time window
                current_time = arrival_time + 5  # Add 5 minutes for delivery
            else:
                return False
        return True

    def compute_shortest_path_graph(
        self, graph: nx.Graph, deliveries: List[DeliveryRequest]
    ) -> nx.DiGraph:
        """Compute the shortest path graph between delivery locations.

        Args:
            graph (nx.Graph): The graph to compute the shortest path distances and paths between delivery locations.
            deliveries (List[DeliveryRequest]): The list of delivery requests.

        Returns:
            nx.DiGraph: The directed graph with the shortest path distances and paths between delivery locations.
        """
        G = nx.DiGraph()
        # Add delivery locations as nodes
        for delivery in deliveries:
            G.add_node(
                delivery.location.segment.origin.id, timewindow=delivery.time_window
            )

        # Compute the shortest path distances and paths between delivery locations
        for source in deliveries:
            for target in deliveries:
                if source != target:
                    # add time windows constraints
                    if (
                        target.time_window + 1 <= source.time_window
                        and target != deliveries[0]
                    ):
                        continue
                    try:
                        shortest_path_length, shortest_path = nx.single_source_dijkstra(
                            graph,
                            source.location.segment.origin.id,
                            target.location.segment.origin.id,
                            weight="length",
                        )
                    except nx.NetworkXNoPath:
                        continue
                    G.add_edge(
                        source.location.segment.origin.id,
                        target.location.segment.origin.id,
                        length=shortest_path_length,
                        path=shortest_path,
                    )

        return G

    def solve_tsp(self, shortest_path_graph: nx.Graph) -> TourComputingResult:
        """Solves the Traveling Salesman Problem (TSP) for a given graph of delivery points and returns the shortest route.

        Args:
            shortest_path_graph (nx.Graph): A graph representing the shortest path between delivery points.

        Returns:
            TourComputingResult: The result of the computed Tour.
        """
        shortest_cycle_length = float("inf")
        shortest_cycle: List[DeliveriesComputingResult] = []
        route = []

        # Generate all permutations of delivery points to find the shortest cycle
        delivery_points = list(shortest_path_graph.nodes())
        warehouse_id = delivery_points.pop(0)
        for permuted_points in itertools.permutations(delivery_points):
            is_valid_tuple = True
            permuted_points = list(permuted_points)
            permuted_points = [warehouse_id] + permuted_points
            cycle_length = 0
            current_time = Config.INITIAL_DEPART_TIME

            times = []

            for i in range(len(permuted_points) - 1):
                source = permuted_points[i]
                target = permuted_points[i + 1]
                if not shortest_path_graph.has_edge(source, target):
                    is_valid_tuple = False
                    break
                travel_distance = shortest_path_graph[source][target]["length"]
                cycle_length += travel_distance

                # Check if the delivery time is within the time window
                time_window = shortest_path_graph.nodes[target]["timewindow"] * 60
                travel_time = (
                    travel_distance / 15000
                ) * 60  # Convert meters to minutes based on speed (15 km/h)
                arrival_time = current_time + travel_time

                if arrival_time < time_window:
                    # Courier arrives before the time window, wait until it starts
                    current_time = (
                        time_window + Config.DELIVERY_TIME
                    )  # Add 5 minutes for delivery
                elif arrival_time <= time_window + Config.TIME_WINDOW_SIZE:
                    # Courier arrives within the time window
                    current_time = (
                        arrival_time + Config.DELIVERY_TIME
                    )  # Add 5 minutes for delivery
                else:
                    # Courier arrives after the time window, this tuple is invalid
                    is_valid_tuple = False
                    break

                times.append(current_time - Config.DELIVERY_TIME)

            if not is_valid_tuple:
                continue
            # Add the length of the last edge back to the starting point to complete the cycle
            if not shortest_path_graph.has_edge(
                permuted_points[-1], permuted_points[0]
            ):
                continue
            cycle_length += shortest_path_graph[permuted_points[-1]][
                permuted_points[0]
            ]["length"]

            if cycle_length < shortest_cycle_length:
                shortest_cycle_length = cycle_length
                shortest_cycle = list(zip(permuted_points, [0] + times))

        # Compute the actual route from the shortest cycle
        if shortest_cycle == []:
            return []

        for i in range(len(shortest_cycle) - 1):
            source, source_time = shortest_cycle[i]
            target, target_time = shortest_cycle[i + 1]
            dijkstra_path = shortest_path_graph[source][target]["path"]
            route = route + dijkstra_path
            route.pop()

        # Complete the route with the path from the last delivery point to the first
        dijkstra_path = shortest_path_graph[shortest_cycle[-1][0]][
            shortest_cycle[0][0]
        ]["path"]

        route = route + dijkstra_path

        return TourComputingResult(
            route=route,
            deliveries=shortest_cycle[1:],
        )
