#!/usr/bin/env python
import sys
import re
sys.path += [ "../.."]
from PyQt4 import QtCore, QtGui
from boadata.trees.file import DirectoryTree
try:
    from boadata.trees.sql import DatabaseTree
except ImportError:
    pass
from boadata.gui.qt import MainWindow, DataTreeModel


def run_app():
    app = QtGui.QApplication(sys.argv)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        # TODO: Implement tree-opening protocols
        if re.search("sql.*://", path):
            node = DatabaseTree(path)
        else:
            node = DirectoryTree(path)
        model = DataTreeModel(node) 
    else:
        model = None

    mw = MainWindow()
    if model:
        mw.show_tree(model)
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()