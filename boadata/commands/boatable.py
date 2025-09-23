from typing import List, Optional

import polars as pl
import typer
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual_fastdatatable import DataTable
from textual_fastdatatable.backend import PolarsBackend

from boadata.cli import (
    try_apply_sql,
    try_load,
    try_query,
    try_select_columns,
    try_select_rows,
    try_sort,
)
from boadata.core import DataObject

run_app = typer.Typer()


@run_app.command()
def main(
    uri: str,
    type: Optional[str] = typer.Option(None, help="The type of the object."),
    columns: Optional[List[str]] = typer.Option(
        None, "--column", "-c", help="List of columns to show"
    ),
    query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Query to run (as in pandas query)"
    ),
    sql: Optional[str] = typer.Option(None, help="SQL to run on the object."),
    sortby: Optional[str] = typer.Option(None, help="Sort by column(s)."),
    expand: bool = typer.Option(
        False, "--expand", "-x", help="Show each row expanded."
    ),
    lines: Optional[str] = typer.Option(None, "--lines", "-l", help="Lines (as range)"),
    limit: Optional[int] = typer.Option(None, help="Maximum number of lines to show"),
    sample: Optional[int] = typer.Option(
        None, help="Sample a number of lines randomly"
    ),
    parameter: Optional[List[str]] = typer.Option(
        None,
        "--param",
        "-p",
        help="Additional parameters for loader, specified as key=value",
    ),
):
    do = try_load(uri, type=type, parameters=parameter)
    do = try_apply_sql(do, sql=sql)
    do = try_query(do, query=query)
    do = try_select_columns(do, columns=columns)
    do = try_sort(do, sortby=sortby)
    do = try_select_rows(do, lines=lines, sample=sample)

    do = do.convert("pandas_data_frame")
    if limit and do.shape[0] > limit:
        typer.echo(
            f"The row count is higher than the limit ({do.shape[0]}), dropping lines after that..."
        )
        do = do.head(limit)

    TableApp(do=do, uri=uri).run()  # title=uri, log="textual.log", do=do, uri=uri)


class TableApp(App):
    do: DataObject
    uri: str
    df: pl.DataFrame

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self, *, do: DataObject, uri: str, **kwargs):
        super().__init__(**kwargs)
        self.do = do
        self.uri = uri
        self.df = pl.DataFrame(do.inner_data)
        self.title = f"{self.uri} ({self.df.shape[0]} rows)"

    def compose(self) -> ComposeResult:
        backend = PolarsBackend.from_dataframe(self.df)
        yield Header()
        yield DataTable(backend=backend, zebra_stripes=True)
        yield Footer()
