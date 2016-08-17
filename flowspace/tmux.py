from earthdragon.tools import Timer
from flowspace.shell import run
import re

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

pid = run('xdotool getactivewindow')


panes = get_panes()
print(panes)
