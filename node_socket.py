from node_graphics_socket import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4


class Socket:
    def __init__(self, node, socket_type, index=0, position=LEFT_TOP):
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.graphics_socket = QDMGraphicsSocket(self, self.socket_type)

        self.graphics_socket.setPos(*self.node.get_socket_pos(index, position))

        self._edge = None

    def __str__(self):
        return f"<Socket {hex(id(self))[2:5]}...{hex(id(self))[-3:]} >"

    def get_socket_position(self):
        return self.node.get_socket_pos(self.index, self.position)

    def set_connected_edge(self, edge):
        self._edge = edge

    def has_edge(self):
        return self._edge is not None
