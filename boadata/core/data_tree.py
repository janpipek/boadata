from __future__ import annotations

import os
from typing import TYPE_CHECKING

from .data_node import DataNode

if TYPE_CHECKING:
    from typing import List, Type


class DataTree(DataNode):
    """A node that forms the top in the tree view."""

    registered_trees: List[Type[DataTree]] = []

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return False

    @staticmethod
    def register_tree(cls: Type[DataTree]) -> None:
        DataTree.registered_trees += [cls]
        return cls

    @classmethod
    def from_uri(cls, uri: str) -> DataTree:
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
                raise RuntimeError(
                    "No tree understood could be created from URI=" + uri
                )
            return tree
        else:
            return cls(uri)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.uri})>"

    # mime_types = ()
