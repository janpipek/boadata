from collections import OrderedDict


class DataProperties(object):
    '''Data object properties.

    There can be a single list of properties (default),
    or a dictionary of properties for different categories.
    '''

    def __init__(self, data={}):
        self.default = data
        self.named = OrderedDict()

    def add(self, data, key=None):
        '''Set the properties.

        :param data: a dictionary of properties
        :param key: optional name of the category
        '''
        if not key:
            self.default = data
        else:
            self.named[key] = data

    def __nonzero__(self):
        '''Test emptiness of properties.'''
        return bool(self.default or self.named)