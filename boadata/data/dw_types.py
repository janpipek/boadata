import re

import datadotworld as dw

from .pandas_types import PandasDataFrameBase
from boadata.core import DataObject


@DataObject.register_type()
class DataDotWorldTable(PandasDataFrameBase):
    type_name = "dw_table"

    _re = re.compile("dw://(\\w|\-)+/(\\w|\-)+/(\\w|\-)+$")

    @classmethod
    def accepts_uri(cls, uri):
        # print(type(uri))
        return re.match(DataDotWorldTable._re, uri) is not None

    @classmethod
    def from_uri(cls, uri, **kwargs):
        print("dsuir", uri)
        dataset_name = "/".join(uri.split("/")[2:-1])
        print("dsload", dataset_name)
        dataset = dw.load_dataset(dataset_name)
        df = dataset.dataframes[uri.split("/")[-1]]
        return cls(inner_data=df, uri=uri)

