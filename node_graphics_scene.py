import math

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        self._color_background = QColor("#393939")
        self.scene_width, self.scene_height = 64000, 64000
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")
        self.gridSize = 20
        self.gridSquares = 5

        self.pen_light = QPen(self._color_light)
        self.pen_light.setWidth(1)
        self.pen_dark = QPen(self._color_dark)
        self.pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def set_scene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light, lines_dark = [], []

        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(QLine(left, y, right, y)))

        painter.setPen(self.pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self.pen_dark)
        painter.drawLines(*lines_dark)
