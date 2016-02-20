from ..backends.webkit import WebkitBackend
from . import View
import pandas_profiling
import tempfile
import os


@View.register_view
class PandasSummaryView(View):
    title = "Data summary"

    @classmethod
    def accepts(cls, data_object):
        return data_object.is_convertible_to("pandas_data_frame")

    def create_widget(self):
        do = self.data_object.convert("pandas_data_frame").inner_data
        self.output_dir = tempfile.mkdtemp()
        report = pandas_profiling.ProfileReport(do)
        path = os.path.join(self.output_dir, "report.html")
        report.to_file(path)

        return WebkitBackend.create_widget(uri=path)