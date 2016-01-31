from PyQt4.QtGui import QTextEdit
from .view import View


@View.register_view
class TextView(View):
    title = "Text"

    @classmethod
    def accepts(cls, data_object):
        """

        :type data_object: boadata.core.DataObject
        :rtype bool
        """
        return data_object.is_convertible_to("text")

    def __init__(self, data_object):
        super(TextView, self).__init__(data_object)

    def create_widget(self):
        self.text_widget = QTextEdit()
        do = self.data_object.convert("text")
        self.text_widget.setText(do.inner_data)
        return self.text_widget
