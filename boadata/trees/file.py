from ..core import DataNode
import os
import mimetypes

class PathNode(DataNode):
    def __init__(self, path, parent=None):
        super(PathNode, self).__init__(parent)
        self.path = path
    
    @property
    def title(self):
        return os.path.basename(self.path)        

    @property
    def mime_type(self):
        return mimetypes.guess_type(self.path)   

class FileNode(PathNode):
    pass

class DirectoryNode(PathNode):
    def load_children(self):
        items = os.listdir(self.path)
        items = [os.path.join(self.path, item) for item in items]
        files = sorted(item for item in items if os.path.isfile(item))
        dirs = sorted(item for item in items if os.path.isdir(item))
        for d in dirs:
            self.add_child(DirectoryNode(d, self))
        for f in files:
            self.add_child(FileNode(f, self))