__version__ = str('0.3.4')

# Suppress the unpleasant pandas/seaborn<->matplotlib warning
import warnings
warnings.filterwarnings("ignore", module="matplotlib")


def load(uri, type=None, *args, **kwargs):
    from . import core
    from . import data     # Loads all formats
    if type:
        return core.DataObject.registered_types[type].from_uri(uri, *args, **kwargs)
    else:
        return core.DataObject.from_uri(uri, *args, **kwargs)


def wrap(native_object, force=True, **kwargs):
    """Change some data object into a wrapped boadata type."""
    from . import core
    from . import data     # Loads all formats
    try:
        return core.DataObject.from_native(native_object, **kwargs)
    except RuntimeError as ex:
        if not force:
            return native_object
        raise


def unwrap(boadata_object, **kwargs):
    """Change boadata object into its native type.

    :type boadata_object: boadata.core.data_object.DataObject
    :param kwargs:
    :return:
    """
    from .core import DataObject
    if isinstance(boadata_object, DataObject):
        return boadata_object.inner_data
    else:
        return boadata_object


def apply(native_object, function):
    result = unwrap(function(wrap(native_object)))
