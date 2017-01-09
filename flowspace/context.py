from flowspace.xtools import get_active_window_title
from flowspace import vim
from flowspace.tmux import tmux_context, tmux_parse_window_title, get_panes

def _tmux_context(title):
    context = {}
    res = tmux_parse_window_title(title)
    if not res:
        return context

    panes = get_panes(res['tmux_session'])
    tmux_panes = {}
    for pane_id, pane in panes.items():
        pane_context = pane.__dict__
        tmux_panes[pane_id] = pane_context

    context['tmux_panes'] = tmux_panes

    context['active_pane'] = context['tmux_panes'][res['tmux_pane_id']]
    context.update(res)

    return context

def gen_context():
    context = {}

    title = get_active_window_title()
    is_vim = vim.is_vim(title)
    geoms = vim._vim_geoms(title)
    context['title'] = title
    context['is_vim'] = is_vim
    context['vim_geoms'] = geoms

    tmux_context = _tmux_context(title)
    if tmux_context:
        context.update(tmux_context)

    return context

if __name__ == '__main__':
    import pprint
    context = gen_context();
    pprint.pprint(context)
