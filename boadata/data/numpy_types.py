from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion, ConstructorConversion
import numpy as np


@DataConversion.discover
@ConstructorConversion.enable_to("pandas_data_frame", condition=lambda x: x.ndim == 2)
@ConstructorConversion.enable_to("pandas_series", condition=lambda x: x.ndim == 1)
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

    @DataConversion.condition(lambda x: x.ndim <= 2)
    def __to_csv__(self, uri, **kwargs):
        np.savetxt(uri, self.inner_data, delimiter=",")
        csv_type = DataObject.registered_types["csv"]
        return csv_type.from_uri(uri, source=self)

    def __getitem__(self, *args):
        return NumpyArray(self.inner_data.__getitem__(*args), source=self)