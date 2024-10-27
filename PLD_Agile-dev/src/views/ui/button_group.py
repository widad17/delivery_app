from typing import List

from PyQt6 import QtCore
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from src.views.ui.button import Button, ButtonCorners


class ButtonGroup(QWidget):
    """A widget that groups a list of buttons horizontally.

    Args:
        buttons (List[Button]): A list of buttons to be grouped together.
    """

    def __init__(self, buttons: List[Button]) -> None:
        super().__init__()

        layout = QHBoxLayout()

        layout.setSpacing(1)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        for i, button in enumerate(buttons):
            if i == 0:
                button.setCorners(ButtonCorners.LEFT)
            elif i == len(buttons) - 1:
                button.setCorners(ButtonCorners.RIGHT)
            else:
                button.setCorners(ButtonCorners.NONE)

            layout.addWidget(button)
