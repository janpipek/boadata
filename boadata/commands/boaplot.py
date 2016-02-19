from boadata import load
from boadata.gui.qt.views import PlotView
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

    view = PlotView(data_object=do)
    widget = view.create_widget(*sys.argv[2:])
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())