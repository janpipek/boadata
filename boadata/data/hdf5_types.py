from boadata.core import DataObject
import h5py


@DataObject.register_type
class Hdf5Dataset(DataObject):
    real_type = h5py.Dataset

    type_name = "hdf5_dataset"

    @property
    def shape(self):
        return self.inner_data.shape

    @property
    def ndim(self):
        return len(self.shape)


class Hdf5Table(DataObject):
    pass