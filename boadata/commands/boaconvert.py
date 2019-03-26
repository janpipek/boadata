#!/usr/bin/env python3
import click

from boadata.core import DataObject
from boadata import __version__
from boadata.cli import try_load, try_apply_sql, try_select_columns, try_select_rows, try_sort


@click.command()
@click.version_option(__version__)
@click.argument("from_uri", nargs=-1)
@click.option("-T", "--in-type", default=None, help="What type is the object.")
@click.option("-o", "--output-uri", required=False, help="Where to write")
@click.option("-c", "--columns", required=False, help="List of columns to show")
@click.option("-s", "--sql", required=False, help="SQL to run on the object.")
@click.option("-t", "--type", default=None, help="What type should be the destination object.")
@click.option("-l", "--lines", required=False, help="Lines (as range)")
@click.option("-p", "--parameter", help="Additional parameters for loader, specified as key=value", multiple=True)
@click.option("-S", "--sortby", required=False, help="Sort by column(s).")
def run_app(from_uri, output_uri, in_type, parameter, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    type = kwargs.get("type")

    do = try_load(from_uri[0], type=in_type, parameters=parameter)
    if len(from_uri) > 1:
        others = (try_load(from_uri[i]) for i in range(1, len(from_uri)))
        do = do.concat(*others)        
    
    do = try_apply_sql(do, kwargs)
    do = try_select_columns(do, kwargs)
    do = try_sort(do, kwargs)
    do = try_select_rows(do, kwargs)

    if output_uri:
        if not type:
            for conversion in do.allowed_conversions:
                type_candidate = DataObject.registered_types[conversion[1]]
                if type_candidate.accepts_uri(output_uri):
                    type = conversion[1]
                    break
        if not type:
            print("No suitable output type found.")
            exit(-1)

        do.convert(type, uri=output_uri)
    else:
        print("Allowed conversions")
        print("-------------------")
        for conversion in do.allowed_conversions:
            print(conversion[1])


if __name__ == "__main__":
    run_app()
