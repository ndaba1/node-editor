from PyQt5.QtWidgets import QGraphicsItem
from node_graphics_node import QDMGraphicsNode
from node_content_widget import *
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM


class Node(QGraphicsItem):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):

        super().__init__()
        self.scene = scene
        self.title = title

        self.scene.add_node(self)
        self.node_content = QDMNodeContentWidget(self)
        self.node_graphics = QDMGraphicsNode(self)
        self.scene.gr_scene.addItem(self.node_graphics)
        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []
        self.modifiers = []
        count = 0
        for item in inputs:
            socket = Socket(node=self, index=count, position=LEFT_BOTTOM, socket_type=item)
            count += 1
            self.inputs.append(socket)

        count = 0
        for item in outputs:
            socket = Socket(node=self, index=count, position=RIGHT_TOP, socket_type=item)
            count += 1
            self.outputs.append(socket)

    def __str__(self):
        return f"<Node {hex(id(self))[2:5]}...{hex(id(self))[-3:]} >"

    @property
    def pos(self):
        return self.node_graphics.pos()

    def set_pos(self, x, y):
        self.node_graphics.setPos(x, y)

    def get_socket_pos(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.node_graphics.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.node_graphics.height - self.node_graphics.edge_size - index * self.socket_spacing
        else:
            y = self.node_graphics.title_height + self.node_graphics.padding + self.node_graphics.edge_size + index * 24

        return [x, y]

    def update_connected_edges(self):
        for socket in self.inputs + self.outputs:
            if socket.has_edge():
                socket._edge.update_position()

    def remove(self):
        for socket in (self.inputs+self.outputs):
            if socket.has_edge():
                socket._edge.remove()

        self.scene.gr_scene.removeItem(self.node_graphics)
        self.node_graphics = None

        self.scene.remove_node(self)