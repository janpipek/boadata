import sys
sys.path += [ "../.."]
from PyQt4 import QtCore, QtGui
from boadata.trees.file import DirectoryNode
from boadata.gui.qt import DataTreeView, DataTreeModel

def item_clicked(index):
    import pyqtgraph as pg
    node = index.internalPointer().data_node
    if node.has_object():
        data_object = node.data_object
        if len(data_object.shape) == 1:
            pg.plot(data_object.to("numpy_array"))
        if len(data_object.shape) == 2 and data_object.shape[1] == 2:
            data = data_object.to("numpy_array")
            pg.plot(data[:,0], data[:,1])

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    branch = DirectoryNode(sys.argv[1]) 
    model = DataTreeModel(branch)
    view = DataTreeView(model)
    view.setMinimumHeight(600)
    view.setMinimumWidth(800)
    view.setWindowTitle("Boadata tree example")
    # view.doubleClicked.connect(item_clicked)
    view.show()
    sys.exit(app.exec_())
