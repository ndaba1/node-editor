from PyQt5.QtWidgets import QDockWidget, QWidget, QListWidget


class QDMGraphicsDockWidget(QWidget):
    def __init__(self):
        super(QDMGraphicsDockWidget, self).__init__()
        self.list_widget = QListWidget()
        self.list_widget.addItem("Google")
        self.list_widget.addItem("Google")
        self.list_widget.addItem("Google")
        self.list_widget.addItem("Google")
        self.list_widget.addItem("Google")


class QDMDockWidget(QDockWidget):
    def __init__(self):
        super(QDMDockWidget, self).__init__()
        self.dock_widget_graphics = QDMGraphicsDockWidget()

        self.setWidget(self.dock_widget_graphics)
        self.setFloating(False)
        self.setGeometry(0, 0, 300, 600)



