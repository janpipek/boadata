import boadata.trees
from boadata.core.data_tree import DataTree
import sys
import click


@click.command()
@click.argument("uri")
@click.option('-f', "--full", default=False, is_flag=True, help="Show full path")
def run_app(uri, **kwargs):
    tree = None
    for cls in DataTree.registered_trees:
        if cls.accepts_uri(uri):
            tree = cls(uri)
    if not tree:
        print("URI not understood: {0}".format(uri))
        sys.exit(-1)
    else:
        tree.dump(full_title=kwargs.get("full"))