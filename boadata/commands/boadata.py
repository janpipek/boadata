#!/usr/bin/env python
import os
import sys
import re
from boadata.gui import qt   # Force sip API

from PyQt4 import QtGui
from boadata.trees.file import DirectoryTree, FileNode
from boadata.trees.generic import GenericTree
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
            if os.path.isdir(path):
                node = DirectoryTree(path)
            elif os.path.isfile(path):
                file_node = FileNode(path)
                if file_node.has_subtree():
                    node = file_node.subtree()
                else:
                    node = GenericTree()
                    node.title = "Open Files"
                    node.add_child(file_node)
            else:
                raise Exception("Cannot open path %s" % path)
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