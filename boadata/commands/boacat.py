#!/usr/bin/env python
import sys
import click
from boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-l", "--limit", required=False, default=1000, help="Limit the number of rows to be printed.")
def run_app(uri, type, **kwargs):
    kwargs = {key : value for key, value in kwargs.items() if value is not None}

    from boadata import load
    do = load(uri, type)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    if "sql" in kwargs:
        do = do.sql(kwargs.get("sql"), table_name="data")
    do = do.convert("pandas_data_frame")
    if do.shape[0] > kwargs.get("limit", 2*62):
        print("The row count is higher than the limit ({0}), dropping lines after that...".format(do.shape[0]))
        do = do.head(kwargs.get("limit"))

    from tabulate import tabulate
    print(tabulate(do.inner_data, do.columns, tablefmt="orgtbl"))