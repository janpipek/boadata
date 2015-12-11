from ..core import DataObject
from .file import register_object_generator
import pandas as pd
import numpy as np


class CsvFile(DataObject):
    def __init__(self, path, node=None):
        super(CsvFile, self).__init__(node)
        self.path = path

    ndim = 2

    @property
    def shape(self):
        return self.as_numpy_array().shape

    def as_pandas_frame(self):
        kwargs = {}

        # Heuristics to enable Geant4 scoring files
        with open(self.path) as f:
            for line in f:
                if line.startswith("#"):
                    kwargs["skiprows"] = kwargs.get("skiprows", 0) + 1
                    kwargs["header"] = None
                else:
                    break
        return pd.read_csv(self.path, **kwargs)

    def as_numpy_array(self):
        return np.array(self.as_pandas_frame())

    def as_text(self):
        with open(self.path) as f:
            return f.read()

    def __repr__(self):
        return "CsvFile('{0}')".format(self.path)

    @property
    def title(self):
        return self.path


register_object_generator(".csv", CsvFile)