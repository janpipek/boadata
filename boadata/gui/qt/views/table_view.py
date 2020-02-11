from Orange.data.table import Table
from Orange.data.pandas_compat import table_from_frame
from Orange.widgets.data.owtable import OWDataTable

from .view import View


@View.register_view
class TableView(View):
    title = "Table"

    supported_types = ("pandas_data_frame",)

    def create_widget(self, parent=None):
        ow = OWDataTable()
        df = self.data_object.convert("pandas_data_frame").inner_data
        table = table_from_frame(df)
        ow.set_dataset(table, self.data_object.name)
        ow.left_side.hide()
        return ow