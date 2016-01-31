from boadata.trees.file import DirectoryTree
import sys

def run_app():
    uri = sys.argv[1]
    try:
        tree = DirectoryTree(uri)
    except:
        print("URI not understood.")
        exit(-1)
    tree.dump()