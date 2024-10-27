from dataclasses import dataclass
from typing import Callable, Optional

from PyQt6.QtWidgets import QWidget

from src.models.tour import Delivery, Tour


@dataclass
class ToursTableColumn:
    header: str
    render: Callable[[Tour, Delivery], QWidget]
    width: Optional[int] = None
