from boadata.core import DataObject
from boadata.core.data_conversion import DataConversion, OdoConversion, ConstructorConversion
from .mixins import GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin, CopyableMixin
import numpy as np


@ConstructorConversion.enable_to("pandas_series", condition=lambda x: x.ndim == 1)
class NumpyArrayBase(DataObject, CopyableMixin):
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

    def __to_numpy_array__(self):
        return NumpyArray(inner_data=self.inner_data, source=self)

    @DataConversion.condition(lambda x: x.ndim == 2)
    def __to_pandas_data_frame__(self, name=None, columns=None, **kwargs):
        import pandas as pd
        data = pd.DataFrame(data=self.inner_data, columns=columns, **kwargs)
        klass = DataObject.registered_types["pandas_data_frame"]
        if not name:
            name = self.name
        return klass(inner_data=data, source=self, name=name)

    def __repr__(self):
        return "{0}(shape={1}, dtype={2})".format(self.__class__.__name__, self.shape, self.inner_data.dtype)

    def histogram(self, *args, **kwargs):
        """
        :rtype: boadata.data.plotting_types.HistogramData
        """
        data = self.inner_data
        if self.dtype.kind not in "iuf":
            raise RuntimeError("Not supported")
            # import collections
            # map = collections.defaultdict(lambda: 0)
            # for item in data.flatten():
            #     map[item] += 1
            # pairs = ((key, map[key]) for key in sorted(map.keys()))
            # return collections.OrderedDict(pairs)
        else:
            from physt import h1
            inner_data = h1(data, **kwargs)
            from .plotting_types import HistogramData
            return HistogramData(inner_data=inner_data, source=self)

    def mode(self):
        """Mode interpreted as in scipy.mode"""
        import scipy
        result = scipy.stats.mode(self.inner_data, axis=None)[0]
        return result[0]

    def where(self, condition):
        """Run a condition on numpy array

        :type condition: lambda (callable?)
        """
        ufunc = np.frompyfunc(condition, 1, 1)
        indices = ufunc(self.inner_data).astype(bool)
        # raise RuntimeError("eee: {0}".format(indices.dtype))
        inner_data = self.inner_data[indices]
        return type(self)(inner_data=inner_data, source=self)


@DataObject.register_type(default=True)
@DataObject.proxy_methods("flatten")
class NumpyArray(NumpyArrayBase, GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin):
    type_name = "numpy_array"

    @classmethod
    def random(cls, *shape):
        data = np.random.rand(*shape)
        return cls(inner_data=data)
