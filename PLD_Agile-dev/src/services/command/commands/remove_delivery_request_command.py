from typing import Optional

from src.models.tour import DeliveryRequest, TourID
from src.services.command.abstract_command import AbstractCommand
from src.services.tour.tour_service import TourService


class RemoveDeliveryRequestCommand(AbstractCommand):
    __delivery_request_id: TourID
    __tour_id: Optional[TourID] = None
    __delivery_request: Optional[DeliveryRequest] = None

    def __init__(
        self, delivery_request_id: TourID, tour_id: Optional[TourID] = None
    ) -> None:
        """
        Args:
            delivery_request_id (TourID): ID of the delivery request to remove
            tour_id (Optional[TourID], optional): ID of the tour to remove the delivery from (same as DeliveryMan ID). Defaults to None.
        """
        super().__init__("Retrait d'une demande de livraison")
        self.__delivery_request_id = delivery_request_id
        self.__tour_id = tour_id

    def execute(self) -> None:
        self.__delivery_request = TourService.instance().remove_delivery_request(
            delivery_request_id=self.__delivery_request_id, tour_id=self.__tour_id
        )

    def undo(self) -> None:
        if not self.__delivery_request:
            raise Exception("No delivery request to undo")

        TourService.instance().add_delivery_request(
            position=self.__delivery_request.location.segment.origin,
            tour_id=self.__tour_id,
            time_window=self.__delivery_request.time_window,
        )
        self.__delivery_request = None
