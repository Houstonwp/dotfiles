# Global Codex Instructions

- When installing software or tools, first check if Homebrew can install them. If not available via Homebrew, ask the user which installation method they want to use.
- For project dependencies, use the language's dependency management tool (e.g., `uv` for Python, `cargo` for Rust).
- Any Python usage must go through `uv` for running code, scripts, development, etc. Do not use system `python`, `pip`, or other runners.

## Output And Comments

- Avoid meta-narration: do not describe that a decision was made, that an artifact is structured a certain way, or that information is represented elsewhere unless it adds actionable value.
- Prefer the operative state or next action directly. Example: write `Blocked by #216 and #218`, not `Execution dependencies are represented by GitHub blocker relationships, not duplicated here`.
- Code comments should explain non-obvious behavior, invariants, or constraints. Do not add comments that merely narrate chosen structure, repeat the code, or memorialize process decisions.
