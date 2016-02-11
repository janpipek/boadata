from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, IdentityConversion
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
@IdentityConversion.enable_from("pandas_data_frame")
@IdentityConversion.enable_from("csv")
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

    def _read_pandas(self):
        return pd.read_table(self.uri, names=["x", "y", "z", "Bx", "By", "Bz"], index_col=False, delim_whitespace=True, skiprows=2)

    @DataConversion.register("field_table", "pandas_data_frame")
    def to_pandas_data_frame(self, **kwargs):
        data = self._read_pandas()
        constructor = DataObject.registered_types["pandas_data_frame"]
        return constructor(innner_data=data, source=self, uri=self.uri, **kwargs)

    @DataConversion.register("field_table", "text")
    def to_text(self, **kwargs):
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-6:] == ".TABLE"

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)
