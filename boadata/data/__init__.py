"""Module containing all data objects understood by boadata."""

from .csv_types import CSVFile
from .field_types import (
    ComsolFieldTextFile,
    FieldTableFile,
    OperaFieldTextFile,
    VectorFieldMap,
)
from .geant4_types import Geant4Scoring
from .json_types import JsonFileDataset
from .numpy_types import NumpyArray
from .pandas_types import PandasDataFrame, PandasSeries
from .plotting_types import HistogramData, XYPlotDataSeries  # , XYPlotDataSet
from .sql_types import DatabaseTable
from .text_types import TextFile
from .xarray_types import XarrayDataArray, XarrayDataset


try:
    from .dw_types import DataWorldTable
except ImportError:
    pass

try:
    # Dependence on h5py
    from .hdf5_types import Hdf5Dataset  # , Hdf5Table
except ImportError:
    pass

try:
    # Dependence on pydataset
    from .pydataset_types import PyDataSet
except ImportError:
    pass

try:
    # Dependence on pydons
    from .matlab_types import MatlabFigXYData
except ImportError:
    pass

try:
    # Dependence on xlrd...
    from .excel_types import ExcelSheet
except ImportError:
    pass

try:
    # Dependence on feather
    from .feather_types import FeatherFile
except ImportError:
    pass


try:
    from .parquet_types import ParquetFile
except ImportError:
    pass


try:
    from .avro_types import AvroFile
except ImportError:
    pass
