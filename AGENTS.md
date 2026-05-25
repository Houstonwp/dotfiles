# Agent Instructions

## Package Manager
Use Homebrew through `Brewfile` for machine-level tools. Use GNU Stow for dotfile installation.

## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: (the agent model's name and attribution byline)
```

## Key Conventions
- Repo is macOS dotfiles managed with GNU Stow
- Add dotfiles under top-level package dirs; stow from repo root with `--target="$HOME"` (e.g. `stow --target="$HOME" zsh`)
- Keep secrets, auth files, generated caches, histories, and session state out of Git

## Config Inventory
- tracked: atuin, aws template, bottom, codex durable config, gh, git, kitty, lazygit, nvim, starship, zsh, zshenv
- not tracked: credentials, tokens, shell histories, app databases, generated caches, vendored tool runtimes, Codex sessions/worktrees/logs/state, Claude state, SSH keys, AWS credentials
