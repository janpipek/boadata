import csv
import logging
import re
from typing import Optional

from clevercsv.wrappers import csv2df
import pandas as pd

from boadata.core import DataConversion, DataObject
from boadata.core.data_conversion import ChainConversion, IdentityConversion

from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class CSVFile(PandasDataFrameBase):
    type_name = "csv"

    def __to_text__(self, **kwargs) -> "boadata.data.text_types.TextFile":
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return bool(re.search("\\.[tc]sv(\\.gz)?$", uri.lower()))

    @classmethod
    def _fallback_read(cls, uri: str, **kwargs) -> pd.DataFrame:
        with open(uri, "r") as fin:
            lines = [line for line in csv.reader(fin)]
        try:
            return pd.DataFrame(lines[1:], columns=lines[0]).infer_objects(
                # convert_numeric=True
            )
        except:
            return pd.DataFrame(lines).infer_objects() # convert_numeric=True)

    @classmethod
    def from_uri(cls, uri: str, index_col=False, source: Optional[DataObject] = None, **kwargs) -> "CSVFile":
        if not "sep" in kwargs and re.search("\\.tsv(\\.gz)?", uri.lower()):
            kwargs["sep"] = "\\t"

        def _clever_csv_read():
            return csv2df(uri, **kwargs)

        methods = {
            "clevercsv": _clever_csv_read,
            "pandas_c": lambda: pd.read_csv(uri, index_col=index_col, **kwargs),
            "pandas_python": lambda: pd.read_csv(uri, index_col=index_col, engine="python", sep=None, **kwargs),
            "stdlib_csv": lambda: cls._fallback_read(uri, **kwargs),
        }
        result = None
        for name, method in methods.items():
            try:
                data = method()
                result = cls(inner_data=data, uri=uri, source=source, **kwargs)
                logging.debug(f"Used {name} method to parse the CSV file '{uri}'.")
                break
            except:
                pass
        if result:
            if not result.name:
                import os

                result.inner_data.name = os.path.splitext(os.path.basename(uri))[0]
            return result
        raise RuntimeError(
            "No CSV reading method understands the file: {0}".format(uri)
        )
