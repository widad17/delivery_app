import unittest

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.intersection import Intersection
from src.models.map.segment import Segment
from src.models.tour import ComputedDelivery, ComputedTour, DeliveryRequest, TourRequest
from src.models.tour.delivery_location import DeliveryLocation


class TestDeliveryLocation(unittest.TestCase):
    """Tests class for DeliveryLocation."""

    def test_should_create(self):
        """Test if DeliveryLocation can be created."""
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        assert DeliveryLocation(segment, 0.0)

    def test_should_not_create(self):
        """Test if DeliveryLocation can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            DeliveryLocation()


class TestDeliveryRequest(unittest.TestCase):
    """Tests class for DeliveryRequest."""

    def test_should_create(self):
        """Test if DeliveryRequest can be created."""
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        location = DeliveryLocation(segment, 0.0)
        assert DeliveryRequest(location, 0)

    def test_should_not_create(self):
        """Test if DeliveryRequest can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            DeliveryRequest()


class TestComputedDelivery(unittest.TestCase):
    """Tests class for ComputedDelivery."""

    def test_should_create(self):
        """Test if ComputedDelivery can be created."""
        intersection = Intersection(1.0, 1.0, 1.0)
        segment = Segment(0, "", intersection, intersection, 1.0)
        delivery_location = DeliveryLocation(segment, 0.0)
        assert ComputedDelivery(delivery_location, 0.0)

    def test_should_not_create(self):
        """Test if ComputedDelivery can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            ComputedDelivery()


class TestTourRequest(unittest.TestCase):
    """Tests class for TourRequest."""

    def test_should_create(self):
        """Test if TourRequest can be created."""
        delivery_man = DeliveryMan("", [])
        assert TourRequest([], {}, delivery_man, "red")

    def test_should_not_create(self):
        """Test if TourRequest can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            TourRequest()


class TestComputedTour(unittest.TestCase):
    """Tests class for ComputedTour."""

    def test_should_create(self):
        """Test if ComputedTour can be created."""
        delivery_man = DeliveryMan("", [])
        assert ComputedTour([], delivery_man, [], 1.0, "")

    def test_should_not_create(self):
        """Test if ComputedTour can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            ComputedTour()
