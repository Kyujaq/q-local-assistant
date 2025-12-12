# Coding Standards

## General Principles
- Code must be clear, maintainable, well-typed, and easy for both humans and dev agents to reason about.
- Prefer clarity and robustness over clever tricks.

## Python Standards
- **Strict type hints everywhere** (functions, methods, classes, variables where appropriate).
- **Docstrings required** for:
  - every module
  - every class
  - every public function
- One purpose per module whenever possible.
- Avoid global state except where explicitly justified.

## Formatting & Linting
- **Ruff**: linting, error detection, code style.
- **Black**: formatting (run after ruff).
- Code checked with both tools before merging.

## Function & Module Size
- **Moderate limits**:
  - Functions ideally < ~80 lines unless justified.
  - Modules ideally < ~500 lines unless the domain requires more.
- Large classes should be broken into components.

## Comments & Intent
- Write comments explaining the intent behind non-obvious code.
- Docstrings should explain *what* the function does, not necessarily *how*.

## Tests
- Unit tests must exist for new functions or edge cases.
- Integration tests required when touching orchestrator/agent interactions or HA integration.
- Tests belong under:
  - `tests/unit/`
  - `tests/integration/`

## Git Commit Style
- `feat(module): summary`
- `fix(module): summary`
- `refactor(module): summary`
- `test: summary`
- `docs: summary`
- Message body may contain rationale, test notes, or links to feature specs.