from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.controllers.navigator.page import Page
from src.views.ui import Button, Callout, Separator, Text, TextSize


class DeleteDeliveryManFormView(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("Remove a deliveryman", TextSize.H2)

        options_label = Text("Select a deliveryman:", TextSize.H3)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addWidget(options_label)

        self.setLayout(layout)
