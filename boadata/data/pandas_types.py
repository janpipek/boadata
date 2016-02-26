from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import MethodConversion
from .mixins import GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin
import pandas as pd


class _PandasBase(DataObject, GetItemMixin, StatisticsMixin, NumericalMixin):
    def __to_csv__(self, uri, **kwargs):
        self.inner_data.to_csv(uri)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=uri, source=self)


@DataObject.proxy_methods("head")
class PandasDataFrameBase(_PandasBase):
    real_type = pd.DataFrame

    def hist(self, *args, **kwargs):
        return {col: self[col].hist(*args, **kwargs) for col in self.columns}

    def sql(self, sql, table_name=None):
        """Run SQL query on columns of the table.

        Uses SQLite in-memory storage to create temporary table.
        """
        from sqlalchemy import create_engine
        from boadata import wrap

        if not table_name:
            table_name = self.name
        if not table_name:
            raise RuntimeError("Cannot run SQL queries on unnamed dataframe. Specify table_name argument...")
        engine = create_engine('sqlite:///:memory:')
        self.inner_data.to_sql(table_name, engine)
        # TODO: some clean up???
        return wrap(pd.read_sql_query(sql, engine), source=self)

    def __to_xy_dataseries__(self, x=None, y=None, **kwargs):
        constructor = DataObject.registered_types["xy_dataseries"]
        if not x and not y:
            # Auto from 2 dim
            if len(self.columns) == 1:
                return self[self.columns[0]].convert("xy_dataseries")
            elif len(self.columns) == 2:
                xdata = self[self.columns[0]]
                ydata = self[self.columns[1]]
                xname = xdata.name or "x"
                yname = ydata.name or "y"
            else:
                raise RuntimeError("Cannot convert dataframes with more than 2 columns")
        elif x:
            if not y:
                try:
                    ydata = self.evaluate(x)
                except:
                    ydata = self[x]
                xdata = range(ydata.shape[0])       # TODO: proper index???
                xname = "x"
                yname = x
            else:
                try:
                    xdata = self.evaluate(x)
                except:
                    xdata = self[x]
                try:
                    ydata = self.evaluate(y)
                except:
                    ydata = self[y]
                xname = x
                yname = y
        else:
            raise RuntimeError("Cannot specify col2 and not col1.")
        return constructor(xdata, ydata, xname=kwargs.get("xname", xname), yname=kwargs.get("yname", yname))

    @DataObject.columns.setter
    def columns(self, new_names):
        if (len(new_names) != len(self.columns)):
            raise RuntimeError("Wrong number of columns for renaming")
        self.inner_data.columns = new_names

    def add_column(self, name, expression):
        if name in self.columns:
            raise RuntimeError("Column already exists: {0}".format(name))
        new_column = self.evaluate(expression, wrap=False)
        self.inner_data[name] = new_column

@DataObject.proxy_methods("dropna", "head")
@DataObject.proxy_methods("hist", through="numpy_array")
class PandasSeriesBase(_PandasBase, AsArrayMixin):
    real_type = pd.Series

    @property
    def ndim(self):
        return 1

    def __repr__(self):
        return "{0} (name={1}, shape={2}, dtype={3})".format(self.__class__.__name__,
                                                             self.inner_data.name, self.shape, self.dtype)

    def __to_xy_dataseries__(self, **kwargs):
        constructor = DataObject.registered_types["xy_dataseries"]
        x = range(self.shape[0])     # TODO: Change to proper index
        y = self
        if self.inner_data.name:
            name = self.inner_data.name
        else:
            name = "data"
        return constructor(x, y, xname="#", yname=name)


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
