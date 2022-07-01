from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable

import blinker

from boadata.core.data_object import UnknownDataObjectError


if TYPE_CHECKING:
    from typing import Iterator, List, Optional, Tuple

    from boadata.core.data_object import DataObject


class DataNode:
    """A branch/leaf in a data tree.

    Signals:
    --------
    There are three blinker-based signals emitted by the data node:
    * child_added(child)
    * child_removed(child)
    * changed

    They are not emitted before children are loaded.
    """

    def __init__(self, parent: Optional[DataNode] = None, uri: Optional[str] = None):
        self.parent = parent
        self.children_loaded = False
        self._children = []
        self._data_object = None
        self._uri = uri

    node_type: str = "Unknown"

    # Signals
    child_added = blinker.Signal("child_added")
    child_removed = blinker.Signal("child_removed")
    changed = blinker.Signal("changed")

    @property
    def data_object(self) -> Optional[DataObject]:
        """The data object

        This is the default, relatively inefficient variant, based on URI.
        If there is no object, returns None:
        """
        if not self.uri:
            return None

        # Force registration
        import boadata.data  # noqa: F401

        try:
            return DataObject.from_uri(self.uri)
        except UnknownDataObjectError:
            return None

    @property
    def uri(self) -> Optional[str]:
        return self._uri

    def iter_children(self) -> Iterator[DataNode]:
        # TODO: Make this default?
        yield from self.children

    def walk(
        self,
        *,
        current_level: int = 0,
        current_subtree: bool = False,
        include_self: bool = True,
        include_children: bool = True,
        include_subtree: bool = True,
        max_level: Optional[int] = None,
    ) -> Iterator[Tuple[int, bool, DataNode]]:
        if max_level is not None and current_level > max_level:
            return
        if include_self:
            yield current_level, current_subtree, self
        if (max_level is None) or (current_level < max_level):
            if include_children:
                for child in self.iter_children():
                    yield from child.walk(
                        current_level=current_level + 1, max_level=max_level
                    )
            if include_subtree:
                if self.has_subtree():
                    yield from self.subtree().walk(
                        current_level=current_level + 1,
                        current_subtree=True,
                        include_self=False,
                        max_level=max_level,
                    )

    @property
    def title(self):
        return str(self)

    @property
    def full_title(self):
        if self.parent:
            return self.parent.full_title + "/" + self.title
        else:
            return self.title

    def subtree(self) -> DataNode:
        from boadata import tree

        return tree(self.uri)

    def has_subtree(self) -> bool:
        """Whether the node can serve as a root of another tree."""
        from .data_tree import DataTree

        for cls in DataTree.registered_trees:
            if cls.accepts_uri(self.uri) and cls != self.__class__:
                return True
        return False

    @property
    def children(self) -> Iterable[DataNode]:
        """Lazy access to children."""
        # TODO: Add option to disable caching
        if not self.children_loaded:
            self._children = []
            self.load_children()
            self.children_loaded = True
            self.changed.send(self)
        return self._children

    @property
    def child_names(self) -> List[str]:
        return [child.title for child in self.children]

    def add_child(self, child: DataNode) -> None:
        if child not in self._children:
            child.parent = self
            self.changed.connect(self._on_changed, sender=child)
            self._children.append(child)
            if self.children_loaded:
                self.child_added.send(self, child=child)
                self._on_changed()
            logging.debug("Child %s added to node %s." % (child.title, self.title))

    def remove_child(self, child: DataNode) -> None:
        if child in self._children:
            self._children.remove(child)
            if self.children_loaded:
                self.child_removed.send(self, child=child)
                self._on_changed()
            logging.debug("Child %s removed node %s." % (child.title, self.title))

    def load_children(self) -> None:
        """Initially load children.

        This method is called when children are requested from a fresh node.

        For leaf nodes, this method does not nothing.
        For branch nodes, it has to be overriden.
        """
        pass

    def reload_children(self) -> None:
        """Force children reloading."""
        self._children = []
        self.children_loaded = False
        self.changed.send(self)

    def _on_changed(self, *args):
        """Called after any change of this node or its children."""
        self.changed.send(self)

    def _repr_html_(self) -> str:
        """Simple HTML representation to be used e.g. in IPython."""
        # TODO: Reimplement in terms of walk
        s = self.title
        if self.children:
            s += "<ul>"
            for child in self.children:
                s += "<li>%s</li>" % child._repr_html_()
            s += "</ul>"
        return s

    def __getitem__(self, name):
        if isinstance(name, int):
            if name > len(self.children):
                return None
            return self.children[name]
        for child in self.children:
            if child.title == name:
                return child
        return None


# Event logging
@DataNode.child_added.connect
def _log_child_added(sender, *args, **kwargs):
    logging.debug("Event 'child_added' sent from node %s." % sender.title)


@DataNode.child_removed.connect
def _log_child_removed(sender, *args, **kwargs):
    logging.debug("Event 'child_removed' sent from node %s." % sender.title)


@DataNode.changed.connect
def _log_changed(sender, *args, **kwargs):
    logging.debug("Event 'changed' sent from node %s." % sender.title)
