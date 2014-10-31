import file
import logging

try:
    import hdf5
except:
    logging.warning("HDF5 could not be loaded.")

try:
    import excel
except ImportError:
    logging.warning("Excel could not be loaded.")

try:
    import sql
except ImportError:
    logging.warning("SQL could not be loaded.")

try:
    import csv
except ImportError:
    logging.warning("CSV could not be loaded.")