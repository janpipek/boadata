from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QLabel
from view import View, register_view

class PropertyView(View):
    title = "Properties"

    def __init__(self, data_object):
        super(PropertyView, self).__init__(data_object)
        self.props = data_object.properties

    def create_table(self, props):
        if props:
            table = QTableWidget()

            for m, item in enumerate(props.items()):
                key, value = item
                table.setItem(m, 0, QTableWidgetItem(key))
                table.setItem(m, 1, QTableWidgetItem(value))

            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            return table
        else:
            return QLabel("No properties.")

    @classmethod
    def accepts(cls, data_object):
        '''Accepts all data objects.'''
        return True

    @property
    def widget(self):
        if hasattr(self.props, "keys"):
            props = self.props
            tabs = True
        else:
            tabs = False
        self.table = self.create_table(self.props)
        return self.table

register_view(PropertyView)
