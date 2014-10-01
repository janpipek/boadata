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
        '''Build menu from available views.'''
        
        class ViewAction(object):
            def __init__(self, view, data_object, main_window):
                self.view = view
                self.data_object = data_object
                self.main_window = main_window

            def __call__(self):
                self.main_window.show_view(self.view, self.data_object)

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
                        # pass
                        menu.addAction(view.title, ViewAction(view, data_object, self.main_window))
            if not menu.isEmpty():
                menu.exec_(self.viewport().mapToGlobal(position))



