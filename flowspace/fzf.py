"""
Purpoe of this module is to help make complicated fzf entries where you are
merging multiple target sources and then munging their labels. So instead of
having something like:

/root/frank/bob/dir1/file1
/root/frank/bob/dir1/file2
/root/frank/bob/dir2/file2

You can have

dir1/file1 (bob)
dir1/file2 (bob)
dir2/file2 (bob)

using "{relative_path} (bob)" as your label

the utilities here will translate the label back to the full path target.

Since these are simple dicts, you can munge multiple sources together as long
as the keys don't collide.
"""
import os
import sh


SKIP_NAMES = ['.git']

def find_filetargets(path, max_depth=None, include_files=True, include_dirs=True,
                     current_depth=1, **kwargs):
    targets = []
    dirs = []
    for entry in os.scandir(path):
        if entry.name in SKIP_NAMES:
            continue
        is_dir = entry.is_dir()
        if is_dir:
            dirs.append(entry)
            if include_dirs:
                targets.append(entry)
            continue
        if include_files:
            targets.append(entry)

    if max_depth is None or current_depth < max_depth:
        for dir in dirs:
            try:
                subtargets = find_filetargets(dir.path, max_depth=max_depth,
                                              include_files=include_files,
                                              include_dirs=include_dirs,
                                              current_depth=current_depth+1
                                             )
                targets.extend(subtargets)
            except PermissionError:
                pass

    return targets

def gen_label_maker(label, path):
    has_relative = False
    if '{relative_path}' in label:
        has_relative = True
        path_len = len(str(path)) + 1 # get rid of leading /

    def _label_maker(entry):
        name = entry.name
        if has_relative:
            relative_path = entry.path[path_len:]
        return label.format(**locals())
    return _label_maker

def gen_target_dict(path, **kwargs):
    """
    """
    label = kwargs.pop('label', "{name}")
    label_maker = gen_label_maker(label, path=path)

    targets = find_filetargets(path, **kwargs)
    target_dict = {label_maker(entry):entry.path for entry in targets}
    return target_dict
