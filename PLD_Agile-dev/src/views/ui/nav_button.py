from enum import Enum
from typing import Optional

from PyQt6.QtGui import QIcon

from src.controllers.navigator.navigator import Navigator
from src.views.ui.button import Button, ButtonCorners

NavigationButtonTarget = Enum("NavigationButtonTarget", ["REPLACE", "PUSH"])


class NavigationButton(Button):
    """A button that represents a navigation link in the UI.

    Args:
        text (str): The text to display on the button.
        link (str): The link to navigate to when the button is clicked.
        navigator (Navigator): The navigator object that handles the navigation logic.
        target (NavigationButtonTarget, optional): The target navigation action to perform when the button is clicked. Defaults to NavigationButtonTarget.PUSH.
        icon (Optional[QIcon], optional): The icon to display on the button. Defaults to None.
        corners (ButtonCorners, optional): The corners of the button to round. Defaults to ButtonCorners.ALL.
    """

    __active: bool = False

    def __init__(
        self,
        text: str,
        link: str,
        navigator: Navigator,
        target: NavigationButtonTarget = NavigationButtonTarget.PUSH,
        icon: Optional[QIcon] = None,
        corners: ButtonCorners = ButtonCorners.ALL,
    ):
        super().__init__(text, icon, corners)
        self.__link = link

        self.clicked.connect(
            lambda: navigator.replace(link)
            if target == NavigationButtonTarget.REPLACE
            else navigator.push(link)
        )

        navigator.current_route_name.subscribe(
            lambda route_name: self.__update_active(route_name)
        )

    def __update_active(self, route_name: str) -> None:
        self.__active = self.__link == route_name
        self.setDisabled(self.__active)
        self._update_style()

    def active(self) -> bool:
        return self.__active
