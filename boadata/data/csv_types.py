from boadata.core import DataObject
import pandas as pd
import odo


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

    @classmethod
    def from_uri(cls, uri, index_col=False, **kwargs):
        resource = odo.resource(uri)
        if hasattr(resource, "dialect"):
            kwargs.update(resource.dialect)
        print(kwargs)
        try:
            data = odo.odo(uri, pd.DataFrame, index_col=index_col, **kwargs)
        except:
            data = pd.read_csv(uri, index_col=index_col, **kwargs)
        return cls(inner_data=data, uri=uri, **kwargs)
