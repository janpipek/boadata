from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import MethodConversion
from .mixins import GetItemMixin, StatisticsMixin
import pandas as pd


class PandasDataFrameBase(DataObject, GetItemMixin, StatisticsMixin):
    real_type = pd.DataFrame

    def __to_csv__(self, uri, **kwargs):
        self.inner_data.to_csv(uri)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=uri, source=self)


class PandasSeriesBase(DataObject, GetItemMixin, StatisticsMixin):
    real_type = pd.Series

    @property
    def ndim(self):
        return 1

    def __to_csv__(self, path, **kwargs):
        self.inner_data.to_csv(path)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=path, source=self)


@DataObject.register_type(default=True)
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
class PandasDataFrame(PandasDataFrameBase):
    type_name = "pandas_data_frame"


@DataObject.register_type(default=True)
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
class PandasSeries(PandasSeriesBase):
    type_name = "pandas_series"

    real_type = pd.Series

    @property
    def ndim(self):
        return 1

    def __to_csv__(self, path, **kwargs):
        self.inner_data.to_csv(path)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=path, source=self)
