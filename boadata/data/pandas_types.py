from boadata.core import DataObject
from boadata.core.data_conversion import MethodConversion, DataConversion
from .mixins import GetItemMixin, StatisticsMixin, NumericalMixin, AsArrayMixin, CopyableMixin
import pandas as pd
import numpy as np
import types
from .. import wrap


class _PandasBase(DataObject, GetItemMixin, StatisticsMixin, NumericalMixin, CopyableMixin):
    """Shared behaviour for all pandas-based types.

    These include Series and DataFrame based types.
    """
    def __to_csv__(self, uri, **kwargs):
        self.inner_data.to_csv(uri, **kwargs)
        klass = DataObject.registered_types["csv"]
        return klass.from_uri(uri=uri, source=self)


@DataObject.proxy_methods("head")
class PandasDataFrameBase(_PandasBase):
    real_type = pd.DataFrame

    def histogram(self, bins=None, columns=None, weights=None, **kwargs):
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

    def drop_columns(self, columns, allow_nonexistent=False):
        if isinstance(columns, str):
            columns = [columns]
        if allow_nonexistent:
            columns = [column for column in columns if column in self.columns]
        self.inner_data.drop(columns, axis=1, inplace=True)

    def rename_columns(self, col_dict):
        """Change columns names.

        :param col_dict: New names
        :type col_dict: list | dict

        If col_dict is a dict, it is used as a mapping (non-matching ignored)
        If col_dict is a list, all columns are renamed to this (size checked)
        """
        if isinstance(col_dict, list):
            if len(col_dict) != len(self.columns):
                raise RuntimeError("Invalid number of columns to rename")
            new_names = col_dict
        elif isinstance(col_dict, dict):
            new_names = [col_dict.get(col, col) for col in self.columns]
        elif isinstance(col_dict, types.FunctionType):
            new_names = [col_dict(col) for col in self.columns]
        else:
            raise RuntimeError("Column names not understood.")
        self.inner_data.columns = new_names

    def reorder_columns(self, cols):
        # TODO: Can there be duplicates in DataFrame? Perhaps not
        if not set(cols) == set(self.columns):
            raise RuntimeError("The new ordering of columns must be complete. {0} is not {1}"
                               .format(set(cols), set(self.columns)))
        self.inner_data = self.inner_data[cols]

    def add_column(self, expression, name=None):
        if name in self.columns:
            raise RuntimeError("Column already exists: {0}".format(name))
        self._create_column(expression, name)

    def _create_column(self, expression, name=None):
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

    def replace_column(self, name, expression):
        if name not in self.columns:
            raise IndexError("The column {0} does not exist".format(name))
        self._create_column(expression, name)

    def dropna(self, **kwargs):
        kwargs["inplace"] = True
        self.inner_data.dropna(**kwargs)

    def append(self, other, **kwargs):
        other = wrap(other)
        if not isinstance(other, PandasDataFrameBase):
            try:
                other = other.convert("pandas_data_frame")
            except:
                raise TypeError("Only dataframes may be appended to dataframes.")
        if self.columns:
            if other.columns:
                if not other.columns == self.columns:
                    raise RuntimeError("Both dataframes must have same column names")
            if not np.all(other.inner_data.dtypes == self.inner_data.dtypes):
                raise RuntimeError("Both dataframes must have same column dtypes.")
        self.inner_data = self.inner_data.append(other.inner_data, **kwargs)


@DataObject.proxy_methods("dropna", "head")
@DataObject.proxy_methods("histogram", through="numpy_array")
@DataObject.proxy_methods("abs")
class PandasSeriesBase(_PandasBase, AsArrayMixin):
    """Abstract class for all types based on pandas Series"""

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
            name = self.name or "Data"
        df = pd.DataFrame()
        df[name] = self.inner_data
        return DataObject.from_native(df, source=self)

    def mode(self):
        """Mode interpreted as in scipy.mode"""
        result = self.inner_data.mode()
        return result.min()


@DataObject.register_type(default=True)
@MethodConversion.enable_to("numpy_array", method_name="as_matrix")
class PandasDataFrame(PandasDataFrameBase):
    type_name = "pandas_data_frame"

    def __init__(self, inner_data=None, *args, **kwargs):
        if inner_data is None:
            inner_data = pd.DataFrame()
        super(PandasDataFrame, self).__init__(inner_data, *args, **kwargs)

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
