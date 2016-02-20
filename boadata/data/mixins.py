from boadata.core import DataObject


class GetItemMixin(object):
    """Enable proxing of GetItem."""
    def __getitem__(self, *args):
        return DataObject.from_native(self.inner_data.__getitem__(*args))


@DataObject.proxy_methods([
    "sum", "std", "max", "mean"
])
class StatisticsMixin(object):
    pass