import sys
import click
from  boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
def run_app(uri, type, **kwargs):
    kwargs = {key : value for key, value in kwargs.items() if value is not None}

    from boadata import load
    do = load(uri, type)
    if "sql" in kwargs:
        do = do.sql(kwargs.get("sql"), table_name="data")       

    from boadata.gui import qt   # Force sip
    from qtpy import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    # TODO: Think here?
    from . import enable_ctrl_c
    enable_ctrl_c()    

    from boadata.gui.qt import DataObjectWindow
    window = DataObjectWindow(data_object=do)
    window.show()
    window.setWindowTitle(do.uri)

    sys.exit(app.exec_())