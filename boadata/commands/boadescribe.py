#!/usr/bin/env python3
import sys

import click
from pandas import DataFrame, RangeIndex

from boadata import __version__
from boadata.cli import try_load, try_apply_sql


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
@click.option("-S", "--summary", help="Include summary using pandas describe.", is_flag=True)
def run_app(uri, type, parameter, **kwargs):
    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, kwargs)

    print("Type: {0}".format(do.type_name))
    print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
    print("Data shape: {0}".format(do.shape))
    columns = do.columns
    if hasattr(do.inner_data, "index"):
        # TODO: Include in the interface rather...
        print("Index:")
        index = do.inner_data.index
        s = f"  - {index.name or '<no name>'}"
        try:
            if isinstance(index, RangeIndex):
                s += f" ({index.start}..{index.stop}"
                if index.step != 1:
                    s += f", step={step}"
                s += ")"
            else:
                s += " (dtype={0})".format(index.dtype)
        except:
            pass
        print(s)
    if columns:
        print("Columns:")
        for name in columns:
            s = "  - {0}".format(name)
            try:
                s += " (dtype={0})".format(do[name].dtype)
            except:
                pass
            print(s)
    if kwargs.get("summary"):
        print("Summary (DataFrame.describe()):")
        if isinstance(do.inner_data, DataFrame):
            df: DataFrame = do.inner_data
            print("\n".join("  " + line for line in str(df.describe()).splitlines()))
        else:
            print("  Not supported :-(")


if __name__ == "__main__":
    run_app()
