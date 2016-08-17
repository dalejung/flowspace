from earthdragon.tools import Timer
from flowspace.shell import run
import re
import operator

DIR_MAP = {
    'up': {
        'edge': 'top',
        'edge_op': min,
    },
    'right': {
        'edge': 'right',
        'edge_op': max,
    },
    'down': {
        'edge': 'bottom',
        'edge_op': max,
    },
    'left': {
        'edge': 'left',
        'edge_op': min,
    },
}

class TmuxPane:
    def __init__(self, id, active, top, right, bottom, left):
        self.id = id
        self.active = active
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def __repr__(self):
        s = 'TmuxPane({id}, {active}, {top}, {right}, {bottom}, {left})'
        return s.format(**self.__dict__)

def get_tmux_window(pid):
    """
    Linux specific function that get the tmux session of the client specified
    by pid. This depends on the tmux.conf settings that updates the
    window title. This specific function currently relies on:

    ```
    set -g set-titles-string "{#S:#I} #T"
    ```

    This is necessary because the functions like `tmux splitw` and
    `tmux client_session` use the $TMUX variable which is not always correct.

    Using the window title is the only consistent way I've found to always
    correctly detect session attached to the client.

    https://github.com/tmux/tmux/issues/503

    Might be worth unsetting $TMUX.
    """
    xprop_name = run("xprop -id {pid} WM_NAME".format(pid=int(pid)))
    matches = re.search(r'\{(.*)\}', xprop_name)
    if matches:
        out = matches.group(1)
        session_name, window_index = out.split(':')
        return session_name, window_index

def parse_pane(line):
    id, geom, active = line.split(':')
    top, right, bottom, left = map(int, geom.split(','))
    active = active == '1'
    pane = TmuxPane(id, active, top, right, bottom, left)
    return pane

def get_panes():
    F = "#{pane_id}:#{pane_top},#{pane_right},#{pane_bottom},#{pane_left}:#{pane_active}"
    out = run("tmux list-panes -F \"{F}\"", F=F)
    lines = out.split()

    panes = {pane.id: pane for pane in map(parse_pane, lines)}
    return panes

def get_active_pane_id(panes):
    try:
        pane = next(filter(lambda x: x.active, panes.values()))
    except StopIteration:
        raise Exception("No pane give and not active pane.")
    return pane.id

def at_edge(direction, pane_id=None):
    """
    Detects whether a tmux-pane is at the edge of its containing tmux-window.

    Defaults to the current "active" pane if not pane_id is passed in
    """
    conf = DIR_MAP[direction]
    edge = conf['edge']
    reducer = conf['edge_op']

    panes = get_panes()
    if pane_id is None:
        pane_id = get_active_pane_id(panes)
    pane = panes[pane_id]
    pane_edge = getattr(pane, edge)

    edge_extreme = reducer(map(lambda x: getattr(x, edge), panes.values()))

    return edge_extreme == pane_edge

