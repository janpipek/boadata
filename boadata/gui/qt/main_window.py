from PyQt4.QtGui import QMainWindow, QMdiArea, QDockWidget, QMdiSubWindow, QAction, qApp
from PyQt4 import QtCore
from data_tree_view import DataTreeView

# Inspired by https://github.com/Werkov/PyQt4/blob/master/examples/mainwindows/mdi/mdi.py

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.setCentralWidget(self.mdiArea)
        self.create_menus()
        self.setWindowTitle("Boa data")

    def create_menus(self):
        exitAction = QAction('&Exit', self)        
        # exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def show_tree(self, model):
        widget = DataTreeView(model, main_window=self)
        self.tree_dock = QDockWidget("Data tree", self)
        self.tree_dock.setWidget(widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.tree_dock)

    def show_view(self, view, data_object):
        widget = view(data_object).widget

        # Not working yet
        sw = QMdiSubWindow()
        sw.setWidget(widget)
        sw.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        sw.setWindowTitle(data_object.title + "(" + view.title + ")")
        
        self.mdiArea.addSubWindow(sw)
        sw.show()
        sw.widget().show()
        widget.setFocus()