from .view import View
from ..backends.matplotlib import MatplotlibBackend

# @View.register_view
class PlotView(View):
    def accepts(cls, data_object):
        return True

    def create_widget(self, xcol=0, ycol=1, plot_type="scatter", **kwargs):
        df = self.data_object.convert("pandas_data_frame")

        # TODO: More intensive guessing!
        try:
            x = df.evaluate(xcol).inner_data
            y = df.evaluate(ycol).inner_data
        except Exception as e:
            print(e)
            x = df[xcol].inner_data
            y = df[ycol].inner_data

        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()
        if plot_type == "line":
            ax[0].plot(x, y)
        elif plot_type == "scatter":
            ax[0].scatter(x, y)
        ax[0].set_xlabel(xcol)
        ax[0].set_ylabel(ycol)
        return widget