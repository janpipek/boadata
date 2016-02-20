from .view import View
from ..backends.matplotlib import MatplotlibBackend
from boadata import unwrap
import seaborn as sns


@View.register_view
class PlotView(View):
    title = "Plot"

    @classmethod
    def accepts(cls, data_object):
        if data_object.ndim == 1:
            return True
        if data_object.ndim == 2 and data_object.shape[1] <= 2:
            return True
        return False

    def create_widget(self, xcol=None, ycol=None, plot_type="scatter", **kwargs):
        df = self.data_object
        if xcol and ycol:
            try:
                x = df.evaluate(xcol)
            except Exception as e:
                x = df[xcol]
            try:
                y = df.evaluate(ycol)
            except Exception as e:
                y = df[ycol]
        elif len(df.columns) == 2:
            xcol, ycol = tuple(df.columns)
            x = df[df.columns[0]]
            y = df[df.columns[1]]
        elif len(df.columns) == 1:
            xcol, ycol = "#", df.columns[0]
            y = df[df.columns[1]]
            x = range(0, df.shape[1])
        elif df.ndim == 1:
            y = df
            x = range(0, df.shape[1])
        x = unwrap(x)
        y = unwrap(y)

        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()
        if plot_type == "line":
            ax[0].plot(x, y)
        elif plot_type == "scatter":
            ax[0].scatter(x, y)
        elif plot_type == "box":
            ax[0].bar(x, y)
        ax[0].set_xlabel(xcol)
        ax[0].set_ylabel(ycol)

        if kwargs.get("logx"):
            ax[0].set_xscale("log")
        if kwargs.get("logy"):
            ax[0].set_yscale("log")
        return widget