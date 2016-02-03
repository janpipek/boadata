from boadata.core import DataObject
from boadata.gui.qt import DataObjectWindow
import sys

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui

def run_app():
    uri = sys.argv[1]
    do = DataObject.from_uri(uri)

    app = QtGui.QApplication(sys.argv)
    window = DataObjectWindow(data_object=do)
    window.show()
    window.setWindowTitle(do.uri)

    sys.exit(app.exec_())