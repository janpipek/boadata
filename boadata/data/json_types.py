from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import IdentityConversion, ChainConversion
import pandas as pd
import odo
from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class JsonFileDataset(PandasDataFrameBase):
    type_name = "json"

    @classmethod
    def accepts_uri(cls, uri):
        return uri and uri.endswith(".json")

    @classmethod
    def from_uri(cls, uri, index_col=False, source=None, **kwargs):
        resource = odo.resource(uri)
        methods = [
            lambda: odo.odo(uri, pd.DataFrame, index_col=index_col, **kwargs),
            lambda: pd.read_json(uri, **kwargs)
        ]
        for method in methods:
            try:
                data = method()
                result = cls(inner_data=data, uri=uri, source=source, **kwargs)
                break
            except:
                pass
        if result:
            if not result.name:
                import os
                result.inner_data.name = os.path.splitext(os.path.basename(uri))[0]
            return result
        raise RuntimeError("No JSON reading method understands the file.")    

