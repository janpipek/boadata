from typing import List, Optional

import typer

from boadata import __version__  # noqa: F401
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
    from_uri: List[str],
    output_uri: Optional[str] = typer.Option(None, "--output-uri", "-o"),
    in_type: Optional[str] = typer.Option(None, help="The type of the input object."),
    out_type: Optional[str] = typer.Option(None, help="The type of the output object."),
    columns: Optional[List[str]] = typer.Option(None, help="List of columns to show"),
    filter: Optional[str] = typer.Option(
        None, help="Query to run (as in pandas query)"
    ),
    sql: Optional[str] = typer.Option(None, help="SQL to run on the object."),
    sortby: Optional[str] = typer.Option(None, help="Sort by column(s)."),
    lines: Optional[str] = typer.Option(None, help="Lines (as range)"),
    sample: Optional[int] = typer.Option(
        None, help="Sample a number of lines randomly"
    ),
    parameter: Optional[List[str]] = typer.Option(
        None, help="Additional parameters for loader, specified as key=value"
    ),
):
    """Convert a data object to another type."""
    do = try_load(from_uri[0], type=in_type, parameters=parameter)
    if len(from_uri) > 1:
        others = (try_load(from_uri[i]) for i in range(1, len(from_uri)))
        do = do.concat(*others)

    do = try_apply_sql(do, sql=sql)
    do = try_query(do, query=filter)
    do = try_select_columns(do, columns=columns)
    do = try_sort(do, sortby=sortby)
    do = try_select_rows(do, lines=lines, sample=sample)

    if output_uri:
        if not out_type:
            for conversion in do.allowed_conversions:
                type_candidate = DataObject.registered_types[conversion[1]]
                if type_candidate.accepts_uri(output_uri):
                    out_type = conversion[1]
                    break
        if not out_type:
            print("No suitable output type found.")
            exit(-1)

        do.convert(out_type, uri=output_uri)
    else:
        print("Allowed conversions")
        print("-------------------")
        for conversion in do.allowed_conversions:
            print(conversion[1])


if __name__ == "__main__":
    run_app()
