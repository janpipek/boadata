import sys
from collections import OrderedDict
import StringIO
import blinker


class DataNode(object):
    '''A branch/leaf in a data tree.
    '''
    
    def __init__(self, parent=None):
        self.parent = parent
        self.children_loaded = False
        self._children = []        
        self._data_object = None

    node_type = "Unknown"

    # Signals
    child_added = blinker.Signal("child_added")
    child_removed = blinker.Signal("child_removed")
    changed = blinker.Signal("changed")

    @property
    def icon(self):
        return None

    @property
    def data_object(self):
        return None

    def has_object(self):
        return (self._data_object is not None) or hasattr(self, "create_data_object")

    @property
    def data_object(self):
        if self._data_object is None:
            if hasattr(self, "create_data_object"):
                self._data_object = self.create_data_object()
        return self._data_object

    # TODO: data_object setter
    # TODO: signal data_object changed

    @property
    def properties(self):
        return OrderedDict()

    @property
    def children(self):
        return []

    @property
    def title(self):
        return unicode(self)    

    @property
    def full_title(self):
        if self.parent:
            return self.parent.full_title + "/" + self.title
        else:
            return self.title

    @property
    def descendants(self):
        """Recursive iterator of all descendants."""
        for child in self.children:
            yield child
            for descendant in child.descendants:
                yield descendant

    #TODO: enumerate descendants with indices

    def subtree(self):
        return None

    def has_subtree(self):
        '''Whether the node can serve as a root of another tree.'''
        return self.subtree() is not None

    @property
    def children(self):
        '''Lazy access to children.'''
        # TODO: Add option to disable caching
        if not self.children_loaded:
            self.load_children()
            self.children_loaded = True
        return self._children

    def add_child(self, child, send_signal=True):
        child.parent = self
        child.changed.connect(lambda _: self.changed.send(self), sender=child)
        self._children.append(child)
        if send_signal:
            self.child_added.send(self, child=child)
            self.changed.send(self)

    def remove_child(self, child, send_signal=True):
        self._children.remove(child)
        if send_signal:
            self.child_removed.send(self, child=child)
            self.changed.send(self)

    def load_children(self):
        pass

    def reload_children(self):
        '''Forces children reloading.'''
        self._children = []
        self.children_loaded = False
        self.changed.send(self)

    def dump(self, stream=sys.stdout, indent=u"  ", subtree=False, in_depth=0, children_only=False, data_object_info=False):
        if not children_only:
            stream.write(in_depth * indent)
            stream.write(self.title)
            # stream.write(str(self.has_object()))
            if data_object_info and self.has_object():
                # stream.write("!")
                stream.write(" (" + " x ".join(str(i) for i in self.data_object.shape) + ")")
        if self.has_subtree() and subtree:
            stream.write(":")
            self.subtree().dump(stream, indent, subtree, in_depth, children_only=True, data_object_info=data_object_info)
        else:
            stream.write("\n")
        for child in self.children:    
            child.dump(stream, indent, subtree, in_depth+1, data_object_info=data_object_info)

      
class DataTree(DataNode):
    '''A node that can be top-level in the tree view.
    '''

    @property
    def menu_title(self):
        '''Title of the menu displayed in main menu bar.

        Override if not equal to title.
        '''
        return self.title

    @property
    def menu_actions(self):
        '''Qt actions that should be put into the menu in main menu bar.'''
        return []