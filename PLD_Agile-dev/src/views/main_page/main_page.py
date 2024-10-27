from typing import List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QPushButton,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from src.controllers.navigator.page import Page
from src.services.map.map_service import MapService
from src.services.tour.tour_service import TourService
from src.views.modules.main_page_navigator.navigator import get_main_page_navigator
from src.views.modules.main_page_navigator.routes import MainPageNavigationRoutes
from src.views.ui.button import Button
from src.views.ui.button_group import ButtonGroup
from src.views.utils.theme import Theme
from views.main_page.map.map_view import MapView


class MainPage(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QHBoxLayout()

        # Add components in the screen
        layout.addLayout(self.__build_map_view())
        layout.addWidget(get_main_page_navigator().get_router_outlet())

        self.setLayout(layout)

    def __build_map_view(self) -> QLayout:
        # Define components to be used in this screen
        map_layout = QVBoxLayout()

        map_buttons_layout = QHBoxLayout()

        map_view = MapView()
        (
            change_map_button,
            reset_map_button,
            map_zoom_out_button,
            map_zoom_in_button,
        ) = self.__build_map_action_buttons(map_view)

        map_zoom_buttons = ButtonGroup([map_zoom_out_button, map_zoom_in_button])

        # Add components in the screen
        map_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        map_buttons_layout.addWidget(change_map_button)
        map_buttons_layout.addWidget(reset_map_button)
        map_buttons_layout.addWidget(map_zoom_buttons)

        map_layout.addWidget(map_view)
        map_layout.addLayout(map_buttons_layout)

        return map_layout

    def __build_map_action_buttons(self, map_view: MapView) -> Tuple[QWidget]:
        change_map_button = Button("Change map")
        reset_map_button = Button("Reset zoom")
        map_zoom_out_button = Button(icon="minus")
        map_zoom_in_button = Button(icon="plus")

        change_map_button.clicked.connect(lambda: self.__change_map(map_view))
        reset_map_button.clicked.connect(map_view.fit_map)
        map_zoom_out_button.clicked.connect(map_view.zoom_out)
        map_zoom_in_button.clicked.connect(map_view.zoom_in)

        map_view.ready.subscribe(
            lambda ready: [
                button.setDisabled(not ready)
                for button in [
                    change_map_button,
                    reset_map_button,
                    map_zoom_out_button,
                    map_zoom_in_button,
                ]
            ]
        )

        return (
            change_map_button,
            reset_map_button,
            map_zoom_out_button,
            map_zoom_in_button,
        )

    def __change_map(self, map_view: MapView) -> None:
        TourService.instance().clear()
        MapService.instance().clear()
        get_main_page_navigator().replace(MainPageNavigationRoutes.LOAD_MAP)
