from boadata import load
import boadata.data
from boadata.gui.qt.views import PlotView
import sys
import click

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui


@click.command()
@click.argument("uri")
@click.argument("x", default=None, required=False) #, help="Column or expression to be displayed on x axis.")
@click.argument("y", default=None, required=False) #, help="Column or expression to be displayed on y axis.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-s", "--scatter", "plot_type", default=True, flag_value="scatter", help="Scatter plot")
@click.option("-b", "--box", "plot_type", default=False, flag_value="box", help="Box plot")
@click.option("-l", "--line", "plot_type", default=False, flag_value="line", help="Line plot")
# @click.option("-j", "--joint", "plot_type", default=False, flag_value="joint", help="Joint plot")
@click.option("--logx", default=False, is_flag=True, help="Logarithmic scale on X axis")
@click.option("--logy", default=False, is_flag=True, help="Logarithmic scale on Y axis")
def run_app(uri, x, y, type, **kwargs):
    try:
        do = load(uri, type)
    except:
        print("URI not understood:", uri)
        exit(-1)

    app = QtGui.QApplication(sys.argv)

    view = PlotView(data_object=do)
    if y:
        y = y.split(",")
    widget = view.create_widget(x, y, **kwargs)
    widget.show()
    widget.setWindowTitle(do.uri)
    sys.exit(app.exec_())