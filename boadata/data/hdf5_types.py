from boadata.core import DataObject
import h5py

# @DataObject.register_type

# class Hdf5Meta(DataObject):
#     @classmethod
#     def from_uri(cls, uri, **kwargs):
#


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

    @classmethod
    def accepts_uri(cls, uri):
        return ".h5::" in uri or ".hdf5::" in uri


class Hdf5Table(DataObject):
    pass