import typer 

from boadata.commands import boatree

run_app = typer.Typer()
run_app.add_typer(boatree.run_app, name="tree")