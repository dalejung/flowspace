import i3

def focus_window(direction):
    i3.focus(direction)

def get_active_output():
    workspaces = i3.get_workspaces()
    for ws in workspaces:
        if ws['focused']:
            return ws['output']

def switch_workspace(config, active_output, ws_num):
    offset = config['offset']
    output_config = config['output_config']
    base_num = output_config.get(active_output, 1)
    ws_num = (ws_num - 1) + base_num
    i3.workspace(str(ws_num))

class I3Tree:
    def __init__(self, obj, name=None):
        if name is None:
            name = obj['name']
        self.obj = obj
        self.name = name

    def __repr__(self):
        name = self.name
        bits = ["name={name}"]

        if self._has_nodes():
            nodes = self._get_nodes()
            bits.append("nodes={nodes_repr}")
            nodes_repr = [n.name for n in nodes]

        tmpl = "I3Tree({0})".format(",".join(bits))
        return tmpl.format(**locals())

    def _has_nodes(self):
        nodes = self._get_nodes_raw()
        return nodes is not None

    def _get_nodes(self):
        nodes = self._get_nodes_raw()
        return nodes or []

    def _get_nodes_raw(self):
        if 'nodes' in self:
            return self['nodes']
        if self.name == 'nodes':
            return self

    def __getitem__(self, key):
        if key in self.obj:
            return self._wrap(self.obj[key], key)
        nodes = self._get_nodes()

        for node in nodes:
            if node['name'] == key:
                return self._wrap(node, key)
        raise KeyError(key)

    def __iter__(self):
        return (I3Tree(o) for o in self.obj)

    def __contains__(self, key):
        return key in self.obj

    def _wrap(self, obj, key=None):
        if isinstance(obj, (dict, list)):
            return I3Tree(obj, key)
        return obj

    def keys(self):
        return self.obj.keys()

    def treeview(self, repr_func=lambda x: x.name +' '+ x['type'], depth=0):
        lines = []
        lines.append("  "*depth + repr_func(self))
        for node in self._get_nodes():
            lines.append(node.treeview(repr_func=repr_func, depth=depth+1))
        return '\n'.join(lines)

#tree = I3Tree(i3.get_tree())
#def dale(self):
#    attrs = ['name', 'type', 'focused', 'id']
#    attrs = ['{{{0}}}'.format(attr) for attr in attrs]
#    FMT = " ".join(attrs)
#    return FMT.format(**self.obj)
#print(tree.treeview(repr_func=dale))

# create a different view that will map the workspace container to it's screena
# nd workspace.

# i3.focus(con_id=12323)
