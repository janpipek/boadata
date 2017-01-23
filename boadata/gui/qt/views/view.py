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

    def create_widget(self, parent=None, *args, **kwargs):
        raise NotImplementedError("You have to implement create_widget.")

    @classmethod
    def show(cls, data_object, *args, **kwargs):
        """Create a view and show it.

        Blocks the execution for the time the GUI is displayed.
        """
        from .. import get_application
        # import signal
        # sig = signal.getsignal(signal.SIGINT)
        app = get_application()
        view = cls(data_object)
        widget = view.create_widget(parent=None, *args, **kwargs)
        widget.show()
        widget.setWindowTitle(data_object.name or data_object.uri or "Untitled")
        # signal.signal(signal.SIGINT, lambda a1, a2: widget.close())
        return app.exec_()

    registered_views = []

    @staticmethod
    def register_view(view):
        """Add a view class to the list of offered ones.

        Can be used as a decorator
        """
        View.registered_views.append(view)
        return view