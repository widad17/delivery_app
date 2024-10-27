from dataclasses import dataclass, field
from datetime import time

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour.delivery_location import DeliveryLocation

DeliveryID = int
"""Type alias for a delivery ID
"""


@dataclass
class Delivery:
    """Base class for a delivery. This represent a delivery that can be requested or computed which has a location."""

    location: DeliveryLocation
    """Location of the delivery
    """

    @property
    def id(self) -> DeliveryID:
        """ID of the delivery that is unique for a DeliveryLocation

        Returns:
            DeliveryID: ID of the delivery
        """
        return hash(f"{self.location.segment.id}{self.location.positionOnSegment}")


@dataclass
class DeliveryRequest(Delivery):
    """Represents a delivery request that has a location and a time window."""

    time_window: int
    """Time window of the request. This number represent the hour of the time window.
    
    For example, time_window=8 means that the time window if from 8h to 9h.
    """

    @staticmethod
    def create_from_computed(
        computed_delivery: "ComputedDelivery",
    ) -> "DeliveryRequest":
        """Creates an instance of DeliveryRequest from a ComputedDelivery.

        Args:
            computed_delivery (ComputedDelivery): Computed delivery to create the delivery request from

        Returns:
            DeliveryRequest: Created instance
        """
        return DeliveryRequest(
            location=computed_delivery.location,
            time_window=computed_delivery.time.hour,
        )


@dataclass
class ComputedDelivery(Delivery):
    """Represent a computed delivery that has a location and a time."""

    time: time
    """Computed time of the delivery
    """

    @staticmethod
    def create_from_request(
        delivery_request: DeliveryRequest, time: time
    ) -> "ComputedDelivery":
        """Creates an instance of ComputedDelivery from a DeliveryRequest and a time.

        Args:
            delivery_request (DeliveryRequest): Delivery request to create the computed delivery from
            time (time): Computed time of the delivery

        Returns:
            ComputedDelivery: Created instance
        """
        return ComputedDelivery(
            location=delivery_request.location,
            time=time,
        )
