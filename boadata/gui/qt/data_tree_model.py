from PyQt4 import QtCore, QtGui

class DataTreeModel(QtCore.QAbstractItemModel):
    # index(), parent(), rowCount(), columnCount(), and data()
    def __init__(self, data_node, parent=None):
        super(DataTreeModel, self).__init__(parent)
        self.data_node = data_node
        self.rootItem = DataTreeItem(self.data_node)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())            

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent
        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return ["Name", "Type", "Shape"][section]
        return None        

class DataTreeItem(object):
    def __init__(self, data_node, parent=None, subtrees=True):
        self.parent = parent
        self.data_node = data_node
        self.childItems = []
        for node_child in data_node.children:
            self.childItems.append(DataTreeItem(node_child, self))
        if data_node.has_subtree():
            for tree_child in data_node.subtree().children:
                self.childItems.append(DataTreeItem(tree_child, self))

    def data(self, column):
        if column == 0:
            return QtCore.QString(self.data_node.title)
        elif column == 1:
            node_type = self.data_node.node_type
            if self.data_node.has_subtree():
                node_type += " (%s)" % self.data_node.subtree().node_type
            return node_type
        elif self.data_node.has_object():
            if column == 2:
                return " x ".join(unicode(dim) for dim in self.data_node.data_object.shape)
        return ""

    def row(self):
        if self.parent:
            return self.parent.childItems.index(self)
        return 0        

    def childCount(self):
        return len(self.childItems)

    def child(self, row):
        return self.childItems[row]

    def columnCount(self):
        return 3