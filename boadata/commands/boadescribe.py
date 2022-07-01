from typing import List, Optional

import typer
from pandas import DataFrame, RangeIndex

from boadata.cli import try_apply_sql, try_load


run_app = typer.Typer()


@run_app.command()
def main(
    uri: str,
    type: Optional[str] = typer.Option(None, help="The type of the object."),
    sql: Optional[str] = typer.Option(None, help="SQL to run on the object."),
    summary: bool = typer.Option(False, help="Include summary using pandas describe."),
    parameter: Optional[List[str]] = typer.Option(
        None, help="Additional parameters for loader, specified as key=value"
    ),
):
    """Show information about a particular data object."""

    do = try_load(uri, type, parameters=parameter)
    do = try_apply_sql(do, sql=sql)

    print("Type: {0}".format(do.type_name))
    print("Underlying type: {0}".format(do.inner_data.__class__.__name__))
    print("Data shape: {0}".format(do.shape))
    columns = do.columns
    if hasattr(do.inner_data, "index"):
        # TODO: Include in the interface rather...
        print("Index:")
        index = do.inner_data.index
        s = f"  - {index.name or '<no name>'}"
        try:
            if isinstance(index, RangeIndex):
                s += f" ({index.start}..{index.stop}"
                if index.step != 1:
                    s += f", step={index.step}"
                s += ")"
            else:
                s += " (dtype={0})".format(index.dtype)
        except RuntimeError:
            pass
        print(s)
    if columns:
        print("Columns:")
        for name in columns:
            s = f"  - {name}"
            try:
                s += " (dtype={0})".format(do[name].dtype)
            except RuntimeError:
                pass
            print(s)
    if summary:
        print("Summary (DataFrame.describe()):")
        if isinstance(do.inner_data, DataFrame):
            df: DataFrame = do.inner_data
            print("\n".join("  " + line for line in str(df.describe()).splitlines()))
        else:
            print("  Not supported :-(")


if __name__ == "__main__":
    main()
