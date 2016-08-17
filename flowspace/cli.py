import click
from . import tmux

@click.group()
def cli():
    pass

@click.group(name='tmux')
def tmux_group():
    pass

@click.command(name='at-edge')
@click.argument('direction')
def pane_at_edge(direction):
    _at_edge = tmux.at_edge(direction)
    click.echo(_at_edge)

@click.command(name='select-pane')
@click.argument('direction')
def select_pane(direction):
    tmux.select_pane(direction)

@click.command(name='debug')
def tmux_debug():
    msg = tmux.tmux_debug()
    click.echo(msg)

tmux_group.add_command(pane_at_edge)
tmux_group.add_command(select_pane)
tmux_group.add_command(tmux_debug)
cli.add_command(tmux_group)
