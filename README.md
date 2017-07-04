vim_mattermost is a matter_most plugin for Neovim/Vim to watch posts realtime.

## Requirements
vim_mattermost requires Neovim with `if_python3`.
If `:echo has("python3")` returns `1`, then you're done; otherwise, see below.

You can enable Python3 interface with `pip`:

    pip3 install neovim

If you want to read the Neovim-python/python3 interface install documentation,
you should read `:help provider-python`.
