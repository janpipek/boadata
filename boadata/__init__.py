__version__ = str('0.3.3')

def load(uri, type=None, *args, **kwargs):
    from . import core
    from . import data     # Loads all formats
    if type:
        return core.DataObject.registered_types[type].from_uri(uri, *args, **kwargs)
    else:
        return core.DataObject.from_uri(uri, *args, **kwargs)


def wrap(native_object, **kwargs):
    """Change some data object into a wrapped boadata type."""
    from . import core
    from . import data     # Loads all formats
    return core.DataObject.from_native(native_object)


def unwrap(boadata_object, **kwargs):
    """Change boadata object into its native type.

    :type boadata_object: boadata.core.data_object.DataObject
    :param kwargs:
    :return:
    """
    return boadata_object.inner_data


def apply(native_object, function):
    from . import core
    wrapped = wrap(native_object)
    result = function(wrapped)
    if isinstance(result, core.DataObject):
        result = unwrap(result)
    return result