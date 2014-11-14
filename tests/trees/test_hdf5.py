import unittest
from h5py import File, Group
import tempfile
import os
import numpy as np
from boadata.trees.hdf5 import DatasetNode, FileNode, GroupNode


class TestHdf5Tree(unittest.TestCase):
    def test_open_empty_file(self):
        try:
            _, fname = tempfile.mkstemp(".h5")
            with File(fname, "w") as h5f:
                pass
            h5node = FileNode(fname)
            self.assertFalse(h5node.children)
        finally:
            os.remove(fname)

    def test_nonexistent_file(self):
        try:
            dirpath = tempfile.mkdtemp()
            fpath = os.path.join(dirpath, "non-existent.h5")
            self.assertRaises(IOError, lambda: FileNode(fpath))
        finally:
            os.removedirs(dirpath)
        pass

    def test_existing_file_structure(self):
        '''Creates the following structure:
        file
        +-ggg[]
        | +-ggg-ddd
        +-ddd
        +-ggg2
        '''
        try:
            _, fname = tempfile.mkstemp(".h5")
            with File(fname, "w") as h5f:
                group = h5f.create_group("ggg")
                dataset = h5f.create_dataset("ddd", data=np.random.rand(3, 3))
                group_dataset = group.create_dataset("ggg-ddd", data=np.random.rand(3, 3, 3))
                h5f.create_group("ggg2")
            h5node = FileNode(fname)

            self.assertEqual(3, len(h5node.children))
            self.assertItemsEqual(("ggg", "ddd", "ggg2"), (c.title for c in h5node.children))

            groupnode = [n for n in h5node.children if n.title == "ggg"][0]
            self.assertEqual(h5node, groupnode.parent)
            assert isinstance(groupnode, GroupNode)
            assert not isinstance(groupnode, DatasetNode)
            assert not isinstance(groupnode, FileNode)
            self.assertEqual(1, len(groupnode.children))
            childnode = groupnode.children[0]
            self.assertEqual("ggg-ddd", childnode.title)
            self.assertEqual(groupnode, childnode.parent)
            self.assertEqual(0, len(childnode.children))
            assert isinstance(childnode, DatasetNode)

            datanode2 = [n for n in h5node.children if n.title == "ddd"][0]
            assert isinstance(datanode2, DatasetNode)

            group2node = [n for n in h5node.children if n.title == "ggg2"][0]
            self.assertEqual(0, len(group2node.children))
        finally:
            os.remove(fname)


class TestHdf5Properties(unittest.TestCase):
    pass