from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion, ConstructorConversion
from .mixins import GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin
import numpy as np


class NumpyArrayBase(DataObject):
    real_type = np.ndarray

    @property
    def shape(self):
        return self.inner_data.shape

    def dropna(self, flatten=False):
        if self.ndim > 1 and not flatten:
            raise RuntimeError("dropna not allowed for multidimensional arrays. Override by flatten=True")
        x = self.inner_data
        return DataObject.from_native(x[~np.isnan(x)])

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

    def hist(self, bins, *args, **kwargs):
        if self.dtype.kind in ["O", "U"]:
            import collections
            map = collections.defaultdict(lambda: 0)
            for item in self.inner_data.flatten():
                map[item] += 1
            pairs = ((key, map[key]) for key in sorted(map.keys()))
            return collections.OrderedDict(pairs)
        else:
            return np.histogram(self.inner_data, bins, *args, **kwargs)


@DataObject.register_type(default=True)
@ConstructorConversion.enable_to("pandas_data_frame", condition=lambda x: x.ndim == 2)
@ConstructorConversion.enable_to("pandas_series", condition=lambda x: x.ndim == 1)
@DataObject.proxy_methods("flatten")
class NumpyArray(DataObject, GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin):
    type_name = "numpy_array"
