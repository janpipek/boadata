from .view import View
from ..backends.matplotlib import MatplotlibBackend

# @View.register_view
class HistogramView(View):
    def accepts(cls, data_object):
        return True

    def create_widget(self, xcol=None, bins=50):
        if xcol is not None:
            data = self.data_object[xcol].inner_data
        else:
            data = self.data_object.inner_data

        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()
        ax[0].hist(data, bins)
        return widget