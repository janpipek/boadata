from .view import View, registered_views
from .property_view import PropertyView
from .xy_plot_view import XYPlotView

try:
    from .table_view import TableView
except:
    pass