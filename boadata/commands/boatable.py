from boadata import __version__
import sys
import click


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
    from . import enable_ctrl_c
    enable_ctrl_c()    

    from boadata.gui.qt.views import TableView
    view = TableView(data_object=do)
    widget = view.create_widget(None)
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())