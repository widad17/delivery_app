from typing import List

import networkx as nx
from pytest import fixture

from src.models.map import Intersection, Segment
from src.models.tour import DeliveryLocation, DeliveryRequest
from src.services.tour.tour_computing_service import TourComputingService


@fixture
def tour_service():
    return TourComputingService.instance()


def test_compute_tours(tour_service):
    # tour_service.compute_tours()
    pass


def test_compute_shortest_path_graph(tour_service):
    # Create a simple graph for testing
    G = nx.DiGraph()
    G.add_node(1, latitude=0.0, longitude=0.0)
    G.add_node(2, latitude=1.0, longitude=1.0)
    G.add_node(3, latitude=2.0, longitude=2.0)
    G.add_node(4, latitude=3.0, longitude=3.0)
    G.add_edge(1, 2, length=1.0)
    G.add_edge(1, 3, length=2.0)
    G.add_edge(2, 3, length=1.5)
    G.add_edge(3, 4, length=2.5)

    # Define a set of delivery locations
    delivery_locations: List[DeliveryRequest] = [
        DeliveryRequest(
            DeliveryLocation(
                Segment(-1, "", Intersection(0, 0, i), Intersection(0, 0, i), 0), 0
            ),
            8,
        )
        for i in [1, 2, 4]
    ]

    # Compute the shortest path graph
    shortest_path_graph = tour_service.compute_shortest_path_graph(
        G, delivery_locations
    )

    # Check if the resulting graph is a valid NetworkX DiGraph
    assert isinstance(shortest_path_graph, nx.DiGraph)

    # Check if the edges and path data are correctly calculated
    assert shortest_path_graph[1][2]["length"] == 1.0
    assert shortest_path_graph[1][4]["length"] == 4.5
    assert shortest_path_graph[2][4]["length"] == 4

    assert shortest_path_graph[1][2]["path"] == [1, 2]
    assert shortest_path_graph[1][4]["path"] == [1, 3, 4]
    assert shortest_path_graph[2][4]["path"] == [2, 3, 4]


def test_solve_tsp_should_return_solution(tour_service):
    # Create a sample complete directed graph
    G = nx.DiGraph()
    G.add_node(0, timewindow=8)
    G.add_node(1, timewindow=8)
    G.add_node(2, timewindow=8)

    G.add_edge(0, 1, length=1.0, path=[0, 23, 56, 1])
    G.add_edge(1, 0, length=2.0, path=[1, 12, 16, 0])
    G.add_edge(0, 2, length=3.0, path=[0, 5, 33, 2])
    G.add_edge(2, 0, length=4.0, path=[2, 42, 27, 0])
    G.add_edge(1, 2, length=5.0, path=[1, 7, 6, 2])

    path = tour_service.solve_tsp(G)

    # Check if the above graph is a valid NetworkX DiGraph
    assert isinstance(G, nx.DiGraph)
    assert path.route == [0, 23, 56, 1, 7, 6, 2, 42, 27, 0]


def test_solve_tsp_should_return_empty_solution_if_cul_de_sac(tour_service):
    # Create a sample complete directed graph
    G = nx.DiGraph()
    G.add_node(0, timewindow=8)
    G.add_node(1, timewindow=8)
    G.add_node(2, timewindow=8)

    G.add_edge(0, 1, length=1.0, path=[0, 23, 56, 1])
    G.add_edge(1, 0, length=2.0, path=[1, 12, 16, 0])
    G.add_edge(0, 2, length=3.0, path=[0, 5, 33, 2])
    G.add_edge(1, 2, length=5.0, path=[1, 7, 6, 2])

    path = tour_service.solve_tsp(G)

    # Check if the above graph is a valid NetworkX DiGraph
    assert isinstance(G, nx.DiGraph)
    assert path == []


# Test for time window constraints
def test_solve_tsp_should_fail_if_delivery_not_in_time_window(tour_service):
    # Create a sample complete directed graph
    G = nx.DiGraph()
    G.add_node(0, timewindow=8)
    G.add_node(1, timewindow=8)
    G.add_node(2, timewindow=10)
    G.add_node(3, timewindow=11)

    G.add_edge(0, 1, length=1.0, path=[0, 23, 56, 1])
    G.add_edge(1, 0, length=2.0, path=[1, 12, 16, 0])
    G.add_edge(0, 2, length=3.0, path=[0, 5, 33, 2])
    G.add_edge(2, 0, length=4.0, path=[2, 42, 27, 0])
    G.add_edge(1, 2, length=500000000000000000.0, path=[1, 7, 6, 2])
    G.add_edge(1, 3, length=5.0, path=[1, 9, 54, 2, 3])
    G.add_edge(3, 1, length=6.0, path=[3, 54, 9, 1])
    G.add_edge(3, 2, length=7.0, path=[3, 4, 19, 2])
    G.add_edge(2, 3, length=8.0, path=[2, 4, 7, 3])
    G.add_edge(3, 0, length=555.0, path=[3, 2, 99, 33, 0])

    path = tour_service.solve_tsp(G)

    # Check if the above graph is a valid NetworkX DiGraph
    assert isinstance(G, nx.DiGraph)
    assert path == []


def test_solve_tsp_should_pass_if_delivery_in_time_window(tour_service):
    # Create a sample complete directed graph
    G = nx.DiGraph()
    G.add_node(0, timewindow=8)
    G.add_node(1, timewindow=8)
    G.add_node(2, timewindow=10)
    G.add_node(3, timewindow=11)

    G.add_edge(0, 1, length=1.0, path=[0, 23, 56, 1])
    G.add_edge(1, 0, length=2.0, path=[1, 12, 16, 0])
    G.add_edge(0, 2, length=3.0, path=[0, 5, 33, 2])
    G.add_edge(2, 0, length=4.0, path=[2, 42, 27, 0])
    G.add_edge(1, 2, length=50.0, path=[1, 7, 6, 2])
    G.add_edge(1, 3, length=5.0, path=[1, 9, 54, 2, 3])
    G.add_edge(3, 1, length=6.0, path=[3, 54, 9, 1])
    G.add_edge(3, 2, length=7.0, path=[3, 4, 19, 2])
    G.add_edge(2, 3, length=8.0, path=[2, 4, 7, 3])
    G.add_edge(3, 0, length=555.0, path=[3, 2, 99, 33, 0])

    path = tour_service.solve_tsp(G)

    # Check if the above graph is a valid NetworkX DiGraph
    assert isinstance(G, nx.DiGraph)
    assert path.route == [0, 23, 56, 1, 7, 6, 2, 4, 7, 3, 2, 99, 33, 0]
