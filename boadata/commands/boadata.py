#!/usr/bin/env python
import sys
import click
from boadata import __version__


@click.command()
@click.version_option(__version__)
@click.argument("uri", default=None, required=False)
def run_app(uri=None):
    import boadata.data
    import boadata.trees          # Load all trees
    from boadata.gui import qt    # Force sip API
    from PyQt4 import QtGui
    from boadata.core.data_tree import DataTree
    from boadata.gui.qt import MainWindow, DataTreeModel

    app = QtGui.QApplication(sys.argv)

    if uri:
        tree = None
        try:
            for cls in DataTree.registered_trees:
                if cls.accepts_uri(uri):
                    tree = cls(uri)
        except:
            print("URI not understood.")
            exit(-1)
        if not tree:
            print("URI not understood.")
            exit(-1)
        model = DataTreeModel(tree)
    else:
        model = None

    mw = MainWindow()
    if model:
        mw.show_tree(model)
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()