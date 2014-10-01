from collections import OrderedDict

class DataProperties(object):
    '''Data object properties.'''
    def __init__(self, data={}):
        self.default = data
        self.named = OrderedDict()

    def add(self, data, key=None):
        if not key:
            self.default = data
        else:
            self.named[key] = data

    def __nonzero__(self):
        return bool(self.default or self.named)