from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        super().__init__(socket.node.node_graphics)

        self.own_socket = socket
        self.radius = 6.0
        self.outline_width = 1
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52e220"),
            QColor("#FF0056a6"),
            QColor("#FFa86db1"),
            QColor("#FFb54747"),
            QColor("#FFdbe220"),
        ]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, option: 'QStyleOptionGraphicsItem', widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width)
        )

    # def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
    #     print("Socket was clicked")
