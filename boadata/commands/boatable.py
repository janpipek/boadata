from boadata import load
from boadata.gui.qt.views import TableView
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
    view = TableView(data_object=do)
    widget = view.create_widget()
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())