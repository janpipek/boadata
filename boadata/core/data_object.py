class DataObject(object):
    @property
    def title(self):
        return str(self)

    @property
    def conversions(self):
        '''Available object conversions.

        It is possible to override this property if conversion list is not static.
        '''
        return tuple(attr.strip("_").partition("_")[2] for attr in dir(self) if attr.startswith("__as_") and attr.endswith("__"))


