from boadata.core import DataObject
import pandas as pd


@DataObject.register_type
class PandasDataFrame(DataObject):
    type_name = "pandas_data_frame"

    real_type = pd.DataFrame

    @property
    def shape(self):
        return self.inner_data.shape

    @property
    def ndim(self):
        return 2
