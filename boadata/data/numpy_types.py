from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion
import numpy as np
import pandas as pd


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

    @DataConversion.register("numpy_array", "pandas_data_frame", condition=lambda x: x.ndim == 2)
    def to_pandas_data_frame(self):
        data = pd.DataFrame(self.inner_data)
        klass = DataObject.registered_types["pandas_data_frame"]
        return klass(data, source=self)