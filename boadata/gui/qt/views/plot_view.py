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
        if data_object.ndim == 2 and (2 in data_object.shape or 1 in data_object.shape):
            return True
        return False

    def create_widget(self, xcol=None, ycols=None, plot_type="scatter", **kwargs):
        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()

        if not isinstance(ycols, list):
            ycols = [ycols]
        for ycol in ycols:
            data = self.data_object.convert("xy_dataseries", x=xcol, y=ycol)

            if plot_type == "line":
                ax[0].plot(data.x, data.y, label=data.yname)
            elif plot_type == "scatter":
                ax[0].scatter(data.x, data.y, label=data.yname, marker=".", s=1)
            elif plot_type == "box":
                ax[0].bar(data.x, data.y, label=data.yname)
            ax[0].set_xlabel(kwargs.get("xlabel", data.xname))
            if len(ycols) == 1:
                ax[0].set_ylabel(kwargs.get("ylabel", data.yname))

        if kwargs.get("logx"):
            ax[0].set_xscale("log")
        if kwargs.get("logy"):
            ax[0].set_yscale("log")
        if len(ycols) > 1:
            ax[0].set_ylabel(kwargs.get("ylabel", "y"))
            ax[0].legend()
        return widget