from ..core import DataObject
from file import register_object_generator
import pandas as pd
import numpy as np

class CsvFile(DataObject):
    def __init__(self, path, node=None):
        super(CsvFile, self).__init__(node)
        self.path = path

    def as_pandas_frame(self):
        return pd.read_csv(self.path)

    def as_numpy_array(self):
        return np.array(self.as_pandas_frame())

    @property
    def title(self):
        return self.path

register_object_generator(".csv", CsvFile)