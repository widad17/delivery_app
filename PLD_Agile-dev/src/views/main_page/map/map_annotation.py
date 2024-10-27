from dataclasses import dataclass

from PyQt6.QtWidgets import QAbstractGraphicsShapeItem


@dataclass
class MapAnnotation:
    shape: QAbstractGraphicsShapeItem
    scale: float = 1
