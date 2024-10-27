from typing import List, Optional

from reactivex import Observable
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.map import Map
from src.services.singleton import Singleton


class MapService(Singleton):
    __map: BehaviorSubject[Optional[Map]]

    def __init__(self) -> None:
        self.__map = BehaviorSubject(None)

    @property
    def map(self) -> Observable[Optional[Map]]:
        return self.__map

    @property
    def is_loaded(self) -> Observable[bool]:
        return self.__map.pipe(map(lambda map: map is not None))

    def get_map(self) -> Map:
        if not self.__map.value:
            raise Exception("Map not loaded")

        return self.__map.value

    def set_map(self, map: Map) -> None:
        self.__map.on_next(map)

    def clear(self) -> None:
        self.__map.on_next(None)
