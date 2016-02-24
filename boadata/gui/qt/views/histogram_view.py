from .view import View
from ..backends.matplotlib import MatplotlibBackend
from boadata import unwrap
import numpy as np


# @View.register_view
class HistogramView(View):
    def accepts(cls, data_object):
        return True

    def create_widget(self, xcol=None, bins=50, **kwargs):
        if xcol is not None:
            try:
                data = self.data_object.evaluate(xcol)
            except:
                data = self.data_object[xcol]
        else:
            data = self.data_object
            xcol = "x"
        data = unwrap(data.dropna().convert("numpy_array"))

        widget, fig = MatplotlibBackend.create_figure_widget()
        fig.add_subplot(111)
        ax = fig.get_axes()
        ax[0].hist(data, bins,
                   normed=kwargs.get("relative")
        )
        xlabel = kwargs.get("xlabel", xcol)
        ax[0].set_xlabel(xlabel)

        if "title" in kwargs:
            ax[0].set_title(kwargs["title"])
        return widget