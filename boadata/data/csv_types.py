from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import OdoConversion, IdentityConversion
import pandas as pd
import odo


@DataObject.register_type
@IdentityConversion.enable_to("pandas_data_frame")
class CSVFile(DataObject):
    type_name = "csv"

    real_type = pd.DataFrame

    ndim = 2

    @DataConversion.register("csv", "text")
    def to_text(self, **kwargs):
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @property
    def shape(self):
        return self.inner_data.shape

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-4:] == ".csv"

    def __getitem__(self, item):
        item = self.convert("pandas_data_frame")[item]
        item.source = self
        return item

    @classmethod
    def from_uri(cls, uri, index_col=False, source=None, **kwargs):
        resource = odo.resource(uri)
        if hasattr(resource, "dialect"):
            kwargs.update(resource.dialect)
        try:
            data = odo.odo(uri, pd.DataFrame, index_col=index_col, **kwargs)
        except:
            data = pd.read_csv(uri, index_col=index_col, **kwargs)
        return cls(inner_data=data, uri=uri, source=source, **kwargs)

