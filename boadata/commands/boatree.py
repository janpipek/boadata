import boadata.trees
from boadata.core.data_tree import DataTree
import sys

def run_app():
    uri = sys.argv[1]
    tree = None
    for cls in DataTree.registered_trees:
        if cls.accepts_uri(uri):
            tree = cls(uri)
    if not tree:
        print("URI not understood: {0}".format(uri))
        sys.exit(-1)
    else:
        tree.dump()