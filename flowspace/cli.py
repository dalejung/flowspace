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

@click.command(name='workspace-switcher')
@click.argument('outputs')
@click.argument('offset')
@click.argument('ws_num')
def workspace_switcher(outputs, offset, ws_num):
    """
    Allow relative workspace switching per monitor.
    You still need to setup the workspaces in your i3 config.
    See readme
    """
    from .i3wm import switch_workspace, get_active_output

    offset = int(offset)

    config = {}
    config['offset'] = offset

    output_config = {}
    for i, output in enumerate(outputs.split(',')):
        output_config[output] = 1 + i * offset

    config['output_config'] = output_config
    ws_num = int(ws_num)
    active_output = get_active_output()
    switch_workspace(config, active_output, ws_num)

cli.add_command(workspace_switcher)
