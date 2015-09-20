import sys
from collections import OrderedDict
import blinker
import logging
from six import text_type


class DataNode(object):
    '''A branch/leaf in a data tree.

    Signals:
    --------
    There are three blinker-based signals emitted by the data node:
    * child_added(child)
    * child_removed(child)
    * changed

    They are not emitted before children are loaded.
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

    def has_object(self):
        return (self._data_object is not None) or hasattr(self, "create_data_object")

    @property
    def data_object(self):
        if self._data_object is None:
            if hasattr(self, "create_data_object"):
                self._data_object = self.create_data_object()
                logging.debug("Data object created from node %s." % self.title)
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
        return text_type(self)

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
            self._children = []
            self.load_children()
            self.children_loaded = True
            self.changed.send(self)
        return self._children

    def add_child(self, child):
        if not child in self._children:
            child.parent = self
            self.changed.connect(self._on_changed, sender=child)
            self._children.append(child)
            if self.children_loaded:
                self.child_added.send(self, child=child)
                self._on_changed()
            logging.debug("Child %s added to node %s." % (child.title, self.title))

    def remove_child(self, child):
        if child in self._children:
            self._children.remove(child)
            if self.children_loaded:
                self.child_removed.send(self, child=child)
                self._on_changed()
            logging.debug("Child %s removed node %s." % (child.title, self.title))

    def load_children(self):
        '''Initially load children.

        This method is called when children are requested from a fresh node.

        For leaf nodes, this method does not nothing.
        For branch nodes, it has to be overriden.
        '''
        pass

    def reload_children(self):
        '''Force children reloading.'''
        self._children = []
        self.children_loaded = False
        self.changed.send(self)

    def _on_changed(self, *args):
        '''Called after any change of this node or its children.'''
        self.changed.send(self)

    def dump(self, stream=sys.stdout, indent=u"  ", subtree=False, in_depth=0, children_only=False, data_object_info=False):
        '''Write a textual representation of the tree.'''
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

    def _repr_html_(self):
        '''Simple HTML representation to be used e.g. in IPython.'''
        s = self.title
        if self.children:
            s += "<ul>"
            for child in self.children:
                s += "<li>%s</li>" % child._repr_html_()
            s += "</ul>"
        return s

      
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
        # TODO: Move elsewhere?
        return []


# Event logging
@DataNode.child_added.connect
def _log_child_added(sender, *args, **kwargs):
    logging.debug("Event 'child_added' sent from node %s." % sender.title)

@DataNode.child_removed.connect
def _log_child_removed(sender, *args, **kwargs):
    logging.debug("Event 'child_removed' sent from node %s." % sender.title)

@DataNode.changed.connect
def _log_changed(sender, *args, **kwargs):
    logging.debug("Event 'changed' sent from node %s." % sender.title)
