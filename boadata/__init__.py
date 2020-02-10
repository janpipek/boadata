from typing import Optional
import warnings

__version__ = '0.3.13'

# Suppress the unpleasant pandas/seaborn<->matplotlib warning
warnings.filterwarnings("ignore", module="matplotlib")


def load(uri: str, type: Optional[str] = None, *args, **kwargs) -> 'boadata.core.DataObject':
    """Load an object from some URI.

    :param type: If present, forces this type to be used.
    """
    from . import core
    from . import data     # Loads all formats
    if type:
        return core.DataObject.registered_types[type].from_uri(uri, *args, **kwargs)
    else:
        return core.DataObject.from_uri(uri, *args, **kwargs)


def wrap(native_object, force: bool = True, **kwargs) -> 'boadata.core.DataObject':
    """Change some data object into a wrapped boadata type.

    :param force: If false, wrapping an unsupported object will result that object.
    """
    from . import core
    from . import data     # Loads all formats
    try:
        return core.DataObject.from_native(native_object, **kwargs)
    except RuntimeError as ex:
        if not force:
            return native_object
        raise


def unwrap(boadata_object: 'boadata.core.DataObject', **kwargs):
    """Change boadata object into its native type."""
    from .core import DataObject
    if isinstance(boadata_object, DataObject):
        return boadata_object.inner_data
    else:
        return boadata_object


def apply(native_object, function, *args, **kwargs):
    """Wrap an object, run something on it and then unwrap the result."""
    result = unwrap(function(wrap(native_object), *args, **kwargs))


def tree(uri: str) -> 'boadata.core.data_tree.Datatree':
    """Load a tree from some URI."""
    from boadata import trees  # Enforce tree loading
    from boadata.core.data_tree import DataTree

    tree = None
    for cls in DataTree.registered_trees:
        if cls.accepts_uri(uri):
            try:
                tree = cls(uri)
            except:
                pass
    if not tree:
        raise RuntimeError("No tree understood could be created from URI=" + uri)
    return tree
