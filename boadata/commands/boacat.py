#!/usr/bin/env python
import sys
import click
from boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
def run_app(uri, type, **kwargs):
    from boadata import load
    do = load(uri, type)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    if "sql" in kwargs:
        do = do.sql(kwargs.get("sql"), table_name="data")
    do = do.convert("pandas_data_frame")

    from tabulate import tabulate
    print(tabulate(do.inner_data, do.columns))