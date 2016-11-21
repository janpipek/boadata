from .view import View
from ..backends.matplotlib import MatplotlibBackend
from boadata import unwrap
import seaborn as sns


# @View.register_view
class HistogramView(View):
    def accepts(cls, data_object):
        return True

    def create_widget(self, parent=None, xcol=None, bins=50, **kwargs):
        if xcol is not None:
            try:
                data = self.data_object.evaluate(xcol)
            except:
                data = self.data_object[xcol]
        else:
            data = self.data_object
            xcol = "x"
        data = unwrap(data.dropna().convert("numpy_array"))

        widget, fig = MatplotlibBackend.create_figure_widget(parent=parent)
        fig.add_subplot(111)
        ax = fig.get_axes()

        extra_args = {}
        if not kwargs.get("hist"):
            extra_args["kde_kws"] = {"shade": True}

        sns.distplot(data, hist=kwargs.get("hist", False), kde=kwargs.get("kde", False),
                     bins=bins, rug=kwargs.get("rug", False), ax=ax[0], **extra_args)
        xlabel = kwargs.get("xlabel", xcol)
        ax[0].set_xlabel(xlabel)

        if "title" in kwargs:
            ax[0].set_title(kwargs["title"])
        return widget