from typing import Optional

from src.models.map.position import Position
from src.models.tour import DeliveryRequest, TourID
from src.services.command.abstract_command import AbstractCommand
from src.services.tour.tour_service import TourService


class AddDeliveryRequestCommand(AbstractCommand):
    __position: Position
    __tour_id: TourID
    __time_window: int
    __delivery_request: Optional[DeliveryRequest] = None

    def __init__(self, position: Position, tour_id: TourID, time_window: int) -> None:
        """
        Args:
            position (Position): Position of the delivery request
            tour_id (TourID): Tour ID to which to add the delivery request (Same as DeliveryMan ID)
            time_window (int): Time window of the delivery request
        """

        super().__init__("Ajout d'une demande de livraison")
        self.__position = position
        self.__tour_id = tour_id
        self.__time_window = time_window

    def execute(self) -> None:
        self.__delivery_request = TourService.instance().add_delivery_request(
            position=self.__position,
            tour_id=self.__tour_id,
            time_window=self.__time_window,
        )

    def undo(self) -> None:
        if not self.__delivery_request:
            raise Exception("Cannot undo a command that has not been executed")

        TourService.instance().remove_delivery_request(
            delivery_request_id=self.__delivery_request.id,
            tour_id=self.__tour_id,
        )
        self.__delivery_request = None
