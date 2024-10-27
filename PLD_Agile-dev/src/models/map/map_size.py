import sys
from dataclasses import dataclass
from typing import Type, TypeVar

from src.models.map.position import Position

T = TypeVar("T", bound="MapSize")


@dataclass
class MapSize:
    """Represents the size of a map."""

    __min: Position
    """Minimum position of the map.
    """
    __max: Position
    """Maximum position of the map.
    """
    area: float
    """Area of the map.
    """

    def __init__(self, min: Position, max: Position) -> None:
        self.__min = min
        self.__max = max
        self.area = self.__calculate_area()

    @classmethod
    def inverse_max_size(cls: Type[T]) -> T:
        """Creates a MapSize instance with the inverted maximum possible size. (min = System MAX, max = System MIN)

        Args:
            cls (Type[T]): MapSize class

        Returns:
            T: MapSize instance
        """
        return cls(
            Position(sys.maxsize, sys.maxsize),
            Position(sys.maxsize * -1, sys.maxsize * -1),
        )

    @property
    def min(self) -> Position:
        """Minimum position of the map.

        Returns:
            Position: Minimum position of the map.
        """
        return self.__min

    @min.setter
    def min(self, value: Position) -> None:
        """Minimum position of the map.

        Args:
            value (Position): Minimum position of the map.

        Returns:
            None
        """
        self.__min = value
        self.area = self.__calculate_area()

    @property
    def max(self) -> Position:
        """Maximum position of the map.

        Returns:
            Position: Maximum position of the map.
        """
        return self.__max

    @max.setter
    def max(self, value: Position) -> None:
        """Maximum position of the map.

        Args:
            value (Position): Maximum position of the map.

        Returns:
            None
        """
        self.__max = value
        self.area = self.__calculate_area()

    @property
    def width(self) -> float:
        """Width of the map.

        Returns:
            float: Width of the map.
        """
        return self.__max.longitude - self.__min.longitude

    @property
    def height(self) -> float:
        """Height of the map.

        Returns:
            float: Height of the map.
        """
        return self.__max.latitude - self.__min.latitude

    def __calculate_area(self) -> float:
        """Calculate the area of the map.

        Returns:
            float: Area of the map.
        """
        return (self.__max.latitude - self.__min.latitude) * (
            self.__max.longitude - self.__min.longitude
        )
