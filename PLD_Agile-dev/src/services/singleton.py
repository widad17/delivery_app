from abc import ABC
from typing import Type, TypeVar

T = TypeVar("T", bound="Singleton")


class Singleton(ABC):
    __instance = None

    @classmethod
    def instance(cls: Type[T]) -> T:
        """Static access method."""
        if cls.__instance == None:
            cls.__instance = cls()

        return cls.__instance

    @classmethod
    def reset(cls: Type[T]) -> None:
        cls.__instance = None

    def __init__(self) -> None:
        if self.__instance != None:
            raise Exception("This class is a singleton!")
