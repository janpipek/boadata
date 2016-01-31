from boadata.core import DataObject
import sys
import odo


def run_app():
    uri = sys.argv[1]
    try:
        do = DataObject.from_uri(uri)
        print("Type: {0}".format(do.type_name))
        print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
        print("Data shape: {0}".format(do.shape))
        columns = do.columns
        if columns:
            print("Column names: {0}".format(", ".join(columns)))
    except:
        print("URI not understood.")