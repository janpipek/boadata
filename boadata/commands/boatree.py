import sys
import click
from boadata import __version__, tree


@click.command()
@click.version_option(__version__)
@click.argument("uri")
@click.option('-f', "--full-title", default=False, is_flag=True, help="Show full path")
@click.option('-i', "--info", default=False, is_flag=True, help="Show data info")
def run_app(uri, **kwargs):
    try:
        the_tree = tree(uri)
    except:
        print("URI not understood: {0}".format(uri))
        sys.exit(-1)
    else:
        the_tree.dump(full_title=kwargs.get("full_title"), data_object_info=kwargs.get("info"))