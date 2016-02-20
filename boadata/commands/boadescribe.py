from boadata import load
import sys
import click


@click.command()
@click.argument("uri")
@click.option("-t", "--type", default=None, help="What type is the object.")
def run_app(uri, type, **kwargs):
    do = load(uri, type)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    print("Type: {0}".format(do.type_name))
    print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
    print("Data shape: {0}".format(do.shape))
    columns = do.columns
    if columns:
        print("Columns:")
        for name in columns:
            s = "  - {0}".format(name)
            try:
                s += " (dtype={0})".format(do[name].dtype)
            except:
                pass
            print(s)
