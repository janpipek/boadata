from .view import View
import pyqtgraph as pg


@View.register_view
class TableView(View):
    title = "Table"

    supported_types = ("pandas_data_frame",)

    def create_widget(self, parent=None):
        df = self.data_object.convert("pandas_data_frame").inner_data
        data = df.to_records(index=False)
        data = data[:1000]
        pw = pg.TableWidget(parent)
        pw.setData(data)
        return pw