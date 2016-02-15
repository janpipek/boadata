import logging


class View(object):
    """

    :type title: string
    :type data_object: boadata.core.DataObject
    """
    title = "Unknown view"

    @classmethod
    def accepts(cls, data_object):
        """

        This is the default implementation.

        :type data_object: boadata.core.DataObject
        :rtype bool
        :return:
        """
        for type_ in cls.supported_types:
            if data_object.is_convertible_to(type_):
                return True
        return False

    supported_types = []

    def __init__(self, data_object):
        self.data_object = data_object
        self.data_object.changed.connect(self.on_object_changed)

    def on_object_changed(self, sender, *args, **kwargs):
        pass    # Override

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