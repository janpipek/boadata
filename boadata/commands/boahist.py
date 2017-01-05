import sys
import click
from boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.argument("x", default=None, required=False)
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option('-n', "--bins", default=50, type=int, help="How many bins")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option('-r', "--relative", default=False, is_flag=True, help="Show relative frequency")
# @click.option("-a", "--all", default=False, is_flag=True, help="Show histograms for all")
@click.option("--logy", default=False, is_flag=True, help="Logarithmic scale on Y axis")
@click.option("--xlabel", required=False, help="Label to be displayed on X axis")
@click.option("--title", required=False, help="Title of the plot")
@click.option("--kde", is_flag=True, default=False, help="Include smooth KDE line")
@click.option("--rug", is_flag=True, default=False, help="Include rugs")
@click.option("--hist/--no-hist", default=True, help="Show histogram boxes")
def run_app(uri, x, bins, type, **kwargs):
    from boadata import load
    try:
        do = load(uri, type)
    except:
        print("URI not understood:", uri)
        sys.exit(-1)

    from boadata.gui import qt   # Force sip
    from qtpy import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    from . import enable_ctrl_c
    enable_ctrl_c()

    kwargs = {key : value for key, value in kwargs.items() if value is not None}

    from boadata.gui.qt.views import HistogramView
    def show(x):
         view = HistogramView(data_object=do)
         widget = view.create_widget(xcol=x, bins=bins, **kwargs)
         widget.show()
         widget.setWindowTitle(do.uri)

    # TODO: not working properly
    if kwargs.get("all") and False:
        i = 0
        for x in do.columns:
            col = do[x]
            try:
                if col.dtype != object:
                    view = HistogramView(data_object=col)
                    widget = view.create_widget(None, bins=bins, **kwargs)
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

if __name__ == "__main__":
    run_app()