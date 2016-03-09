from boadata.core import DataObject
from .pandas_types import PandasDataFrameBase
import pandas as pd
import xlrd


@DataObject.register_type()
class ExcelSheet(PandasDataFrameBase):
    type_name = "excel_sheet"

    @classmethod
    def from_uri(cls, uri, **kwargs):
        file, sheet = uri.split("::")
        xls = pd.ExcelFile(file)
        sheet = xls.parse(sheet)
        return cls(inner_data=sheet, uri=uri)
