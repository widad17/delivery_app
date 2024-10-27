from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4


@dataclass
class DeliveryMan:
    name: str
    """Name of the delivery man (for display).
    """
    availabilities: List[int]
    """List of number representing its availabilities.
    
    The number represent the start hour of the time window. For example, 8 means 8:00 AM to 9:00 AM.
    """
    id: UUID = field(default_factory=uuid4)
    """ID of the delivery man
    """
