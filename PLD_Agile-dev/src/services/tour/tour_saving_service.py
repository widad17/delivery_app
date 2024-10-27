import pickle
from typing import Dict

from src.models.tour import ComputedTour, TourID
from src.services.singleton import Singleton


class TourSavingService(Singleton):
    def save_tours(self, tours: Dict[TourID, ComputedTour], path: str) -> None:
        pickle.dump(tours, open(path, "wb"))

    def load_tours(self, path: str) -> Dict[TourID, ComputedTour]:
        return pickle.load(open(path, "rb"))
