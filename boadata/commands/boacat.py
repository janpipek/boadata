from typing import List, Optional
import typer

from boadata import __version__
from boadata.cli import try_load, try_apply_sql, try_filter, try_select_columns, try_select_rows, try_sort
from boadata.cli import show_expanded, show_table


run_app = typer.Typer()


@run_app.command()
def main(
    uri: str,
    type: Optional[str] = typer.Option(None, help="The type of the object."),
    columns: Optional[List[str]] = typer.Option(None, help="List of columns to show"),
    filter: Optional[str] = typer.Option(None, help="Query to run (as in pandas query)"),
    sql: Optional[str] = typer.Option(None, help="SQL to run on the object."),
    sortby: Optional[str] = typer.Option(None, help="Sort by column(s)."),
    expand: bool = typer.Option(False, help="Show each row expanded."),
    lines: Optional[str] = typer.Option(None, help="Lines (as range)"),
    sample: Optional[int] = typer.Option(None, help="Sample a number of lines randomly"),
    parameter: Optional[List[str]] = typer.Option(None, help="Additional parameters for loader, specified as key=value"),
):
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    expand = kwargs.pop("expand", False)

    do = try_load(uri, type=type, parameters=parameter)
    do = try_apply_sql(do, sql=sql)
    do = try_filter(do, filter=filter)
    do = try_select_columns(do, columns=columns)
    do = try_sort(do, sortby=sortby)
    do = try_select_rows(do, lines=lines, sample=sample)

    do = do.convert("pandas_data_frame")
    if do.shape[0] > kwargs.get("limit", 2 ** 62):
        typer.echo(
            f"The row count is higher than the limit ({do.shape[0]}), dropping lines after that..."
        )
        do = do.head(kwargs.get("limit"))

    if expand:
        show_expanded(do)
    else:
        show_table(do)

run_app.command()(main)


if __name__ == "__main__":
    run_app()
