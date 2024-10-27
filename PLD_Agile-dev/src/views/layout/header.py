from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.services.command.command_service import CommandService
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes
from src.views.ui import Button, Callout, Separator, Text, TextSize
from src.views.ui.button_group import ButtonGroup
from src.views.ui.nav_button import NavigationButton


class Header(QWidget):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QHBoxLayout()
        title = Text("Delivery System v1.0", TextSize.H1)

        undo_button = Button(icon="undo")
        redo_button = Button(icon="redo")
        command_button_group = ButtonGroup([undo_button, redo_button])
        command_button_group.layout().setAlignment(Qt.AlignmentFlag.AlignRight)

        undo_button.clicked.connect(CommandService.instance().undo)
        redo_button.clicked.connect(CommandService.instance().redo)

        CommandService.instance().can_undo().subscribe(undo_button.setEnabled)
        CommandService.instance().can_redo().subscribe(redo_button.setEnabled)

        home_button = NavigationButton(
            text="Home",
            link=AppNavigationRoutes.MAIN,
            navigator=get_app_navigator(),
        )
        delivery_button = NavigationButton(
            text="Manage Deliverymen",
            link=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
            navigator=get_app_navigator(),
        )
        button_group = ButtonGroup([home_button, delivery_button])

        # Add components in the screen
        layout.addWidget(title)
        layout.addWidget(command_button_group)
        layout.addWidget(button_group)

        self.setLayout(layout)
