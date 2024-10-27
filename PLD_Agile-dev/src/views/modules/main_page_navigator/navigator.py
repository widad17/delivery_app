from src.controllers.navigator.navigator import Navigator

MAIN_PAGE_NAVIGATOR = "main_page_navigator"


def get_main_page_navigator():
    return Navigator.get_navigator(MAIN_PAGE_NAVIGATOR)
