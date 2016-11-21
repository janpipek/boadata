from .view import View
from ..backends.matplotlib import MatplotlibBackend
from ..widgets.column_select import ColumnSelect
from boadata import unwrap
import seaborn as sns
from qtpy import QtCore, QtWidgets
import numpy as np


@View.register_view
class PlotView(View):
    title = "Plot"

    @classmethod
    def accepts(cls, data_object):
        # TODO: update for single...
        if data_object.columns:
            return True
        return False

    def create_dock(self, main_widget):
        widget = QtWidgets.QWidget()

        self.x_list = ColumnSelect(self.data_object, widget)
        self.x_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.x_list.select_columns([self.xcol])
        self.x_list.selectionModel().selectionChanged.connect(lambda a, b: self.update())

        self.y_list = ColumnSelect(self.data_object, widget)
        self.y_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.y_list.select_columns(self.ycols)
        self.y_list.selectionModel().selectionChanged.connect(lambda a, b: self.update())

        vbox = QtWidgets.QVBoxLayout()

        vbox.addWidget(QtWidgets.QLabel("Data series (X)"))
        vbox.addWidget(self.x_list, 1)

        vbox.addWidget(QtWidgets.QLabel("Data series (Y)"))
        vbox.addWidget(self.y_list, 4)

        widget.setLayout(vbox)

        self.dock = QtWidgets.QDockWidget("Data", main_widget)
        self.dock.setWidget(widget)
        main_widget.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)

    def update(self):
        self.figure.clear()
        self.figure.add_subplot(111)
        ax = self.figure.get_axes()

        self.xcol = self.x_list.selected_columns()[0]
        self.ycols = self.y_list.selected_columns()

        for i, ycol in enumerate(self.ycols):
            data = self.data_object.convert("xy_dataseries", x=self.xcol, y=ycol)
            if data.y.dtype not in (np.dtype(float), np.dtype(int)):
                continue
            if self.plot_type == "line":
                ax[0].plot(data.x, data.y, label=data.yname)
            elif self.plot_type == "scatter":
                ax[0].plot(data.x, data.y, "o", label=data.yname, c=self.palette[i], markersize=12)
            elif self.plot_type == "box":
                ax[0].bar(data.x, data.y, label=data.yname)
            ax[0].set_xlabel(self.kwargs.get("xlabel", data.xname))
            if len(self.ycols) == 1:
                ax[0].set_ylabel(self.kwargs.get("ylabel", data.yname))

        if self.kwargs.get("logx"):
            ax[0].set_xscale("log")
        if self.kwargs.get("logy"):
            ax[0].set_yscale("log")
        if len(self.ycols) > 1:
            ax[0].set_ylabel(self.kwargs.get("ylabel", "y"))
        ax[0].legend()
        self.figure.tight_layout()
        self.figure.canvas.draw()

    @property
    def palette(self):
        return sns.color_palette("muted")

    def create_widget(self, parent=None, xcol=None, ycols=None, plot_type="scatter", **kwargs):
        self.window = QtWidgets.QMainWindow(parent=parent)

        self.plot_type = plot_type
        self.plot_widget, self.figure = MatplotlibBackend.create_figure_widget()
        self.xcol = xcol
        self.ycols = ycols

        if self.data_object.columns:
            if not self.xcol:
                self.xcol = self.data_object.columns[0]
            if not self.ycols:
                self.ycols = self.data_object.columns[1:2]

        self.kwargs = kwargs

        self.window.setCentralWidget(self.plot_widget)
        self.create_dock(self.window)
        self.update()

        return self.window