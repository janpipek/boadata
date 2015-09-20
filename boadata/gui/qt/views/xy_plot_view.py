from .view import View, register_view
import numpy as np
from PyQt4 import QtGui, QtCore
import logging

backends = []

# Try import pyqtgraph backend
try:
    import pyqtgraph as pg

    class PyQtGraphBackend(object):
        @classmethod
        def create_plot_widget(cls, x, y):
            pw = pg.PlotWidget()
            pw.plot(x, y)
            return pw
    backends.append(PyQtGraphBackend)
except ImportError as ex:
    logging.warning("Could not import pyqtgraph.")

# Try import matplotlib backend
try:
    import matplotlib
    from matplotlib.figure import Figure
    from matplotlib.backend_bases import key_press_handler
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar)

    class MatplotlibBackend(object):
        @classmethod
        def create_plot_widget(cls, x, y):
            # Inspiration:
            # http://matplotlib.org/examples/user_interfaces/embedding_in_qt4_wtoolbar.html
            fig = Figure()
            
            widget = QtGui.QWidget()
            layout = QtGui.QVBoxLayout()
            widget.setLayout(layout)

            # The canvas widget
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QtGui.QSizePolicy.Expanding,
               QtGui.QSizePolicy.Expanding)
            canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
            canvas.updateGeometry()

            # The toolbar
            mpl_toolbar = NavigationToolbar(canvas, widget)

            def on_key_press(event):
                key_press_handler(event, canvas, mpl_toolbar)
            
            # Draw the plot itself
            axes = fig.add_subplot(111)
            canvas.mpl_connect('key_press_event', on_key_press)
            axes.plot(x, y)
            # fig.tight_layout()

            # Lay it out
            layout.addWidget(canvas)
            layout.addWidget(mpl_toolbar)
            return widget
            # return canvas
    backends.append(MatplotlibBackend)
except ImportError as ex:
    logging.warning("Could not import matplotlib.")


class XYPlotView(View):
    title = "XY Plot"

    def __init__(self, data_object):
        super(XYPlotView, self).__init__(data_object)
        self.backend = backends[1]

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
                elif data.shape[1] == 2:
                    x = data[:,0]
                    y = data[:,1]
                else:
                    raise Exception("Invalid 2D matrix to plot")
            else:
                raise Exception("Invalid matrix to plot")
        return self.backend.create_plot_widget(x, y)

register_view(XYPlotView)