from .view import View
from ..backends.matplotlib import MatplotlibBackend

# @View.register_view
class PlotView(View):
    def accepts(cls, data_object):
        return True

    def create_widget(self, xcol=0, ycol=1):
        df = self.data_object.convert("pandas_data_frame")

        x = df[xcol].inner_data
        y = df[ycol].inner_data

        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()
        ax[0].scatter(x, y)
        return widget