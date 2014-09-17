import sys
from collections import OrderedDict
import StringIO

class DataNode(object):
    """

    DataNode can also be a DataObject.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.children_loaded = False
        self._children = []        

    @property
    def icon(self):
        return None

    @property
    def data_object(self):
        return None

    @property
    def properties(self):
        return OrderedDict()

    @property
    def children(self):
        return []

    @property
    def title(self):
        return str(self)    

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
        return self.subtree() is not None

    @property
    def children(self):
        """Lazy access to children."""
        # TODO: Add option to disable caching
        if not self.children_loaded:
            self.load_children()
            self.children_loaded = True
        return self._children

    def add_child(self, child):
        child.parent = self   # Force here?
        self._children.append(child)

    def load_children(self):
        pass

    def dump(self, stream=sys.stdout, indent=u"  ", subtree=False, in_depth=0, children_only=False):
        if not children_only:
            stream.write(in_depth * indent)
            stream.write(self.title)
        if self.has_subtree() and subtree:
            stream.write(":")
            self.subtree().dump(stream, indent, subtree, in_depth, children_only=True)
        else:
            stream.write("\n")
        for child in self.children:    
            child.dump(stream, indent, subtree, in_depth+1)
        
