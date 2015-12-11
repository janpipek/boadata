import logging

registered_views = []


class View(object):
    title = "Unknown view"

    def __init__(self, data_object):
        self.data_object = data_object
        logging.info("View %s created for object %s." % (self.title, data_object.title))

    @classmethod
    def supported_types(cls):
        return []

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        for type in cls.supported_types():
            if type in data_object.conversions:
                return True
        return

    def __repr__(self):
        return self.__class__.__name__


def register_view(view):
    registered_views.append(view)