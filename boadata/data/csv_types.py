from boadata.core import DataObject
import pandas as pd


@DataObject.register_type
class CSVFile(DataObject):
    type_name = "csv"

    real_type = pd.DataFrame

    ndim = 2

    def is_convertible_to(self, new_type_name):
        if new_type_name == "text":
            return True
        else:
            return super(CSVFile, self).is_convertible_to(new_type_name)

    def convert(self, new_type_name, **kwargs):
        if new_type_name == "text":
            constructor = DataObject.registered_types[new_type_name]
            return constructor.from_uri(self.uri, source=self, **kwargs)
        else:
            return super(CSVFile, self).convert(new_type_name, **kwargs)

    @property
    def shape(self):
        return self.inner_data.shape

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-4:] == ".csv"