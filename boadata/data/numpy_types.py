from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion, ConstructorConversion
from .mixins import GetItemMixin
import numpy as np


@DataObject.register_type(default=True)
@ConstructorConversion.enable_to("pandas_data_frame", condition=lambda x: x.ndim == 2)
@ConstructorConversion.enable_to("pandas_series", condition=lambda x: x.ndim == 1)
@DataObject.proxy_methods("flatten")
class NumpyArray(DataObject, GetItemMixin):
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

    def __repr__(self):
        return "{0}(shape={1}, dtype={2})".format(self.__class__.__name__, self.shape, self.inner_data.dtype)
