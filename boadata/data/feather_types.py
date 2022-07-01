from typing import Optional

import feather

from boadata.core import DataObject
from boadata.core.data_conversion import ChainConversion, IdentityConversion

from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class FeatherFile(PandasDataFrameBase):
    type_name = "feather"

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return uri[-8:] == ".feather"

    @classmethod
    def from_uri(
        cls, uri: str, source: Optional[DataObject] = None, **kwargs
    ) -> "FeatherFile":
        data = feather.read_dataframe(uri)
        result = cls(inner_data=data, uri=uri, source=source, **kwargs)
        return result
