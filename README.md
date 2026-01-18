# dotfiles

## Inventory (tracked)
- bottom -> ~/.config/bottom
- gh -> ~/.config/gh
- git -> ~/.config/git
- kitty -> ~/.config/kitty
- lazygit -> ~/.config/lazygit
- nvim -> ~/.config/nvim
- starship -> ~/.config/starship.toml
- zsh -> ~/.config/zsh
- zshenv -> ~/.zshenv

## Inventory (not tracked)
- ~/.config: agent-workflow, atuin, aws, gh-copilot, github-copilot, nexus, oh-my-zsh, opencode, uv
- ~: .aws, .cache, .cargo, .claude, .claude.json, .claude.json.backup, .codex, .duckdb, .duckdb_history, .local, .npm, .plastic4, .rustup, .ssh, .zsh_history, .DS_Store

## Using GNU Stow
- from repo root: `stow zsh zshenv nvim gh git kitty lazygit bottom starship`
- remove a package: `stow -D zsh`
