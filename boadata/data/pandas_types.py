from boadata.core import DataObject
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

    def histogram(self, bins, columns=None, weights=None, **kwargs):
        """Histogram data on all numeric columns.

        :param bins: number of bins or edges (numpy-like)
        :param weights: as in numpy.histogram, but can be a column name as well

        kwargs
        ------
        - dropna: don't include nan values (these make zero values)
        - range: as in numpy.histogram

        In contrast to pandas hist method, this does not show the histogram.
        """
        if not columns:
            # All numeric
            columns = [col for col in self.columns if self.inner_data[col].dtype.kind in "iuf"]
        if isinstance(columns, str):
            columns = [columns]
        if isinstance(weights, str):
            columns = [col for col in columns if col != weights]
        weights = self[weights]
        return {col: self[col].histogram(bins=bins, weights=weights, **kwargs) for col in columns}

    def sql(self, sql, table_name=None):
        """Run SQL query on columns of the table.

        :param table_name: name of the temporary table (default is the name of the dataframe)

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

    def __to_pandas_data_frame__(self):
        return PandasDataFrame(inner_data=self.inner_data, source=self)

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

    def __to_excel_sheet__(self, uri):
        if "::" in uri:
            file, sheet = uri.split("::")
        else:
            file = uri
            sheet = self.name or "Unknown"
        self.inner_data.to_excel(file, sheet)
        uri = "{0}::{1}".format(file, sheet)
        klass = DataObject.registered_types.get("excel_sheet")
        return klass.from_uri(uri=uri, source=self)

    def rename_columns(self, col_dict):
        new_names = [col_dict.get(col, col) for col in self.columns]
        self.inner_data.columns = new_names

    def add_column(self, expression, name=None):
        if name in self.columns:
            raise RuntimeError("Column already exists: {0}".format(name))
        if isinstance(expression, str):
            new_column = self.evaluate(expression, wrap=False)
            if not name:
                name = expression
        elif isinstance(expression, PandasSeriesBase):
            new_column = expression.inner_data
            if not name:
                name = new_column.name
        elif isinstance(expression, pd.Series):
            new_column = expression
            if not name:
                name = new_column.name
        self.inner_data[name] = new_column


@DataObject.proxy_methods("dropna", "head")
@DataObject.proxy_methods("histogram", through="numpy_array")
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

    def __to_pandas_data_frame__(self, name=None):
        if not name:
            name = self.name = "Data"
        df = pd.DataFrame()
        df[name] = self.inner_data
        return DataObject.from_native(df, source=self)

@DataObject.register_type(default=True)
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
class PandasDataFrame(PandasDataFrameBase):
    type_name = "pandas_data_frame"

    def __repr__(self):
        return "{0} (name={1}, shape={2})".format(self.__class__.__name__, self.name, self.shape)


@DataObject.register_type(default=True)
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
class PandasSeries(PandasSeriesBase):
    type_name = "pandas_series"

    real_type = pd.Series

    @property
    def ndim(self):
        return 1
