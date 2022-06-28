"""Command-line interface utility functions."""
from __future__ import annotations
import signal
import sys
from typing import TYPE_CHECKING

from tabulate import tabulate

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


def try_apply_sql(do: DataObject, sql: Optional[str]) -> DataObject:
    if sql:
        do = do.sql(sql, table_name="data")
    return do


def try_filter(do: DataObject, filter: Optional[str]) -> DataObject:
    if filter:
        do = do.query(filter)
    return do


def try_select_columns(do: DataObject, columns: Optional[List[str]]) -> DataObject:
    if columns:
        if not hasattr(do, "select_columns"):
            print("The data object does not support column selection.")
            sys.exit(-1)
        do = do.select_columns(columns)
    return do


def try_select_rows(do: DataObject, lines: Optional[str], sample: Optional[int]) -> DataObject:
    if lines is not None:
        indexer = slice(*(int(l) if l else None for l in lines.split(":")))
        do = do.select_rows(indexer)
    if sample is not None:
        do = do.sample_rows(sample)
    return do


def try_sort(do: DataObject, sortby: Optional[str]) -> DataObject:
    if sortby:
        columns = sortby.split(",")
        do = do.sort_by(columns)
    return do


def enable_ctrl_c():
	"""Enable Ctrl-C in the console."""
	signal.signal(signal.SIGINT, signal.SIG_DFL)


def show_table(do: DataObject):
    print(tabulate(do.inner_data, do.columns, tablefmt="orgtbl", showindex=False, missingval="?"))


def show_expanded(do: DataObject):
    try:
        # TODO: Rewrite in terms of typer
        import colorama
        highlight = colorama.Fore.LIGHTGREEN_EX
        normal = colorama.Fore.LIGHTBLUE_EX
        reset = colorama.Fore.RESET
    except ImportError:
        highlight = ""
        normal = ""
        reset = ""

    for i in range(do.shape[0]):
        for column in do.columns:
            value = do.inner_data.iloc[i][column]
            line = (normal + str(column) + reset + ": " + highlight + str(value) + reset)
            print(line)
        print("--------------------------------- " + str(i))
