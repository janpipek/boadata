import os
from collections import OrderedDict

import pandas as pd
import numpy as np
import xarray as xr

from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, IdentityConversion, ChainConversion, MethodConversion

from .xarray_types import XarrayDatasetBase, XarrayDataArrayBase
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

    def __to_pandas_data_frame__(self):
        df = self.inner_data.to_dataframe().reset_index()
        return DataObject.from_native(df, source=self)

    # TODO: Some interpolation?


@DataObject.register_type()
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=["uri"])
@ChainConversion.enable_from("csv", through="pandas_data_frame", condition=lambda c: len(c.columns) == 4)
class ScalarFieldMap(AbstractFieldMap, XarrayDataArrayBase):
    """A scalar variable that is defined for each point in a 3D mesh.
    """
    type_name = "scalar_field_map"

    @classmethod
    @DataConversion.condition(lambda x: len(x.columns) == 4)
    def __from_pandas_data_frame__(cls, origin, axis_columns=None, value_column=None):
        if not axis_columns:
            axis_columns = origin.inner_data.columns[:3]
        if not value_column:
            value_column = origin.inner_data.columns[3]
        axis_columns = list(axis_columns)
        df = origin.inner_data.set_index(axis_columns)
        data = xr.DataArray.from_series(df[value_column])
        return cls(inner_data=data, source=origin)


