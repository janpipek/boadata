#!/usr/bin/env python3
from boadata import __version__
from boadata.cli import qt_app, try_load, try_apply_sql
import sys
import click


@click.command()
@click.argument("uri")
@click.version_option(__version__)
@click.argument(
    "x", default=None, required=False
)  # , help="Column or expression to be displayed on x axis.")
@click.argument(
    "y", default=None, required=False
)  # , help="Column or expression to be displayed on y axis.")
@click.option("-q", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
@click.option(
    "-s",
    "--scatter",
    "plot_type",
    default=True,
    flag_value="scatter",
    help="Scatter plot",
)
@click.option(
    "-b", "--box", "plot_type", default=False, flag_value="box", help="Box plot"
)
@click.option(
    "-l", "--line", "plot_type", default=False, flag_value="line", help="Line plot"
)
# @click.option("-j", "--joint", "plot_type", default=False, flag_value="joint", help="Joint plot")
@click.option("--logx", default=False, is_flag=True, help="Logarithmic scale on X axis")
@click.option("--logy", default=False, is_flag=True, help="Logarithmic scale on Y axis")
@click.option("--xlabel", help="Title for x axis", required=False)
@click.option("--ylabel", help="Title for y axis", required=False)
def run_app(uri, x, y, type, parameter, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, kwargs)

    if y:
        y = y.split(",")

    with qt_app():
        from boadata.gui.qt.views import PlotView

        view = PlotView(data_object=do)
        widget = view.create_widget(None, x, y, **kwargs)
        widget.show()
        widget.setWindowTitle(do.uri)


if __name__ == "__main__":
    run_app()
