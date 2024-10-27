from pytest import fixture

from src.models.map.intersection import Intersection
from src.models.map.map import Map
from src.models.map.map_size import MapSize
from src.models.map.position import Position
from src.models.map.segment import Segment
from src.services.map.delivery_location_service import DeliveryLocationService
from src.services.map.map_service import MapService


class TestDeliveryLocationService:
    service: DeliveryLocationService

    @fixture(autouse=True)
    def setup(self):
        self.service = DeliveryLocationService.instance()

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

        DeliveryLocationService.reset()
        MapService.reset()

        self.service = None

    def test_should_create_service(self):
        assert self.service is not None

    def test_should_find_intersection_if_is_exact(self):
        delivery_location = self.service.find_delivery_location_from_position(
            Position(3, 3)
        )

        assert delivery_location.segment.origin.id == 3

    def test_should_find_closest_intersection(self):
        delivery_location = self.service.find_delivery_location_from_position(
            Position(0.1, 0.1)
        )

        assert delivery_location.segment.origin.id == 0
