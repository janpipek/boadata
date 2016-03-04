from .view import View
from ..backends.matplotlib import MatplotlibBackend
from ..widgets.column_select import ColumnSelect
from boadata import unwrap
import seaborn as sns
from PyQt4 import QtCore, QtGui


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

    def create_dock(self, main_widget):
        widget = QtGui.QLabel()

        self.dock = QtGui.QDockWidget("Data", main_widget)

        self.x_list = ColumnSelect(self.data_object)
        self.x_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.x_list.select_columns([self.xcol])
        self.x_list.selectionModel().selectionChanged.connect(self.axis_changed)

        self.y_list = ColumnSelect(self.data_object)
        self.y_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.y_list.select_columns(self.ycols)
        self.y_list.selectionModel().selectionChanged.connect(self.axis_changed)

        vbox = QtGui.QVBoxLayout()

        vbox.addWidget(QtGui.QLabel("Data series (X)"))
        vbox.addWidget(self.x_list)

        vbox.addWidget(QtGui.QLabel("Data series (Y)"))
        vbox.addWidget(self.y_list)

        widget.setLayout(vbox)

        self.dock.setWidget(widget)
        main_widget.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock)

    def axis_changed(self, _, __):
        self.update()

    def update(self):
        self.figure.clear()
        self.figure.add_subplot(111)
        ax = self.figure.get_axes()

        self.xcol = self.x_list.selected_columns[0]
        self.ycols = self.y_list.selected_columns

        for ycol in self.ycols:
            data = self.data_object.convert("xy_dataseries", x=self.xcol, y=ycol)
            if self.plot_type == "line":
                ax[0].plot(data.x, data.y, label=data.yname)
            elif self.plot_type == "scatter":
                ax[0].scatter(data.x, data.y, label=data.yname, marker=".", s=1)
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

    def create_widget(self, xcol=None, ycols=None, plot_type="scatter", **kwargs):
        self.window = QtGui.QMainWindow()

        self.plot_type = plot_type
        self.plot_widget, self.figure = MatplotlibBackend.create_figure_widget()
        self.xcol = xcol
        self.ycols = ycols

        if self.data_object.columns:
            if not self.xcol:
                self.xcol = self.data_object.columns[0]
            if not self.ycols:
                self.ycols = self.data_object.columns[1:]

        self.kwargs = kwargs

        self.create_dock(self.window)
        self.update()
        self.window.setCentralWidget(self.plot_widget)


        return self.window