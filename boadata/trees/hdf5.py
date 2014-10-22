from ..core import DataNode, DataObject, DataProperties, DataTree
import h5py
from file import register_tree_generator
import os
import pandas as pd
import numpy as np

def create_hdf_node(h5_object):
    if isinstance(h5_object, h5py.Group):
        return GroupNode(h5_object)
    elif isinstance(h5_object, h5py.Dataset):
        return DatasetNode(h5_object)
    else:
        print "Warning: unknown hdf5 item type - %s" % type(h5_object)


class Hdf5Node(DataNode):
    def __init__(self, h5_object, parent=None):
        super(Hdf5Node, self).__init__(parent)
        self.h5_object = h5_object

    def load_children(self):
        for key, value in self.h5_object.items():
            child = create_hdf_node(value)
            if child:
                self.add_child(child)     

    @property
    def title(self):
        return self.h5_object.name.rsplit("/", 1)[1]


class FileNode(Hdf5Node, DataTree):
    def __init__(self, path, parent=None):
        super(FileNode, self).__init__(parent)
        self.path = path
        self.h5_object = h5py.File(self.path, "r")

    node_type = "HDF5 file"

    @property
    def title(self):
        return os.path.basename(self.path) + "(HDF5)"


class GroupNode(Hdf5Node):
    node_type = "HDF5 group"


class DatasetObject(DataObject):
    def __init__(self, h5_dataset, node=None):
        super(DatasetObject, self).__init__(node)
        self.h5_dataset = h5_dataset

    @property
    def shape(self):
        return self.h5_dataset.shape

    @property
    def ndim(self):
        return len(self.h5_dataset.shape)

    @property
    def properties(self):
        return DataProperties(self.h5_dataset.attrs)

    def as_numpy_array(self):
        return np.array(self.h5_dataset)


class DatasetNode(Hdf5Node):
    node_type = "HDF5 dataset"

    def create_data_object(self):
        return DatasetObject(self.h5_object, self)

    def load_children(self):
        pass



register_tree_generator(".hdf5", FileNode)
register_tree_generator(".h5", FileNode)