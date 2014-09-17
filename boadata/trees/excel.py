from ..core import DataNode, DataObject
from file import register_tree_generator
import pandas as pd
import numpy as np

class ExcelSheetObject(DataObject):
    def __init__(self, xls, sheet_name, node=None):
        super(ExcelSheetObject, self).__init__(node)
        self.xls = xls
        self.sheet_name = sheet_name

    def as_pandas_frame(self):
        try:
            return self.xls.parse(self.sheet_name)
        except:
            return pd.DataFrame()

    def as_numpy_array(self):
        return np.array(self.as_pandas_frame())

    @property
    def shape(self):
        df = self.as_pandas_frame()
        return df.shape

class ExcelSheetNode(DataNode):
    def __init__(self, xls, sheet_name, parent=None):
        super(ExcelSheetNode, self).__init__(parent)
        self.xls = xls
        self.sheet_name = sheet_name

    @property
    def title(self):
        return self.sheet_name

    def create_data_object(self):
        return ExcelSheetObject(self.xls, self.sheet_name, self)


class ExcelFile(DataNode):
    def __init__(self, path, parent=None):
        super(ExcelFile, self).__init__(parent)
        self.path = path
        self.xls = None # Load it lazily

    def load_children(self):
        if not self.xls:
            self.xls = pd.ExcelFile(self.path)
        for sheet_name in self.xls.sheet_names:
            self.add_child(ExcelSheetNode(self.xls, sheet_name, self))


register_tree_generator("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ExcelFile)
register_tree_generator("application/vnd.ms-excel", ExcelFile)