from enum import Enum
from typing import Optional

from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QWidget

from src.views.utils.theme import Color


class TextSize(Enum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    label = 5


class Text(QLabel):
    """A custom QLabel widget that allows for easy styling of text.

    Args:
        text (str): The text to display.
        size (TextSize): The size of the text.
        parent (Optional[QWidget]): The parent widget.

    Attributes:
        None

    Methods:
        get_font_size(size: TextSize) -> int: Returns the font size based on the given TextSize.
        get_font_weight(size: TextSize) -> int: Returns the font weight based on the given TextSize.
        __get_color() -> str: Returns the color of the text.
        set_effects(size: TextSize) -> None: Sets the graphics effect for the text.
    """

    def __init__(
        self, text: str, size: TextSize = TextSize.H1, parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(text, parent=parent)

        self.setStyleSheet(
            f"""
            font-weight: {self.get_font_weight(size)};
            font-size: {self.get_font_size(size)}px;
            color: {self.__get_color()};
        """
        )
        self.set_effects(size)

    def get_font_size(self, size: TextSize) -> int:
        if size == TextSize.H1:
            return 18
        elif size == TextSize.H2:
            return 16
        elif size == TextSize.H3:
            return 14
        else:
            return 12

    def get_font_weight(self, size: TextSize) -> int:
        if size == TextSize.H1:
            return 700
        elif size == TextSize.H2:
            return 600
        elif size == TextSize.H3:
            return 500
        elif size == TextSize.label:
            return 600
        else:
            return 400

    def __get_color(self) -> str:
        return Color.PRIMARY_CONTRAST.value

    def set_effects(self, size: TextSize) -> None:
        if size == TextSize.label:
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(0.55)
            self.setGraphicsEffect(effect)
