from .tmux import at_edge, select_pane, tmux_parse_window_title, tmux_context
from .xtools import get_active_window_title, send_keys
from . import i3wm
from . import vim

def select_pane_active(direction, context=None):
    """ integration tmux select-pane with session_name from title """
    title = get_active_window_title()
    res = tmux_parse_window_title(title)
    select_pane(direction, session_name=res['tmux_session'])

def neovim_focus(direction, context):
    import neovim
    pane_pid = context['pane_pid']
    path = f'/tmp/nvim_{pane_pid}'
    nvim = neovim.attach('socket', path=path)
    vimdir = vim.DIR_MAP[direction]
    nvim.command(f'wincmd {vimdir}')

MODE_SWITCH = {
    'i3': i3wm.focus_window,
    'vim': neovim_focus,
    'tmux': select_pane_active
}

def move_focus(direction):
    title = get_active_window_title()


    context = {}
    context['title'] = title

    res = tmux_context(title)
    if res:
        context.update(res)

    mode = _move_focus(direction, context)
    callback = MODE_SWITCH[mode]
    callback(direction, context)

def _move_focus(direction, context):
    if vim.is_vim(context['title']) and not vim.vim_window_at_edge(direction, context):
        return 'vim'

    if 'tmux_session' not in context:
        return 'i3'

    if not at_edge(direction, session_name=context['tmux_session']):
        return 'tmux'
    else:
        return 'i3'
