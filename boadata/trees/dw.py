import re

import datadotworld as dw

from boadata.core import DataNode, DataTree


def _get_token():
    return dw._get_instance(profile="default")._config.auth_token


def _get_data(what):
    if what not in ["own", "contributing", "liked"]:
        raise RuntimeError("Not understood")
    import requests

    data = {}
    headers = {"authorization": "Bearer {0}".format(_get_token())}
    response = requests.get(
        "https://api.data.world/v0/user/datasets/{0}".format(what),
        data=data,
        headers=headers,
    )
    res = response.json()
    return res["records"]


class DataDotWorldTableNode(DataNode):
    node_type = "data.world table"

    def __init__(self, parent, table_name):
        uri = "/".join([parent.uri, table_name])
        super(DataDotWorldTableNode, self).__init__(parent, uri=uri)
        self.table_name = table_name

    @property
    def title(self):
        return self.table_name

    @property
    def data_object(self):
        from boadata.data.dw_types import DataDotWorldTable

        return DataDotWorldTable.from_uri(self.uri)


@DataTree.register_tree
class DataDotWorldDataSetNode(DataTree):
    _re = re.compile("^dw://(\\w|\-)+/(\\w|\-)+/?$")

    node_type = "data.world dataset"

    def __init__(self, uri, parent=None, include_owner=True):
        super(DataDotWorldDataSetNode, self).__init__(parent, uri=uri.strip("/"))
        self.owner = self.uri.split("/")[2]
        self.data_set_name = self.uri.split("/")[3]
        self.data_set = None
        self.include_owner = include_owner

    @property
    def title(self):
        if self.include_owner:
            return "/".join(self.uri.split("/")[2:])
        else:
            return self.data_set_name

    def load_children(self):
        if self.data_set is None:
            full_name = self.owner + "/" + self.data_set_name
            self.data_set = dw.load_dataset(full_name)
        for table_name in self.data_set.dataframes.keys():
            self.add_child(DataDotWorldTableNode(self, table_name))

    @classmethod
    def accepts_uri(cls, uri):
        return re.match(DataDotWorldDataSetNode._re, uri or "") is not None


class DataDotWorldUserSub(DataNode):
    def __init__(self, parent, source):
        super(DataDotWorldUserSub, self).__init__(parent=parent)
        self.source = source

    @property
    def title(self):
        return self.source

    def load_children(self):
        records = _get_data(self.source)
        for dataset in records:
            owner = dataset["owner"]
            id = dataset["id"]
            uri = "dw://{0}/{1}".format(owner, id)
            self.add_child(
                DataDotWorldDataSetNode(uri=uri, include_owner=(self.source != "own"))
            )


@DataTree.register_tree
class DataDotWorldOwnTree(DataTree):
    _re = re.compile("^dw://$")

    node_type = "data.world user tables"

    def __init__(self, uri, parent=None):
        super(DataDotWorldOwnTree, self).__init__(parent, uri=uri)

    @property
    def title(self):
        return "Your data.world datasets"

    def load_children(self):
        self.add_child(DataDotWorldUserSub(self, "own"))
        self.add_child(DataDotWorldUserSub(self, "contributing"))
        self.add_child(DataDotWorldUserSub(self, "liked"))

    @classmethod
    def accepts_uri(cls, uri):
        return re.match(DataDotWorldOwnTree._re, uri or "") is not None
