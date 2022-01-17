from __future__ import annotations

import os

import pandas as pd

from boadata.core import DataObject
from boadata.data.pandas_types import PandasDataFrameBase


@DataObject.register_type()
class ExcelSheet(PandasDataFrameBase):
    type_name = "excel_sheet"

    EXTENSIONS = [".xls", ".xlsx"]

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        if "::" in uri:
            file, sheet = uri.split("::")
        else:
            file, sheet = uri, None
        file = os.path.abspath(file)
        dir = os.path.dirname(file)
        ext = os.path.splitext(os.path.basename(file))[1].lower()
        return os.path.isdir(dir) and ext in cls.EXTENSIONS

    @classmethod
    def from_uri(cls, uri: str, **kwargs) -> ExcelSheet:
        file, sheet = uri.split("::")
        xls = pd.ExcelFile(file)
        sheet = xls.parse(sheet)
        return cls(inner_data=sheet, uri=uri)
