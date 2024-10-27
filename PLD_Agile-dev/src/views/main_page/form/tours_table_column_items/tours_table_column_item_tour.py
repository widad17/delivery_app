from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.models.tour import Delivery, Tour


class ToursTableColumnItemTour(QWidget):
    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tour_item = QLabel("     ")
        tour_item.setStyleSheet(
            f"""
            background-color: {tour.color};
        """
        )

        layout.addWidget(tour_item)
