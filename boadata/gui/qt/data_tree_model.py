from qtpy import QtCore, QtGui
from six import text_type


class DataTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data_node, parent=None):
        super(DataTreeModel, self).__init__(parent)
        self.data_node = data_node
        self.rootItem = DataTreeItem(self.data_node)
        data_node.changed.connect(self.on_node_changed, sender=data_node)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        """
        :type index: QtCore.QModelIndex
        :type role: int
        """
        if not index.isValid():
            return None
        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        elif role == QtCore.Qt.DecorationRole:
            if item.data_node.icon:
                return item.data_node.icon
            else:
                if item.data_node.children:
                    return QtGui.QIcon.fromTheme("folder")
                elif item.data_node.has_subtree():
                    return QtGui.QIcon.fromTheme("package-x-generic")
                else:
                    return None    # TODO: provide default
        return None

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
        if (orientation == QtCore.Qt.Horizontal
            and role == QtCore.Qt.DisplayRole):
            return ["Name", "Type", "Shape"][section]
        return None

    def on_node_changed(self, sender):
        self.reload()

    def reload(self):
        self.rootItem.reload_items()
        self.modelReset.emit()

    @property
    def title(self):
        return self.data_node.title


class DataTreeItem(object):
    def __init__(self, data_node, parent=None, subtrees=True):
        self.parent = parent
        self.data_node = data_node
        self.reload_items()

    def data(self, column):
        if column == 0:
            return self.data_node.title
        elif column == 1:
            node_type = self.data_node.node_type
            if self.data_node.has_subtree():
                node_type += " (%s)" % self.data_node.subtree().node_type
            return node_type
        elif self.data_node.has_object():
            if column == 2:
                if self.data_node.data_object.shape:
                    return " x ".join(text_type(dim) for dim in self.data_node.data_object.shape)
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
        return 1
        # return 3

    def reload_items(self):
        self.childItems = []
        for node_child in self.data_node.children:
            self.childItems.append(DataTreeItem(node_child, self))
        if self.data_node.has_subtree():
            subtree = self.data_node.subtree()
            if subtree:
                for tree_child in subtree.children:
                    self.childItems.append(DataTreeItem(tree_child, self))