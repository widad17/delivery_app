from dataclasses import dataclass

from src.views.main_page.map.map_annotation import MapAnnotation

AlignBottom = bool


@dataclass
class MapMarker(MapAnnotation):
    align_bottom: AlignBottom = False
