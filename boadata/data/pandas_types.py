from boadata.core import DataObject, DataConversion
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

    @DataConversion.register("pandas_data_frame", "csv")
    def to_csv(self, path, **args):
        self.inner_data.to_csv(path)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=path, source=self)


@DataObject.register_type
class PandasSeries(DataObject):
    type_name = "pandas_series"

    real_type = pd.Series

    @property
    def ndim(self):
        return 1
