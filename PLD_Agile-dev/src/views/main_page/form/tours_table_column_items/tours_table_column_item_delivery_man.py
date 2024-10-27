from typing import Dict
from uuid import UUID

from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QWidget

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import Delivery, Tour
from src.services.command.command_service import CommandService
from src.services.command.commands.update_delivery_request_delivery_man_command import (
    UpdateDeliveryRequestDeliveryMan,
)
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.tour.tour_service import TourService


class ToursTableColumnItemDeliveryMan(QWidget):
    __tour: Tour
    __delivery: Delivery
    __delivery_men_control: QComboBox

    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__()

        self.__tour = tour
        self.__delivery = delivery

        self.__build()

        delivery_man_subscription = (
            DeliveryManService.instance().delivery_men.subscribe(
                self.__update_delivery_men_control_items
            )
        )

        is_computing_subscription = TourService.instance().is_computing.subscribe(
            self.__handle_is_computing
        )

        self.destroyed.connect(delivery_man_subscription.dispose)
        self.destroyed.connect(is_computing_subscription.dispose)

    def __build(self):
        self.__build_delivery_men_control()

        layout = QHBoxLayout()
        layout.addWidget(self.__delivery_men_control)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def __build_delivery_men_control(self):
        self.__delivery_men_control = QComboBox()

    def __update_delivery_men_control_items(self, delivery_men: Dict[int, DeliveryMan]):
        try:
            self.__delivery_men_control.clear()
        except:
            return

        try:
            self.__delivery_men_control.currentIndexChanged.disconnect()
        except TypeError:
            pass

        for i, delivery_man in enumerate(delivery_men.values()):
            self.__delivery_men_control.addItem(
                delivery_man.name, userData=delivery_man.id
            )

            if self.__tour.delivery_man.id == delivery_man.id:
                self.__delivery_men_control.setCurrentIndex(i)

        self.__delivery_men_control.currentIndexChanged.connect(
            lambda: self.__handle_delivery_man_change(
                self.__delivery_men_control.currentData()
            )
        )

    def __handle_delivery_man_change(self, delivery_man_id: UUID):
        if delivery_man_id is None or delivery_man_id == self.__tour.delivery_man.id:
            return

        CommandService.instance().execute(
            UpdateDeliveryRequestDeliveryMan(
                delivery_request_id=self.__delivery.id,
                tour_id=self.__tour.id,
                delivery_man_id=delivery_man_id,
            )
        )

    def __handle_is_computing(self, is_computing: bool):
        try:
            self.setEnabled(not is_computing)
        except:
            pass
