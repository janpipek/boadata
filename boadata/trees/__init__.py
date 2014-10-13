import file
import hdf5

try:
    import excel
except ImportError:
    print "Excel could not be loaded."