import pandas as pd
import seaborn as sns

from boadata.core import DataObject
from boadata.core.data_conversion import ChainConversion, IdentityConversion

from .pandas_types import PandasDataFrameBase

try:
    import pydataset

    @DataObject.register_type()
    @IdentityConversion.enable_to("pandas_data_frame")
    class PyDataSet(PandasDataFrameBase):
        type_name = "pydataset"

        @classmethod
        def accepts_uri(cls, uri) -> bool:
            if uri[:12] == "pydataset://":
                return True
            else:
                return False

        @classmethod
        def from_uri(cls, uri: str, **kwargs) -> "PyDataSet":
            dataset_name = uri.split("://")[1]
            data = pydataset.data(dataset_name)
            return PyDataSet(inner_data=data, uri=uri)

except:
    pass


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
class SeabornDataSet(PandasDataFrameBase):
    type_name = "seaborn_dataset"

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        if uri.startswith("seaborn://"):
            return True
        else:
            return False

    @classmethod
    def from_uri(cls, uri: str, **kwargs) -> "SeabornDataSet":
        dataset_name = uri.split("://")[1]
        data = sns.load_dataset(dataset_name)
        return cls(inner_data=data, uri=uri)
