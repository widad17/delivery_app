from typing import Optional

from src.models.tour import DeliveryID, TourID
from src.services.command.abstract_command import AbstractCommand
from src.services.tour.tour_service import TourService


class UpdateDeliveryRequestTimeWindowCommand(AbstractCommand):
    __delivery_request_id: DeliveryID
    __tour_id: TourID
    __time_window: int
    __previous_time_window: Optional[int] = None

    def __init__(
        self, delivery_request_id: DeliveryID, tour_id: TourID, time_window: int
    ) -> None:
        super().__init__("Ajustement de la fenêtre de temps d'une demande de livraison")
        self.__delivery_request_id = delivery_request_id
        self.__tour_id = tour_id
        self.__time_window = time_window

    def execute(self) -> None:
        self.__previous_time_window = (
            TourService.instance().update_delivery_request_time_window(
                delivery_request_id=self.__delivery_request_id,
                tour_id=self.__tour_id,
                time_window=self.__time_window,
            )
        )

    def undo(self) -> None:
        if self.__previous_time_window is None:
            raise Exception("Cannot undo a command that has not been executed")

        TourService.instance().update_delivery_request_time_window(
            delivery_request_id=self.__delivery_request_id,
            tour_id=self.__tour_id,
            time_window=self.__previous_time_window,
        )

        self.__previous_time_window = None
