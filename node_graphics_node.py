from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def load_style_sheet(filename):
    print("StyleSheet Loading: ", filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf_8"))


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = "qss/nodestyle.qss"
        load_style_sheet(self.stylesheet_filename)

        self.graphics_content = QGraphicsProxyWidget(self)
        self.node = node
        self.content = self.node.node_content

        self.title_item = QGraphicsTextItem(self)
        self._title_color = Qt.GlobalColor.white
        self._title_font = QFont("Ubuntu", 11)
        self.padding = 10.0

        self.width = 180
        self.height = 240
        self.edge_size = 10
        self.title_height = 30.0
        self.brush_title = QBrush(QColor("#FF313131"))
        self.brush_background = QBrush(QColor("#EF212121"))

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self.init_title()
        self.title = self.node.title

        self.init_ui()
        self.init_content()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            2 * self.edge_size + self.width,
            2 * self.edge_size + self.height
        )

    def init_ui(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    def init_title(self):
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.padding, 3)
        self.title_item.setTextWidth(
            self.width
            - 2 * self.padding
        )

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def init_content(self):
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.graphics_content.setWidget(self.content)
        self.graphics_content.node = self.node

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        super(QDMGraphicsNode, self).mouseMoveEvent(event)
        for node in self.scene().scene.nodes:
            if node.node_graphics.isSelected():
                node.update_connected_edges()

    def paint(self, painter, option: 'QStyleOptionGraphicsItem', widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path_outline.simplified())
