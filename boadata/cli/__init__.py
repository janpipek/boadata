"""Command-line interface utility functions."""
import contextlib
import signal
import sys
from typing import Dict, List, Optional

from boadata import load


def try_load(uri: str, type: Optional[str] = None, parameters: List[str] = None) -> 'boadata.core.DataObject':
    """Use parameters from command-line to load the data object.

    :param uri: URI of the object
    :param type: Force a type
    :param parameters: collection of "key=value" strings
    """
    parameters = dict([param.split("=", 1) for param in parameters]) if parameters else {}
    do = load(uri, type, **parameters)
    if not do:
        print("URI not understood: {0}").format(uri)
        sys.exit(-1)
    return do


def try_apply_sql(do: 'boadata.core.DataOject', kwargs: dict) -> 'boadata.core.DataObject':
    sql = kwargs.pop("sql", None)
    if sql:
        do = do.sql(sql, table_name="data")
    return do


def try_select_columns(do: 'boadata.core.DataObject', kwargs: dict) -> 'boadata.core.DataObject':
    columns = kwargs.pop("columns", None)
    if columns:
        columns = columns.split(",")
        if not hasattr(do, "select_columns"):
            print("The data object does not support column selection.")
            sys.exit(-1)
        do = do.select_columns(columns)
    return do


def try_select_rows(do: 'boadata.core.DataObject', kwargs: dict) -> 'boadata.core.DataObject':
    lines = kwargs.pop("lines", None)
    if lines:
        indexer = slice(*(int(l) if l else None for l in lines.split(":")))
        do = do.select_rows(indexer)
    return do


def try_sort(do: 'boadata.core.DataObject', kwargs: dict) -> 'boadata.core.DataObject':
    sortby = kwargs.pop("sortby", None)
    if sortby:
        columns = sortby.split(",")
        do = do.sort_by(columns)
    return do


def enable_ctrl_c():
	"""Enable Ctrl-C in the console."""
	signal.signal(signal.SIGINT, signal.SIG_DFL)


@contextlib.contextmanager
def qt_app():
    from boadata.gui import qt  # Force sip
    from qtpy import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    enable_ctrl_c()
    
    try:
        yield app
        sys.exit(app.exec_())
    finally:
        sys.exit(-1)
