from PyQt6.QtWidgets import QLabel

from src.models.tour import Delivery, Tour


class ToursTableColumnItemAddress(QLabel):
    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__(delivery.location.segment.name)
