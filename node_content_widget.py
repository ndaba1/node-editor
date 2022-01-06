from PyQt5.QtWidgets import *


class QDMNodeContentWidget(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.wdg_label = QLabel("This is a title")
        self.init_ui()

    def init_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QDMTextEdit("foo"))

    def set_editing_flag(self, value):
        self.node.scene.gr_scene.views()[0].editing_flag = value


class QDMTextEdit(QTextEdit):
    def keyPressEvent(self, event) -> None:
        super(QDMTextEdit, self).keyPressEvent(event)

    def focusInEvent(self, event) -> None:
        super(QDMTextEdit, self).focusInEvent(event)
        self.parentWidget().set_editing_flag(True)

    def focusOutEvent(self, event) -> None:
        self.parentWidget().set_editing_flag(False)
        super(QDMTextEdit, self).focusOutEvent(event)
