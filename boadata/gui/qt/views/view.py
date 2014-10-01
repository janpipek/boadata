registered_views = []

class View(object):
    title = "Unknown view"

    def __init__(self, data_object):
        self.data_object = data_object

    @classmethod
    def supported_types(cls):
        return []

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        for type in cls.supported_types():
            if type in data_object.conversions:
                return True
        return False

def register_view(view):
    registered_views.append(view)