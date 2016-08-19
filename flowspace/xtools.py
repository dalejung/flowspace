import re
from .shell import run

def get_active_window_title():
    pid = run('xdotool getactivewindow')
    xprop_name = run("xprop -id {pid} WM_NAME".format(pid=int(pid)))
    matches = re.search(r'\"(.*)\"$', xprop_name)
    title = matches.group(1)
    return title

def send_keys(text):
    out = run('xvkbd -text "{text}"', text=text)
