from dataclasses import dataclass

from src.models.map.position import Position


@dataclass
class Marker:
    """Represents a marker on the map. This is used purely for display purposes."""

    position: Position
    """Position of the marker.
    """
