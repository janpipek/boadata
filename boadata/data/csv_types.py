from boadata.core import DataObject, DataConversion
from boadata.core.data_conversion import IdentityConversion, ChainConversion
import pandas as pd
import odo
from .pandas_types import PandasDataFrameBase


@DataObject.register_type()
@IdentityConversion.enable_to("pandas_data_frame")
@ChainConversion.enable_to("numpy_array", through="pandas_data_frame")
class CSVFile(PandasDataFrameBase):
    type_name = "csv"

    def __to_text__(self, **kwargs):
        constructor = DataObject.registered_types["text"]
        return constructor.from_uri(self.uri, source=self, **kwargs)

    @classmethod
    def accepts_uri(cls, uri):
        return uri[-4:] == ".csv"

    @classmethod
    def _fallback_read(cls, uri, **kwargs):
        import csv
        with open(uri, "r") as fin:
            lines = [line for line in csv.reader(fin)]
        try:
            return pd.DataFrame(lines[1:], columns=lines[0]).convert_objects(convert_numeric=True)
        except:
            return pd.DataFrame(lines).convert_objects(convert_numeric=True)

    @classmethod
    def from_uri(cls, uri, index_col=False, source=None, **kwargs):
        #resource = odo.resource(uri)
        #if hasattr(resource, "dialect"):
        #    kwargs.update(resource.dialect)

        methods = [
            # lambda: pd.read_csv(uri, index_col=index_col, parse_dates=[0], **kwargs),
            lambda: pd.read_csv(uri, index_col=index_col, delimiter=",\s*", engine="python", **kwargs),
            lambda: pd.read_csv(uri, index_col=index_col, delimiter=None, engine="python", **kwargs),
            lambda: pd.read_csv(uri, index_col=index_col, delim_whitespace=True, **kwargs),
            lambda: pd.read_csv(uri, index_col=index_col, **kwargs),
            lambda: odo.odo(uri, pd.DataFrame, index_col=index_col, **kwargs),
            lambda: cls._fallback_read(uri, **kwargs)
        ]
        result = None
        for method in methods:
            try:
                data = method()
                result = cls(inner_data=data, uri=uri, source=source, **kwargs)
                if result.shape[1] != 1:
                    break
            except BaseException as ex:
                print(ex)
                pass
        if result:
            if not result.name:
                import os
                result.inner_data.name = os.path.splitext(os.path.basename(uri))[0]
            return result
        raise RuntimeError("No CSV reading method understands the file: {0}".format(uri))
