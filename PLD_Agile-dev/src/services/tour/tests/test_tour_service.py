from pytest import fixture

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.intersection import Intersection
from src.models.map.map import Map
from src.models.map.map_size import MapSize
from src.models.map.position import Position
from src.models.map.segment import Segment
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.map.map_service import MapService
from src.services.tour.tour_service import TourService


class TestTourService:
    service: TourService
    delivery_man: DeliveryMan

    @fixture(autouse=True)
    def setup(self):
        self.service = TourService.instance()

        self.delivery_man = DeliveryManService.instance().create_delivery_man(
            "John Doe"
        )

        intersections = [
            Intersection(0, 0, 0),
            Intersection(1, 2, 1),
            Intersection(2, 2, 2),
            Intersection(3, 3, 3),
        ]

        segments = {
            0: {
                1: Segment(100, "A", intersections[0], intersections[1], length=1),
                2: Segment(104, "E", intersections[0], intersections[2], length=1),
            },
            1: {
                0: Segment(105, "A", intersections[1], intersections[0], length=1),
                2: Segment(106, "B", intersections[1], intersections[2], length=1),
            },
            2: {
                0: Segment(104, "E", intersections[2], intersections[0], length=1),
                1: Segment(106, "B", intersections[2], intersections[1], length=1),
                3: Segment(107, "C", intersections[2], intersections[3], length=1),
            },
            3: {
                2: Segment(107, "C", intersections[3], intersections[2], length=1),
            },
        }

        MapService.instance().set_map(
            Map(
                intersections={
                    intersection.id: intersection for intersection in intersections
                },
                segments=segments,
                warehouse=intersections[0],
                size=MapSize(Position(0, 0), Position(3, 3)),
            )
        )

        yield

        TourService.reset()
        DeliveryManService.reset()
        MapService.reset()

        self.service = None

    def test_should_create_tour_service(self):
        assert self.service is not None

    def test_should_add_delivery_request(self):
        self.service.compute_tours = lambda: None

        self.service.add_delivery_request(Position(1, 1), 0, self.delivery_man.id)

        assert (
            len(self.service.tour_requests.value.get(self.delivery_man.id).deliveries)
            == 1
        )

    def test_should_add_multiple_delivery_request(self):
        self.service.compute_tours = lambda: None

        self.service.add_delivery_request(Position(1, 1), 0, self.delivery_man.id)
        self.service.add_delivery_request(Position(2, 2), 0, self.delivery_man.id)

        assert (
            len(self.service.tour_requests.value.get(self.delivery_man.id).deliveries)
            == 2
        )

    def test_should_add_only_one_delivery_request_for_a_location(self):
        self.service.compute_tours = lambda: None

        self.service.add_delivery_request(Position(1, 1), 0, self.delivery_man.id)
        self.service.add_delivery_request(Position(1.01, 1.01), 0, self.delivery_man.id)

        assert (
            len(self.service.tour_requests.value.get(self.delivery_man.id).deliveries)
            == 1
        )

    def test_should_remove_delivery_request(self):
        self.service.compute_tours = lambda: None

        delivery_request = self.service.add_delivery_request(
            Position(1, 1), 0, self.delivery_man.id
        )

        self.service.remove_delivery_request(delivery_request.id, self.delivery_man.id)

        assert (
            len(self.service.tour_requests.value.get(self.delivery_man.id).deliveries)
            == 0
        )

    def test_should_update_delivery_request_time_window(self):
        NEW_TIME_WINDOW = 10
        self.service.compute_tours = lambda: None

        delivery_request = self.service.add_delivery_request(
            Position(1, 1), 0, self.delivery_man.id
        )

        self.service.update_delivery_request_time_window(
            delivery_request.id, self.delivery_man.id, NEW_TIME_WINDOW
        )

        assert (
            self.service.tour_requests.value.get(self.delivery_man.id)
            .deliveries.get(delivery_request.id)
            .time_window
            == NEW_TIME_WINDOW
        )

    def test_should_update_delivery_request_delivery_man(self):
        delivery_man_2 = DeliveryManService.instance().create_delivery_man("Jane Doe")
        self.service.compute_tours = lambda: None

        delivery_request = self.service.add_delivery_request(
            Position(1, 1), 0, self.delivery_man.id
        )

        self.service.update_delivery_request_delivery_man(
            delivery_request.id, self.delivery_man.id, delivery_man_2.id
        )

        assert (
            self.service.tour_requests.value.get(delivery_man_2.id).deliveries.get(
                delivery_request.id
            )
            is not None
        )
