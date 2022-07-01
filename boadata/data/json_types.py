import json
import os
from typing import Optional

import pandas as pd

from boadata.core import DataConversion, DataObject
from boadata.core.data_conversion import ChainConversion, IdentityConversion

from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class JsonFileDataset(PandasDataFrameBase):
    type_name = "json"

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return uri and uri.endswith(".json")

    @staticmethod
    def _read_normalized_lines(uri: str, **kwargs) -> pd.DataFrame:
        with open(uri, "r") as infile:
            objects = [json.loads(line) for line in infile if line.strip()]
        normalized_objects = pd.io.json.json_normalize(objects)
        return pd.DataFrame(normalized_objects, **kwargs)

    @staticmethod
    def _read_normalized(uri: str, **kwargs) -> pd.DataFrame:
        with open(uri, "r") as infile:
            objects = json.load(infile)
        normalized_objects = pd.json_normalize(objects)
        return pd.DataFrame(normalized_objects, **kwargs)

    @classmethod
    def from_uri(
        cls,
        uri: str,
        index_col: bool = False,
        source: Optional[DataObject] = None,
        **kwargs
    ) -> "JsonFileDataset":
        methods = [
            lambda: JsonFileDataset._read_normalized(uri, **kwargs),
            lambda: JsonFileDataset._read_normalized_lines(uri, **kwargs),
            lambda: pd.read_json(uri, lines=True, **kwargs),
        ]

        result = None
        for method in methods:
            try:
                data = method()
                result = cls(inner_data=data, uri=uri, source=source, **kwargs)
                break
            except:
                pass

        if result:
            if not result.name:
                result.inner_data.name = os.path.splitext(os.path.basename(uri))[0]
            return result
        raise RuntimeError("No JSON reading method understands the file.")
