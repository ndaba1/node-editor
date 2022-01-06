from node_graphics_edge import *

DIRECT_EDGE = 1
BEZIER_EDGE = 2
DEBUG = False


class Edge:
    def __init__(self, scene, start_socket, end_socket, edge_type=DIRECT_EDGE):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket._edge = self
        if self.end_socket is not None:
            self.end_socket._edge = self

        self.edge_graphics = QDMGraphicsEdgeDirect(self) if (edge_type == DIRECT_EDGE) else QDMGraphicsEdgeBezier(self)

        self.update_position()
        self.scene.gr_scene.addItem(self.edge_graphics)
        self.scene.add_edge(self)

    def __str__(self):
        return f"<Edge {hex(id(self))[2:5]}...{hex(id(self))[-3:]} >"

    def update_position(self):
        source_pos = self.start_socket.get_socket_position()
        source_pos[0] += self.start_socket.node.node_graphics.pos().x()
        source_pos[1] += self.start_socket.node.node_graphics.pos().y()
        self.edge_graphics.set_source(*source_pos)
        if self.end_socket is not None:
            destination_pos = self.end_socket.get_socket_position()
            destination_pos[0] += self.end_socket.node.node_graphics.pos().x()
            destination_pos[1] += self.end_socket.node.node_graphics.pos().y()
            self.edge_graphics.set_destination(*destination_pos)
        else:
            self.edge_graphics.set_destination(*source_pos)
        self.edge_graphics.update()

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket._edge = None
        if self.end_socket is not None:
            self.end_socket._edge = None
        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.gr_scene.removeItem(self.edge_graphics)
        self.edge_graphics = None
        try:
            self.scene.remove_edge(self)
        except ValueError:
            pass
        if DEBUG: print("View:EDGE --> Edge Removed", self)

