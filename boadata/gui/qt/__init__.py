import sip
sip.setapi('QString', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)


from .data_tree_model import DataTreeModel
from .data_tree_view import DataTreeView
from .main_window import MainWindow
from .data_object_window import DataObjectWindow
from .selectable_item_list_view import SelectableItemListView

from . import views

_application = None

def get_application():
    import sys
    from qtpy import QtWidgets

    global _application
    if not _application:
        _application = QtWidgets.QApplication(sys.argv)
    return _application
