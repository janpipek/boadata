from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QLabel
from view import View, register_view

class PropertyView(View):
    title = "Properties"

    def __init__(self, data_object):
        super(PropertyView, self).__init__(data_object)
        self.props = data_object.properties

    def create_table(self, props):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(len(props.items()))

        for m, item in enumerate(props.items()):
            key, value = item
            table.setItem(m, 0, QTableWidgetItem(unicode(key)))
            table.setItem(m, 1, QTableWidgetItem(unicode(value)))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        return table

    @classmethod
    def accepts(cls, data_object):
        '''Accepts all data objects.'''
        return data_object.properties

    @property
    def widget(self):
        self.table = self.create_table(self.props.default)
        return self.table

register_view(PropertyView)
