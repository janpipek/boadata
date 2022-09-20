from typing import List, Optional

import pandas as pd
import typer
from rich.table import Table
from textual import events
from textual.app import App
from textual.scrollbar import ScrollTo
from textual.widgets import ScrollView

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

    TableApp.run(title=uri, log="textual.log", do=do, uri=uri)


class TableApp(App):
    # Inspired by https://github.com/Textualize/textual/blob/main/examples/big_table.py

    body: ScrollView

    do: DataObject

    uri: str

    @property
    def df(self) -> pd.DataFrame:
        return self.do.inner_data

    def __init__(self, *args, do: DataObject, uri: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.do = do
        self.uri = uri

    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_key(self, event):
        if event.key in ["up", "pageup"]:
            await self.body.handle_scroll_up()
        if event.key in ["down", " ", "pagedown"]:
            await self.body.handle_scroll_down()
        if event.key == "right":
            await self.body.handle_scroll_right()
        if event.key == "left":
            await self.body.handle_scroll_left()
        if event.key == "home":
            await self.body.handle_scroll_to(ScrollTo(self, x=0, y=0))

    async def on_mount(self, event: events.Mount) -> None:

        self.body = body = ScrollView(auto_width=True)

        await self.view.dock(body)

        async def add_content():
            table = Table(title=self.uri)

            table.add_column(self.df.index.name or "#")

            for c in self.df.columns:
                table.add_column(c)

            for row in self.df.itertuples():
                table.add_row(*[str(r) for r in row])

            await body.update(table)

        await self.call_later(add_content)


if __name__ == "__main__":
    run_app()
