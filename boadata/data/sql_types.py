from boadata.core.data_object import OdoDataObject, DataObject
from boadata.core.data_conversion import OdoConversion, ChainConversion
import sqlalchemy as sa


@OdoConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=("uri",))
@DataObject.register_type
class DatabaseTable(OdoDataObject):
    type_name = "db_table"

    real_type = sa.Table

    @classmethod
    def accepts_uri(cls, uri):
        if uri.startswith("sqlite:///"):
            return True
        return False

    @property
    def ndim(self):
        return 2

    @property
    def shape(self):
        rows = self.inner_data.count().execute().fetchone()[0]
        cols = len(self.columns)
        return (cols, rows)

    def __getitem__(self, item):
        return self.convert("pandas_data_frame")[item]

    @property
    def columns(self):
        return [col.name for col in self.inner_data.columns.values()]