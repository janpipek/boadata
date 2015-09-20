from .data_properties import DataProperties


class DataObject(object):
    '''A basic object that contains data representable by boadata.

    Typically, some of the nodes have data objects,
    An object can have multiple representations (like numpy array, etc.)
    '''
    def __init__(self, node=None):
        self.node = node

    @property
    def title(self):
        return str(self)

    @property
    def properties(self):
        return DataProperties()

    # TODO: Give this some meaning
    read_only = True

    @property
    def conversions(self):
        '''Available object conversions.

        It is possible to override this property if conversion list is not static.
        '''
        return tuple(attr.partition("_")[2] for attr in dir(self) if attr.startswith("as_"))

    def to(self, conversion):
        '''Perform the conversion.
        '''
        attr = 'as_' + conversion
        if not hasattr(self, attr):
            raise RuntimeError("Conversion not supported.")
        return getattr(self, attr)()

    def converts_to(self, format):
        '''Whether the object can be represented as a format.

        :param format: name of the type (like numpy_array, pandas_frame, ...)
        '''
        return format in self.conversions

    @property
    def shape(self):
        return None

    @property
    def ndim(self):
        return None