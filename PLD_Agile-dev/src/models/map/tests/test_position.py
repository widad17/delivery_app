import unittest

from src.models.map.position import Position


class TestPosition(unittest.TestCase):
    """Tests class for Position."""

    def test_should_create(self):
        """Test if Position can be created."""
        assert Position(0, 0) is not None

    def test_should_not_create(self):
        """Test if Position can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            Position()

    def test_should_get_longitude_equals_x(self):
        """Test if Position can get its longitude and x. They should be the same."""
        LONGITUDE = 420

        assert Position(LONGITUDE, 0).longitude == LONGITUDE
        assert Position(LONGITUDE, 0).x == LONGITUDE

    def test_should_get_latitude_equals_y(self):
        """Test if Position can get its latitude and y. They should be the same."""
        LATITUDE = 69

        assert Position(0, LATITUDE).latitude == LATITUDE
        assert Position(0, LATITUDE).y == LATITUDE

    def test_should_get_max(self):
        """Test if Position can get the maximum position between the current position and the given position."""
        assert Position(1, 1).max(Position(2, 2)) == Position(2, 2)
        assert Position(1, 1).max(Position(2, 2), Position(3, 3)) == Position(3, 3)

    def test_should_get_min(self):
        """Test if Position can get the minimum position between the current position and the given position."""
        assert Position(1, 1).min(Position(2, 2)) == Position(1, 1)
        assert Position(1, 1).min(Position(2, 2), Position(3, 3)) == Position(1, 1)
