#!/usr/bin/env python
import sys
from boadata.gui import qt    # Force sip API
import boadata.trees          # Load all trees
from boadata.core.data_tree import DataTree

from PyQt4 import QtGui
from boadata.gui.qt import MainWindow, DataTreeModel
import boadata.data


def run_app():
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv) > 1:
        uri = sys.argv[1]
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