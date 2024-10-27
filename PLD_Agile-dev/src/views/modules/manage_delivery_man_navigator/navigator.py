from src.controllers.navigator.navigator import Navigator

MANAGE_DELIVERY_MAN_NAVIGATOR = "manage_delivery_man_navigator"


def get_manage_delivery_man_navigator():
    return Navigator.get_navigator(MANAGE_DELIVERY_MAN_NAVIGATOR)
