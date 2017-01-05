from boadata import __version__
import sys
import click


@click.command()
@click.argument("uri")
@click.version_option(__version__)
@click.argument("x", default=None, required=False) #, help="Column or expression to be displayed on x axis.")
@click.argument("y", default=None, required=False) #, help="Column or expression to be displayed on y axis.")
@click.option("--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-s", "--scatter", "plot_type", default=True, flag_value="scatter", help="Scatter plot")
@click.option("-b", "--box", "plot_type", default=False, flag_value="box", help="Box plot")
@click.option("-l", "--line", "plot_type", default=False, flag_value="line", help="Line plot")
# @click.option("-j", "--joint", "plot_type", default=False, flag_value="joint", help="Joint plot")
@click.option("--logx", default=False, is_flag=True, help="Logarithmic scale on X axis")
@click.option("--logy", default=False, is_flag=True, help="Logarithmic scale on Y axis")
@click.option("--xlabel", help="Title for x axis", required=False)
@click.option("--ylabel", help="Title for y axis", required=False)
def run_app(uri, x, y, type, **kwargs):
    kwargs = {key : value for key, value in kwargs.items() if value is not None}
    
    from boadata import load
    try:
        do = load(uri, type)
    except:
        print("URI not understood:", uri)
        exit(-1)

    if "sql" in kwargs:
        do = do.sql(kwargs.get("sql"), table_name="data")        

    from boadata.gui import qt   # Force sip   
    from qtpy import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    from . import enable_ctrl_c
    enable_ctrl_c()

    from boadata.gui.qt.views import PlotView
    view = PlotView(data_object=do)
    if y:
        y = y.split(",")
    widget = view.create_widget(None, x, y, **kwargs)
    widget.show()
    widget.setWindowTitle(do.uri)

    sys.exit(app.exec_())