import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_socket import *

EDGE_CP_ROUNDNESS = 100


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.PenStyle.DashLine)
        self._pen_dragging.setWidth(2)
        self._pen.setWidth(2.0)

        self.pos_source = [0, 0]
        self.pos_destination = [200, 200]

        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.setZValue(-1)

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def intersects_with(self, p1, p2):
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calc_path()
        return cutpath.intersects(path)

    def paint(self, painter, option: 'QStyleOptionGraphicsItem', widget=None):
        self.setPath(self.calc_path())

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._color_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

    def calc_path(self):
        raise NotImplemented("This method has to be overridden in a child class")


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_destination[0], self.pos_destination[1])
        return path


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def calc_path(self):
        s = self.pos_source
        d = self.pos_destination
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.edge.start_socket.position

        if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
            cpx_s *= -1
            cpx_d *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                (s[1] - d[1]) if (s[1] != d[1]) else 0.0001
                )
            ) * EDGE_CP_ROUNDNESS
            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                (d[1] - s[1]) if (s[1] != d[1]) else 0.0001
                )
            ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d,
                     self.pos_destination[0], self.pos_destination[1]
                     )
        return path
