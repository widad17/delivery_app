from xml.etree.ElementTree import Element

from pytest import fixture

from src.services.map.map_loader_service import MapLoaderService


class TestMapLoaderService:
    map_loader_service: MapLoaderService

    @fixture(autouse=True)
    def setup_method(self):
        self.map_loader_service = MapLoaderService.instance()

        yield

        MapLoaderService.reset()

    @fixture
    def root(self):
        root = Element("map")

        root.append(Element("warehouse", attrib={"address": "1"}))

        root.append(
            Element(
                "intersection", attrib={"id": "1", "latitude": "0", "longitude": "0"}
            )
        )
        root.append(
            Element(
                "intersection", attrib={"id": "2", "latitude": "0", "longitude": "1"}
            )
        )
        root.append(
            Element(
                "intersection", attrib={"id": "3", "latitude": "1", "longitude": "0"}
            )
        )

        root.append(
            Element(
                "segment",
                attrib={
                    "name": "segment1",
                    "origin": "1",
                    "destination": "2",
                    "length": "1.1",
                },
            )
        )
        root.append(
            Element(
                "segment",
                attrib={
                    "name": "segment2",
                    "origin": "1",
                    "destination": "3",
                    "length": "10.23",
                },
            )
        )

        return root

    def test_should_create(self):
        assert self.map_loader_service is not None

    def test_should_create_map_from_xml(self, root):
        map = self.map_loader_service.create_map_from_xml(root)

        assert map is not None

    def test_should_create_map_from_xml_with_intersections(self, root):
        map = self.map_loader_service.create_map_from_xml(root)

        assert len(map.intersections) == 3

    def test_should_create_map_from_xml_with_segments(self, root):
        map = self.map_loader_service.create_map_from_xml(root)

        assert len(map.segments) == 1
        assert len(map.segments[1]) == 2

    def test_should_create_map_from_xml_with_warehouse(self, root):
        map = self.map_loader_service.create_map_from_xml(root)

        assert map.warehouse is not None

    def test_should_throw_if_create_map_from_xml_without_warehouse(self, root):
        root.remove(root.find("warehouse"))

        try:
            self.map_loader_service.create_map_from_xml(root)

            assert False
        except Exception as e:
            assert str(e) == "No warehouse found in the XML file"
