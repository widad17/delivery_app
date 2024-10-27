from dataclasses import dataclass
from enum import Enum
from typing import Generic, Type, TypeVar

from PyQt6.QtWidgets import QWidget

RouteName = TypeVar("RouteName", Enum, str)
"""Type of the route name.
"""


@dataclass
class Route(Generic[RouteName]):
    name: RouteName
    """Name of the route.
    """

    widget: Type[QWidget]
    """Qt widget to display as the page.
    """
