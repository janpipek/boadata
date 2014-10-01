from PyQt4.QtGui import QMainWindow, QMdiArea, QDockWidget
from PyQt4 import QtCore
from data_tree_view import DataTreeView

# Inspired by https://github.com/Werkov/PyQt4/blob/master/examples/mainwindows/mdi/mdi.py

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.create_menus()

    def create_menus(self):
        pass

    def show_tree(self, model):
        widget = DataTreeView(model)
        self.tree_dock = QDockWidget("Data tree", self)
        self.tree_dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.tree_dock)