from PyQt5.QtWidgets import *

from node_edge import Edge
from node_graphics_scene import QDMGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_view import QDMGraphicsView
from node_scene import NodeScene
from node_node import Node
from node_socket import Socket


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = NodeScene()
        # self.grScene = self.scene.gr_scene
        self.layout = QVBoxLayout()
        self.view = QDMGraphicsView(self.scene.gr_scene, self)

        self.add_nodes()
        self.init_ui()

    def init_ui(self):
        # self.setGeometry(100, 100, 800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # instantiate the View
        self.setLayout(self.layout)

        # show the view
        self.layout.addWidget(self.view)
        self.setWindowTitle("Node IDE")
        # self.add_debug_content()
        self.show()

    def add_nodes(self):
        node1 = Node(self.scene, "Div", inputs=[1, 2, 4], outputs=[1])
        node2 = Node(self.scene, "Nav", inputs=[1, 2], outputs=[1])
        node3 = Node(self.scene, "Div", inputs=[1, 2, 3], outputs=[1])
        node4 = Node(self.scene, "Footer", inputs=[1, 2], outputs=[1])
        node5 = Node(self.scene, "Section", inputs=[1, 2, 3], outputs=[1])
        node1.set_pos(-350, -250)
        node2.set_pos(-75, 0)
        node3.set_pos(200, -150)
        node4.set_pos(100, 200)
        node5.set_pos(22, 46)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=2)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], edge_type=2)


    def add_debug_content(self):
        green_brush = QBrush(Qt.GlobalColor.green)
        outline_pen = QPen(Qt.GlobalColor.black)

        outline_pen.setWidth(2)
        rect = self.scene.addRect(-100, -100, 80, 100, outline_pen, green_brush)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
