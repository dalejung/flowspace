flowspace
=========

Current components:

`i3-wm`
`tmux`
`vim`

Workspace
---------

1. Normalize tmux panes and i3 windows so that movement is streamlined.
2. Maybe normalize vim panes, though I don't use split vim windows.
3. Turn off wrap around
4. Allow workspace metadata. Currently use this to set a name per i3 workspace.
   This is used to key the automatic tmux session that are generated per
   terminal instance.

`.i3/config`

```
# change focus
bindsym Mod4+Shift+$left exec zsh -c "flowspace move-focus left"
bindsym Mod4+Shift+$down exec zsh -c "flowspace move-focus down"
bindsym Mod4+Shift+$up exec zsh -c "flowspace move-focus up"
bindsym Mod4+Shift+$right exec zsh -c "flowspace move-focus right"
```
