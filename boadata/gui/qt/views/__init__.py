from .view import View

from .text_view import TextView
from .table_view import TableView
from .field_view import FieldView
from .plot_view import PlotView

try:
    from .pandas_summary import PandasSummaryView
except:
    pass