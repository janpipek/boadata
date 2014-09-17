from ..core import DataNode, DataObject
from file import register_tree_generator
import pandas as pd


class ExcelSheet(DataNode, DataObject):
    def __init__(self, xls, sheet_name, parent=None):
        super(ExcelSheet, self).__init__(parent)
        self.xls = xls
        self.sheet_name = sheet_name

    @property
    def title(self):
        return self.sheet_name

    def as_pandas_frame(self):
        return self.xls.parse(self.sheet_name)


class ExcelFile(DataNode):
    def __init__(self, path, parent=None):
        super(ExcelFile, self).__init__(parent)
        self.path = path
        self.xls = None # Load it lazily

    def load_children(self):
        if not self.xls:
            self.xls = pd.ExcelFile(self.path)
        for sheet_name in self.xls.sheet_names:
            self.add_child(ExcelSheet(self.xls, sheet_name, self))


register_tree_generator("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ExcelFile)
register_tree_generator("application/vnd.ms-excel", ExcelFile)
