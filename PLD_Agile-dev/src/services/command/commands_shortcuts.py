from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget

from src.services.command.command_service import CommandService
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes


def init_commands_shortcuts(widget: QWidget):
    QShortcut(QKeySequence.StandardKey.Undo, widget).activated.connect(
        lambda: CommandService.instance().undo()
        if get_app_navigator().get_current_route_name() == AppNavigationRoutes.MAIN
        else None
    )
    QShortcut(QKeySequence.StandardKey.Redo, widget).activated.connect(
        lambda: CommandService.instance().redo()
        if get_app_navigator().get_current_route_name() == AppNavigationRoutes.MAIN
        else None
    )
