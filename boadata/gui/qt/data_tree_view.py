from qtpy import QtCore, QtGui, QtWidgets
# from .views import registered_views
from six import text_type
import logging


class DataTreeView(QtWidgets.QTreeView):
    '''A customized tree view widget for data tree model.'''

    def __init__(self, model, parent=None, main_window=None):
        super(DataTreeView, self).__init__(parent)
        self.main_window = main_window
        self.setModel(model)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.openContextMenu)
        self.createMainMenu()
        self.doubleClicked.connect(self.on_double_click)

    def createMainMenu(self):
        '''Add a menu to main menu bar if the model offers it.

        The node has to implement menu_actions property for that.
        '''
        node = self.model().data_node
        actions = node.menu_actions
        if actions:
            self.menu = self.main_window.menuBar().addMenu(node.menu_title)
            for action in actions:
                self.menu.addAction(action)

    def on_double_click(self, index):
        data_node = index.internalPointer().data_node
        if data_node.has_object():
            self.main_window.show_object(data_node.data_object)

    def openContextMenu(self, position):
        '''Build context menu from available views of a node.
        '''

        class ViewAction(object):
            '''A Qt action resulting in showing a view for the object.'''
            def __init__(self, view, data_object, main_window):
                self.view = view
                self.data_object = data_object
                self.main_window = main_window

            def __call__(self):
                try:
                    self.main_window.show_view(self.view, self.data_object)
                except Exception as exc:
                    import traceback
                    message_box = QtGui.QMessageBox()
                    message_box.setWindowTitle("Error initializing "
                                               + self.view.title)
                    message_box.setText(text_type(exc))
                    message_box.setDetailedText(traceback.format_exc())
                    message_box.setIcon(QtGui.QMessageBox.Warning)
                    message_box.exec_()

        menu = QtGui.QMenu()
        indexes = self.selectedIndexes()
        if len(indexes) > 0:
            data_node = indexes[0].internalPointer().data_node
            if data_node.has_object():
                data_object = data_node.data_object
                for view in registered_views:
                    try:
                        if view.accepts(data_object):
                            menu.addAction(view.title, ViewAction(view, data_object,
                                                                  self.main_window))
                    except Exception as exc:
                        logging.warning("Cannot check acceptance for the combination {0} and {1}".format(view, data_object))
            if not menu.isEmpty():
                menu.exec_(self.viewport().mapToGlobal(position))
