from boadata.core import DataObject
import xarray as xr
from .mixins import GetItemMixin, SetItemMixin, StatisticsMixin, NumericalMixin, CopyableMixin


class _XarrayBase(DataObject, GetItemMixin, StatisticsMixin, NumericalMixin, CopyableMixin):
    @property
    def axes(self):
        """

        :rtype: list[str]
        """
        return list(self.inner_data.coords.keys())

    def __to_pandas_data_frame__(self):
        return DataObject.from_native(self.inner_data.to_dataframe())


class XarrayDatasetBase(_XarrayBase, SetItemMixin):
    @property
    def shape(self):
        # TODO: This is probably completely wrong!!!
        return (len(self.axes),) + self.inner_data[self.columns[0]].shape

    @property
    def columns(self):
        return list(self.inner_data.data_vars.keys())

    def add_column(self, key, expression):
        if isinstance(expression, str):
            try:
                result = self.evaluate(expression, wrap=False)
                self.inner_data = self.inner_data.merge({key : (self.axes, result)})
            except:
                raise RuntimeError("Error when evaluating {0}".format(expression))
        else:
            raise RuntimeError("Cannot add column {0} from {1}".format(key, expression))
        return self

    def _safe_rename(self, a_dict):
        safe_prefix = "safe" + "_".join(self.axes + self.columns + list(a_dict.values()))
        dict1 = {key : safe_prefix + value for key, value in a_dict.items()}
        dict2 = {safe_prefix + value : value for _, value in a_dict.items()}
        self.inner_data = self.inner_data.rename(dict1).rename(dict2)

    def rename_columns(self, col_dict):
        if any((col not in self.columns for col in col_dict.keys())):
            raise RuntimeError("Column not present")
        else:
            self._safe_rename(col_dict)

    def rename_axes(self, ax_dict):
        if any((col not in self.axes for col in ax_dict.keys())):
            raise RuntimeError("Column not present")
        else:
            self._safe_rename(ax_dict)

    def __repr__(self):
        return "{0}({1} -> {2}, shape={3})".format(self.__class__.__name__, ", ".join(self.axes), ", ".join(self.columns), self.shape)

    real_type = xr.Dataset


class XarrayDataArrayBase(_XarrayBase):
    real_type = xr.DataArray

    def __repr__(self):
        return "{0}({1}, shape={2}, dtype={3})".format(self.__class__.__name__, ", ".join(self.axes), self.shape, self.dtype)

    @property
    def dtype(self):
        return self.inner_data.data.dtype

    def __to_numpy_array__(self):
        return DataObject.from_native(self.inner_data.data)


@DataObject.register_type(default=True)
class XarrayDataset(XarrayDatasetBase):
    type_name = "xarray_dataset"


@DataObject.register_type(default=True)
class XarrayDataArray(XarrayDataArrayBase):
    type_name = "xarray_data_array"

    @classmethod
    def from_native(cls, native_object, **kwargs):
        if not native_object.ndim:
            return native_object.dtype.type(native_object)
        else:
            if isinstance(native_object, XarrayDataArrayBase):
                return native_object.convert(cls.type_name, **kwargs)
            return cls(inner_data=native_object, **kwargs)

    @classmethod
    def __from_pandas_data_frame__(cls, origin, value_column=None):
        """

        :type origin: boadata.data.PandasDataFrame
        :param axis_columns: list[str] | None
        :param value_columns: list[str] | None
        :return:
        """
        if not value_column:
            value_column = origin.columns[-1]
        axis_columns = [column for column in origin.columns if column != value_column]
        df = origin.inner_data.set_index(axis_columns)
        data = xr.Dataset.from_dataframe(df)[value_column]
        return cls(inner_data=data, source=origin)
