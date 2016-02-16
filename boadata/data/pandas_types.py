from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import MethodConversion
import pandas as pd


@DataObject.register_type
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
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
    def to_csv(self, uri, **kwargs):
        self.inner_data.to_csv(uri)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=uri, source=self)

    # @DataConversion.register("pandas_data_frame", "numpy_array")
    # def to_numpy_array(self, **kwargs):
    #     data = self.inner_data.as_matrix()
    #     klass = DataObject.registered_types["numpy_array"]
    #     return klass(data, source=self)

    def __getitem__(self, item):
        return PandasSeries(self.inner_data[item], source=self)


@DataObject.register_type
class PandasSeries(DataObject):
    type_name = "pandas_series"

    real_type = pd.Series

    @property
    def ndim(self):
        return 1

    @DataConversion.register("pandas_series", "numpy_array")
    def to_numpy_array(self, **kwargs):
        data = self.inner_data.as_matrix()
        klass = DataObject.registered_types["numpy_array"]
        return klass(data, source=self)

    @DataConversion.register("pandas_series", "csv")
    def to_csv(self, path, **kwargs):
        self.inner_data.to_csv(path)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=path, source=self)
