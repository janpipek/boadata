import warnings
from typing import Optional

import pandas as pd

from boadata.core import DataObject
from boadata.core.data_conversion import ChainConversion, IdentityConversion

from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class ParquetFile(PandasDataFrameBase):
    type_name = "parquet"

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return uri[-8:] == ".parquet" or uri[-11:] == ".parquet.gz"

    @classmethod
    def from_uri(
        cls, uri: str, *, source: Optional[DataObject] = None
    ) -> "ParquetFile":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = pd.read_parquet(uri)
        return cls(inner_data=data, uri=uri, source=source)
