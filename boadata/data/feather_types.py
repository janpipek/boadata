import feather

from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import IdentityConversion, ChainConversion
from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class FeatherFile(PandasDataFrameBase):
    type_name = "feather"

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-8:] == ".feather"

    @classmethod
    def from_uri(cls, uri, source=None, **kwargs):
        data = feather.read_dataframe(uri)
        result = cls(inner_data=data, uri=uri, source=source, **kwargs)
        return result
