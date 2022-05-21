import click
from flowspace import get_logger
logger = get_logger()

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
@click.argument('ws_per_monitor')
@click.argument('ws_num')
def workspace_switcher(outputs, ws_per_monitor, ws_num):
    """
    Allow relative workspace switching per monitor.
    You still need to setup the workspaces in your i3 config.
    See readme
    """
    from .i3wm import switch_workspace, get_active_output

    ws_per_monitor = int(ws_per_monitor)
    logger.warning(f"per {ws_per_monitor}")

    config = {}
    config['ws_per_monitor'] = ws_per_monitor

    output_config = {}
    for i, output in enumerate(outputs.split(',')):
        output_config[output] = 1 + i * ws_per_monitor


    config['output_config'] = output_config
    ws_num = int(ws_num)
    active_output = get_active_output()
    logger.warning(f"ws active_output: {active_output} {ws_per_monitor}")
    logger.warning(f"ws {output_config} {outputs}")
    switch_workspace(config, active_output, ws_num)

cli.add_command(workspace_switcher)


import flowspace.vim as vim
@click.group(name='vim')
def vim_group():
    pass

@click.command(name='send-command')
@click.argument('pane_pid')
@click.argument('command', nargs=-1)
def send_command(pane_pid, command):
    command = ' '.join(command)
    vim.vim_command(pane_pid, command)

vim_group.add_command(send_command)

cli.add_command(vim_group)
