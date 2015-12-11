from PyQt4.QtGui import QTextEdit
from .view import View, register_view
from six import text_type


class TextView(View):
    title = "Contents"

    def __init__(self, data_object):
        super(TextView, self).__init__(data_object)

    @classmethod
    def accepts(cls, data_object):
        '''Accepts all data objects.'''
        return data_object.converts_to("text")

    @property
    def widget(self):
        self.text_widget = QTextEdit()
        self.text_widget.setText(self.data_object.as_text())
        return self.text_widget


register_view(TextView)

