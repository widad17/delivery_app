import unittest

from src.models.delivery_man.delivery_man import DeliveryMan


class TestDeliveryMan(unittest.TestCase):
    """Test class for DeliveryMan.""" ""

    def test_should_create(self):
        """Test if DeliveryMan can be created."""
        assert DeliveryMan("", []) is not None

    def test_should_not_create(self):
        """Test if DeliveryMan can't be created with invalid arguments."""
        with self.assertRaises(TypeError):
            DeliveryMan()
