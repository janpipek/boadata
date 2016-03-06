from . import file

try:
    # Dependence on h5py
    from . import hdf5
except:
    pass

try:
    # Dependence on pydataset
    from . import pydaset
except:
    pass
from . import sql

try:
    # Dependence on pydons
    from . import matlab
except:
    pass

try:
    from . import excel
except:
    pass
