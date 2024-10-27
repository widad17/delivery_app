from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget


class Callout(QLabel):
    """A custom QLabel widget that displays a callout message with a specific style.

    Args:
        text (str): The text to be displayed in the callout.
        parent (Optional[QWidget], optional): The parent widget of the callout. Defaults to None.
    """

    STYLE_SHEET = """
        color: #ffffff;
        background-color: #515764;
        font-weight: 500;
        padding: 12px;
        border-radius: 3px;
    """

    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.STYLE_SHEET)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
