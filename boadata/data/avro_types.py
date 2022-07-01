from __future__ import annotations

import re
from contextlib import contextmanager
from typing import List, Optional, Tuple

import fastavro
import pandas as pd

from boadata.core import DataObject
from boadata.core.data_conversion import ChainConversion


@DataObject.register_type()
@DataObject.proxy_methods(
    "select_rows",
    "select_columns",
    "sample_rows",
    "query",
    through="pandas_data_frame",
    same_class=False,
)
@ChainConversion.enable_to("csv", through="pandas_data_frame", pass_kwargs=["uri"])
class AvroFile(DataObject):
    type_name = "avro"

    @contextmanager
    def _get_reader(self):
        with open(self.uri, "rb") as fp:
            reader = fastavro.reader(fp)
            yield reader

    def __to_pandas_data_frame__(self, **kwargs):
        # https://gist.github.com/LouisAmon/300b4a906a6d25a7fb5d2c4d174d242e
        with self._get_reader() as reader:
            records = [r for r in reader]
            # Populate pandas.DataFrame with records

            data_frame_type = DataObject.registered_types["pandas_data_frame"]
            return data_frame_type(
                inner_data=pd.DataFrame.from_records(records), source=self
            )

    @property
    def columns(self) -> Optional[List[str]]:
        with self._get_reader() as reader:
            if reader.schema["type"] == "record":
                return [field["name"] for field in reader.schema["fields"]]
            else:
                return []

    # TODO: Introduce schema

    @classmethod
    def accepts_uri(cls, uri: str) -> bool:
        return bool(re.search("\\.avro$", uri.lower())) and fastavro.is_avro(uri)

    @classmethod
    def from_uri(cls, uri: str) -> AvroFile:
        return AvroFile(uri=uri)

    @property
    def shape(self) -> Tuple[int, ...]:
        with self._get_reader() as reader:
            return len(list(reader)), len(self.columns)
