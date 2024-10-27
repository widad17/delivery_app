from src.controllers.navigator import Route
from src.views.manage_delivery_man_page.add_delivery_man_form_view import (
    AddDeliveryManFormView,
)
from src.views.manage_delivery_man_page.delete_delivery_man_form_view import (
    DeleteDeliveryManFormView,
)
from src.views.manage_delivery_man_page.modify_delivery_man_form_view import (
    ModifyDeliveryManFormView,
)
from src.views.manage_delivery_man_page.read_delivery_man import ReadDeliveryMan
from src.views.modules.manage_delivery_man_navigator.navigator import (
    get_manage_delivery_man_navigator,
)
from src.views.modules.manage_delivery_man_navigator.routes import (
    ManageDeliveryManNavigationRoutes,
)


def init_manage_delivery_man_navigator():
    get_manage_delivery_man_navigator().init(
        routes=[
            Route(name=ManageDeliveryManNavigationRoutes.MENU, widget=ReadDeliveryMan),
            Route(
                name=ManageDeliveryManNavigationRoutes.ADD_DELIVERY_MAN_FORM,
                widget=AddDeliveryManFormView,
            ),
            Route(
                name=ManageDeliveryManNavigationRoutes.MODIFY_DELIVERY_MAN_FORM,
                widget=ModifyDeliveryManFormView,
            ),
            Route(
                name=ManageDeliveryManNavigationRoutes.DELETE_DELIVERY_MAN_FORM,
                widget=DeleteDeliveryManFormView,
            ),
        ],
        default_name=ManageDeliveryManNavigationRoutes.MENU,
    )
