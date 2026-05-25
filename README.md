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

## Inventory (not tracked)
- secrets and auth: ~/.ssh, ~/.aws, ~/.config/aws/credentials, ~/.codex/auth.json, gh hosts.yml
- application state: ~/.cache, ~/.local/state, ~/.local/share/atuin, ~/.codex/sessions, ~/.codex/logs, ~/.codex/worktrees
- generated tool data: ~/.cargo registries, ~/.rustup toolchains, ~/.local/share/uv, ~/.local/share/nvim, ~/.local/share/gh
- history files: ~/.zsh_history, ~/.duckdb_history, ~/.sqlite_history
- stale or app-owned surfaces: ~/.config/fish, ~/.claude, ~/.claude.json, ~/.config/github-copilot

## Using GNU Stow
- from repo root: `stow --target="$HOME" zsh zshenv nvim gh git kitty lazygit bottom starship`
- include newer config packages: `stow --target="$HOME" atuin aws codex`
- remove a package: `stow -D zsh`

## Bootstrap
- install packages and restow core config: `./bootstrap.sh`
- include config packages that may need adoption on an existing machine: `./bootstrap.sh --all --adopt`
