registered_views = []

class View(object):
    title = "Unknown view"

    def __init__(self, data_object):
        self.data_object = data_object

    # @classmethod
    # def all(cls):
    #     return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in all_subclasses(s)]

    @classmethod
    def supported_types(cls):
        return []

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        for supported_type in cls.supported_types():
            if supported_types in data_object.conversions:
                return True
        return False

def register_view(view):
    registered_views.append(view)