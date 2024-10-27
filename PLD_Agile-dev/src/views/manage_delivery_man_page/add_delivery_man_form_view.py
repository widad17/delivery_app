from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox, QVBoxLayout
from reactivex import Observable

from src.controllers.navigator.page import Page
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.views.ui import Button, Text, TextSize


class AddDeliveryManFormView(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("Create a deliveryman", TextSize.H2)

        name_label = Text("Name", TextSize.label)
        name_input = QLineEdit()

        buttons_layout = QHBoxLayout()
        add_button = Button("Create")

        # Connect the 'clicked' signal to the handler function
        add_button.clicked.connect(self.add_delivery_man)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.addWidget(add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def add_delivery_man(self):
        name_input = self.findChild(QLineEdit)
        name = name_input.text()

        if not name:
            return  # Don't proceed if the name is empty

        # Call the service to create a delivery man
        delivery_man = DeliveryManService.instance().create_delivery_man(name)

        # Show a pop-up message
        message_box = QMessageBox()
        message_box.setWindowTitle("Success")
        message_box.setText(f"Delivery man '{delivery_man.name}' added successfully.")
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

        # Clear the input field
        name_input.clear()
