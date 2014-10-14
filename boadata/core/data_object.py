from data_properties import DataProperties

class DataObject(object):
    def __init__(self, node=None):
        self.node = node

    @property
    def title(self):
        return str(self)

    @property
    def properties(self):
        return DataProperties()

    @property
    def conversions(self):
        '''Available object conversions.

        It is possible to override this property if conversion list is not static.
        '''
        return tuple(attr.partition("_")[2] for attr in dir(self) if attr.startswith("as_"))

    def to(self, conversion):
        attr = "as_" + conversion
        if not hasattr(self, attr):
            raise "Conversion not supported."
        return getattr(self, attr)()

    def converts_to(self, format):
        return format in self.conversions

    @property
    def shape(self):
        return None

    @property
    def ndim(self):
        return None