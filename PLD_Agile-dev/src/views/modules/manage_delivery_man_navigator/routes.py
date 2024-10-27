from enum import Enum


class ManageDeliveryManNavigationRoutes(Enum):
    MENU = "menu"
    ADD_DELIVERY_MAN_FORM = "add_delivery_man_form"
    MODIFY_DELIVERY_MAN_FORM = "modify_delivery_man_form"
    DELETE_DELIVERY_MAN_FORM = "delete_delivery_man_form"


class ManageDeliveryManNavigationNames(Enum):
    MENU = "List of deliverymen"
    ADD_DELIVERY_MAN_FORM = "Create a deliveryman"
    MODIFY_DELIVERY_MAN_FORM = "Modify a deliveryman"
    DELETE_DELIVERY_MAN_FORM = "Remove a deliveryman"
