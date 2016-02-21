from boadata.core import DataObject
from boadata import wrap


@DataObject.proxy_methods([
    "__getitem__"
])
class GetItemMixin(object):
    """Enable proxing of GetItem."""
    pass


class SetItemMixin(object):
    def __setitem__(self, key, value, unwrap=True):
        import boadata
        if unwrap:
            value = boadata.unwrap(value)
        self.inner_data[key] = value


@DataObject.proxy_methods([
    "sum", "std", "max", "mean"
])
class StatisticsMixin(object):
    pass

@DataObject.proxy_methods([
    "__add__", "__radd__", "__sub__", "__rsub__",
    "__mul__", "__rmul__", "__matmul__", "__rmatmul__",
    "__truediv__", "__rtruediv__", "__floordiv__", "__rfloordiv__",
    "__mod__", "__rmod__", "__divmod__", "__rdivmod__",
    "__pow__", "__rpow__"
])
class NumericalMixin(object):
    pass


class AsArrayMixin(object):
    """Enable the object to be converted to native numpy array.

    Including this mixin, you can use the object in matplotlib and seaborn
    """
    def __array__(self):
        import numpy as np
        return self.convert("numpy_array").inner_data

    def astype(self, *args):
        return self.__array__().astype(*args)