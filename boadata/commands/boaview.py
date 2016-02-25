import sys
import click
from  boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
def run_app(uri, type, **kwargs):
    from boadata import load
    do = load(uri, type)

    from boadata.gui import qt   # Force sip
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    # TODO: Think here?
    from . import enable_ctrl_c
    enable_ctrl_c()    

    from boadata.gui.qt import DataObjectWindow
    window = DataObjectWindow(data_object=do)
    window.show()
    window.setWindowTitle(do.uri)

    sys.exit(app.exec_())