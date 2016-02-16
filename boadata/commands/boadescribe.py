from boadata.core import DataObject
import sys


def run_app():
    uri = sys.argv[1]
    do = DataObject.from_uri(uri)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    print("Type: {0}".format(do.type_name))
    print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
    print("Data shape: {0}".format(do.shape))
    columns = do.columns
    if columns:
        print("Column names: {0}".format(", ".join(columns)))
