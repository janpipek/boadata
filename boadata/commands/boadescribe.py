#!/usr/bin/env python3
import sys

import click

from boadata import __version__
from boadata.cli import try_load, try_apply_sql


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
def run_app(uri, type, parameter, **kwargs):
    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, kwargs)

    print("Type: {0}".format(do.type_name))
    print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
    print("Data shape: {0}".format(do.shape))
    columns = do.columns
    if columns:
        print("Columns:")
        for name in columns:
            s = "  - {0}".format(name)
            try:
                s += " (dtype={0})".format(do[name].dtype)
            except:
                pass
            print(s)


if __name__ == "__main__":
    run_app()
