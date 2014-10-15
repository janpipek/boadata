from view import View, register_view
import pyqtgraph as pg
import numpy as np
from collections import OrderedDict

class TableView(View):
    title = "Table"

    @classmethod
    def accepts(cls, data_object):
        '''Default variant.'''
        if data_object.converts_to("xy"):
            return True
        if data_object.converts_to("pandas_frame"):
            return True
        if data_object.converts_to("numpy_array"):
            if data_object.ndim <= 2:
                return True
        return False

    @property
    def widget(self):
        if self.data_object.converts_to("xy"):
            data = np.array(self.data_object.to("xy"))
        elif self.data_object.converts_to("pandas_frame"):
            data = []
            df = self.data_object.to("pandas_frame")
            for index, row in df.iterrows():
                data.append(row.to_dict())
            # np.array(self.data_object.to("pandas_frame"))            
        elif self.data_object.converts_to("numpy_array"):
            data = self.data_object.to("numpy_array")
            if data.ndim == 1:
                data = data.reshape(data.shape[0], 1)
        pw = pg.TableWidget()
        pw.setData(data)
        return pw

register_view(TableView)