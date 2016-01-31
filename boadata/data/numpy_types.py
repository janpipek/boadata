from boadata.core import DataObject
import numpy as np


@DataObject.register_type
class NumpyArray(DataObject):
    real_type = np.ndarray

    type_name = "numpy_array"

    @property
    def shape(self):
        return self.inner_data.shape

    @property
    def ndim(self):
        return self.inner_data.ndim