from .view import View, register_view
import pyqtgraph as pg
from PyQt4.QtCore import Qt
import numpy as np
import logging


class TableView(View):
    title = "Table"

    # @classmethod
    # def accepts(cls, data_object):
    #     '''Default variant.'''
    #     if data_object.is_convertible_to("xy"):
    #         return True
    #     if data_object.is_convertible_to("pandas_data_frame"):
    #         return True
    #     if data_object.is_convertible_to("numpy_array"):
    #         if data_object.ndim <= 2:
    #             return True
    #     return False

    def create_widget(self):
        if self.data_object.is_convertible_to("pandas_data_frame"):
            df = self.data_object.convert("pandas_data_frame").inner_data
            data = df.to_records(index=False)
            # for index, row in df.iterrows():
            #     data.append(row.to_dict())
            data = data[:1000]
        else:
            raise RuntimeError("Cannot interpret dataobject {0} as DataFrame.".format(self.data_object))
        pw = pg.TableWidget()
        pw.setData(data)
        return pw

register_view(TableView)