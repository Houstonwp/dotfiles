# Rust Cleanup Reference

Use this reference when the Simplify change set includes Rust files.

## Reuse

- Search for existing helpers, traits, newtypes, builders, validators, and domain modules before accepting new utility code.
- Prefer standard library path, string, iterator, parsing, and error APIs over hand-rolled equivalents.
- Reuse established error types and conversion patterns instead of adding ad hoc strings or catch-all variants.
- Keep crate boundaries intact. If a helper belongs in another crate or module, make that boundary explicit instead of reaching through internals.

## Quality

- Prefer borrowing over cloning when ownership is not required, but do not create awkward lifetimes for cold-path code.
- Use domain enums, newtypes, and constants instead of raw strings or magic numbers.
- Avoid widening public APIs for one caller. Prefer a request/config struct or an existing domain object when parameters are growing.
- Flatten deeply nested `match` or `if` blocks with guard clauses, helper functions, or small local match tables.
- Keep comments for non-obvious invariants, unsafe reasoning, subtle performance constraints, or compatibility requirements.
- Avoid adding speculative generic abstractions. Extract only when repeated behavior is real in the current codebase.

## Efficiency

- Watch for unnecessary `clone`, `to_string`, `format!`, `collect`, sorting, allocation, or conversion in hot paths.
- Avoid repeated lookup work when a borrowed map/set or cached handle already exists.
- Prefer streaming or buffered I/O for large files; do not read entire files when only a section is needed.
- Do not pre-check file existence before opening/removing/renaming; perform the operation and handle `io::ErrorKind`.
- For async Rust, use `join!`, `try_join!`, or task sets only when operations are independent and cancellation/error semantics remain correct.
- Make no-op update paths preserve the same value/reference when that is the repository's change signal.

## Verification Cues

Prefer repository instructions. Common Rust checks include:

```bash
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps
```
