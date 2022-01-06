from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QDMGraphicsCutline(QGraphicsItem):
    def __init__(self, parent=None):
        super(QDMGraphicsCutline, self).__init__(parent)

        self.line_points = []

        self._pen = QPen(Qt.GlobalColor.white)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        return QRectF(0, 0, 1, 1)

    def paint(self, painter, option: 'QStyleOptionGraphicsItem', widget=None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)