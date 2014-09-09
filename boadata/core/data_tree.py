class DataNode(object):
    @property
    def icon(self):
        return None


class DataTree(DataNode):
    pass


class DataBranch(DataNode):
    # Nodes
    pass


class DataLeaf(DataNode):
    pass