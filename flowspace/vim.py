from flowspace.xtools import get_active_window_title, send_keys
import neovim

DIR_MAP = {
    'up': 'k',
    'down': 'j',
    'left': 'h',
    'right': 'l',
}

def is_vim(title):
    bits = title.split()
    if bits[0] == 'vim <':
        return True
    if bits[0].startswith('{') and bits[1] == 'vim':
        return True

def vim_window_at_edge(direction, context):
    title = context['title']

    if not is_vim(title):
        return

    # geoms are in form of (int,int,int,int)
    bits = title.split()
    for bit in bits:
        if not bit.startswith('(') or not bit.endswith(')'):
            continue

        geoms = bit[1:-1].split(',')
        if len(geoms) != 4:
            continue

        try:
            geoms = list(map(int, geoms))
        except ValueError:
            continue

    up, right, down, left = geoms
    return locals()[direction]
