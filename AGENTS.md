# Agent Instructions

## Package Manager
None

## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: (the agent model's name and attribution byline)
```

## Key Conventions
- Repo is macOS dotfiles managed with GNU Stow
- Add dotfiles under top-level package dirs; stow from repo root (e.g. `stow zsh`)

## Config Inventory
- tracked: bottom, gh, git, kitty, lazygit, nvim, starship, zsh, zshenv
- not tracked: agent-workflow, atuin, aws, gh-copilot, github-copilot, nexus, oh-my-zsh, opencode, uv, .aws, .cache, .cargo, .claude, .claude.json, .claude.json.backup, .codex, .duckdb, .duckdb_history, .local, .npm, .plastic4, .rustup, .ssh, .zsh_history, .DS_Store
