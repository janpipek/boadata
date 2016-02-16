from ..core import DataNode, DataObject, DataProperties, DataTree
import odo
import os


class TableNode(DataNode):
    def __init__(self, table_name, parent=None):
        super(TableNode, self).__init__(parent)
        self.table_name = table_name

    @property
    def title(self):
        return self.table_name

    def has_subtree(self):
        return False

    @property
    def uri(self):
        return self.parent.uri + "::" + self.table_name

    node_type = "SQL Table"


@DataTree.register_tree
class DatabaseTree(DataTree):
    def __init__(self, uri, parent=None):
        if os.path.isfile(uri):
            uri = "sqlite:///" + uri
        super(DatabaseTree, self).__init__(parent, uri=uri)
        self._db = None

    node_type = "SQL Database"

    @property
    def db(self):
        if not self._db:
            self._db = odo.resource(self.uri)
        return self._db

    def load_children(self):
        for name in self.db.table_names():
            child = TableNode(name, self)
            self.add_child(child)

    @property
    def title(self):
        return "Database ({0})".format(self.uri)

    @classmethod
    def accepts_uri(cls, uri):
        if not uri:
            return False
        if uri.endswith(".sqlite") and os.path.isfile(uri):
            return True
        for schema in ["sqlite"]:
            if uri.startswith(schema + ":///"):
                return True
        return False