#!/usr/bin/env python3
import sys

import click
from tabulate import tabulate

from boadata import __version__
from boadata.cli import try_load, try_apply_sql, try_select_columns, try_select_rows, try_sort
from boadata.core import DataObject


def show_table(do: DataObject):
    print(tabulate(do.inner_data, do.columns, tablefmt="orgtbl"))


def show_expanded(do: DataObject):
    try:
        import colorama
        highlight = colorama.Fore.LIGHTGREEN_EX
        normal = colorama.Fore.LIGHTBLUE_EX
        reset = colorama.Fore.RESET
    except ImportError:
        highlight = ""
        normal = ""
        reset = ""

    for i in range(do.shape[0]):
        for column in do.columns:
            value = do.inner_data.iloc[i][column]
            line = (normal + str(column) + reset + ": " + highlight + str(value) + reset)
            print(line)
        print("--------------------------------- " + str(i))


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-c", "--columns", required=False, help="List of columns to show")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-S", "--sortby", required=False, help="Sort by column(s).")
@click.option("-x", "--expand", is_flag=True, default=False, help="Show each row expanded.")
@click.option("-l", "--lines", required=False, help="Lines (as range)")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
def run_app(uri, type, parameter, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    expand = kwargs.pop("expand", False)

    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, kwargs)
    do = try_select_columns(do, kwargs)
    do = try_sort(do, kwargs)
    do = try_select_rows(do, kwargs)

    do = do.convert("pandas_data_frame")
    if do.shape[0] > kwargs.get("limit", 2 ** 62):
        print(
            "The row count is higher than the limit ({0}), dropping lines after that...".format(
                do.shape[0]
            )
        )
        do = do.head(kwargs.get("limit"))

    if expand:
        show_expanded(do)
    else:
        show_table(do)


if __name__ == "__main__":
    run_app()
