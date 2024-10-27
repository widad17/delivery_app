from typing import Optional
from uuid import UUID

from src.models.tour import DeliveryID, TourID
from src.services.command.abstract_command import AbstractCommand
from src.services.tour.tour_service import TourService


class UpdateDeliveryRequestDeliveryMan(AbstractCommand):
    __delivery_request_id: DeliveryID
    __tour_id: TourID
    __delivery_man_id: UUID
    __previous_delivery_man_id: Optional[UUID] = None

    def __init__(
        self, delivery_request_id: DeliveryID, tour_id: TourID, delivery_man_id: UUID
    ) -> None:
        super().__init__("Ajustement du livreur d'une demande de livraison")
        self.__delivery_request_id = delivery_request_id
        self.__tour_id = tour_id
        self.__delivery_man_id = delivery_man_id

    def execute(self) -> None:
        self.__previous_delivery_man_id = (
            TourService.instance().update_delivery_request_delivery_man(
                delivery_request_id=self.__delivery_request_id,
                tour_id=self.__tour_id,
                delivery_man_id=self.__delivery_man_id,
            )
        )

    def undo(self) -> None:
        if self.__previous_delivery_man_id is None:
            raise Exception("Cannot undo a command that has not been executed")

        TourService.instance().update_delivery_request_delivery_man(
            delivery_request_id=self.__delivery_request_id,
            tour_id=self.__delivery_man_id,
            delivery_man_id=self.__previous_delivery_man_id,
        )

        self.__previous_delivery_man_id = None
