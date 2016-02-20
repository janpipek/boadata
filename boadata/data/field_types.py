from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, IdentityConversion, ChainConversion, MethodConversion
import pandas as pd
import numpy as np
import xarray as xr
import os
from .xarray_types import XarrayDatasetBase
from .pandas_types import PandasDataFrameBase


class AbstractFieldMap():
    def get_last_axis(self, axis1, axis2):
        """Get the third axis for two selected ones.

        :rtype: str
        """
        for ax in self.axes:
            if ax not in (axis1, axis2):
                return ax

    def get_corresponding_column(self, axis):
        i = self.axes.index(axis)
        return self.columns[i]

    def get_slice(self, axis, value, tolerance=1e-6):
        kwargs = {
            "method": "nearest",
            axis: value,
            "tolerance": tolerance
        }
        return self.__class__(self.inner_data.sel(**kwargs))

    def get_axis_values(self, axis):
        """All unique coordinates along a given axis.

        :rtype: list
        """
        axis_values = self.inner_data[axis]
        if axis_values.ndim > 0:
            return axis_values.to_series().tolist()
        else:
            return [float(axis_values)]


@DataObject.register_type()
@MethodConversion.enable_to("pandas_data_frame", method_name="to_dataframe")
@ChainConversion.enable_to("csv", through="pandas_data_frame")
@ChainConversion.enable_from("csv", through="pandas_data_frame", condition=lambda c: len(c.columns) == 6)
class VectorFieldMap(AbstractFieldMap, XarrayDatasetBase):
    """A vector variable that is defined for each point in a 3D mesh.

    The data are stored as pandas DataFrame with columns for position and field values.
    """
    type_name = "vector_field_map"

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

    # def __to_pandas_data_frame__(self):
    #     self.inner_data.to_dataframe()


@DataObject.register_type()
@ChainConversion.enable_to("vector_field_map", through="pandas_data_frame")
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
        return constructor(data, source=self, uri=self.uri, **kwargs)

    def __to_text__(self, **kwargs):
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-6:] == ".TABLE"

    @classmethod
    def from_uri(cls, uri, **kwargs):
        return cls(uri=uri, **kwargs)


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("vector_field_map", through="pandas_data_frame")
class ComsolFieldTextFile(PandasDataFrameBase):
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
                for line in in_lines.splitlines():
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
