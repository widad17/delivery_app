from src.controllers.navigator.navigator import Navigator

APP_NAVIGATOR = "app_navigator"


def get_app_navigator():
    return Navigator.get_navigator(APP_NAVIGATOR)
