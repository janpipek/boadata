from pydataset import data
from boadata.core import DataTree, DataNode


class PydatasetNode(DataNode):
    def __init__(self, name, description, parent=None):
        super(PydatasetNode, self).__init__()
        self.name = name
        self.description = description

    @property
    def uri(self):
        return "pydataset://{0}".format(self.name)

    def load_children(self):
        pass

    @property
    def title(self):
        return "{0} ({1})".format(self.name, self.description)


@DataTree.register_tree
class PydatasetTree(DataTree):
    @classmethod
    def accepts_uri(cls, uri):
        return uri == "pydataset://"

    @property
    def title(self):
        return "pydataset data sets"

    def load_children(self):
        for row in data().itertuples():
            child = PydatasetNode(row[1], row[2], self)
            if child:
                self.add_child(child)