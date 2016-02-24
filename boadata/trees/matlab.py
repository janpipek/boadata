from boadata.core import DataNode, DataTree
import h5py
import logging
import os
import pydons


class _MatlabNode(DataNode):
    def __init__(self, parent, name, fb_node):
        super(_MatlabNode, self).__init__(parent)
        self.name = name
        self.fb_node = fb_node

    @property
    def title(self):
        return self.name

    def load_children(self):
        for name, value in self.fb_node.items():
            if isinstance(value, pydons.MatStruct):
                child = Matlab73Struct(self, name, value)
            elif isinstance(value, pydons.LazyDataset):
                child = Matlab73Dataset(self, name, value)
            else:
                pass
                # print ("Unknown: {0}".format(type(value)))
            self.add_child(child)


class Matlab73Dataset(_MatlabNode):
    def load_children(self):
        return None


class Matlab73Struct(_MatlabNode):
    pass


@DataTree.register_tree
class Matlab73Tree(_MatlabNode):
    def __init__(self, path, parent=None):
        self.path = path
        fb_node = pydons.FileBrowser(self.path, any_keys=True)
        super(Matlab73Tree, self).__init__(parent, self.path, fb_node)


    @classmethod
    def accepts_uri(cls, uri):
        return uri and os.path.isfile(uri) and (uri.endswith(".fig") or uri.endswith(".mat"))

    @property
    def title(self):
        return os.path.basename(self.path)

