from collections import OrderedDict
from data_types import SelectableMixin, DictionaryNotifierMixin

class SelectableItemList(SelectableMixin, DictionaryNotifierMixin, OrderedDict):
    '''An abstract selectable list with keys and values.'''

    def item_title(self, key):
        value = self[key]
        return self._item_title(value)

    def item_full_title(self, key):
        value = self[key]
        return self._item_full_title(value)

    def _item_title(self, value):
        return str(value)

    def _item_full_title(self, value):
        return repr(value)