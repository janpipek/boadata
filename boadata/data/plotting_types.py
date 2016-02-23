from boadata.core import DataObject
import pandas as pd
import numpy as np
from boadata import unwrap


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


@DataObject.register_type()
class XYPlotDataSeries(XYPlotDataSeriesBase):
    type_name = "xy_dataseries"


#
#
# @DataObject.register_type()
# class XYPlotDataSet(DataObject):
#     type_name = "xy_dataset"
#
#     real_type = pd.DataFrame
