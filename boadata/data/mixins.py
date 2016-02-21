from boadata.core import DataObject


class GetItemMixin(object):
    """Enable proxing of GetItem."""
    def __getitem__(self, *args):
        return DataObject.from_native(self.inner_data.__getitem__(*args))


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