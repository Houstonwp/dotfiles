#!/usr/bin/env zsh
set -euo pipefail

repo_dir=${0:A:h}
packages=(
  bottom
  gh
  git
  kitty
  lazygit
  nvim
  starship
  zsh
  zshenv
)
extra_packages=(
  atuin
  aws
  codex
)
stow_args=(--restow)

usage() {
  print "usage: ./bootstrap.sh [--all] [--adopt]"
}

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
    --all)
      packages+=("${extra_packages[@]}")
      ;;
    --adopt)
      stow_args+=(--adopt)
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v brew >/dev/null 2>&1; then
  print -u2 "Homebrew is required before bootstrapping these dotfiles."
  print -u2 "Install it from https://brew.sh, then rerun this script."
  exit 1
fi

brew bundle --file "$repo_dir/Brewfile"

cd "$repo_dir"
stow --target="$HOME" "${stow_args[@]}" "${packages[@]}"
