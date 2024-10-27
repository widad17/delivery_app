from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from src.models.tour import Delivery, Tour
from src.services.command.command_service import CommandService
from src.services.command.commands.remove_delivery_request_command import (
    RemoveDeliveryRequestCommand,
)
from src.views.ui import Button


class ToursTableColumnItemActions(QWidget):
    __tour: Tour
    __delivery: Delivery

    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__()

        self.__tour = tour
        self.__delivery = delivery

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        remove_btn = Button(icon="trash")
        remove_btn.clicked.connect(self.__handle_remove_click)

        layout.addWidget(remove_btn)

    def __handle_remove_click(self):
        CommandService.instance().execute(
            RemoveDeliveryRequestCommand(
                delivery_request_id=self.__delivery.id,
                tour_id=self.__tour.id,
            )
        )
