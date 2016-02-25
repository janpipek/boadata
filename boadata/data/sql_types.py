from boadata.core.data_object import OdoDataObject, DataObject
from boadata.core.data_conversion import OdoConversion, ChainConversion
import sqlalchemy as sa
import re
import os


@DataObject.register_type()
@OdoConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=("uri",))
class DatabaseTable(OdoDataObject):
    type_name = "db_table"

    real_type = sa.Table

    schemas = ("sqlite", "postgresql", "mysql", "mssql", "oracle", "firebird")

    @classmethod
    def accepts_uri(cls, uri):
        if not uri:
            return False
        for schema in DatabaseTable.schemas:
            if re.match("^{0}(\+.+)?://.+::.+".format(schema), uri):
                return True
        if os.path.isfile(uri) and os.path.splitext(uri)[1] in (".db", ".sqlite", ".sqlite3"):
            return True
        return False

    @property
    def ndim(self):
        return 2

    @property
    def shape(self):
        rows = self.inner_data.count().execute().fetchone()[0]
        cols = len(self.columns)
        return (rows, cols)

    def __getitem__(self, item):
        return self.convert("pandas_data_frame")[item]

    @property
    def columns(self):
        return [col.name for col in self.inner_data.columns.values()]