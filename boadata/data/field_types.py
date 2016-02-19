from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, IdentityConversion, ChainConversion
import pandas as pd
import numpy as np
import xarray as xr
import os
import re


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


@DataConversion.discover
@DataObject.register_type
@ChainConversion.enable_to("csv", through="pandas_data_frame")
@ChainConversion.enable_from("csv", through="pandas_data_frame", condition=lambda c: len(c.columns) == 6)
class VectorFieldMap(AbstractFieldMap):
    """A vector variable that is defined for each point in a 3D mesh.

    The data are stored as pandas DataFrame with columns for position and field values.
    """
    type_name = "vector_field_map"

    ndim = 4

    field_ndim = 3

    real_type = xr.Dataset

    @classmethod
    @DataConversion.condition(lambda x: len(x.columns) == 6)
    def __from_pandas_data_frame__(cls, origin, axis_columns=None, value_columns=None):
        """

        :type origin: boadata.data.PandasDataFrame
        :param axis_columns: list[str] | None
        :param value_columns: list[str] | None
        :return:
        """
        if not axis_columns:
            axis_columns = origin.inner_data.columns[:3]
        axis_columns = list(axis_columns)
        df = origin.inner_data.set_index(axis_columns)
        data = xr.Dataset.from_dataframe(df)
        return cls(inner_data=data, source=origin)

    def __to_pandas_data_frame__(self):
        self.inner_data.to_data_frame()


@DataConversion.discover
@DataObject.register_type
class FieldTableFile(DataObject):
    type_name = "field_table"

    ndim = 2

    real_type = None

    def __init__(self, **kwargs):
        super(FieldTableFile, self).__init__(**kwargs)

    def _read_pandas(self):
        return pd.read_table(self.uri, names=["x", "y", "z", "Bx", "By", "Bz"], index_col=False, delim_whitespace=True, skiprows=2)

    def __to_pandas_data_frame__(self, **kwargs):
        data = self._read_pandas()
        constructor = DataObject.registered_types["pandas_data_frame"]
        return constructor(innner_data=data, source=self, uri=self.uri, **kwargs)

    def __to_text__(self, **kwargs):
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-6:] == ".TABLE"

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)


@IdentityConversion.enable_to("pandas_data_frame")
@DataObject.register_type
@ChainConversion.enable_to("vector_field_map", through="pandas_data_frame")
class ComsolFieldTextFile(DataObject):
    type_name = "comsol_field"

    real_type = pd.DataFrame

    @classmethod
    def accepts_uri(cls, uri):
        if not os.path.isfile(uri):
            return False
        try:
            with open(uri, "rb") as f:
                file_data = f.read(1000)
                in_lines = file_data.decode()
                for line in in_lines:
                    if line.startswith("% Version") and "COMSOL" in line:
                        return True
        except:
            return False

    @classmethod
    def from_uri(cls, uri, index_col=False, source=None, **kwargs):
        header_lines = []
        with open(uri, "r") as f:
            for line in f:
                if line.startswith("%"):
                    header_lines.append(line.strip())
                else:
                    break
        frags = header_lines[-1][1:].strip().split()
        column_names = [ frag for frag in frags if not frag.startswith("(")]
        data = pd.read_csv(uri, skiprows=len(header_lines), index_col=False, header=None, delimiter="\\s+", engine="python", names=column_names)
        return cls(inner_data=data, uri=uri)
