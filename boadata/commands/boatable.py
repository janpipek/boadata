from boadata import __version__
import sys
import click


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
    from . import enable_ctrl_c
    enable_ctrl_c()    

    from boadata.gui.qt.views import TableView
    view = TableView(data_object=do)
    widget = view.create_widget()
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())