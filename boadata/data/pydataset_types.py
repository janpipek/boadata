import pydataset
import pandas as pd
from boadata.core import DataObject


@DataObject.register_type
class PyDataSet(DataObject):
    real_type = pd.DataFrame

    @classmethod
    def accepts_uri(cls, uri):
        if uri[:12] == "pydataset://":
            return True
        else:
            return False

    def is_convertible_to(self, new_type_name):    # TODO: Fix this!!!!
        if "field" in new_type_name:
            return False
        return super(PyDataSet, self).is_convertible_to(new_type_name)

    @classmethod
    def from_uri(cls, uri, **kwargs):
        dataset_name = uri.split("://")[1]
        data = pydataset.data(dataset_name)
        return PyDataSet(inner_data=data, uri=uri)