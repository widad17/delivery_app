from typing import Dict

from PyQt6.QtCore import QObject, pyqtSignal

from src.models.tour import (
    NonComputedTour,
    Tour,
    TourComputingResult,
    TourID,
    TourRequest,
)
from src.services.map.map_service import MapService
from src.services.tour.tour_computing_service import TourComputingService
from src.services.tour.tour_time_computing_service import TourTimeComputingService


class TourComputingWorker(QObject):
    finished = pyqtSignal(object)
    __tour_requests: Dict[TourID, TourRequest]
    result: Dict[TourID, Tour]

    def __init__(self, tour_request: Dict[TourID, TourRequest]) -> None:
        super().__init__()
        self.__tour_requests = tour_request

    def run(self):
        """Long-running task."""
        map = MapService.instance().get_map()

        tours_intersection_ids: Dict[TourID, TourComputingResult] = {}

        for id, tour_request in self.__tour_requests.value.items():
            try:
                if len(tour_request.deliveries) > 0:
                    tours_intersection_ids[
                        id
                    ] = TourComputingService.instance().compute_tour(tour_request, map)
            except Exception as e:
                tours_intersection_ids[id] = []

        computed_tours: Dict[TourID, Tour] = {}

        for id, tour_intersection_ids in tours_intersection_ids.items():
            if tour_intersection_ids:
                try:
                    computed_tours[
                        id
                    ] = TourTimeComputingService.instance().get_computed_tour_from_route_ids(
                        self.__tour_requests.value[id], tour_intersection_ids
                    )
                except Exception as e:
                    computed_tours[id] = NonComputedTour.create_from_request(
                        self.__tour_requests.value[id],
                        [f"Erreur lors du calcul du temps de parcours : {str(e)}"],
                    )
            else:
                computed_tours[id] = NonComputedTour.create_from_request(
                    self.__tour_requests.value[id], ["Impossible de trouver un chemin."]
                )

        self.result = computed_tours

        self.finished.emit(2)
