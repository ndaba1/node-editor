import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from node_dock_widget import QDMDockWidget
from node_editor_widget import NodeEditorWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # dock_widget = QDMDockWidget()
        central_widget = NodeEditorWidget()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setCentralWidget(central_widget)
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)
        self.setWindowTitle("Node IDE")

        # self.statusBar().showMessage("Ready")
        # self.menuBar().addMenu("&File")

        self.setAutoFillBackground(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

