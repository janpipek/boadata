from view import View, register_view
import pyqtgraph as pg
import numpy as np

class XYPlotView(View):
    title = "XY Plot"

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        if data_object.converts_to("xy"):
            return True
        if data_object.converts_to("numpy_array"):
            if data_object.ndim == 1:
                return True
            if data_object.ndim == 2:
                if 2 in data_object.shape[0]:
                    return True
        return False

    @property
    def widget(self):
        if self.data_object.converts_to("xy"):
            x, y = self.data_object.to("xy")
        if self.data_object.converts_to("numpy_array"):
            data = self.data_object.to("numpy_array")
            if data.ndim == 1:
                x = np.arange(data.shape[0])
                y = data
            elif data.ndim == 2:
                if data.shape[0] == 2:
                    x = data[0]
                    y = data[1]
                else:
                    raise Exception("Invalid 2D matrix to plot")
            else:
                raise Exception("Invalid matrix to plot")
        pw = pg.PlotWidget()
        pw.plot(x, y)
        return pw

register_view(XYPlotView)