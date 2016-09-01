from flowspace.shell import run
import re

DIR_MAP = {
    'up': {
        'tmux_opt': '-U',
        'edge': 'top',
        'edge_op': min,
    },
    'right': {
        'tmux_opt': '-R',
        'edge': 'right',
        'edge_op': max,
    },
    'down': {
        'tmux_opt': '-D',
        'edge': 'bottom',
        'edge_op': max,
    },
    'left': {
        'tmux_opt': '-L',
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

def tmux_parse_window_title(window_title):
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
    matches = re.search(r'\{(.*)\}', window_title)
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

def get_panes(session_name=':'):
    F = "#{pane_id}:#{pane_top},#{pane_right},#{pane_bottom},#{pane_left}:#{pane_active}"
    out = run("tmux list-panes -t {session_name} -F \"{F}\"", F=F, session_name=session_name)
    lines = out.split()

    panes = {pane.id: pane for pane in map(parse_pane, lines)}
    return panes

def get_active_pane_id(panes):
    try:
        pane = next(filter(lambda x: x.active, panes.values()))
    except StopIteration:
        raise Exception("No pane give and not active pane.")
    return pane.id

def at_edge(direction, pane_id=None, session_name=':'):
    """
    Detects whether a tmux-pane is at the edge of its containing tmux-window.

    Defaults to the current "active" pane if not pane_id is passed in
    """
    conf = DIR_MAP[direction]
    edge = conf['edge']
    reducer = conf['edge_op']

    panes = get_panes(session_name)
    if pane_id is None:
        pane_id = get_active_pane_id(panes)
    pane = panes[pane_id]
    pane_edge = getattr(pane, edge)

    edge_extreme = reducer(map(lambda x: getattr(x, edge), panes.values()))

    return edge_extreme == pane_edge

def select_pane(direction, session_name=':'):
    conf = DIR_MAP[direction]
    tmux_opt = conf['tmux_opt']
    run("tmux select-pane {tmux_opt} -t {session_name}", tmux_opt=tmux_opt,
        session_name=session_name)

def tmux_debug():
    msg = run("tmux display-message -p \"#{client_session}\"")
    return msg
