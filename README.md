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

`.vimrc`

```
" Turn on setting the title.

autocmd BufEnter * let &titlestring = s:MyTitle()
if &term == "screen-256color"
    set t_ts=]2;
    set t_fs=\\
endif
set title

function! IsEdgeWindow(direction)
    let curNr = winnr()
    execute 'wincmd ' . a:direction
    let s:isEdge = 1
    if winnr() != curNr
      let s:isEdge = 0
      wincmd p
    endif
    return s:isEdge
endfunction

function! s:recalcWindowEdge()
  let w:leftEdge = IsEdgeWindow("h")
  let w:rightEdge = IsEdgeWindow("l")
  let w:topEdge = IsEdgeWindow("k") 
  let w:bottomEdge = IsEdgeWindow("j") 
  return w:topEdge.','.w:rightEdge.','.w:bottomEdge.','.w:leftEdge
endfunction

let w:allEdge = s:recalcWindowEdge()

autocmd WinEnter * let w:allEdge = s:recalcWindowEdge()
autocmd WinEnter * let &titlestring = s:MyTitle()

function! s:MyTitle()
  let l:buffername = expand("%:t")
  return "vim " . "<".l:buffername ."> ("  .w:allEdge . ")"
endfunction
```
