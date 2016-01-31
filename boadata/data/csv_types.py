from boadata.core import DataObject
import pandas as pd


@DataObject.register_type
class CSVFile(DataObject):
    type_name = "csv"

    real_type = pd.DataFrame

    ndim = 2

    @property
    def shape(self):
        return self.inner_data.shape

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-4:] == ".csv"