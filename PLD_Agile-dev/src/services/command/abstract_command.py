from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    __name: str

    def __init__(self, name: str) -> None:
        self.__name = name

    def __str__(self) -> str:
        return self.__name

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass
