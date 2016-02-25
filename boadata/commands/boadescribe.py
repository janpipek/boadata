#!/usr/bin/env python
import sys
import click
from boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type is the object.")
def run_app(uri, type, **kwargs):
    kwargs = {key : value for key, value in kwargs.items() if value is not None}

    from boadata import load
    do = load(uri, type)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    if "sql" in kwargs:
        do = do.sql(kwargs.get("sql"), table_name="data")    

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