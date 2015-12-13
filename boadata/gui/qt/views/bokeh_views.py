from .view import register_view
from .html_views import AbstractHtmlView
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import INLINE


class AbstractBokehView(AbstractHtmlView):
    def create_html(self):
        fig = self.create_figure()
        html = file_html(fig, INLINE, "Title")
        print(html)
        return html

    def create_figure(self):
        raise NotImplementedError("You have to implement `create_figure` method")


class BokehXYPlot(AbstractBokehView):
    title = "XY plot (bokeh)"

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        if data_object.converts_to("xy"):
            return True
        if data_object.converts_to("numpy_array"):
            if data_object.ndim == 1:
                return True
            if data_object.ndim == 2:
                if 2 in data_object.shape:
                    return True
        return False

    def create_figure(self):
        fig = figure()
        data = self.data_object.to("numpy_array")
        fig.line(data[:,0], data[:,1])
        return fig

register_view(BokehXYPlot)