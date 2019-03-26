#!/usr/bin/env python3
import sys

import click

from boadata import __version__
from boadata.cli import try_load, try_apply_sql, qt_app


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
def run_app(uri, type, parameter, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, kwargs)

    with qt_app():
        from boadata.gui.qt import DataObjectWindow

        window = DataObjectWindow(do)
        window.show()
        window.setWindowTitle(do.uri)


if __name__ == "__main__":
    run_app()
