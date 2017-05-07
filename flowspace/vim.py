from flowspace.xtools import get_active_window_title, send_keys

DIR_MAP = {
    'up': 'k',
    'down': 'j',
    'left': 'h',
    'right': 'l',
}

def is_vim(title):
    bits = title.split()
    if bits[0].startswith('{'):
        bits.pop()
    if len(bits) < 2:
        return False
    if bits[0] == 'vim' and bits[1].startswith('<'):
        return True

def _vim_geoms(title):
    if not is_vim(title):
        return

    geoms = None
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

    return geoms

def vim_window_at_edge(direction, title):
    geoms = _vim_geoms(title)
    up, right, down, left = geoms
    return locals()[direction]

def vim_command(pane_pid, command):
    import neovim
    path = f'/tmp/nvim_{pane_pid}'
    nvim = neovim.attach('socket', path=path)
    nvim.command(command)
