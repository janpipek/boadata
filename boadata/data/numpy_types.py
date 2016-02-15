from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion, ConstructorConversion
import numpy as np
import pandas as pd


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

    @DataConversion.register("numpy_array", "csv", condition=lambda x: x.ndim <= 2)
    def to_csv(self, uri, **kwargs):
        np.savetxt(uri, self.inner_data, delimiter=",")
        csv_type = DataObject.registered_types["csv"]
        return csv_type.from_uri(uri, source=self)