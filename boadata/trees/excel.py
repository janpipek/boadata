from boadata.core import DataNode, DataTree
import pandas as pd
import os
import xlrd  # This is used by pandas to import excel


class ExcelSheetNode(DataNode):
    def __init__(self, xls, sheet_name, parent=None):
        super(ExcelSheetNode, self).__init__(parent)
        self.xls = xls
        self.sheet_name = sheet_name

    node_type = "Excel sheet"

    @property
    def title(self):
        return self.sheet_name

    @property
    def data_object(self):
        from boadata.data.excel_types import ExcelSheet
        data = self.xls.parse(self.sheet_name)
        return ExcelSheet(inner_data=data, uri=self.uri)


@DataTree.register_tree
class ExcelFile(DataTree):
    def __init__(self, path, parent=None):
        super(ExcelFile, self).__init__(parent)
        self.path = path
        self.xls = None # Load it lazily

    node_type = "Excel"

    def load_children(self):
        if not self.xls:
            self.xls = pd.ExcelFile(self.path)
        for sheet_name in self.xls.sheet_names:
            self.add_child(ExcelSheetNode(self.xls, sheet_name, self))

    @classmethod
    def accepts_uri(cls, uri):
        if not uri or not os.path.isfile(uri):
            return False
        if os.path.splitext(uri)[1] in [".xls", ".xlsx", ".xlmx"]:
            return True
        return False

    # mime_types = (
    #     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     "application/vnd.ms-excel"
    # )
