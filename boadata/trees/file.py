import mimetypes
import os
from pathlib import Path

from boadata.core import DataNode, DataTree


class PathNode(DataNode):
    @property
    def path(self) -> Path:
        return Path(self.uri)

    @property
    def title(self):
        return self.path.name

    @property
    def mime_type(self):
        return mimetypes.guess_type(self.path)


class FileNode(PathNode):
    node_type = "File"


class DirectoryNode(PathNode):
    node_type = "Directory"

    def load_children(self) -> None:
        items = os.listdir(str(self.path))
        items = [os.path.join(str(self.path), item) for item in items]
        files = sorted(item for item in items if os.path.isfile(item))
        dirs = sorted(item for item in items if os.path.isdir(item))
        for d in dirs:
            self.add_child(DirectoryNode(self, d))
        for f in files:
            self.add_child(FileNode(self, f))


@DataTree.register_tree
class DirectoryTree(DirectoryNode, DataTree):
    @property
    def title(self):
        return self.uri + " (Directory)"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and os.path.isdir(uri)
