from __future__ import annotations

import warnings
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any, Optional

    from boadata.core import DataObject, DataTree

__version__ = "0.4.1"

# Suppress the unpleasant pandas/seaborn<->matplotlib warning
warnings.filterwarnings("ignore", module="matplotlib")


def load(uri: str, type: Optional[str] = None, *args, **kwargs) -> DataObject:
    """Load an object from some URI.

    :param type: If present, forces this type to be used.
    """
    from . import data  # Loads all formats
    from . import core

    if type:
        return core.DataObject.registered_types[type].from_uri(uri, *args, **kwargs)
    else:
        return core.DataObject.from_uri(uri, *args, **kwargs)


def wrap(native_object, force: bool = True, **kwargs) -> DataObject:
    """Change some data object into a wrapped boadata type.

    :param force: If false, wrapping an unsupported object will result that object.
    """
    from . import data  # Loads all formats
    from . import core

    try:
        return core.DataObject.from_native(native_object, **kwargs)
    except RuntimeError:
        if not force:
            return native_object
        raise


def unwrap(boadata_object: DataObject, **kwargs) -> Any:
    """Change boadata object into its native type."""
    from .core import DataObject

    if isinstance(boadata_object, DataObject):
        return boadata_object.inner_data
    else:
        return boadata_object


def apply(native_object, function, *args, **kwargs):
    """Wrap an object, run something on it and then unwrap the result."""
    result = unwrap(function(wrap(native_object), *args, **kwargs))
    return result


def tree(uri: str) -> DataTree:
    """Load a tree from some URI."""
    from boadata import trees  # Enforce tree loading
    from boadata.core.data_tree import DataTree

    tree = None
    for cls in DataTree.registered_trees:
        if cls.accepts_uri(uri):
            try:
                tree = cls(uri=uri)
            except RuntimeError:
                pass
    if not tree:
        raise RuntimeError("No tree understood could be created from URI=" + uri)
    return tree
