import click

@click.group()
def cli():
    pass

from .tmux.cli import tmux_group
cli.add_command(tmux_group)

from .movement import move_focus

@click.command(name="move-focus")
@click.argument('direction')
def move_focus_cmd(direction):
    move_focus(direction)

cli.add_command(move_focus_cmd)
