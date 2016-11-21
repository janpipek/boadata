from qtpy import QtCore, QtGui, QtWidgets


class ColumnModel(QtCore.QAbstractListModel):
    def __init__(self, data_object, parent=None):
        """

        :type data_object: boadata.core.DataObject
        :return:
        """
        super(ColumnModel, self).__init__(parent)
        self.columns = list(data_object.columns)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return 0
        else:
            return len(self.columns)

    def data(self, index, role=None):
        """
        :type index: QtCore.QModelIndex
        :type role: int
        """
        if not index.isValid():
            return None
        # item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return self.columns[index.row()]

    def add_column(self, name):
        if not name in self.columns:
            self.columns.append(name)

    def get_index(self, name):
        return self.columns.index(name)


class ColumnSelect(QtWidgets.QListView):
    def __init__(self, data_object, parent=None):
        super(ColumnSelect, self).__init__(parent)
        self.setModel(ColumnModel(data_object, self))

    # @property
    def selected_columns(self):
        return [self.model().data(index, QtCore.Qt.DisplayRole) for index in self.selectedIndexes()]

    def select_columns(self, columns):
        for c in columns:
            self.model().add_column(c)

        rows = [self.model().get_index(name) for name in columns]
        indexes = [self.model().index(i, 0, QtCore.QModelIndex()) for i in rows]
        ranges = [QtCore.QItemSelectionRange(index) for index in indexes]
        selection = QtCore.QItemSelection()
        for range in ranges:
            selection.append(range)
        self.selectionModel().select(selection, QtCore.QItemSelectionModel.ClearAndSelect)

