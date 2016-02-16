from .data_node import DataNode


class DataTree(DataNode):
    registered_trees = []

    '''A node that can be top-level in the tree view.
    '''

    @property
    def menu_title(self):
        '''Title of the menu displayed in main menu bar.

        Override if not equal to title.
        '''
        return self.title

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