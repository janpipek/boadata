from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import MethodConversion
from .mixins import GetItemMixin, StatisticsMixin, NumericalMixin
import pandas as pd


class _PandasBase(DataObject, GetItemMixin, StatisticsMixin, NumericalMixin):
    def __to_csv__(self, uri, **kwargs):
        self.inner_data.to_csv(uri)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=uri, source=self)


class PandasDataFrameBase(_PandasBase):
    real_type = pd.DataFrame

    def hist(self, *args, **kwargs):
        return {col: self[col].hist(*args, **kwargs) for col in self.columns}


@DataObject.proxy_methods("dropna")
@DataObject.proxy_methods("hist", through="numpy_array")
class PandasSeriesBase(_PandasBase):
    real_type = pd.Series

    @property
    def ndim(self):
        return 1

    def __repr__(self):
        return "{0} (name={1}, shape={2}, dtype={3})".format(self.__class__.__name__,
                                                             self.inner_data.name, self.shape, self.dtype)


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
