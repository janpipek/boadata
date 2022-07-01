import re

import datadotworld as dw

from boadata.core import DataObject
from boadata.core.data_conversion import ChainConversion

from .pandas_types import PandasDataFrameBase


@ChainConversion.enable_from(
    "csv", through="pandas_data_frame", pass_kwargs=["user", "dataset", "table"]
)
@DataObject.register_type()
class DataDotWorldTable(PandasDataFrameBase):
    type_name = "dw_table"

    URI_RE = re.compile(r"dw://(\w|\-)+/(\w|\-)+/(\w|\-)+$")

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return re.match(DataDotWorldTable.URI_RE, uri) is not None

    @classmethod
    def from_uri(cls, uri: str, **kwargs) -> "DataDotWorldTable":
        dataset_name = "/".join(uri.split("/")[2:-1])
        dataset = dw.load_dataset(dataset_name)
        df = dataset.dataframes[uri.split("/")[-1]]
        return cls(inner_data=df, uri=uri, **kwargs)

    @classmethod
    def __from_pandas_data_frame__(
        cls, df: PandasDataFrameBase, user: str, dataset: str, table: str
    ) -> "DataDotWorldTable":
        with dw.open_remote_file(
            "{0}/{1}".format(user, dataset), "{0}.csv".format(table)
        ) as w:
            print(df.inner_data)
            df.inner_data.to_csv(w, index=False)
        uri = "dw://{0}/{1}/{2}".format(user, dataset, table)
        return DataDotWorldTable.from_uri(uri, source=df)
