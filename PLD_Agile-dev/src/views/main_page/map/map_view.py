import math
from typing import Dict, List, Literal, Optional, Tuple

from PyQt6.QtCore import QEvent, QLineF, QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QLinearGradient,
    QMouseEvent,
    QPen,
    QPolygonF,
    QTransform,
    QWheelEvent,
)
from PyQt6.QtWidgets import (
    QAbstractGraphicsShapeItem,
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QSizePolicy,
    QWidget,
)
from reactivex import Observable
from reactivex.subject import BehaviorSubject

from src.models.map import Map, Position, Segment
from src.models.tour import ComputedTour, Delivery, DeliveryLocation, Tour, TourID
from src.services.command.command_service import CommandService
from src.services.command.commands.add_delivery_request_command import (
    AddDeliveryRequestCommand,
)
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.map.map_service import MapService
from src.services.tour.tour_service import TourService
from src.views.main_page.map.map_annotation_collection import (
    MapAnnotationCollection,
    MarkersTypes,
    SegmentTypes,
)
from src.views.main_page.map.map_marker import AlignBottom, MapMarker
from src.views.utils.icon import get_icon_pixmap
from src.views.utils.theme import Theme
from views.main_page.map.map_segment import MapSegment


class MapView(QGraphicsView):
    """Widget to display a Map"""

    MAX_SCALE = 8
    """Maximum scale factor for the map (1 = no zoom, 2 = 2x zoom, etc.)
    """
    SCROLL_INTENSITY = 2
    """Intensity of the zoom when scrolling (higher = more zoom)
    """
    DEFAULT_ZOOM_ACTION = 1.25
    """Zoom factor when clicking on the zoom in/out buttons
    """
    MARKER_INITIAL_SIZE = 0.045
    """Marker size when zoom is 1 (1 = marker is same width as the map)
    """
    MARKER_ZOOM_ADJUSTMENT = 0.35
    """Amount of zoom adjustment for the markers (1 = marker stays the same size, 0 = marker scales with the map)
    """
    MARKER_RESOLUTION_RESOLUTION = 250
    """Image resolution of the marker
    """
    SEGMENT_INITIAL_SIZE = 0.00005
    """Size of a segment when zoom is 1
    """
    SEGMENT_ZOOM_ADJUSTMENT = -0.075
    """Amount of zoom adjustment for the segments (1 = segment stays the same size, 0 = segment scales with the map)
    """
    MIN_SEGMENT_LENGTH_FOR_ARROW = 50
    """Minimum length of a segment to display an arrow
    """

    __scene: Optional[QGraphicsScene] = None
    __map: Optional[Map] = None
    __scale_factor: int = 1
    __marker_size: Optional[int] = None
    __map_annotations: MapAnnotationCollection = MapAnnotationCollection()
    __ready: BehaviorSubject[bool] = BehaviorSubject(False)
    __is_computing: bool = False

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__set_config()

        MapService.instance().map.subscribe(
            lambda map: self.set_map(map) if map else self.reset()
        )
        TourService.instance().tour_requests_delivery_locations.subscribe(
            self.__on_update_delivery_locations
        )
        TourService.instance().computed_tours.subscribe(self.__on_update_computed_tours)
        TourService.instance().is_computing.subscribe(self.__handle_is_computing)

    @property
    def ready(self) -> Observable[bool]:
        """Subject that emit a boolean when the map is ready to be used"""
        return self.__ready

    def set_map(self, map: Map):
        """Set the map and initialize the view

        Arguments:
            map (Map): Map to display
        """
        scene_rect = QRectF(
            map.size.min.longitude,
            map.size.min.latitude,
            map.size.width,
            map.size.height,
        )

        if self.__scene:
            self.reset()
            self.__scene.setSceneRect(scene_rect)
        else:
            self.__scene = QGraphicsScene(scene_rect)

        self.__map = map

        self.__scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setScene(self.__scene)

        for segment in map.get_all_segments():
            self.__add_segment(segment)

        self.__marker_size = self.__scene.sceneRect().width() * self.MARKER_INITIAL_SIZE

        self.add_marker(
            position=map.warehouse,
            icon="warehouse",
            color=QColor("#105723"),
            align_bottom=False,
            scale=1,
        )

        self.fit_map()

        self.__ready.on_next(True)

    def fit_map(self):
        """Adjust the view to fit the all map"""
        if self.__scene:
            self.fitInView(self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.__scale_factor = 1
            self.__scale_map(1)

    def add_marker(
        self,
        position: Position,
        icon: QIcon | str = "map-marker-alt",
        color: QColor = QColor("#f54242"),
        align_bottom: AlignBottom = True,
        scale: float = 1,
        marker_type: MarkersTypes = MarkersTypes.Default,
    ) -> MapMarker:
        """Add a marker on the map at a given position

        Args:
            position (Position): Position of the marker
            icon (str, optional): Icon to display. Defaults to "map-marker-alt".
            color (QColor, optional): Color of the icon. Defaults to QColor("#f54242").
            align_bottom (AlignBottom, optional): Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
        marker_size = self.__marker_size * scale

        icon_pixmap = get_icon_pixmap(icon, self.MARKER_RESOLUTION_RESOLUTION, color)
        icon_position = self.__get_marker_position(position, marker_size, align_bottom)

        icon_shape = self.__scene.addPixmap(icon_pixmap)
        icon_shape.setPos(icon_position)
        icon_shape.setScale(marker_size / self.MARKER_RESOLUTION_RESOLUTION)
        icon_shape.setZValue(10000)

        marker = MapMarker(icon_shape, align_bottom=align_bottom, scale=scale)

        self.__adjust_marker(marker)

        self.__map_annotations.markers.append(marker_type, marker)

        return marker

    def zoom_in(self):
        """Zoom in the map"""
        self.__scale_map(self.DEFAULT_ZOOM_ACTION)

    def zoom_out(self):
        """Zoom out the map"""
        self.__scale_map(1 / self.DEFAULT_ZOOM_ACTION)

    def reset(self):
        """Reset the map to its initial state"""
        self.__ready.on_next(False)
        if self.__scene:
            self.__scene.clear()
        self.__scale_factor = 1
        self.__marker_size = None
        self.__map_annotations.clear_all()
        self.__map = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Method called when the user scrolls on the map

        Zoom the map in/out depending on the scroll direction
        """
        if self.__scene and event.angleDelta().y() != 0:
            self.__scale_map(
                1
                + (self.__map.size.area * self.SCROLL_INTENSITY)
                * event.angleDelta().y()
            )

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        """Method called when the user double clicks on the map

        Send the position of the click to the on_map_click subject
        """
        if not self.__scene:
            return
        if self.__is_computing:
            return

        position = self.mapToScene(event.pos())
        position = Position(position.x(), position.y())

        delivery_man, time_window = DeliveryManService.instance().get_selected_values()
        CommandService.instance().execute(
            AddDeliveryRequestCommand(
                position=position,
                tour_id=delivery_man.id,
                time_window=time_window,
            )
        )

    def __on_update_delivery_locations(
        self,
        deliveries: Tuple[Optional[Delivery], List[DeliveryLocation]],
    ):
        selected_delivery, delivery_locations = deliveries

        for marker in self.__map_annotations.markers.get(MarkersTypes.Delivery):
            self.__scene.removeItem(marker.shape)

        self.__map_annotations.markers.clear(MarkersTypes.Delivery)

        for delivery_location in delivery_locations:
            self.__map_annotations.markers.append(
                MarkersTypes.Delivery,
                self.add_marker(
                    position=delivery_location.segment.origin,
                    icon="map-marker-alt",
                    color=QColor("#f54242"),
                    scale=1.5
                    if (
                        selected_delivery
                        and delivery_location == selected_delivery.location
                    )
                    else 1,
                ),
            )

    def __on_update_computed_tours(self, computed_tours: Dict[TourID, Tour]):
        for maker in self.__map_annotations.segments.get(SegmentTypes.Tour):
            self.__scene.removeItem(maker.shape)
            if maker.arrow_shape:
                self.__scene.removeItem(maker.arrow_shape)

        self.__map_annotations.segments.clear(SegmentTypes.Tour)

        segments: Dict[int, Tuple[Segment, List[ComputedTour]]] = {}

        for computed_tour in computed_tours.values():
            if not computed_tour or not isinstance(computed_tour, ComputedTour):
                continue

            for segment in computed_tour.route:
                # We get an unique identifier for the segment regardless of the direction
                segment_id = f"{min(segment.origin.id, segment.destination.id)}-{max(segment.origin.id, segment.destination.id)}"

                if segment_id not in segments:
                    segments[segment_id] = (segment, [])
                segments[segment_id][1].append(computed_tour)

        i = 0
        for _, (segment, tours) in segments.items():
            segment_can_be_added = segment.length > self.MIN_SEGMENT_LENGTH_FOR_ARROW

            self.__add_segment(
                segment=segment,
                color=[QColor(tour.color) for tour in tours],
                scale=2,
                segment_type=SegmentTypes.Tour,
                show_arrow=(i % 3 == 0) and segment_can_be_added,
            )

            i += 1 if segment_can_be_added else 0

    def __add_segment(
        self,
        segment: Segment,
        color: QColor | List[QColor] = QColor("#9c9c9c"),
        scale: float = 1,
        segment_type: SegmentTypes = SegmentTypes.Default,
        show_arrow: bool = False,
    ) -> None:
        """Add a segment on the map

        Args:
            segment (Segment): Segment
            color (QColor, optional): Color. Defaults to Qt.GlobalColor.black.
        """
        colors = [color] if isinstance(color, QColor) else color

        line = QLineF(
            segment.origin.longitude,
            segment.origin.latitude,
            segment.destination.longitude,
            segment.destination.latitude,
        )

        segmentLine = self.__scene.addLine(
            line,
            QPen(
                QBrush(colors[0]),
                self.__get_pen_size() * scale,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            ),
        )

        self.__set_brush_for_segment(segmentLine, line, colors)

        arrow_shape = None
        if show_arrow:
            arrow_shape = self.__scene.addPolygon(
                self.__calculate_arrow(line),
                pen=segmentLine.pen(),
                brush=segmentLine.pen().brush(),
            )

            arrow_shape.setZValue(100)

        self.__map_annotations.segments.append(
            segment_type, MapSegment(segmentLine, scale, arrow_shape)
        )

    def __scale_map(self, factor: float):
        """Scales the map for a given factor. This is used to zoom in and out.

        Args:
            factor (float): Scale factor
        """
        if not self.__scene:
            return

        updated_scale = self.__scale_factor * factor

        if updated_scale < 1:
            self.fit_map()
        else:
            if updated_scale > self.MAX_SCALE:
                factor = self.MAX_SCALE / self.__scale_factor
                updated_scale = self.MAX_SCALE

            self.__scale_factor = updated_scale
            self.scale(factor, factor)

        self.__adjust_map_graphics()

    def __adjust_map_graphics(self) -> None:
        """Adjust map segments and markers to the current map scale"""
        for segment in self.__map_annotations.segments.get_all():
            pen = segment.shape.pen()
            pen.setWidthF(self.__get_pen_size() * segment.scale)
            segment.shape.setPen(pen)
            segment.arrow_shape.setPen(pen) if segment.arrow_shape else None

        for marker in self.__map_annotations.markers.get_all():
            self.__adjust_marker(marker)

    def __adjust_marker(self, marker: MapMarker) -> None:
        """Adjust a marker to the current map scale

        Args:
            marker (QAbstractGraphicsShapeItem): Marker to adjust
            align_bottom (AlignBottom):  Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
        origin = marker.shape.transformOriginPoint()

        marker_size = self.__marker_size * marker.scale

        translate = self.__get_marker_position(
            origin, marker_size, marker.align_bottom, direction=-1
        )
        scale_factor = 1 / (
            self.__scale_factor * self.MARKER_ZOOM_ADJUSTMENT
            + (1 - self.MARKER_ZOOM_ADJUSTMENT)
        )

        marker.shape.setTransform(
            QTransform()
            .translate(translate.x(), translate.y())
            .scale(scale_factor, scale_factor)
            .translate(-translate.x(), -translate.y())
        )

    def __get_marker_position(
        self,
        position: QPointF | Position,
        marker_size: float,
        align_bottom: bool,
        direction: Literal[1, -1] = 1,
    ) -> QPointF:
        x = position.x() if isinstance(position, QPointF) else position.x
        y = position.y() if isinstance(position, QPointF) else position.y

        return QPointF(
            x - (marker_size / 2 * direction),
            (y - (marker_size * 0.99) * direction)
            if align_bottom
            else (y - (marker_size / 2 * direction)),
        )

    def __get_pen_size(self, scale: float = 1) -> float:
        """Calculate the pen size for a given scale

        Args:
            scale (float, optional): Additional scale. Useful to make some segment bigger than others. Defaults to 1.

        Returns:
            float: Pen size
        """
        return (
            self.SEGMENT_INITIAL_SIZE
            / (
                self.__scale_factor * self.SEGMENT_ZOOM_ADJUSTMENT
                + (1 - self.SEGMENT_ZOOM_ADJUSTMENT)
            )
            * scale
        )

    def __calculate_arrow(self, line: QLineF, size: float = 0.0002) -> QPolygonF:
        # Get and normalize direction of the segment
        direction = line.p2() - line.p1()
        direction /= math.sqrt(direction.x() ** 2 + direction.y() ** 2)

        # Define origin as the middle of the segment
        origin = (line.p1() + line.p2()) / 2 + (direction * size / 2)

        tangent = QPointF(direction.y(), -direction.x())

        return QPolygonF(
            [
                origin - (direction * size) - (tangent * -size / 2),
                origin,
                origin - (direction * size) - (tangent * size / 2),
            ]
        )

    def __set_brush_for_segment(
        self,
        segment_shape: QAbstractGraphicsShapeItem,
        line: QLineF,
        colors: List[QColor],
    ) -> QBrush:
        if len(colors) == 1:
            return QBrush(colors[0])

        brush = QLinearGradient(line.p1(), line.p2())

        count = math.floor(line.length() * 5000)

        for i in range(count):
            brush.setColorAt(i / count, colors[i % len(colors)])
            brush.setColorAt(i / count + 0.0000001, colors[(i + 1) % len(colors)])

        brush.setColorAt(1, colors[count % len(colors)])

        segment_pen = segment_shape.pen()
        segment_pen.setBrush(brush)
        segment_shape.setPen(segment_pen)

    def __set_config(self):
        """Initiate config for the view."""
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.viewport().setCursor(Qt.CursorShape.CrossCursor)

        Theme.set_background_color(self, "white")

    def __handle_is_computing(self, is_computing: bool) -> None:
        self.__is_computing = is_computing
        self.__update_cursor()

    def enterEvent(self, event: QEvent | None) -> None:
        self.__update_cursor()
        return super().enterEvent(event)

    def mouseMoveEvent(self, event: QEvent | None) -> None:
        self.__update_cursor()
        super().mouseMoveEvent(event)

    def __update_cursor(self) -> None:
        self.setCursor(
            Qt.CursorShape.WaitCursor
            if self.__is_computing
            else Qt.CursorShape.CrossCursor
        )
        self.viewport().setCursor(
            Qt.CursorShape.WaitCursor
            if self.__is_computing
            else Qt.CursorShape.CrossCursor
        )
