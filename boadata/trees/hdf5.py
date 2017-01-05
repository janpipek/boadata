from boadata.core import DataNode, DataTree
from .file import FileNode
import h5py
import logging
import os


def create_hdf_node(h5_object):
    """
    :type h5_object: h5py.highlevel.HLObject
    :rtype Hdf5Node
    """
    if isinstance(h5_object, h5py.Group):
        return GroupNode(h5_object)
    elif isinstance(h5_object, h5py.Dataset):
        return DatasetNode(h5_object)
    else:
        logging.warning("Warning: unknown hdf5 item type - %s" % type(h5_object))


class Hdf5Node(DataNode):
    def __init__(self, h5_object, parent=None):
        """

        :type h5_object: h5py.Group | h5py.Dataset
        """
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


@DataTree.register_tree
class Hdf5FileNode(Hdf5Node, DataTree):
    def __init__(self, path, parent=None):
        super(Hdf5FileNode, self).__init__(parent)
        self.path = path
        self.h5_object = h5py.File(self.path, "r")

    node_type = "HDF5 file"

    @property
    def title(self):
        return os.path.basename(self.path) + " (HDF5)"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and h5py.is_hdf5(uri)


class GroupNode(Hdf5Node):
    node_type = "HDF5 group"


class DatasetNode(Hdf5Node):
    node_type = "HDF5 dataset"

    def load_children(self):
        pass

    @property
    def uri(self):
        return "{0}::{1}".format(self.h5_object.file.filename, self.h5_object.name[1:])