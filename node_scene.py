from PyQt5.QtWidgets import QGraphicsScene
from node_graphics_scene import *


class NodeScene:
    def __init__(self):
        super(NodeScene, self).__init__()
        self.gr_scene = QDMGraphicsScene(self)
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.init_ui()

    def init_ui(self):
        self.gr_scene.set_scene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
