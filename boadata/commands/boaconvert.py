#!/usr/bin/env python3
import click

from boadata.core import DataObject
from boadata.cli import try_load


@click.command()
@click.version_option(__version__)
@click.argument("from_uri")
@click.argument("to_uri", required=False, default=None)
@click.option(
    "-t", "--type", default=None, help="What type should be the destination object."
)
def run_app(from_uri, to_uri, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    type = kwargs.get("type")

    do = try_load(from_uri)

    if to_uri:
        if not type:
            for conversion in do.allowed_conversions:
                type_candidate = DataObject.registered_types[conversion[1]]
                if type_candidate.accepts_uri(to_uri):
                    type = conversion[1]
                    break
        if not type:
            print("No suitable output type found.")
            exit(-1)

        do.convert(type, uri=to_uri)
    else:
        print("Allowed conversions")
        print("-------------------")
        for conversion in do.allowed_conversions:
            print(conversion[1])


if __name__ == "__main__":
    run_app()
