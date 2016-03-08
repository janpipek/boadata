from .data_node import DataNode
import os


class DataTree(DataNode):
    """A node that forms the top in the tree view."""

    registered_trees = []

    # TODO: Reconsider
    @property
    def menu_title(self):
        '''Title of the menu displayed in main menu bar.

        Override if not equal to title.
        '''
        return self.title

    # TODO: Reconsider
    @property
    def menu_actions(self):
        '''Qt actions that should be put into the menu in main menu bar.'''
        # TODO: Move elsewhere?
        return []

    @classmethod
    def accepts_uri(cls, uri):
        return False

    @staticmethod
    def register_tree(cls):
        DataTree.registered_trees += [cls]
        return cls

    @classmethod
    def from_uri(cls, uri):
        """Load a tree from some URI.

        :type uri: str
        """
        if cls is DataTree:
            tree = None
            for klass in DataTree.registered_trees:
                if cls.accepts_uri(uri):
                    try:
                        tree = klass(uri)
                    except:
                        pass
                if os.path.isfile(uri):
                    # TODO: Check mime types
                    pass
            if not tree:
                raise RuntimeError("No tree understood could be created from URI=" + uri)
            return tree
        else:
            return cls(uri)

    # mime_types = ()