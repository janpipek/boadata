#!/usr/bin/env python3
import sys

import click

from boadata import __version__
from boadata.cli import try_load, try_apply_sql


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option(
    "-l",
    "--limit",
    required=False,
    default=1000,
    help="Limit the number of rows to be printed.",
)
def run_app(uri, type, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    do = try_load(uri, type)
    do = try_apply_sql(do, kwargs)

    do = do.convert("pandas_data_frame")
    if do.shape[0] > kwargs.get("limit", 2 ** 62):
        print(
            "The row count is higher than the limit ({0}), dropping lines after that...".format(
                do.shape[0]
            )
        )
        do = do.head(kwargs.get("limit"))

    from tabulate import tabulate

    print(tabulate(do.inner_data, do.columns, tablefmt="orgtbl"))


if __name__ == "__main__":
    run_app()
