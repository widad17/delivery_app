from dataclasses import dataclass
from typing import Dict
from xml.etree.ElementTree import Element

from src.models.map.errors import MapLoadingError
from src.models.map.intersection import Intersection


@dataclass
class Segment:
    id: int
    """ID of the segment.
    """
    name: str
    """Name of the segment.
    """
    origin: Intersection
    """Origin intersection.
    """
    destination: Intersection
    """Destination intersection.
    """
    length: float
    """Length of the segment.
    """

    @staticmethod
    def from_element(
        element: Element, intersections: Dict[int, Intersection]
    ) -> "Segment":
        """Creates a Segment instance from an XML element.

        Args:
            element (Element): XML element
            intersections (Dict[int, Intersection]): Dictionary of intersections

        Returns:
            Segment: Segment instance
        """
        name = element.attrib["name"]
        origin = intersections[int(element.attrib["origin"])]
        destination = intersections[int(element.attrib["destination"])]

        if origin is None:
            raise MapLoadingError(
                f"No intersection with ID {element.attrib['origin']} for origin on {element.tag} {name}"
            )
        if destination is None:
            raise MapLoadingError(
                f"No intersection with ID {element.attrib['destination']} for destination on {element.tag} {name}"
            )

        id = hash((origin.id, destination.id))

        return Segment(
            id=id,
            name=name,
            origin=origin,
            destination=destination,
            length=float(element.attrib["length"]),
        )
