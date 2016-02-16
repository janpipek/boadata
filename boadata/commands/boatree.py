import boadata.trees
from boadata.core.data_tree import DataTree
import sys

def run_app():
    uri = sys.argv[1]
    try:
        for cls in DataTree.registered_trees:
            if cls.accepts_uri(uri):
                tree = cls(uri)
    except:
        print("URI not understood.")
        exit(-1)
    tree.dump()