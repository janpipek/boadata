from .view import View
import pyqtgraph as pg


@View.register_view
class TableView(View):
    title = "Table"

    @classmethod
    def accepts(cls, data_object):
        return data_object.is_convertible_to("pandas_data_frame")

    def create_widget(self):
        df = self.data_object.convert("pandas_data_frame").inner_data
        data = df.to_records(index=False)
        data = data[:1000]
        pw = pg.TableWidget()
        pw.setData(data)
        return pw