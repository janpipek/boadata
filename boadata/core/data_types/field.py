import numpy as np
import pandas as pd

class Field(object):
    def __init__(self, data):
        """

        :param data:
        :type data: pd.DataFrame
        :return:
        """
        self.data = data
        self.axes = ("x", "y", "z")
        self.value_prefix = "B"

    def get_plane(self, axis1, axis2, plane3, tolerance=1e-6):
        axis3 = (list({"x", "y", "z"} - { axis1, axis2 }))[0]
        print(axis1, axis2, plane3)
        return self.data[np.abs(self.data[axis3] - plane3) < tolerance]

    def get_axis_values(self, axis):
        return sorted(self.data[axis].unique())

    def get_last_axis(self, axis1, axis2):
        for ax in self.axes:
            if ax not in (axis1, axis2):
                return ax
