from boadata.core import DataObject
from boadata.core.data_conversion import OdoConversion, DataConversion, ChainConversion
from boadata.data.mixins import GetItemMixin
import h5py
import numpy as np


@DataObject.register_type(default=True)
@ChainConversion.enable_to("pandas_data_frame", through="numpy_array", condition=lambda x: x.ndim == 2)
@ChainConversion.enable_to("pandas_series", through="numpy_array", condition=lambda x: x.ndim == 1)
@ChainConversion.enable_to("csv", through="numpy_array", condition=lambda x: x.ndim <= 2)
class Hdf5Dataset(DataObject):
    real_type = h5py.Dataset

    type_name = "hdf5_dataset"

    @property
    def shape(self):
        return self.inner_data.shape

    @property
    def ndim(self):
        return len(self.shape)

    def __to_numpy_array__(self):
        data = np.array(self.inner_data)
        numpy_type = DataObject.registered_types["numpy_array"]
        return numpy_type(data, source=self)

    @classmethod
    def __from_numpy_array__(cls, data_object, uri,  **kwargs):
        file, dataset = uri.split("::")
        h5file = h5py.File(file)
        ds = h5file.create_dataset(dataset, data=data_object.inner_data)
        return Hdf5Dataset(ds, source=data_object, uri=uri)

    @classmethod
    def accepts_uri(cls, uri):
        import odo
        if not(".h5::" in uri or ".hdf5::" in uri):
            return False
        try:
            candidate = odo.odo(uri, cls.real_type)
            if candidate.attrs.get(b"CLASS") != b"TABLE":
                return True
        except:
            pass
        return False


@DataObject.register_type()
@ChainConversion.enable_to("csv", through="pandas_data_frame")
class Hdf5Table(DataObject, GetItemMixin):
    real_type = h5py.Dataset

    type_name = "hdf5_table"

    @classmethod
    def accepts_uri(cls, uri):
        import odo
        if not(".h5::" in uri or ".hdf5::" in uri):
            return False
        try:
            candidate = odo.odo(uri, cls.real_type)
            if candidate.attrs.get(b"CLASS") == b"TABLE":
                return True
        except:
            pass
        return False

    @property
    def columns(self):
        import re
        attrs = dict(self.inner_data.attrs)
        ncols = len([1 for key in attrs.keys() if re.match("FIELD_\\d+_NAME", key)])
        return [attrs["FIELD_{0}_NAME".format(i)].decode() for i in range(ncols)]

    @property
    def ndim(self):
        return 2

    @property
    def shape(self):
        return len(self.inner_data), len(self.columns)

    def __to_xy_dataseries__(self, x, y, **kwargs):
        return self.convert("pandas_data_frame", **kwargs).convert("xy_dataseries", x=x, y=y)

    def __to_pandas_data_frame__(self):
        import pandas as pd
        df = pd.DataFrame(dict({key : pd.Series(self.inner_data[key]) for key in self.columns}))
        df = df[self.columns]
        pd_type = DataObject.registered_types["pandas_data_frame"]
        return pd_type(df, source=self) #, name=self.inner_data.attrs["TITLE"].decode())



