from dataclasses import dataclass


@dataclass
class NavigatorConfig:
    """Class for navigator configuration."""

    allow_push_same_route: bool = False
    """Allow push a route that is already the current route.
    """

    allow_replace_same_route: bool = False
    """Allow replace a route that is already the current route.
    """
