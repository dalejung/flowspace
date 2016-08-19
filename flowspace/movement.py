from .tmux import at_edge, select_pane, tmux_parse_window_title
from .xtools import get_active_window_title, send_keys
from . import i3wm
from . import vim

MODE_SWITCH = {
    'i3': i3wm.focus_window,
    'vim': vim.focus,
    'tmux': select_pane
}

def move_focus(direction):
    mode = _move_focus(direction)
    callback = MODE_SWITCH[mode]
    callback(direction)

def _move_focus(direction):
    title = get_active_window_title()
    if vim.is_vim(title) and not vim.vim_window_at_edge(direction, title):
        return 'vim'

    res = tmux_parse_window_title(title)
    if not res:
        return 'i3'
    session_name, window = res

    if not at_edge(direction, session_name=session_name):
        return 'tmux'
    else:
        return 'i3'
