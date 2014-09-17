import sys
from collections import OrderedDict
import StringIO

class DataNode(object):
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
    def children(self):
        """Lazy access to children."""
        # TODO: Add option to disable caching
        if not self.children_loaded:
            self.load_children()
            self.children_loaded = True
        return self._children

    def add_child(self, child):
        child.parent = self # Force here?
        self._children.append(child)

    def load_children(self):
        pass

    def dump(self, stream=sys.stdout, indent="  "):
        stream.write(self.title + "\n")
        for child in self.children:
            io = StringIO.StringIO()            
            child.dump(io, indent)
            for line in io.getvalue().splitlines():
                stream.write(indent + line + "\n")