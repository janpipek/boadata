# TODO: As object

from ..core import DataObject
import pandas as pd
import numpy as np
from ..core.data_types import Field

class FieldTableFile(DataObject):
    def __init__(self, path, node=None):
        super(FieldTableFile, self).__init__(node)
        self.path = path
        self.reduce_factor = 1

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def shape(self):
        return self.as_field().data.shape

    def as_text(self):
        with open(self.path) as f:
            return f.read()

    def as_field(self):
        data = pd.read_table(self.path, names=["x", "y", "z", "Bx", "By", "Bz"], index_col=False, delim_whitespace=True, skiprows=2)
        field = Field(data)
        if self.reduce_factor > 1:
            field = field.simple_reduce(self.reduce_factor)
        return field

    def __repr__(self):
        return "FieldTableFile('{0}')".format(self.path)

    @property
    def title(self):
        return self.path


register_object_generator(".TABLE", FieldTableFile)