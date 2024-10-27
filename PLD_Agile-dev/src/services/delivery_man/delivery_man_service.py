from typing import Dict, List, Optional, Tuple
from uuid import UUID

from reactivex import Observable, combine_latest
from reactivex.subject import BehaviorSubject

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.delivery_man.errors import DeliveryManError
from src.services.singleton import Singleton


class DeliveryManService(Singleton):
    n1 = DeliveryMan("Josué stcyr", [8, 9, 10, 11])
    n2 = DeliveryMan("clem farhat", [8, 9, 10, 11])
    __delivery_men: BehaviorSubject[Dict[str, DeliveryMan]] = BehaviorSubject(
        {
            n1.id: n1,
            n2.id: n2,
        }
    )
    __selected_delivery_man: BehaviorSubject[Optional[DeliveryMan]] = BehaviorSubject(
        None
    )
    __selected_time_window: BehaviorSubject[Optional[int]] = BehaviorSubject(None)

    @property
    def delivery_men(self) -> Observable[Dict[str, DeliveryMan]]:
        """Returns every Delivery Men.

        Args:
           No args.

        Returns:
            Observable[Dict[DeliveryMan]]: DeliveryMen dictionnary observable instance
        """

        return self.__delivery_men

    @property
    def selected_values(
        self,
    ) -> Observable[Tuple[Optional[DeliveryMan], Optional[int]]]:
        """Returns selected delivery man and time window.

        Returns:
            Observable[Tuple[Optional[DeliveryMan], Optional[int]]]: _description_
        """
        return combine_latest(self.__selected_delivery_man, self.__selected_time_window)

    def get_delivery_man(self, id: UUID) -> DeliveryMan:
        """Get delivery man from its ID.

        Args:
            id (UUID): ID of the delivery man

        Returns:
            DeliveryMan: Delivery man
        """
        return self.__delivery_men.value[id]

    def create_delivery_man(self, name: str) -> DeliveryMan:
        """Creates a Delivery Man and pass it back.

        Args:
            name: a string that represents the name of the delivery name that'll be created

        Returns:
            None
        """

        availabilities = [8, 9, 10, 11]

        if name is None:
            raise DeliveryManError("No name or availabilities provided")

        deliveryman = DeliveryMan(name, availabilities)

        self.__delivery_men.value[deliveryman.id] = deliveryman
        self.__delivery_men.on_next(self.__delivery_men.value)

        return deliveryman

    def modify_delivery_man(
        self, delivery_man: DeliveryMan, delivery_man_info
    ) -> DeliveryMan:
        """Updates a Deliveryman and pass it back.

        Args:
            delivery_man: A DeliveryMan instance to be updated
            delivery_man_info: A dictionary containing the new state
            of the DeliveryMan instance to be update

        Returns:
            DeliveryMan: DeliveryMan instance
        """

        delivery_man = self.__delivery_men.value[delivery_man.id]

        name = delivery_man_info.get("name")
        availabilities = delivery_man_info.get("availabilities")

        if name is not None:
            delivery_man.name = name

        if availabilities is not None:
            delivery_man.availabilities = availabilities

        self.__delivery_men.on_next(self.__delivery_men.value)

        return delivery_man

    def remove_delivery_man(self, delivery_man: DeliveryMan) -> None:
        """Deletes a Deliveryman.

        Args:
            delivery_man: A DeliveryMan instance to be deleted

        Returns:
            None
        """

        del self.__delivery_men.value[delivery_man.id]
        self.__delivery_men.on_next(self.__delivery_men.value)

        return

    def set_selected_delivery_man(self, delivery_man_id: Optional[int]) -> None:
        """Set currently selected delivery man.

        Args:
            delivery_man_id (int): ID of the delivery man to be selected

        Returns:
            None
        """
        self.__selected_delivery_man.on_next(
            self.__delivery_men.value[delivery_man_id]
            if delivery_man_id is not None
            else None
        )

    def set_selected_time_window(self, time_window: Optional[int]) -> None:
        """Set currently selected time window.

        Args:
            time_window (int): Time window to be selected

        Returns:
            None
        """
        self.__selected_time_window.on_next(time_window)

    def get_selected_values(self) -> Tuple[Optional[DeliveryMan], Optional[int]]:
        """
        Returns a tuple containing the selected delivery man and time window.

        Returns:
            Tuple[Optional[DeliveryMan], Optional[int]]: A tuple containing the selected delivery man and time window.
        """
        return (self.__selected_delivery_man.value, self.__selected_time_window.value)

    def overwrite(self, delivery_men: Dict[UUID, DeliveryMan]):
        self.__delivery_men.on_next(delivery_men)
