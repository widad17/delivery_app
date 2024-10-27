from enum import Enum
from typing import Optional

import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QPushButton, QWidget

from src.views.utils.theme import Color, Theme

ButtonCorners = Enum("ButtonCorners", ["ALL", "LEFT", "RIGHT", "TOP", "BOTTOM", "NONE"])


class Button(QPushButton):
    """A custom QPushButton with additional features such as rounded corners and custom styling.

    Args:
        text (Optional[str]): The text to display on the button. Defaults to None.
        icon (Optional[QIcon | str]): The icon to display on the button. Can be a QIcon object or a string representing a FontAwesome icon name. Defaults to None.
        corners (ButtonCorners): The corners of the button to round. Defaults to ButtonCorners.ALL.
        parent (Optional[QWidget]): The parent widget of the button. Defaults to None.
    """

    __disabled: bool = False
    __corners: ButtonCorners = ButtonCorners.ALL

    def __init__(
        self,
        text: Optional[str] = None,
        icon: Optional[QIcon | str] = None,
        corners: ButtonCorners = ButtonCorners.ALL,
        parent: Optional[QWidget] = None,
    ):
        if icon:
            super().__init__(
                icon=qta.icon(f"fa5s.{icon}", color="white", color_disabled="#40FFFFFF")
                if isinstance(icon, str)
                else icon,
                text=text,
                parent=parent,
            )
        else:
            super().__init__(text, parent)

        self.__corners = corners

        self._update_style()

    def setEnabled(self, enabled: bool) -> None:
        self.__disabled = not enabled
        self._update_style()
        super().setDisabled(not enabled)

    def setDisabled(self, disabled: bool) -> None:
        self.__disabled = disabled
        self._update_style()
        super().setDisabled(disabled)

    def setCorners(self, corners: ButtonCorners) -> None:
        self.__corners = corners
        self._update_style()

    def _update_style(self) -> None:
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.__get_background_color()};
                color: {self.__get_color()};
                padding: 8px 16px;
                font-weight: 500;
                {self.__get_corners()}
            }}
            QPushButton:pressed {{
                background-color: {"#80" + Color.PRIMARY.value[1:]};
            }}
        """
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def __get_background_color(self) -> str:
        if self.__disabled:
            return "#80" + Color.PRIMARY.value[1:]
        else:
            return Color.PRIMARY.value

    def __get_color(self) -> str:
        if self.__disabled:
            return "#80" + Color.PRIMARY_CONTRAST.value[1:]
        else:
            return Color.PRIMARY_CONTRAST.value

    def __get_corners(self) -> str:
        top_right, top_left, bottom_right, bottom_left = "0px", "0px", "0px", "0px"

        if self.__corners == ButtonCorners.ALL:
            top_right, top_left, bottom_right, bottom_left = "3px", "3px", "3px", "3px"
        elif self.__corners == ButtonCorners.LEFT:
            top_left, bottom_left = "3px", "3px"
        elif self.__corners == ButtonCorners.RIGHT:
            top_right, bottom_right = "3px", "3px"
        elif self.__corners == ButtonCorners.TOP:
            top_right, top_left = "3px", "3px"
        elif self.__corners == ButtonCorners.BOTTOM:
            bottom_right, bottom_left = "3px", "3px"

        return f"""
            border-top-right-radius: {top_right};
            border-top-left-radius: {top_left};
            border-bottom-right-radius: {bottom_right};
            border-bottom-left-radius: {bottom_left};
        """