@DataObject.register_type()
# @MethodConversion.enable_to("pandas_data_frame", method_name="to_dataframe")
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=["uri"])
@ChainConversion.enable_from("csv", through="pandas_data_frame", condition=lambda c: len(c.columns) == 6)
class VectorFieldMap(AbstractFieldMap, XarrayDatasetBase):
    """A vector variable that is defined for each point in a 3D mesh.
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

    def normalize_column_names(self, field_name, inplace=True):
        inner_data = self.inner_data.rename(
            dict(zip(self.axes + self.columns, ["x", "y", "z"] + [field_name + ax for ax in "xyz"])))
        if inplace:
            self.inner_data = inner_data
        else:
            return self.__class__(inner_data=inner_data, source=self)

    def magnitude(self, column_name="size"):
        """Scalar field produced of vector length at each point.

        :rtype: ScalarFieldMap
        """
        magnitude_column = np.sqrt(sum([self.inner_data[self.columns[i]] ** 2 for i in range(3)]))
        new_inner_data = xr.DataArray(magnitude_column, self.inner_data.coords, name=column_name)
        return ScalarFieldMap(inner_data=new_inner_data, source=self)

    def __to_opera_field__(self, path, length_unit="mm", field_unit="tesla", **kwargs):
        with open(path, "w") as f:
            f.write(" {0} {1}\n".format(" ".join([str(s) for s in self.shape[1:]]), 2))
            for i, ax in enumerate(self.axes):
                f.write(" {0} {1} [{2}]\n".format(i + 1, ax.upper(), length_unit.upper()))
            for j, ax in enumerate(self.columns):
                f.write(" {0} {1} [{2}]\n".format(j + 4, ax.upper(), field_unit.upper()))
            f.write(" 0\n")
            df = self.convert("pandas_data_frame").inner_data
            df.to_csv(f, sep=" ", index=None, header=None, **kwargs)
            return OperaFieldTextFile.from_uri(path, source=self)

        # TODO: Implement conversion to ScalarFieldMap

    def mirror(self, ax, inplace=True):
        """Mirror the axis and the corresponding vector component.

        :type ax: int

        Multiplies both entities by -1.
        """
        if not inplace:
            a_copy = self.copy()
            a_copy.invert_axis(ax, inplace=True)
            return a_copy
        if not ax in (0, 1, 2):
            raise RuntimeError("Cannot invert non-existent axis")
        else:
            self.inner_data[self.axes[ax]] = self.inner_data[self.axes[ax]] * (-1)
            self.inner_data[self.columns[ax]] = self.inner_data[self.columns[ax]] * (-1)

    def _make_interpolators(self, method, bounds_error, fill_value):
        from scipy.interpolate import RegularGridInterpolator
        points = tuple(self.inner_data[axis] for axis in self.axes)
        interpolators = [
            RegularGridInterpolator(points=points, values=np.asarray(self.inner_data[axis]),
                                    method=method, bounds_error=bounds_error, fill_value=fill_value[i])
            for i, axis in enumerate(self.columns)
        ]
        return interpolators

    def interpolate(self, x, y, z, method="linear", bounds_error=False, fill_value=(0, 0, 0)):
        """(Tri-)linear interpolation of the values.

        :param x: coordinate or array of coordinates in x
        :param y: coordinate or array of coordinates in y
        :param z: coordinate or array of coordinates in z
        :param bounds_error:
        :param method
        :param fill_value
        :return:
        """
        # TODO: Check that the grid is regular? But maybe it is by xarray default?
        interpolators = self._make_interpolators(method=method, bounds_error=bounds_error, fill_value=fill_value)

        data = np.concatenate((np.asarray(x)[...,np.newaxis],
                                np.asarray(y)[...,np.newaxis],
                                np.asarray(z)[...,np.newaxis]),
                               axis=-1)
        # data = tuple(np.asarray(t) for t in (x,y,z))
        from boadata import wrap
        return [wrap(interpolators[i](data), force=False) for i in range(3)]
        
    def resample(self, dim1, dim2, dim3, method="linear", inplace=False):
        """Change the grid points using linear (or other) interpolation.
        
        :param dim1: new number of points in x
        :param dim2: new number of points in y
        :param dim3: new number of points in z
        :param method: interpolation method
        """
        # TODO: Include option to resample only precisely
        dims = (dim1, dim2, dim3)
        new_axes = [np.linspace(self[axis].min(), self[axis].max(), dims[i]) for i, axis in enumerate(self.axes)]
        new_mesh = np.meshgrid(*new_axes, indexing="ij")
        new_fields = self.interpolate(*new_mesh, method=method)
        
        print([f.shape for f in new_fields])
        
        coords = OrderedDict([(axis, new_axes[i]) for i, axis in enumerate(self.axes)])
        data = OrderedDict([(column, xr.DataArray(new_fields[i].inner_data, coords=coords, dims=self.axes)) for i, column in enumerate(self.columns)])
        inner_data = xr.Dataset(
            data,
            coords
        )
        if inplace:
            self.inner_data = inner_data
            return self
        else:
            return VectorFieldMap(inner_data=inner_data, source=self)

    def swap_axes(self, ax1, ax2, inplace=True):
        """Swap two axes (and vector components).

        swap(0, 1) means: "What was x, is now y (and vice versa)".

        """
        if not inplace:
            a_copy = self.copy()
            a_copy.swap_axes(ax1, ax2, inplace=True)
            return a_copy
        if {ax1, ax2}.difference({0, 1, 2}):
            raise RuntimeError("Wrong axis id")
        elif ax1 == ax2:
            inner_data = self.inner_data
        else:
            df_columns = self.axes + self.columns

            df = self.convert("pandas_data_frame")
            df.inner_data.reset_index(inplace=True, drop=True)
            df.rename_columns({
                self.axes[ax1]: self.axes[ax2],
                self.axes[ax2]: self.axes[ax1],
                self.columns[ax1]: self.columns[ax2],
                self.columns[ax2]: self.columns[ax1]
            })
            df.reorder_columns(df_columns)
            df.inner_data = df.inner_data.set_index(self.axes)
            self.inner_data = xr.Dataset.from_dataframe(df.inner_data)


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


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("vector_field_map", through="pandas_data_frame")
class OperaFieldTextFile(PandasDataFrameBase):
    """Field maps as exported from Opera.

    Note: one particular setting => may not be applicable.

    The example file looks like this (not indented):

         201 51 51 2
         1 X [MM]
         2 Y [MM]
         3 Z [MM]
         4 BX [TESLA]
         5 BY [TESLA]
         6 BZ [TESLA]
         0
          -50.0000000000      -50.0000000000      -200.000000000      0.182000689291E-02  0.181548320077E-02   0.00000000000
          -50.0000000000      -50.0000000000      -198.000000000      0.182963069824E-02  0.182665326586E-02 -0.222624232502E-03
    """
    type_name = "opera_field"

    @classmethod
    def accepts_uri(cls, uri):
        if not os.path.isfile(uri):
            return False
        return cls._parse_header(uri)[1] is not None

    @classmethod
    def _parse_header(cls, uri):
        """

        :param uri:
        :return: (skiprows, column_names)
        """
        with open(uri, "rb") as f:
            file_data = f.read(1000)
            in_lines = file_data.decode()
            columns = []
            try:
                for i, line in enumerate(in_lines.splitlines()):
                    if i == 0:
                        if len(line.strip().split()) != 4:
                            break
                    elif line.strip() == "0":
                        return i+1, columns
                    else:
                        j, rest = line.strip().split(maxsplit=1)
                        if int(j) != i:
                            break
                        columns.append(rest)
            except:
                pass
            return 0, None

    @classmethod
    def from_uri(cls, uri, **kwargs):
        skiprows, column_names = cls._parse_header(uri)
        data = pd.read_csv(uri, skiprows=skiprows, index_col=False, header=None, delim_whitespace=True,
                           engine="python", names=column_names)
        return cls(inner_data=data, uri=uri)
