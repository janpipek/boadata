from boadata.core import DataObject
from boadata.gui.qt.views import TableView
import sys

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui

def run_app():
    uri = sys.argv[1]
    try:
        do = DataObject.from_uri(uri)
    except:
        print("URI not understood.")
        exit(-1)

    app = QtGui.QApplication(sys.argv)
    view = TableView(data_object=do)
    widget = view.create_widget()
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())