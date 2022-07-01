import sys
from typing import Optional

import typer

from boadata import __version__, tree
from boadata.cli import dump_tree


run_app = typer.Typer()


@run_app.command()
def main(
    uri: str,
    show_full_title: bool = typer.Option(False, "--show-full-title", "-t"),
    show_info: bool = typer.Option(False, "--show-info", "-i"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l"),
    max_depth: Optional[int] = typer.Option(None, "--level", "-L"),
):
    import boadata.data

    # Flags taken from the `exa` tool
    try:
        the_tree = tree(uri)
    except RuntimeError:
        typer.secho(f"URI not understood: {uri}", color="red")
        sys.exit(-1)
    else:
        dump_tree(
            the_tree,
            max_level=max_depth,
            limit=limit,
            show_info=show_info,
            show_full_title=show_full_title,
        )


if __name__ == "__main__":
    main()
