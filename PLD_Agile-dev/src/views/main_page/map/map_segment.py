from dataclasses import dataclass
from typing import Optional

from PyQt6.QtWidgets import QAbstractGraphicsShapeItem

from views.main_page.map.map_annotation import MapAnnotation


@dataclass
class MapSegment(MapAnnotation):
    arrow_shape: Optional[QAbstractGraphicsShapeItem] = None
