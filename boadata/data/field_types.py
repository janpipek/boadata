from boadata.core import DataObject
import pandas as pd
import numpy as np


class AbstractFieldMap(DataObject):
    real_type = pd.DataFrame

    def __init__(self, inner_data=None, uri=None, source=None, value_prefix="B", axes=("x", "y", "z"), **kwargs):
        """

        :type inner_data: pd.DataFrame
        """
        super(AbstractFieldMap, self).__init__(inner_data=inner_data, uri=uri, source=source, **kwargs)
        self.axes = axes
        self.value_prefix = value_prefix

    @property
    def shape(self):
        return self.inner_data.shape

    def get_last_axis(self, axis1, axis2):
        """Get the third axis for two selected ones.

        :rtype: str
        """
        for ax in self.axes:
            if ax not in (axis1, axis2):
                return ax

    def get_plane(self, axis1, axis2, plane3, tolerance=1e-6):
        """Select one plane from the field.

        :rtype: pd.DataFrame
        """
        axis3 = self.get_last_axis(axis1, axis2)
        return self.inner_data[np.abs(self.inner_data[axis3] - plane3) < tolerance]

    def get_axis_values(self, axis):
        """All unique coordinates along a given axis.

        :rtype: list
        """
        return sorted(self.inner_data[axis].unique())

    def simple_reduce(self, factor, copy=True):
        """Field with resolution reduced by a specified factor.

        :return: An independent copy with reduced size
        :type factor: int
        :rtype: Field
        """
        data = self.inner_data
        for ax in self.axes:
            allowed_values = self.get_axis_values(ax)[::factor]
            data = data[data[ax].isin(allowed_values)]
            if copy:
                data = data.copy()
        return VectorFieldMap(data)


@DataObject.register_type
class VectorFieldMap(AbstractFieldMap):
    """A vector variable that is defined for each point in a 3D mesh.

    The data are stored as pandas DataFrame with columns for position and field values.
    """
    type_name = "vector_field_map"

    ndim = 2

    field_ndim = 3


# class ScalarFieldMap(AbstractFieldMap):
#     type_name = "scalar_field_map"
#
#     field_ndim = 1


@DataObject.register_type
class FieldTableFile(DataObject):
    type_name = "field_table"

    ndim = 2

    real_type = None

    def __init__(self, **kwargs):
        super(FieldTableFile, self).__init__(**kwargs)

    def is_convertible_to(self, new_type_name):
        if new_type_name == "text":
            return True
        if new_type_name == "vector_field_map":
            return True
        if new_type_name == "pandas_data_frame":
            return True
        else:
            return super(FieldTableFile, self).is_convertible_to(new_type_name)

    def _read_pandas(self):
        return pd.read_table(self.uri, names=["x", "y", "z", "Bx", "By", "Bz"], index_col=False, delim_whitespace=True, skiprows=2)

    def convert(self, new_type_name, **kwargs):
        if new_type_name == "text":
            constructor = DataObject.registered_types[new_type_name]
            return constructor.from_uri(self.uri, source=self, **kwargs)
        elif new_type_name == "vector_field_map":
            data = self._read_pandas()
            field = VectorFieldMap(inner_data=data, source=self)
            # if self.reduce_factor > 1:
            #     field = field.simple_reduce(self.reduce_factor)
            return field
        elif new_type_name == "pandas_data_frame":
            from .pandas_types import PandasDataFrame
            data = pd.read_table(self.uri, names=["x", "y", "z", "Bx", "By", "Bz"], index_col=False, delim_whitespace=True, skiprows=2)
            return PandasDataFrame(inner_data=data, source=self)
        else:
            return super(FieldTableFile, self).convert(new_type_name, **kwargs)

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-6:] == ".TABLE"

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)
