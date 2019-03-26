#!/usr/bin/env python3
import sys

import click

from boadata import __version__
from boadata.cli import try_load, try_apply_sql, try_select_columns, try_select_rows, qt_app


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-c", "--columns", required=False, help="List of columns to show")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
@click.option("-l", "--lines", required=False, help="Lines (use slice notation)")
def run_app(uri, type, parameter, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    type = kwargs.get("type", None)

    do = try_load(uri, type=type, parameters=parameter)
    do = try_apply_sql(do, kwargs)
    do = try_select_columns(do, kwargs)
    do = try_select_rows(do, kwargs)

    with qt_app():
        from boadata.gui.qt.views import TableView
        
        view = TableView(data_object=do)
        widget = view.create_widget(None)
        widget.show()
        widget.setWindowTitle(do.uri)


if __name__ == "__main__":
    run_app()
