from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QLabel, QTabWidget
from .view import View, register_view
from six import text_type


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
            table.setItem(m, 0, QTableWidgetItem(text_type(key)))
            table.setItem(m, 1, QTableWidgetItem(text_type(value)))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        return table

    @classmethod
    def accepts(cls, data_object):
        '''Accepts all data objects.'''
        return data_object.properties

    @property
    def widget(self):
        self.tabbed_widget = QTabWidget()
        if self.props.default:
            self.tabbed_widget.addTab(self.create_table(self.props.default), "Default")
        for key, value in self.props.named.items():
            self.tabbed_widget.addTab(self.create_table(value), key)
        return self.tabbed_widget


register_view(PropertyView)

