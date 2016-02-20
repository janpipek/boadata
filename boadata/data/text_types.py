from boadata.core import DataObject
import codecs


@DataObject.register_type()
class TextFile(DataObject):
    type_name = "text"

    real_type = str

    @classmethod
    def accepts_uri(cls, uri):
        if uri[-4:] == ".txt":
            return True
        else:
            return False

    @classmethod
    def from_uri(cls, uri, **kwargs):
        with codecs.open(uri, "r", encoding="utf-8") as f:
            return TextFile(uri=uri, inner_data=f.read(), **kwargs)
