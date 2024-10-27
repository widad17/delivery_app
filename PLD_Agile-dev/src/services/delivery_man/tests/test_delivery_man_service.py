from typing import Dict
from xml.etree.ElementTree import Element

from pytest import fixture

from src.models.delivery_man.delivery_man import DeliveryMan
from src.services.delivery_man.delivery_man_service import DeliveryManService


class TestDeliveryManService:
    delivery_man_service: DeliveryManService

    @fixture(autouse=True)
    def setup_method(self):
        self.delivery_man_service = DeliveryManService.instance()

        yield

        DeliveryManService.reset()

    @fixture
    def root(self):
        self.n1 = DeliveryMan("Josué stcyr", [8, 9, 10, 11])
        self.n2 = DeliveryMan("clem farhat", [8, 9, 10, 11])

        root: Dict[str, DeliveryMan] = {
            self.n1.id: self.n1,
            self.n2.id: self.n2,
        }

        return root

    def test_should_create(self, root):
        length = len(self.delivery_man_service.delivery_men.value)
        delivery_man = self.delivery_man_service.create_delivery_man("test")

        assert len(self.delivery_man_service.delivery_men.value) == length + 1
