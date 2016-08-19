from flowspace.xtools import get_active_window_title

def is_vim(title):
    bits = title.split()
    if bits[0] == 'vim':
        return True
    if bits[0].startswith('{') and bits[1] == 'vim':
        return True

def vim_window_at_edge(direction):
    title = get_active_window_title()

    if not is_vim(title):
        return

    bits = title.split()
    geom = bits[-1]
    geoms = map(int, geom[1:-1].split(','))
    up, right, down, left = geoms
    return locals()[direction]

print(vim_window_at_edge('up'))
print(vim_window_at_edge('right'))
print(vim_window_at_edge('down'))
print(vim_window_at_edge('left'))
