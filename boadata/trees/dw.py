import re

import datadotworld as dw

from boadata.core import DataNode, DataTree
from boadata.data.dw_types import DataDotWorldTable


class DataDotWorldTableNode(DataNode):
    node_type = "data.world table"

    def __init__(self, parent, table_name):
        uri = "/".join([parent.uri, table_name])
        super(DataDotWorldTableNode, self).__init__(parent, uri=uri)
        self.table_name = table_name
        #print(uri)

    @property
    def title(self):
        return self.table_name

    @property
    def data_object(self):
        from boadata.data.dw_types import DataDotWorldTable
        return DataDotWorldTable.from_uri(self.uri)


@DataTree.register_tree
class DataDotWorldDataSetNode(DataTree):
    _re = re.compile("dw://(\\w|\-)+/(\\w|\-)+/?$")

    node_type = "data.world dataset"

    def __init__(self, uri, parent=None):
        super(DataDotWorldDataSetNode, self).__init__(parent, uri=uri.strip("/"))
        self.data_set = None

    @property
    def title(self):
        return "/".join(self.uri.split("/")[2:])

    def load_children(self):
        if self.data_set is None:
            dataset_name = "/".join(self.uri.split("/")[2:])
            print("Loading...", dataset_name)
            self.data_set = dw.load_dataset(dataset_name)
        for table_name in self.data_set.dataframes.keys():
            self.add_child(DataDotWorldTableNode(self, table_name))

    @classmethod
    def accepts_uri(cls, uri):
        return re.match(DataDotWorldDataSetNode._re, uri or "") is not None

