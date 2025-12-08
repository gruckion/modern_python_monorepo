# Development Commands

All commands use `uv run poe <task>`:

## Code Quality

| Command | Description |
|---------|-------------|
| `uv run poe fmt` | Format code with Ruff |
| `uv run poe lint` | Lint code with auto-fix |
| `uv run poe check` | Type check with ty |
| `uv run poe test` | Run tests |
| `uv run poe cov` | Run tests with coverage |
| `uv run poe all` | Run all checks |

## CI Commands

| Command | Description |
|---------|-------------|
| `uv run poe ci:fmt` | Check formatting (no fix) |
| `uv run poe ci:lint` | Lint (no fix) |

## Git Hooks

| Command | Description |
|---------|-------------|
| `uv run poe hooks` | Install git hooks |
| `uv run poe hooks:run` | Run hooks on all files |

## Documentation

| Command | Description |
|---------|-------------|
| `uv run poe docs` | Serve docs locally |
| `uv run poe docs:build` | Build static site |
