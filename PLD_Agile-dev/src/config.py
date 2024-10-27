from datetime import datetime, timedelta


class Config:
    INITIAL_DEPART_TIME = 8 * 60
    """Time in minutes when the delivery driver starts his tour from the warehouse (8 a.m. * 60 minutes/hour).
    """

    TIME_WINDOW_SIZE = 60
    """Time window size in minutes.
    """

    TRAVELING_SPEED = 15
    """Speed at which the delivery driver travels between two points in km/h.
    """

    DELIVERY_TIME = 5
    """Time in minutes it takes to deliver a package.
    """

    KMH_TO_MS = 3.6
    """Conversion factor from km/h to m/s.
    """
