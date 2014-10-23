import blinker

class SelectableMixin(object):
    '''Mixin for containers that makes items selectable.

    For dict's, the item represents key.
    '''
    def __init__(self, *args, **kwargs):
        super(SelectableMixin, self).__init__(*args, **kwargs)
        self._selected_items = set()

    item_selected = blinker.Signal("item_selected")
    item_deselected = blinker.Signal("item_deselected")  

    def is_selected(self, item):
        if not item in self:
            raise KeyError('"%s" not in container.')
        else:
            return item in self._selected_items

    @property
    def selected_items(self):
        '''A safe list of selected items.'''
        return [ item for item in self._selected_items if item in self ]

    def select(self, item):
        '''Select an item.'''
        if not item in self:
            raise KeyError('"%s" not in container, cannot select.' % item)
        if not self.is_selected(item):
            self._selected_items.add(item)
            self.item_selected.send(self, item=item)
            return True
        else:
            return False

    def deselect(self, item):
        '''Deselect an item.'''
        if not item in self:
            raise KeyError('"%s" not in container, cannot deselect.' % item)
        if self.is_selected(item):
            self._selected_items.remove(item)
            self.item_deselected.send(self, item=item)   
            return True
        else:
            return False

    def select_all(self):
        for item in self:
            self.select(item)

    def deselect_all(self):
        for item in self:
            self.deselect(item)

class DictionaryNotifierMixin(object):
    item_added = blinker.Signal()
    item_removed = blinker.Signal()

    def __setitem__(self, key, *args, **kwargs):
        notify = not (key in self)
        super(DictionaryNotifierMixin, self).__setitem__(key, *args, **kwargs)
        if notify:
            self.item_added.send(self, key=key)

    def __delitem__(self, key):
        super(DictionaryNotifierMixin, self).__delitem__(item)
        self.item_removed.send(self, key=key)