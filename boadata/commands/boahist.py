from boadata import load
from boadata.gui.qt.views import HistogramView
import sys
import click

from boadata.gui import qt   # Force sip
from PyQt4 import QtGui


@click.command()
@click.argument("uri")
@click.argument("x", default=None, required=False)
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option('-n', "--bins", default=50, type=int, help="How many bins")
@click.option('-r', "--relative", default=False, is_flag=True, help="Show relative frequency")
@click.option("-a", "--all", default=False, is_flag=True, help="Show histograms for all")
# @click.option('-r', "--relative", default=False, is_flag=True, "Show relative frequency")
@click.option("--logy", default=False, is_flag=True, help="Logarithmic scale on Y axis")
def run_app(uri, x, bins, type, **kwargs):
    try:
        do = load(uri, type)
    except:
        print("URI not understood:", uri)
        exit(-1)

    app = QtGui.QApplication(sys.argv)

    def show(x):
         view = HistogramView(data_object=do)
         widget = view.create_widget(xcol=x, bins=bins, **kwargs)
         widget.show()
         widget.setWindowTitle(do.uri)

    if kwargs.get("all"):
        i = 0
        for x in do.columns:
            col = do[x]
            try:
                print(col.dtype)
                if col.dtype != object:
                    view = HistogramView(data_object=col)
                    widget = view.create_widget(bins=bins, **kwargs)
                    widget.show()
                    widget.setWindowTitle(do.uri + "/" + x)
                    i += 1
                    if i > 10:
                        break
            except Exception as e:
                print(e)
    else:
        show(x)

    sys.exit(app.exec_())