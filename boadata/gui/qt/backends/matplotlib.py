from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
import qtpy

if qtpy.API == "pyqt5":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4 import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar)
from qtpy import QtGui, QtCore, QtWidgets

import seaborn as sns   # To style it a bit

class MatplotlibBackend(object):
    @classmethod
    def create_figure_widget(cls, parent=None):
        """

        :rtype tuple(QWidget, Figure)
        """
        # Inspiration:
        # http://matplotlib.org/examples/user_interfaces/embedding_in_qt4_wtoolbar.html
        fig = Figure()

        widget = QtWidgets.QWidget(parent)
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        # The canvas widget
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
           QtWidgets.QSizePolicy.Expanding)
        canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
        canvas.updateGeometry()

        # The toolbar
        mpl_toolbar = NavigationToolbar(canvas, widget)

        def on_key_press(event):
            key_press_handler(event, canvas, mpl_toolbar)
        canvas.mpl_connect('key_press_event', on_key_press)

        # Lay it out
        layout.addWidget(canvas)
        layout.addWidget(mpl_toolbar)
        return widget, fig