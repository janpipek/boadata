from PyQt4 import QtCore, QtGui
# from views import PropertyView
# import pyqtgraph as pg
from views import registered_views

from views import PropertyView

class DataTreeView(QtGui.QTreeView):
    def __init__(self, model, parent=None, main_window=None):
        super(DataTreeView, self).__init__(parent)
        self.main_window = main_window
        self.setModel(model)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def doubleClicked(self, index):
        pass

    def openMenu(self, position):
        # def show_table():
        #     window = QtGui.QMainWindow(self)
        #     table = pg.TableWidget(window)
        #     data = data_object.to("numpy_array")
        #     if len(data.shape) == 1:
        #         data = data.reshape(data.shape[0], 1)
        #     table.setData(data)
        #     table.update()
        #     window.setCentralWidget(table)
        #     window.show()
        #     window.update()

        # def show_graph():
        #     if len(data_object.shape) == 1:
        #         pg.plot(data_object.to("numpy_array"))
        #     if len(data_object.shape) == 2 and data_object.shape[1] == 2:
        #         data = data_object.to("numpy_array")
        #         pg.plot(data[:,0], data[:,1])

        def show_view(view):
            self.parent.show_view(view, data_object)

        menu = QtGui.QMenu()
        indexes = self.selectedIndexes()
        if len(indexes) > 0:
            data_node = indexes[0].internalPointer().data_node
            if data_node.has_object():
                data_object = data_node.data_object
                for view in registered_views:
                    if view.accepts(data_object):
                        menu.addAction(view.title, lambda: self.main_window.show_view(view, data_object))
            if not menu.isEmpty():
                menu.exec_(self.viewport().mapToGlobal(position))



