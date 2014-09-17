from PyQt4 import QtCore, QtGui
import pyqtgraph as pg

class DataTreeView(QtGui.QTreeView):
    def __init__(self, model, parent=None):
        super(DataTreeView, self).__init__(parent)
        self.setModel(model)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def doubleClicked(self, index):
        pass

    def openMenu(self, position):
        def show_table():
            window = QtGui.QMainWindow(self)
            table = pg.TableWidget(window)
            data = data_object.to("numpy_array")
            if len(data.shape) == 1:
                data = data.reshape(data.shape[0], 1)
            table.setData(data)
            table.update()
            window.setCentralWidget(table)
            window.show()
            window.update()

        def show_graph():
            if len(data_object.shape) == 1:
                pg.plot(data_object.to("numpy_array"))
            if len(data_object.shape) == 2 and data_object.shape[1] == 2:
                data = data_object.to("numpy_array")
                pg.plot(data[:,0], data[:,1])

        menu = QtGui.QMenu()
        # menu.addAction("Hah")
        indexes = self.selectedIndexes()
        if len(indexes) > 0:
            data_node = indexes[0].internalPointer().data_node
            if data_node.has_object():
                data_object = data_node.data_object
                print data_object
                if len(data_object.shape) < 3:
                    menu.addAction("Show table", show_table)
                if len(data_object.shape) == 1:
                    menu.addAction("Show graph", show_graph)
                if len(data_object.shape) == 2 and data_object.shape[1] == 2:
                    menu.addAction("Show graph", show_graph)
            menu.exec_(self.viewport().mapToGlobal(position))



