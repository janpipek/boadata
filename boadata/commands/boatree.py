import sys

import typer

from boadata import __version__, tree


run_app = typer.Typer()


@run_app.command()
def main(
    uri: str,
    full_title: bool = False,
    info: bool = False,
):
    try:
        the_tree = tree(uri)
    except:
        typer.secho(f"URI not understood: {uri}", color="red")
        sys.exit(-1)
    else:
        the_tree.dump(
            full_title=full_title, data_object_info=info
        )


if __name__ == "__main__":
    main()
