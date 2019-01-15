from boadata import __version__, load
from boadata.core import DataObject

import click


@click.command()
@click.version_option(__version__)
@click.argument("from_uri")
@click.argument("to_uri")
@click.option("-t", "--type", default=None, help="What type should be the destination object.")
def run_app(from_uri, to_uri, **kwargs):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}
    type = kwargs.get("type")

    do = load(from_uri)
    if not do:
        print("URI not understood: {0}").format(from_uri)
        sys.exit(-1)
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