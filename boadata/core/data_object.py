class DataObject(object):
    @property
    def title(self):
        return str(self)

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

    @property
    def data_object(self):
        return self

