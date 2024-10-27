from src.controllers.navigator.navigator import Route
from src.views.main_page.main_page import MainPage
from src.views.manage_delivery_man_page.manage_delivery_man_page import (
    ManageDeliveryManPage,
)
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes


def init_app_navigator():
    get_app_navigator().init(
        routes=[
            Route(name=AppNavigationRoutes.MAIN, widget=MainPage),
            Route(
                name=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
                widget=ManageDeliveryManPage,
            ),
        ],
        default_name=AppNavigationRoutes.MAIN,
    )
