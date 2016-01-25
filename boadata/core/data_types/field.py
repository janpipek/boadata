import numpy as np
import pandas as pd


class Field(object):
    """A vector variable that is defined for each point in a 3D mesh.

    The data are stored as pandas DataFrame with columns for position and field values.
    """
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
        """Select one plane from the field.

        :rtype: pd.DataFrame
        """
        axis3 = (list({"x", "y", "z"} - {axis1, axis2}))[0]
        return self.data[np.abs(self.data[axis3] - plane3) < tolerance]

    def get_axis_values(self, axis):
        """All unique coordinates along a given axis.

        :rtype: list
        """
        return sorted(self.data[axis].unique())

    def get_last_axis(self, axis1, axis2):
        """Get the third axis for two selected ones.

        :rtype: str
        """
        for ax in self.axes:
            if ax not in (axis1, axis2):
                return ax

    def simple_reduce(self, factor):
        """Field with resolution reduced by a specified factor.

        :return: An independent copy with reduced size
        :type factor: int
        :rtype: Field
        """
        data = self.data
        for ax in self.axes:
            allowed_values = self.get_axis_values(ax)[::factor]
            data = data[data[ax].isin(allowed_values)]
        return Field(data.copy())