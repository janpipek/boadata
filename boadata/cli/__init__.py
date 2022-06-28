"""Command-line interface utility functions."""
from __future__ import annotations
import contextlib
import signal
import sys
from typing import Dict, TYPE_CHECKING

from boadata import load

if TYPE_CHECKING:
    from typing import List, Optional

    from boadata.core import DataObject


def try_load(uri: str, type: Optional[str] = None, parameters: List[str] = None) -> DataObject:
    """Use parameters from command-line to load the data object.

    :param uri: URI of the object
    :param type: Force a type
    :param parameters: collection of "key=value" strings
    """
    kwargs = dict([param.split("=", 1) for param in parameters]) if parameters else {}
    do = load(uri, type, **kwargs)
    if not do:
        raise RuntimeError(f"URI not understood: {uri}")
    return do


def try_apply_sql(do: DataObject, kwargs: dict) -> DataObject:
    sql = kwargs.pop("sql", None)
    if sql:
        do = do.sql(sql, table_name="data")
    return do

def try_filter(do: DataObject, kwargs: dict) -> DataObject:
    query = kwargs.pop("filter", None)
    if query:
        do = do.query(query)
    return do


def try_select_columns(do: DataObject, kwargs: dict) -> DataObject:
    columns = kwargs.pop("columns", None)
    if columns:
        columns = columns.split(",")
        if not hasattr(do, "select_columns"):
            print("The data object does not support column selection.")
            sys.exit(-1)
        do = do.select_columns(columns)
    return do


def try_select_rows(do: DataObject, kwargs: dict) -> DataObject:
    lines = kwargs.pop("lines", None)
    sample = kwargs.pop("sample", None)
    if lines:
        indexer = slice(*(int(l) if l else None for l in lines.split(":")))
        do = do.select_rows(indexer)
    if sample:
        do = do.sample_rows(sample)
    return do


def try_sort(do: DataObject, kwargs: dict) -> DataObject:
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
