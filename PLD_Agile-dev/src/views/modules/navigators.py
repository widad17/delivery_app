from src.views.modules.app_navigator.config import init_app_navigator
from src.views.modules.main_page_navigator.config import init_main_page_navigator
from src.views.modules.manage_delivery_man_navigator.config import (
    init_manage_delivery_man_navigator,
)


def init_navigators():
    init_app_navigator()
    init_main_page_navigator()
    init_manage_delivery_man_navigator()
