from boadata import load
import boadata.data
from boadata.gui.qt import DataObjectWindow
import sys
import click

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui

@click.command()
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
def run_app(uri, type, **kwargs):
    do = load(uri, type)

    app = QtGui.QApplication(sys.argv)
    window = DataObjectWindow(data_object=do)
    window.show()
    window.setWindowTitle(do.uri)

    sys.exit(app.exec_())