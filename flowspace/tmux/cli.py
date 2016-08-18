import click

from . import edge

@click.group(name='tmux')
def tmux_group():
    pass

@click.command(name='at-edge')
@click.argument('direction')
def pane_at_edge(direction):
    _at_edge = edge.at_edge(direction)
    click.echo(_at_edge)

@click.command(name='select-pane')
@click.argument('direction')
def select_pane(direction):
    edge.select_pane(direction)

@click.command(name='debug')
def tmux_debug():
    msg = edge.tmux_debug()
    click.echo(msg)

tmux_group.add_command(pane_at_edge)
tmux_group.add_command(select_pane)
tmux_group.add_command(tmux_debug)
