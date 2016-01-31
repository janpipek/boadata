from PyQt4 import QtGui
from .views import View


class DataObjectWindow(QtGui.QMainWindow):
    def __init__(self, data_object, parent=None, *args, **kwargs):
        super(DataObjectWindow, self).__init__(parent, *args, **kwargs)
        self.data_object = data_object

        self.tabWidget = QtGui.QTabWidget(self)
        for view in View.registered_views:
            if view.accepts(data_object):
                self.tabWidget.addTab(view(data_object).create_widget(), view.title)
            else:
                pass
                # self.tabWidget.addTab(QtGui.QLabel("Not supported"), view.title)

        self.setCentralWidget(self.tabWidget)

