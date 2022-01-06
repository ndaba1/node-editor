from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_edge import Edge, BEZIER_EDGE
from node_graphics_cutline import QDMGraphicsCutline
from node_graphics_edge import QDMGraphicsEdge
from node_graphics_socket import QDMGraphicsSocket

NODE_NOOP = 1
NODE_EDGE_DRAG = 2
NODE_CUTLINE = 3
NODE_SELECT_MODE = 4
NODE_MOVING_MODE = 5

EDGE_DRAG_THRESHOLD = 10

DEBUG = False


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)

        self.grScene = grScene

        self.init_ui()

        self.setScene(self.grScene)

        self.mode = NODE_NOOP
        self.editing_flag = False
        self.cutline = QDMGraphicsCutline()
        self.grScene.addItem(self.cutline)

        self.zoom_in_fac = 1.25
        self.zoom = 10
        self.zoom_clamp = False
        self.zoom_step = 10
        self.zoom_range = [-50, 50]
        self.zoom_out_fac = 1 / self.zoom_in_fac

    def init_ui(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_mouse_press(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.left_mouse_press(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middle_mouse_release(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.left_mouse_release(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_release(event)
        else:
            super().mousePressEvent(event)

    def middle_mouse_press(self, event):
        release_event = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton,
                                 event.modifiers())
        super().mousePressEvent(fake_event)

    def middle_mouse_release(self, event):
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.MouseButton.LeftButton,
                                 event.buttons() | Qt.MouseButton.LeftButton,
                                 event.modifiers())
        self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(fake_event)

    def left_mouse_press(self, event):
        item = self.get_item_at_click(event)
        self.lmb_click_pos = self.mapToScene(event.pos())
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if DEBUG:
                    print("LMB + Shift on", item)
                event.ignore()
                fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                         Qt.MouseButton.LeftButton, event.buttons() | Qt.MouseButton.LeftButton,
                                         event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mousePressEvent(fake_event)
                return
        if type(item) is QDMGraphicsSocket:
            if self.mode == NODE_NOOP:
                self.mode = NODE_EDGE_DRAG
                self.edge_drag_start(item)
                return

        if self.mode == NODE_EDGE_DRAG:
            res = self.edge_drag_end(item)
            if res:
                return

        if item is None:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mode = NODE_CUTLINE
                fake_event = QMouseEvent(QEvent.Type.MouseButtonRelease, event.localPos(), event.screenPos(),
                                         Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton, event.modifiers())
                super().mouseReleaseEvent(fake_event)
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
                return

        super().mousePressEvent(event)

    def left_mouse_release(self, event):
        item = self.get_item_at_click(event)

        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                if DEBUG:
                    print("LMB Release + Shift on", item)
                event.ignore()
                fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                         Qt.MouseButton.LeftButton, Qt.MouseButton.NoButton,
                                         event.modifiers() | Qt.KeyboardModifier.ControlModifier)
                super().mouseReleaseEvent(fake_event)
                return

        if self.mode == NODE_EDGE_DRAG:
            new_lmb_release_pos = self.mapToScene(event.pos())
            dist_scene = new_lmb_release_pos - self.lmb_click_pos
            if (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > EDGE_DRAG_THRESHOLD*EDGE_DRAG_THRESHOLD:
                res = self.edge_drag_end(item)
                if res:
                    return

        if self.mode == NODE_CUTLINE:
            self.cut_intersecting_lines()
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.mode = NODE_NOOP
            return

    def right_mouse_press(self, event):
        super().mousePressEvent(event)
        item = self.get_item_at_click(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge):
                print("RMB DEBUG MODE:", item.edge, "connecting", item.edge.start_socket, "<-->",
                      item.edge.end_socket)
            if type(item) is QDMGraphicsSocket:
                print("RMD DEBUG MODE:", item.own_socket, "has edge:", item.own_socket._edge)
            print("RMB DEBUG MODE:", item)

            if item is None:
                print("SCENE:")
                print(" Nodes:  ")
                for node in self.grScene.scene.nodes: print("    ", node)
                print(" Edges:   ")
                for edge in self.grScene.scene.edges: print("   ", edge)

    def right_mouse_release(self, event):
        super().mouseReleaseEvent(event)

    def edge_drag_start(self, item):
        if DEBUG:
            print("View::Edges -> Start dragging edge")
        if DEBUG:
            print("View::Edges -> assign start socket to...", item.own_socket)
        self.previous_edge = item.own_socket._edge
        self.last_start_socket = item.own_socket
        self.drag_edge = Edge(self.grScene.scene, item.own_socket, None, BEZIER_EDGE)

    def edge_drag_end(self, item):
        self.mode = NODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if item.own_socket != self.last_start_socket:
                    if DEBUG:
                        print("View::Edges -> assign end socket to...", item.own_socket)
                    if item.own_socket.has_edge():
                        item.own_socket._edge.remove()
                    if self.previous_edge is not None:
                        self.previous_edge.remove()
                    self.drag_edge.start_socket = self.last_start_socket
                    self.drag_edge.end_socket = item.own_socket
                    self.drag_edge.start_socket.set_connected_edge(self.drag_edge)
                    self.drag_edge.end_socket.set_connected_edge(self.drag_edge)
                    self.drag_edge.update_position()
            return True

        if DEBUG:
            print("View::Edges -> End dragging edge")
        self.drag_edge.remove()
        self.drag_edge = None
        if self.previous_edge is not None:
            self.previous_edge.start_socket._edge = self.previous_edge

        return False

    def mouseMoveEvent(self, event):
        if self.mode == NODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.edge_graphics.set_destination(pos.x(), pos.y())
            self.drag_edge.edge_graphics.update()

        if self.mode == NODE_CUTLINE:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        zoom_clamp = None

        if event.angleDelta().y() > 0:
            zoom_fac = self.zoom_in_fac
            self.zoom += self.zoom_step

        else:
            zoom_fac = self.zoom_out_fac
            self.zoom -= self.zoom_step

        if self.zoom < self.zoom_range[0]:
            self.zoom, zoom_clamp = self.zoom_range[0], True
        elif self.zoom > self.zoom_range[1]:
            self.zoom, zoom_clamp = self.zoom_range[1], True

        if not zoom_clamp:
            self.scale(zoom_fac, zoom_fac)

    def get_item_at_click(self, event):
        pos = event.pos()
        object = self.itemAt(pos)

        return object

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            if not self.editing_flag:
                self.delete_selected()
            else:
                super(QDMGraphicsView, self).keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def delete_selected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                if DEBUG: print("View::DELETING --> Removing Edge", item)
                item.edge.remove()
            elif hasattr(item, "node"):
                if DEBUG: print("View::DELETING --> Removing Node", item)
                item.node.remove()

    def cut_intersecting_lines(self):
        for index in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[index]
            p2 = self.cutline.line_points[index - 1]
            for edge in self.grScene.scene.edges:
                if edge.edge_graphics.intersects_with(p1, p2):
                    edge.remove()





