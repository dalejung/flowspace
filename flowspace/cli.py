import click

@click.group()
def cli():
    pass

from .tmux.cli import tmux_group
cli.add_command(tmux_group)
