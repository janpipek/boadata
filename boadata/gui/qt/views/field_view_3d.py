from .xy_plot_view import MatplotlibBackend
from .view import View, register_view
from PyQt4 import QtGui, QtCore
import itertools
from mpl_toolkits.mplot3d import axes3d


class FieldView3D(View):
    title = "Field plot (3D)"

    def __init__(self, data_object):
        super(FieldView3D, self).__init__(data_object)
        self.field = self.data_object.to("field")

    @classmethod
    def supported_types(cls):
        return ["field"]

    def create_widget(self):
        widget, self.figure = MatplotlibBackend.create_widget()
        # self.create_toolbar(widget)
        self.redraw()
        return widget

    def redraw(self):
        self.figure.clear()
        axis = self.figure.add_subplot(111, projection='3d')
        axis.quiver(self.field.data[self.field.axes[0]],
                    self.field.data[self.field.axes[1]],
                    self.field.data[self.field.axes[2]],
                    self.field.data[self.field.value_prefix + self.field.axes[0]],
                    self.field.data[self.field.value_prefix + self.field.axes[1]],
                    self.field.data[self.field.value_prefix + self.field.axes[2]])
        self.figure.tight_layout()
        self.figure.canvas.draw()

register_view(FieldView3D)