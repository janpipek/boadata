from boadata.core import DataTree


class GenericTree(DataTree):
    """A tree that accepts adding nodes of any type."""

    def __init__(self, parent=None):
        super(GenericTree, self).__init__(parent)
        self._title = "Generic tree"
        self.children_loaded = True  # Empty by default

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        self._title = new_title
