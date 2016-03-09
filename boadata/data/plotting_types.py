from boadata.core import DataObject
import pandas as pd
import numpy as np
from boadata import unwrap
import numbers


class XYPlotDataSeriesBase(DataObject):
    def __init__(self, x, y, xname="x", yname="y", **kwargs):
        super(XYPlotDataSeriesBase, self).__init__(inner_data=[np.array(unwrap(x)), np.array(unwrap(y))], **kwargs)
        self.xname = xname
        self.yname = yname

    @property
    def x(self):
        return self.inner_data[0]

    @property
    def y(self):
        return self.inner_data[1]

    @property
    def columns(self):
        return (self.xname, self.yname)

    def __repr__(self):
        return "{0}({1} -> {2}, length={3})".format(self.__class__.__name__, self.xname, self.yname, len(self.x))

    def __to_xy_dataseries__(self, **kwargs):
        return XYPlotDataSeries(x=self.x, y=self.y, xname=self.xname, yname=self.yname, source=self)

    def __to_pandas_data_frame__(self, **kwargs):
        data = pd.DataFrame()
        data[self.xname] = self.inner_data[0]
        data[self.yname] = self.inner_data[1]
        klass = DataObject.registered_types["pandas_data_frame"]
        return klass(inner_data=data, source=self)

    @property
    def shape(self):
        return (len(self.x), 2)


@DataObject.register_type()
class XYPlotDataSeries(XYPlotDataSeriesBase):
    type_name = "xy_dataseries"


@DataObject.register_type()
class HistogramData(XYPlotDataSeriesBase):
    type_name = "histogram"

    def __init__(self, bins, values=[], total=None, overflow=0, underflow=0, **kwargs):
        assert len(values) == len(bins) - 1
        super(HistogramData, self).__init__(bins, values, **kwargs)
        if total is not None:
            self.total = total
        else:
            self.total = self.total_weight
        self.overflow = overflow
        self.underflow = underflow

    @property
    def bins(self):
        return self.inner_data[0]

    @property
    def left_edges(self):
        return self.bins[:-1]

    @property
    def right_edges(self):
        return self.bins[1:]

    @property
    def bin_widths(self):
        return self.right_edges - self.left_edges

    @property
    def values(self):
        return self.inner_data[1]

    @property
    def x(self):
        """Centers of the bins (to satisfy XY API)."""
        return 0.5 * (self.left_edges + self.right_edges)

    @property
    def y(self):
        """Heights of the boxes (to satisfy XY API)."""
        return self.values

    @property
    def total_weight(self):
        return self.values.sum()

    def fill(self, value, weight = 1.0):
        """Add a value to the histogram."""
        # TODO: Enable arrays
        bin = np.searchsorted(self.bins, value, side='right')
        if bin == 0:
            self.underflow += 1
            return    # Under
        elif bin == len(self.bins):
            self.overflow += 1
            return
        else:
            self.values[bin - 1] += weight
            self.total += 1
            return bin - 1

    def normalize(self, total_weight=1.0, inplace=False):
        """Normalize the histogram so that the total weight=1.0.

        :param total_weight: What will be the new total weight (default=1)
        :param inplace: True => Update this histogram (and return it), False => return a copy
        """
        factor = (total_weight / self.total_weight)
        if inplace:
            self *= factor
            return self
        else:
            return self * factor            

    def __mul__(self, other):
        if not isinstance(other, numbers.Real):
            raise RuntimeError("Cannot multiply by unreal numbers")
        new_values = self.values * other
        return HistogramData(bins=self.bins, values=new_values, total=self.total, overflow=self.overflow, underflow=self.underflow, source=self)

    def __imul__(self, other):
        if not isinstance(other, numbers.Real):
            raise RuntimeError("Cannot multiply by unreal numbers")
        self.inner_data[1] = self.values * other
        return self

    def __truediv__(self, other):
        return self * (1 / other)

    def __itruediv__(self, other):
        self *= 1 / other
        return self

    def __repr__(self):
        return "{0}(bins={1}, total={2}, overflow={3}, overflow={4})".format(
            self.__class__.__name__, len(self.bins) - 1, self.total, self.underflow, self.overflow)
