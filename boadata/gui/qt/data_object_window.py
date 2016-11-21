from qtpy import QtWidgets
from .views import View


class DataObjectWindow(QtWidgets.QMainWindow):
    def __init__(self, data_object, parent=None, *args, **kwargs):
        super(DataObjectWindow, self).__init__(parent, *args, **kwargs)
        self.data_object = data_object

        self.tabWidget = QtWidgets.QTabWidget(self)
        for view in View.registered_views:
            # print(data_object)
            if view.accepts(data_object):
                try:
                    self.tabWidget.addTab(view(data_object).create_widget(self), view.title)
                except BaseException as exc:
                    print(exc)
                    pass
            else:
                # print("View {0} not supported.".format(view.title))
                pass
                # self.tabWidget.addTab(QtGui.QLabel("Not supported"), view.title)

        self.setWindowTitle(self.data_object.title)
        self.setCentralWidget(self.tabWidget)
