import click
from .tmux import at_edge

@click.group()
def cli():
    pass

@click.group(name='tmux')
def tmux():
    pass

@click.command(name='at-edge')
@click.argument('direction')
def pane_at_edge(direction):
    _at_edge = at_edge(direction)
    click.echo(_at_edge)

tmux.add_command(pane_at_edge)
cli.add_command(tmux)
