import file
import hdf5

try:
    import excel
except ImportError:
    print "Excel could not be loaded."

try:
    import sql
except ImportError:
    print "SQL could not be loaded."