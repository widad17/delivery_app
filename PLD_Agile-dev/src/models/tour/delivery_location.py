from dataclasses import dataclass

from src.models.map.segment import Segment


@dataclass
class DeliveryLocation:
    """Location where a delivery is made. This represents a point on a segment.

    **Notes:** This class was created from our initial architecture where the idea was to allow deliveries to be made anywhere on a segment.
    However, this was not implemented in the end. The positionOnSegment attribute is always 0 and the location is always the segment's origin.
    """

    segment: Segment
    """Segment where the delivery is made.
    """
    positionOnSegment: float
    """Position on the segment where the delivery is made.
    """
