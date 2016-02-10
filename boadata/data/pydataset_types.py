import pydataset
import pandas as pd
from boadata.core import DataObject
from boadata.core.data_conversion import IdentityConversion


@DataObject.register_type
@IdentityConversion.enable_to("pandas_data_frame")
class PyDataSet(DataObject):
    type_name = "pydataset"

    real_type = pd.DataFrame

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