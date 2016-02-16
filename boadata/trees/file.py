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


@DataTree.register_tree
class DirectoryTree(DirectoryNode, DataTree):
    @property
    def title(self):
        return self.uri + " (Directory)"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and os.path.isdir(uri)