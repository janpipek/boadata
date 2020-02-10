import os
import re
from typing import List, Tuple

import pandas as pd
import sqlalchemy as sa

from boadata.core.data_conversion import ChainConversion
from boadata.core.data_object import DataObject
from boadata.data.pandas_types import PandasDataFrameBase


@DataObject.register_type()
# @OdoConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=("uri",))
class DatabaseTable(DataObject):
    type_name = "db_table"

    real_type = sa.Table

    schemas = ("sqlite", "postgresql", "mysql", "mssql", "oracle", "firebird")

    # Regular expressions for matching URI
    URI_DB_PART_RE = r"^{0}(\+.+)?://.+"
    URI_RE = URI_DB_PART_RE + "::.+"

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        if not uri:
            return False
        for schema in DatabaseTable.schemas:
            if re.match(cls.URI_RE.format(schema), uri):
                return True
        if os.path.isfile(uri) and os.path.splitext(uri)[1] in (
            ".db",
            ".sqlite",
            ".sqlite3",
        ):
            return True
        return False

    @property
    def ndim(self) -> int:
        return 2

    @property
    def shape(self) -> Tuple[int, int]:
        rows = self.inner_data.count().execute().fetchone()[0]
        cols = len(self.columns)
        return (rows, cols)

    def __getitem__(self, item):
        return self.convert("pandas_data_frame")[item]

    @property
    def columns(self) -> List[str]:
        return [col.name for col in self.inner_data.columns.values()]


@DataObject.register_type()
class DatabaseQuery(PandasDataFrameBase):
    type_name = "db_query"

    URI_RE = "query@" + DatabaseTable.URI_RE

    @classmethod
    def from_uri(cls, uri: str, **kwargs) -> "DatabaseQuery":
        constr, query = uri[6:].split("::", 1)
        con = sa.create_engine(constr)
        inner_data = pd.read_sql_query(query, con)
        return cls(inner_data=inner_data, uri=uri, **kwargs)

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        if not uri:
            return False
        if uri.startswith("query@"):
            return DatabaseTable.accepts_uri(uri[6:])
        else:
            return False
