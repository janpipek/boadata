from ..backends.matplotlib import MatplotlibBackend
from PyQt4 import QtGui, QtCore
import itertools
from . import View


@View.register_view
class FieldView(View):
    title = "Field plot"

    def __init__(self, data_object):
        super(FieldView, self).__init__(data_object)
        self.field = self.data_object.convert("vector_field_map")
        self.axis1 = self.field.axes[0]
        self.axis2 = self.field.axes[1]
        self.value3 = self.field.get_axis_values(self.field.axes[2])[0]
        self.tolerance = 1e-6

    supported_types = ("vector_field_map",)       # TODO: Add scalar field map

    def create_toolbar(self, widget):
        self.toolBar = QtGui.QToolBar(widget)
        self.toolBar.addWidget(QtGui.QLabel("Plane: "))

        # Radio buttons for axes
        self.buttonGroup = QtGui.QButtonGroup()
        self.radios = {}
        for combination in itertools.combinations(self.field.axes, 2):
            text = "{0}{1}".format(combination[0], combination[1])
            radio = QtGui.QRadioButton(text)
            self.radios[text] = radio
            self.buttonGroup.addButton(radio)
            self.toolBar.addWidget(radio)
            radio.toggled[bool].connect(self.onPlaneSelected)
        self.buttonGroup.buttons()[0].setChecked(True)
        # self.buttonGroup.buttonClicked.connect(self.onPlaneSelected)
        self.toolBar.addSeparator()

        self.sliceIndexSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self.toolBar)
        self.sliceIndexSlider.setTracking(False)
        # self.sliceIndexSlider.setPageStep(1)
        self.sliceIndexSlider.valueChanged.connect(self.onValueSelected)
        self.sliceIndexSlider.sliderMoved.connect(self.onSliderMoved)
        self.sliceIndexSlider.setTickPosition(QtGui.QSlider.TicksAbove)



        self.toolBar.addWidget(self.sliceIndexSlider)

        self.sliceIndexLabel = QtGui.QLabel()
        self.sliceIndexLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.sliceIndexLabel.setFixedWidth(80)

        self.toolBar.addWidget(self.sliceIndexLabel)
        widget.layout().addWidget(self.toolBar)

        self.swapAxesCheckbox = QtGui.QCheckBox("Swap axes", self.toolBar)
        self.swapAxesCheckbox.stateChanged.connect(lambda _: self.redraw())

        self.toolBar.addWidget(self.swapAxesCheckbox)
        return self.toolBar

    def onPlaneSelected(self, _, *args):
        """

        :param button:
        :type button: QtGui.QRadioButton
        :return:
        """
        self.update_axes()

    def onValueSelected(self, _, *args):
        value = self.get_value(self.sliceIndexSlider.value())
        text = "{0} = {1}".format(self.axis3, value)
        self.sliceIndexLabel.setText(text)
        self.value3 = value
        self.redraw()

    def onSliderMoved(self, i, *args):
        value = self.get_value(i)
        text = "{0} = {1}".format(self.axis3, value)
        self.sliceIndexLabel.setText(text)

    def update_axes(self):
        self.axis1, self.axis2 = self.buttonGroup.checkedButton().text()
        self.axis3 = self.field.get_last_axis(self.axis1, self.axis2)
        values = self.field.get_axis_values(self.axis3)
        self.min = values[0]
        if len(values) > 1:
            self.step = values[1] - values[0]
        else:
            self.step = 0
        self.sliceIndexSlider.setMinimum(0)
        self.sliceIndexSlider.setMaximum(len(values) - 1)
        self.sliceIndexSlider.setSingleStep(1)
        self.sliceIndexSlider.setPageStep(3)
        self.sliceIndexSlider.setValue(0)
        self.sliceIndexLabel.setText(str(self.min))
        self.redraw()

    def get_value(self, index):
        return self.min + self.step * index

    def create_widget(self, parent=None):
        widget, self.figure = MatplotlibBackend.create_figure_widget(parent=parent)
        self.create_toolbar(widget)
        self.radios[self.axis1 + self.axis2].setChecked(True)
        self.update_axes()
        return widget

    def redraw(self):
        plane = self.field.get_slice(self.axis3, self.value3, self.tolerance).convert("pandas_data_frame")
        plane = plane.inner_data.reset_index()
        self.figure.clear()
        axis = self.figure.add_subplot(111)
        if self.swapAxesCheckbox.isChecked():
            axis1 = self.axis2
            axis2 = self.axis1
        else:
            axis1 = self.axis1
            axis2 = self.axis2
        axis.set_xlabel(axis1)
        axis.set_ylabel(axis2)
        axis.quiver(plane[axis1], plane[axis2],
                        plane[self.field.get_corresponding_column(axis1)],
                        plane[self.field.get_corresponding_column(axis2)]
                        )
        self.figure.tight_layout()
        self.figure.canvas.draw()