from ..core import DataNode, DataTree
import os
import mimetypes
from six import text_type
import logging


class PathNode(DataNode):
    def __init__(self, path, parent=None):
        super(PathNode, self).__init__(parent)
        self.path = path
    
    @property
    def title(self):
        return text_type(os.path.basename(self.path))

    @property
    def mime_type(self):
        return mimetypes.guess_type(self.path)

    @property
    def uri(self):
        return self.path


class FileNode(PathNode):
    node_type = "File"

    tree_generators = {}

    @staticmethod
    def register_tree_generator(mime_type, func):
        FileNode.tree_generators[mime_type] = func

    def has_subtree(self):
        return self._get_subtree_generator() is not None

    def _get_subtree_generator(self):
        mime = self.mime_type[0]
        if mime in FileNode.tree_generators:
            return FileNode.tree_generators[mime]
        else:
            ext = os.path.splitext(self.path)[1]
            return FileNode.tree_generators.get(ext, None)

    def subtree(self):
        gen = self._get_subtree_generator()
        if not gen:
            return None
        else:
            try:
                return gen(self.path)
            except Exception as ex:
                logging.error(text_type(ex))
                return None


class DirectoryNode(PathNode):
    node_type = "Directory"

    def load_children(self):
        items = os.listdir(self.path)
        items = [os.path.join(self.path, item) for item in items]
        files = sorted(item for item in items if os.path.isfile(item))
        dirs = sorted(item for item in items if os.path.isdir(item))
        for d in dirs:
            self.add_child(DirectoryNode(d, self))
        for f in files:
            self.add_child(FileNode(f, self))


class DirectoryTree(DirectoryNode, DataTree):
    @property
    def title(self):
        return "File Browser"