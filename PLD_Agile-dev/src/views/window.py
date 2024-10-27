from PyQt6.QtWidgets import QGridLayout, QMainWindow, QWidget

from src.services.command.commands_shortcuts import init_commands_shortcuts
from src.views.layout import Header
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.utils.theme import Color, Theme


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(1000, 630)
        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("Delivery System v1.0")

        self.setCentralWidget(self.build_central_widget())

        Theme.set_background_color(self, Color.BACKGROUND)

        init_commands_shortcuts(self)

    def build_central_widget(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        header = Header()
        router_outlet = get_app_navigator().get_router_outlet()

        widget.setLayout(layout)
        layout.addWidget(header, 0, 0)
        layout.addWidget(router_outlet, 1, 0)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)

        return widget
