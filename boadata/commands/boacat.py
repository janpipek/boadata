from typing import List, Optional

import typer

from boadata.cli import (
    show_expanded,
    show_table,
    try_apply_sql,
    try_load,
    try_query,
    try_select_columns,
    try_select_rows,
    try_sort,
)


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

    if expand:
        show_expanded(do)
    else:
        show_table(do)


if __name__ == "__main__":
    run_app()
