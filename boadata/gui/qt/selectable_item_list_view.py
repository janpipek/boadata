from qtpy import QtCore, QtGui, QtWidgets


class SelectableItemListView(QtWidgets.QListView):
    '''A list widget built on top of the SelectableItemList objects.'''
    def __init__(self, item_list, parent=None):
        super(SelectableItemListView, self).__init__(parent)
        self.item_list = item_list
        
        self.model = QtGui.QStandardItemModel(self)
        self.setModel(self.model)
        self.items = {}

        for key in self.item_list:
            self.createItem(key)

        for key in self.item_list.selected_items:
            self.select(key)

        self.model.itemChanged.connect(self.onItemChanged)

        self.item_list.item_added.connect(self.on_added, sender=self.item_list)
        self.item_list.item_removed.connect(self.on_removed, sender=self.item_list)
        self.item_list.item_selected.connect(self.on_selected, sender=self.item_list)
        self.item_list.item_deselected.connect(self.on_deselected, sender=self.item_list)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, point):
        context_menu = QtWidgets.QMenu("Test", self)
        context_menu.addAction("Update list", self.item_list.update)
        context_menu.exec_( self.mapToGlobal(point) )

    def select(self, key):
        item = self.items[key]
        item.setCheckState(QtCore.Qt.Checked)

    def deselect(self, key):
        item = self.items[key]
        item.setCheckState(QtCore.Qt.Unchecked)

    def createItem(self, key, order=None):
        item = QtGui.QStandardItem(self.item_list.item_title(key))
        item.setData(key)
        item.setCheckable(True)
        self.items[key] = item
        self.model.appendRow(item)

    def on_added(self, sender, key):
        self.createItem(key)

    def on_removed(self, sender, key):
        item = self.items[key]
        index = self.model.indexFromItem(item)
        self.model.removeRows(index.row, 1)
        del self.items[key]

    def on_selected(self, sender, item):
        self.select(item)

    def on_deselected(self, sender, item):
        self.deselect(item)

    def onItemChanged(self, item):
        key = item.data().toPyObject()
        if item.checkState() == QtCore.Qt.Checked:
            self.item_list.select(key)
        else:
            self.item_list.deselect(key)     
