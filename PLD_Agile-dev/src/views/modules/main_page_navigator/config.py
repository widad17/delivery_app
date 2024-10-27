from src.controllers.navigator import Route
from src.views.main_page.load_map_page import LoadMapPage
from src.views.modules.main_page_navigator.navigator import get_main_page_navigator
from src.views.modules.main_page_navigator.routes import MainPageNavigationRoutes
from views.main_page.delivery_form_page import DeliveryFormPage


def init_main_page_navigator():
    get_main_page_navigator().init(
        routes=[
            Route(
                name=MainPageNavigationRoutes.LOAD_MAP,
                widget=LoadMapPage,
            ),
            Route(
                name=MainPageNavigationRoutes.DELIVERY_FORM,
                widget=DeliveryFormPage,
            ),
        ],
        default_name=MainPageNavigationRoutes.LOAD_MAP,
    )
