from dataclasses import dataclass
from xml.etree.ElementTree import Element

from src.models.map.position import Position


@dataclass
class Intersection(Position):
    """Represent an intersection on the map."""

    id: int
    """ID of the intersection.
    """

    @staticmethod
    def from_element(element: Element) -> "Intersection":
        """Creates an intersection instance from an XML element.

        Args:
            element (Element): XML element

        Returns:
            Intersection: Intersection instance
        """
        return Intersection(
            id=int(element.attrib["id"]),
            latitude=float(element.attrib["latitude"]),
            longitude=float(element.attrib["longitude"]),
        )
