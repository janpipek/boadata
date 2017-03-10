"""Module containing all data objects understood by boadata."""

from .pandas_types import PandasDataFrame, PandasSeries
from .numpy_types import NumpyArray
from .csv_types import CSVFile
from .json_types import JsonFileDataset
from .text_types import TextFile
from .field_types import VectorFieldMap, FieldTableFile, ComsolFieldTextFile, OperaFieldTextFile
from .sql_types import DatabaseTable
from .plotting_types import XYPlotDataSeries, HistogramData #, XYPlotDataSet
from .xarray_types import XarrayDataArray, XarrayDataset
from .geant4_types import Geant4Scoring

try:
    # Dependence on h5py
    from .hdf5_types import Hdf5Dataset #, Hdf5Table
except:
    pass

try:
    # Dependence on pydataset
    from .pydataset_types import PyDataSet
except:
    pass

try:
    # Dependence on pydons
    from .matlab_types import MatlabFigXYData
except:
    pass

try:
    # Dependence on xlrd...
    from .excel_types import ExcelSheet
except:
    pass

