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


#
#
# @DataObject.register_type()
# class XYPlotDataSet(DataObject):
#     type_name = "xy_dataset"
#
#     real_type = pd.DataFrame
