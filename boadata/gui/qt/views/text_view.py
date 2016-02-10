from PyQt4.QtGui import QTextEdit
from .view import View


@View.register_view
class TextView(View):
    title = "Text"

    supported_types = ("text",)

    def __init__(self, data_object):
        super(TextView, self).__init__(data_object)

    def create_widget(self):
        self.text_widget = QTextEdit()
        self.text_widget.setReadOnly(True)
        do = self.data_object.convert("text")
        self.text_widget.setText(do.inner_data)
        return self.text_widget
