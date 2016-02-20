import pandas as pd
from boadata.core import DataObject
from boadata.core.data_conversion import IdentityConversion, ChainConversion
from .pandas_types import PandasDataFrameBase
import seaborn as sns

try:
    import pydataset
    @DataObject.register_type()
    @IdentityConversion.enable_to("pandas_data_frame")
    class PyDataSet(PandasDataFrameBase):
        type_name = "pydataset"

        @classmethod
        def accepts_uri(cls, uri):
            if uri[:12] == "pydataset://":
                return True
            else:
                return False

        @classmethod
        def from_uri(cls, uri, **kwargs):
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
    def accepts_uri(cls, uri):
        if uri.startswith("seaborn://"):
            return True
        else:
            return False

    @classmethod
    def from_uri(cls, uri, **kwargs):
        dataset_name = uri.split("://")[1]
        data = sns.load_dataset(dataset_name)
        return cls(inner_data=data, uri=uri)