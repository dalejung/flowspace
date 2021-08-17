import os
import glob
import itertools
import re
from pathlib import Path

from xdg import BaseDirectory, DesktopEntry
import pandas as pd

from zouyu import obj_to_frame

DATA_DIRS = BaseDirectory.xdg_data_dirs

def _desktop_files(data_dir):
    app_dir = os.path.join(data_dir, 'applications')
    entries = glob.glob(app_dir + "/*.desktop")
    return entries

def get_desktop_frame():
    desktop_files = itertools.chain(*map(_desktop_files, DATA_DIRS))

    entries = map(DesktopEntry.DesktopEntry, desktop_files)
    entries = list(entries)
    entry = entries[0]
    entries = [e.__dict__ for e in entries]

    frame = obj_to_frame(entries, [
        'content.Desktop Entry.|Name|',
        'content.Desktop Entry.|Exec|',
        'content.Desktop Entry.|Type|',
        'content.Desktop Entry.|Path|',
        'filename',
        'content.Desktop Entry.|Location|',
        'content.Desktop Entry.|NoDisplay|',
        'content.Desktop Entry.|Hidden|',
        'content.Desktop Entry.|Terminal|',
    ])

    frame['filename'] = frame['filename'].map(lambda x: Path(x).name.rsplit('.', 1)[0])

    groups = frame.groupby(['Name']).groups

    dupe_names = [k for k in groups if len(groups[k]) > 1]

    for loc, row in frame.iterrows():
        if row.Name not in dupe_names:
            continue
        frame.loc[loc, 'Name'] = f'{row.Name} ({row.filename})'

    bool_cols = ['NoDisplay', 'Hidden', 'Terminal']
    for col in bool_cols:
        frame[col] = frame[col].astype(bool)

    return frame

def exec_cmd(exec_, name, choice='', location='', path=''):
    """
    Taken from i3-dmenu-desktop
    """
    # Remove deprecated field codes, as the spec dictates.
    exec_ = re.sub('%[dDnNvm]', '', exec_)

    # Replace filename field codes with the rest of the command line.
    # Note that we assume the user uses precisely one file name,
    # not multiple file names.
    exec_ = re.sub('%[fF]', choice, exec_)

    # If the program works with URLs,
    # we assume the user provided a URL instead of a filename.
    # As per the spec, there must be at most one of %f, %u, %F or %U present.
    exec_ = re.sub('%[uU]', choice, exec_)

    # The translated name of the application.
    exec_ = re.sub('%c', name, exec_)

    # location of .desktop file
    exec_ = re.sub('%k', location, exec_)

    # Literal % characters are represented as %%.
    exec_ = re.sub('%%', '%', exec_)

    if path and os.path.exists(path):
        exec_ = 'cd {path} && {exec_}'.format(path=path, exec_=exec_)

    return exec_

def i3_exec_cmd(cmd):
    # i3 executes applications by passing the argument to i3’s “exec” command
    # as-is to $SHELL -c. The i3 parser supports quoted strings: When a string
    # starts with a double quote ("), everything is parsed as-is until the next
    # double quote which is NOT preceded by a backslash (\).
    #
    # Therefore, we escape all double quotes (") by replacing them with \"
    cmd = re.sub('"', '\\"', cmd)
    cmd = 'i3-msg exec "{cmd}"'.format(cmd=cmd)
    return cmd

def i3_exec(*args, **kwargs):
    cmd = exec_cmd(*args, **kwargs)
    print(cmd)
    cmd = i3_exec_cmd(cmd)
    print(cmd)
    os.system(cmd)
