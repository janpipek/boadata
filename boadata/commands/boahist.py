from boadata import load
from boadata.gui.qt.views import HistogramView
import sys

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui

def run_app():
    uri = sys.argv[1]
    try:
        do = load(uri)
    except:
        print("URI not understood.")
        exit(-1)

    app = QtGui.QApplication(sys.argv)

    view = HistogramView(data_object=do)

    if len(sys.argv) > 2:
        column = sys.argv[2]
    else:
        column = None

    if len(sys.argv) > 3:
        bins = int(sys.argv[3])
    else:
        bins = 50
    widget = view.create_widget(column, bins)
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())