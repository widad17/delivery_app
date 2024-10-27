from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QVBoxLayout

from src.controllers.navigator.page import Page
from src.services.map import MapLoaderService
from src.views.modules.main_page_navigator.navigator import get_main_page_navigator
from src.views.modules.main_page_navigator.routes import MainPageNavigationRoutes
from src.views.ui import Button, ButtonGroup, Callout, Separator, Text, TextSize

DEFAULT_BUTTONS = [
    ("Small map", "src/assets/smallMap.xml"),
    ("Medium map", "src/assets/mediumMap.xml"),
    ("Large map", "src/assets/largeMap.xml"),
]


class LoadMapPage(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()

        options_label = Text("Select an option", TextSize.H2)

        load_map_default_label = Text("Load from our default maps:", TextSize.H3)
        default_buttons = []
        for name, path in DEFAULT_BUTTONS:
            button = Button(name)
            button.clicked.connect(lambda _, path=path: self.load_map(path))
            default_buttons.append(button)
        load_map_default_button_group = ButtonGroup(default_buttons)

        separator = Separator()

        load_map_label = Callout("Or load a custom map")
        load_map_layout = QHBoxLayout()
        load_map_button = Button("Load a custom map")
        load_map_button.clicked.connect(self.ask_user_for_map)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(options_label)

        layout.addWidget(load_map_default_label)
        layout.addWidget(load_map_default_button_group)

        layout.addWidget(separator)

        layout.addWidget(load_map_label)

        load_map_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        load_map_layout.addWidget(load_map_button)
        layout.addLayout(load_map_layout)

        self.setLayout(layout)

    def ask_user_for_map(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose map", "${HOME}", "XML files (*.xml)"
        )
        if file_name:
            self.load_map(file_name)

    def load_map(self, path: str) -> None:
        MapLoaderService.instance().load_map_from_xml(path)
        get_main_page_navigator().replace(MainPageNavigationRoutes.DELIVERY_FORM)
