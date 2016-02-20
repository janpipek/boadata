from boadata.core import DataObject
from boadata.core.data_conversion import OdoConversion, DataConversion, ChainConversion
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
        # TODO: Check for file or h5py: in URL
        return ".h5::" in uri or ".hdf5::" in uri


# class Hdf5Table(DataObject):
#    real_type = h5py