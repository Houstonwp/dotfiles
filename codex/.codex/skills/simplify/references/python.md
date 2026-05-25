# Python Cleanup Reference

Use this reference when the Simplify change set includes Python files.

## Reuse

- Search for existing project helpers, fixtures, clients, serializers, validators, and CLI utilities before accepting new functions.
- Prefer `pathlib`, context managers, `tempfile`, `json`, `csv`, `dataclasses`, `enum`, and other standard library tools over custom equivalents.
- Reuse established logging, configuration, retry, error, and test-fixture patterns.
- Use the project's dependency manager and existing libraries; do not add dependencies for trivial cleanup.

## Quality

- Use clear types and small data objects when parameter lists grow.
- Avoid mutable default arguments, broad `except Exception`, silent exception swallowing, and global mutable state.
- Replace stringly typed modes/statuses with enums, literals, constants, or existing domain types when the project already uses them.
- Prefer early returns and small helpers over nested conditionals.
- Keep comments for non-obvious constraints or compatibility reasons, not step-by-step narration.
- Keep test helpers explicit enough that expected behavior is visible.

## Efficiency

- Avoid repeated filesystem scans, imports inside hot paths, repeated parsing, and duplicate API/database calls.
- Use generators or iterators for large streams; do not materialize lists unless reuse or ordering requires it.
- Batch related I/O when the API supports it.
- For async Python, use `asyncio.gather`, task groups, or existing concurrency helpers only when work is independent and error behavior is correct.
- Do not pre-check file existence before opening/removing/renaming; perform the operation and handle `FileNotFoundError`, `FileExistsError`, or `OSError`.
- Clean up file handles, event listeners, tasks, temporary directories, and background workers.

## Verification Cues

Prefer repository instructions. When Python commands are needed, use the project's configured runner. If the project uses `uv`, run Python, test, lint, and typecheck commands through `uv`.

Common commands include:

```bash
uv run pytest
uv run ruff check .
uv run ty check
```
