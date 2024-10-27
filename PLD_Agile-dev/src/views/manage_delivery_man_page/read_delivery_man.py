from typing import Dict, List, Tuple
from uuid import UUID

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QTableWidget, QVBoxLayout, QWidget
from reactivex import Observer, combine_latest

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import Tour
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.tour.tour_service import TourService
from src.views.ui import Button, Callout, Text, TextSize


class ReadDeliveryMan(QWidget):
    __table: QTableWidget

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.__table = QTableWidget()
        self.__table.setColumnCount(3)
        self.__table.setHorizontalHeaderLabels(["Nom", "Disponibilités", ""])
        self.__table.setColumnWidth(0, 200)
        self.__table.setColumnWidth(1, 200)

        layout.addWidget(
            Callout(
                "S'il y a des livreurs sur des tournées, vous ne pourrez pas les supprimer."
            )
        )
        layout.addWidget(self.__table)

        self.setLayout(layout)

        combine_latest(
            DeliveryManService.instance().delivery_men,
            TourService.instance().computed_tours,
        ).subscribe(lambda res: self.__update_table(res[0], res[1]))

    def __update_table(
        self, delivery_men: Dict[UUID, DeliveryMan], computed_tours: List[Tour]
    ):
        self.__table.setRowCount(0)

        for delivery_man in delivery_men.values():
            row_index = self.__table.rowCount()
            self.__table.insertRow(row_index)

            delete_button = Button(icon="trash")
            delete_button.clicked.connect(
                lambda _, delivery_man=delivery_man: self.__delete_delivery_man(
                    delivery_man
                )
            )

            if delivery_man.id in computed_tours:
                delete_button.setEnabled(False)

            self.__table.setCellWidget(row_index, 0, QLabel(delivery_man.name))
            self.__table.setCellWidget(
                row_index,
                1,
                QLabel(self.__availabilities_to_string(delivery_man.availabilities)),
            )
            self.__table.setCellWidget(row_index, 2, delete_button)

    def __availabilities_to_string(self, availabilities: List[int]) -> str:
        joined_availabilities: List[Tuple[int, int]] = []

        for availability in availabilities:
            if (
                len(joined_availabilities) == 0
                or joined_availabilities[-1][1] != availability - 1
            ):
                joined_availabilities.append((availability, availability))
            else:
                joined_availabilities[-1] = (joined_availabilities[-1][0], availability)

        return ", ".join(
            [f"{start}:00 - {end + 1}:00" for start, end in joined_availabilities]
        )

    def __delete_delivery_man(self, delivery_man: DeliveryMan) -> None:
        DeliveryManService.instance().remove_delivery_man(delivery_man)
