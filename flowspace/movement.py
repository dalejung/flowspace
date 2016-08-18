from .tmux import get_active_tmux_window, at_edge, select_pane
from . import i3

def move_focus(direction):
    res = get_active_tmux_window()
    if not res:
        i3.focus(direction)
    session_name, window = res

    if not at_edge(direction, session_name=session_name):
        select_pane(direction)
    else:
        i3.focus(direction)
