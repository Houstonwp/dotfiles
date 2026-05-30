# dotfiles

## Inventory (tracked)
- atuin -> ~/.config/atuin/config.toml
- aws -> ~/.config/aws/config.example
- bottom -> ~/.config/bottom
- codex -> selected ~/.codex config, rules, keybindings, and custom skills
- gh -> ~/.config/gh
- git -> ~/.config/git
- kitty -> ~/.config/kitty
- lazygit -> ~/.config/lazygit
- nvim -> ~/.config/nvim
- starship -> ~/.config/starship.toml
- zsh -> ~/.config/zsh
- zshenv -> ~/.zshenv

## Using GNU Stow
- from repo root: `stow --target="$HOME" zsh zshenv nvim gh git kitty lazygit bottom starship`
- include newer config packages: `stow --target="$HOME" atuin aws codex`
- remove a package: `stow -D --target="$HOME" zsh`
- first-time Codex sync: `stow -n -v --target="$HOME" codex` should be clean before replacing or adopting existing `~/.codex` files

## Bootstrap
- install packages and restow core config: `./bootstrap.sh`
- include config packages that may need adoption on an existing machine: `./bootstrap.sh --all --adopt`
