from boadata.core import DataObject
import xarray as xr
from .mixins import GetItemMixin, StatisticsMixin


class _XarrayBase(DataObject, GetItemMixin, StatisticsMixin):
    @property
    def axes(self):
        """

        :rtype: list[str]
        """
        return list(self.inner_data.coords.keys())

    def __to_numpy_array__(self):
        return DataObject.from_native(self.inner_data.data)


class XarrayDatasetBase(_XarrayBase):
    @property
    def shape(self):
        return (len(self.axes),) + self.inner_data[self.columns[0]].shape

    @property
    def columns(self):
        return list(self.inner_data.data_vars.keys())

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


@DataObject.register_type(default=True)
class XarrayDataset(XarrayDatasetBase):
    type_name = "xarray_dataset"


@DataObject.register_type(default=True)
class XarrayDataArray(XarrayDataArrayBase):
    type_name = "xarray_data_array"