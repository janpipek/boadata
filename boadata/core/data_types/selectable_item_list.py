from collections import OrderedDict
from .data_types import SelectableMixin, DictionaryNotifierMixin


class SelectableItemList(SelectableMixin, DictionaryNotifierMixin, OrderedDict):
    '''An abstract selectable list with keys and values.'''
    # TODO: Order does matter, but we also have to be able to insert items.

    def item_title(self, key):
        '''A title for an item, displayed by default.

        Note: Please, override _item_title method.
        '''
        value = self[key]
        return self._item_title(value)

    def item_full_title(self, key):
        '''A longer title for an item, typically displayed as tooltip.

        Note: Please, override _item_full_title method.
        '''
        value = self[key]
        return self._item_full_title(value)

    def _item_title(self, value):
        return str(value)

    def _item_full_title(self, value):
        return repr(value)

    def update(self):
        '''Request updating of the list if it is dynamically created from some source.

        :returns: True if there was any change.'''
        return False