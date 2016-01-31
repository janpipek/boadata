import logging


class View(object):
    title = "Unknown view"

    @classmethod
    def accepts(cls, data_object):
        return None

    def __init__(self, data_object):
        self.data_object = data_object
        logging.info("View %s created for object %s." % (self.title, data_object.title))

    def __repr__(self):
        return self.__class__.__name__

    def create_widget(self):
        raise NotImplementedError("You have to implement create_widget.")

    registered_views = []

    @staticmethod
    def register_view(view):
        """Add a view class to the list of offered ones.

        Can be used as a decorator
        """
        View.registered_views.append(view)
        return view