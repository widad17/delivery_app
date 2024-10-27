from PyQt6.QtWidgets import QFrame, QWidget


class Separator(QFrame):
    """A custom horizontal line separator widget with a plain shadow and custom color.

    Args:
        parent (QWidget | None): The parent widget of this separator. Defaults to None.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setStyleSheet(
            """
            color: #515764;
        """
        )
