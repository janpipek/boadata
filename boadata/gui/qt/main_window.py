from PyQt4.QtGui import QMainWindow, QMdiArea, QDockWidget, QMdiSubWindow, QAction, qApp, QFileDialog
from PyQt4 import QtCore
from data_tree_view import DataTreeView
from ...trees.file import DirectoryTree
from data_tree_model import DataTreeModel

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
        exit_action = QAction('&Exit', self)
        # exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('&File')
        open_menu = file_menu.addMenu('&Open')

        open_file_action = QAction('&File', self)
        open_file_action.triggered.connect(self.openFile)

        open_dir_action = QAction('&Directory', self)
        open_dir_action.triggered.connect(self.openDirDialog)

        open_menu.addAction(open_file_action)
        open_menu.addAction(open_dir_action)

        file_menu.addAction(exit_action)

    def openFile(self):
        pass

    def openDirDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_():
            directory = unicode(dialog.selectedFiles()[0])
            self.openDir(directory)

    def openDir(self, path):
        node = DirectoryTree(path)
        model = DataTreeModel(node)
        self.show_tree(model)

    def show_tree(self, model):
        widget = DataTreeView(model, main_window=self)
        self.tree_dock = QDockWidget(model.title, self)
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