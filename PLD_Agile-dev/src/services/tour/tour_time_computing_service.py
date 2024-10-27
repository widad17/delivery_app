import math
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple

from models.errors.computing_errors import DeliveriesNotOnRouteError
from src.config import Config
from src.models.map import Segment
from src.models.tour import (
    ComputedDelivery,
    ComputedTour,
    DeliveryID,
    DeliveryRequest,
    TourComputingResult,
    TourRequest,
)
from src.services.map.map_service import MapService
from src.services.singleton import Singleton


class TourTimeComputingService(Singleton):
    def get_computed_tour_from_route_ids(
        self, tour_request: TourRequest, computation_result: TourComputingResult
    ) -> List[ComputedTour]:
        """Create a computed tour from a request and a computed list of route IDs.

        Args:
            tour_request (TourRequest): Tour request
            computation_result (TourComputingResult): Result from the computation

        Returns:
            List[ComputedTour]: Computed tour
        """
        delivery_requests: Dict[int, DeliveryRequest] = {
            delivery.location.segment.origin.id: delivery
            for delivery in tour_request.deliveries.values()
        }
        computed_deliveries: Dict[DeliveryID, ComputedDelivery] = {}

        for delivery_id, time_in_minutes in computation_result.deliveries:
            computed_delivery = ComputedDelivery.create_from_request(
                delivery_requests[delivery_id],
                time=self.__convert_minutes_to_time(time_in_minutes),
            )
            computed_deliveries[computed_delivery.id] = computed_delivery

        return ComputedTour.create_from_request(
            tour_request=tour_request,
            deliveries=computed_deliveries,
            route=self.__convert_route_to_segments(computation_result.route),
        )

    def __convert_route_to_segments(self, route: List[int]):
        return [
            MapService.instance().get_map().segments[origin_id][destination_id]
            for origin_id, destination_id in zip(route, route[1:])
        ]

    def __convert_minutes_to_time(self, minutes: float) -> time:
        """Convert a number of minutes to a time.

        Args:
            minutes (float): Number of minutes

        Returns:
            time: Converted time
        """
        hours, minutes = divmod(minutes, 60)
        return time(hour=int(hours), minute=int(minutes))
