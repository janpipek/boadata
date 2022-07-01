import numpy as np

from boadata.core import DataObject


@DataObject.proxy_methods("__getitem__")
class GetItemMixin:
    """Enable proxing of GetItem."""

    pass


class SetItemMixin:
    def __setitem__(self, key, value, unwrap=True):
        import boadata

        if unwrap:
            value = boadata.unwrap(value)
        self.inner_data[key] = value


@DataObject.proxy_methods("sum", "std", "max", "mean", "min")
class StatisticsMixin:
    """ """

    def quantile(self, n, wrap=True):
        import boadata

        if hasattr(self.inner_data, "quantile"):
            result = self.inner_data.quantile(n)
        elif isinstance(self.inner_data, np.ndarray):
            result = np.percentile(self.inner_data, np.array(n) * 100.0)
        else:
            raise RuntimeError("Object does not support quantiles")
        if wrap:
            return boadata.wrap(result, force=False)
        else:
            return result

    def percentile(self, n, wrap=False):
        return self.quantile(np.array(n) / 100.0, wrap=wrap)

    def median(self):
        return self.quantile(0.5)


@DataObject.proxy_methods(
    "__add__",
    "__radd__",
    "__sub__",
    "__rsub__",
    "__mul__",
    "__rmul__",
    "__matmul__",
    "__rmatmul__",
    "__truediv__",
    "__rtruediv__",
    "__floordiv__",
    "__rfloordiv__",
    "__mod__",
    "__rmod__",
    "__divmod__",
    "__rdivmod__",
    "__pow__",
    "__rpow__",
)
class NumericalMixin:
    pass


class AsArrayMixin:
    """Enable the object to be converted to native numpy array.

    Including this mixin, you can use the object in matplotlib and seaborn
    """

    def __array__(self, *args):
        return np.array(self.convert("numpy_array").inner_data, *args)

    def astype(self, *args):
        return self.__array__().astype(*args)


class IteratorMixin:
    def __iter__(self):
        for item in self.inner_data:
            from boadata import wrap

            yield wrap(item, force=False)


class CopyableMixin:
    def copy(self, *args):
        return self.__class__(inner_data=self.inner_data.copy(*args), source=self)
