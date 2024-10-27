from enum import Enum
from typing import Dict, Generic, TypeVar

from src.models.utils.tagged_collection import TaggedCollection
from src.views.main_page.map.map_annotation import MapAnnotation
from src.views.main_page.map.map_marker import MapMarker
from views.main_page.map.map_segment import MapSegment

SegmentTypes = Enum("SegmentTypes", ["Default", "Tour"])
MarkersTypes = Enum("MarkersTypes", ["Default", "Delivery"])


class MapAnnotationCollection:
    segments: TaggedCollection[SegmentTypes, MapSegment] = TaggedCollection()
    markers: TaggedCollection[MarkersTypes, MapMarker] = TaggedCollection()

    def clear_all(self) -> None:
        self.segments.clear_all()
        self.markers.clear_all()
