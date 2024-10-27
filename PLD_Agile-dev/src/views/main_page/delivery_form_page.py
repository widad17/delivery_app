from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from src.controllers.navigator.page import Page
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import NonComputedTour, Tour, TourID
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.tour.tour_service import TourService
from src.views.main_page.form.tours_table import ToursTable
from src.views.ui import Button, Callout, Separator, Text, TextSize


class DeliveryFormPage(Page):
    __delivery_man_control: QComboBox
    __time_window_control: QComboBox
    __delivery_table: ToursTable
    __errors_container: QLayout

    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        warehouse_location_label = Text("Warehouse Location", TextSize.H2)
        add_deliveries_label = Text("Add deliveries", TextSize.H2)
        add_deliveries_click = Callout(
            "Double-click on the map to add deliveries with the selected deliveryman and time"
        )

        deliveries_label = Text("Deliveries", TextSize.H2)

        # Add components in the screen
        layout.addWidget(warehouse_location_label)
        layout.addLayout(self.__build_warehouse_location())
        layout.addWidget(Separator())
        layout.addWidget(add_deliveries_label)
        layout.addLayout(self.__build_delivery_man_form())
        layout.addWidget(add_deliveries_click)

        layout.addWidget(deliveries_label)
        layout.addLayout(self.__build_errors_container())
        layout.addLayout(self.__build_delivery_table())
        layout.addWidget(Separator())
        layout.addLayout(self.__build_load_tours())

        self.setLayout(layout)

        DeliveryManService.instance().delivery_men.subscribe(
            self.__update_delivery_man_combobox
        )
        TourService.instance().computed_tours.subscribe(
            self.__delivery_table.update_content
        )
        TourService.instance().computed_tours.subscribe(self.__update_errors)

    def compute_tour(self):
        TourService.instance().compute_tours()

    def __build_warehouse_location(self) -> QLayout:
        # Define components to be used in this screen
        layout = QHBoxLayout()

        warehouse_address_label = Text("20 avenue Albert Einstein", TextSize.label)

        layout.addWidget(warehouse_address_label)

        return layout

    def __build_delivery_man_form(self) -> QLayout:
        # Define components to be used in this screen
        layout = QHBoxLayout()

        delivery_man_layout = QVBoxLayout()
        delivery_man_combobox = QComboBox()
        delivery_man_label = Text("Deliveryman", TextSize.label)

        time_window_layout = QVBoxLayout()
        time_window_combobox = QComboBox()
        time_window_label = Text("Time window", TextSize.label)

        delivery_man_layout.addWidget(delivery_man_label)
        delivery_man_layout.addWidget(delivery_man_combobox)

        time_window_layout.addWidget(time_window_label)
        time_window_layout.addWidget(time_window_combobox)

        layout.addLayout(delivery_man_layout)
        layout.addLayout(time_window_layout)

        layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        time_window_layout.setContentsMargins(0, 0, 0, 0)
        time_window_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__delivery_man_control = delivery_man_combobox
        self.__time_window_control = time_window_combobox

        delivery_man_combobox.currentIndexChanged.connect(
            lambda: self.__update_time_window_combobox(
                delivery_man_combobox.currentData()
            )
        )

        delivery_man_combobox.currentIndexChanged.connect(
            lambda: DeliveryManService.instance().set_selected_delivery_man(
                delivery_man_combobox.currentData().id
                if delivery_man_combobox.currentData()
                else None
            )
        )
        time_window_combobox.currentIndexChanged.connect(
            lambda: DeliveryManService.instance().set_selected_time_window(
                time_window_combobox.currentData()
            )
        )

        return layout

    def __build_delivery_table(self) -> QLayout:
        # Define components to be used in this screen
        layout = QVBoxLayout()

        table = ToursTable()

        self.__delivery_table = table

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        """ compute_tour_button = Button("Compute Tour")
        compute_tour_button.clicked.connect(self.compute_tour) """

        save_tour_button = Button("Save Tour")
        save_tour_button.clicked.connect(self.__save_tour)

        # Add components in the screen
        # buttons_layout.addWidget(compute_tour_button)
        buttons_layout.addWidget(save_tour_button)

        layout.addWidget(table)
        layout.addLayout(buttons_layout)

        return layout

    def __build_load_tours(self) -> QLayout:
        # Define components to be used in this screen
        layout = QVBoxLayout()

        load_tour_label = Callout(
            "Or load an existing tour to the current deliveryman and current delivery window"
        )

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        load_tour_button = Button("Load Tour")
        load_tour_button.clicked.connect(self.__load_tour)
        buttons_layout.addWidget(load_tour_button)

        layout.addWidget(load_tour_label)
        layout.addLayout(buttons_layout)

        return layout

    def __build_errors_container(self) -> QLayout:
        # Define components to be used in this screen
        self.__errors_container = QVBoxLayout()

        return self.__errors_container

    def __update_delivery_man_combobox(
        self, delivery_men: Dict[str, DeliveryMan]
    ) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_men.values():
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)

    def __update_time_window_combobox(self, delivery_man: DeliveryMan) -> None:
        current_value = self.__time_window_control.currentData()
        self.__time_window_control.clear()

        if not delivery_man:
            return

        for time_window in delivery_man.availabilities:
            self.__time_window_control.addItem(
                f"{time_window}:00 - {time_window + 1}:00", time_window
            )

        if current_value:
            self.__time_window_control.setCurrentIndex(
                max(self.__time_window_control.findData(current_value), 0)
            )

    def __update_errors(self, tours: Dict[TourID, Tour]) -> None:
        for i in reversed(range(self.__errors_container.count())):
            self.__errors_container.itemAt(i).widget().setParent(None)

        for tour in tours.values():
            if not isinstance(tour, NonComputedTour):
                continue

            for error in tour.errors:
                error_widget = QWidget()
                error_widget.setStyleSheet(
                    "background-color: #211211; color: white; border-radius: 5px;"
                )

                error_layout = QHBoxLayout()
                error_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

                tour_color = QLabel("     ")
                tour_color.setStyleSheet(f"background-color: {tour.color};")

                error_text = QLabel(error)

                error_layout.addWidget(tour_color)
                error_layout.addWidget(error_text)
                error_widget.setLayout(error_layout)

                self.__errors_container.addWidget(error_widget)

    def __save_tour(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer des tours", "Mes tours.tour", "Tour files (*.tour)"
        )
        if file_name:
            TourService.instance().save_tours(file_name)

    def __load_tour(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir des tours", "${HOME}", "Tour files (*.tour)"
        )
        if file_name:
            TourService.instance().load_tours(file_name)

    def __show_popup(self, title, message):
        popup = QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.exec()
