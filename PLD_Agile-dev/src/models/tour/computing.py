from dataclasses import dataclass
from typing import List, Tuple

DeliveriesComputingResult = Tuple[int, float]
"""Represent a delivery's intersection ID with its time in minutes
"""


@dataclass
class TourComputingResult:
    """Class representing the result of a tour computing."""

    route: List[int]
    """List of intersection IDs composing the route
    """
    deliveries: List[DeliveriesComputingResult]
    """List of delivery's intersection IDs with their time in minutes
    """
