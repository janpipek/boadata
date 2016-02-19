__version__ = str('0.3.2')

def load(uri, *args, **kwargs):
    from . import core
    from . import data     # Loads all formats
    return core.DataObject.from_uri(uri, *args, **kwargs)