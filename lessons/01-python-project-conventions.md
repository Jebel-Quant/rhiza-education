# Lesson 1 — Python Project Conventions

Rhiza manages your project's infrastructure files — CI workflows, Makefile, linting config, and so on. It does not touch your application code, but it does assume your project follows standard Python conventions. This lesson describes what those conventions look like so that the tools Rhiza provides work out of the box.

## The `pyproject.toml` file (PEP 621)

Every project in the Rhiza ecosystem has a `pyproject.toml` at the root. This file is the single place Python tooling looks for project metadata and configuration.

[PEP 621](https://peps.python.org/pep-0621/) standardised the `[project]` table, which is the part Rhiza cares about:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A short description of what this project does."
requires-python = ">=3.11"

dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov",
]
```

Key fields:

| Field | Purpose |
|-------|---------|
| `name` | The package name — must be unique on PyPI if you publish |
| `version` | Current version — can also be read dynamically from a `__version__` variable |
| `requires-python` | Minimum Python version; sets expectations for CI |
| `dependencies` | Runtime dependencies; what gets installed by `uv sync` |
| `[project.optional-dependencies]` | Groups like `dev`, `test`, `docs` installed with `uv sync --extra dev` |

> `pyproject.toml` also carries configuration for tools like `ruff`, `pytest`, and `mypy`. Rhiza's `core` bundle writes sensible defaults for these into the file (or alongside it) when you first materialise.

## The src layout

Rhiza expects the **src layout**: your importable package lives inside a `src/` directory, not at the root.

```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── ...
├── tests/
│   └── test_my_project.py
├── pyproject.toml
└── ...
```

### Why src layout?

Without `src/`, Python adds the project root to `sys.path`. This means `import my_project` can accidentally resolve to the source directory rather than the installed package. The symptom: tests pass locally but fail in CI, or you ship broken code because you were testing the wrong thing.

With `src/` layout:

- Imports always resolve to the **installed** package, not the source tree.
- You cannot accidentally import uninstalled code — which catches missing `__init__.py` files and packaging mistakes early.
- Tools like `pytest` and `mypy` behave predictably.

To make the src layout work, tell your build backend where to find the package:

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

Or, if you use Hatchling (the default in many Rhiza-managed projects):

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]
```

uv understands both. Running `uv sync` installs your package in editable mode ([PEP 660](https://peps.python.org/pep-0660/)), so changes in `src/` are immediately reflected without reinstalling.

## The `tests/` folder

Tests live in a top-level `tests/` directory, parallel to `src/`:

```
tests/
├── conftest.py       # shared fixtures
├── test_core.py
└── integration/
    └── test_api.py
```

Conventions Rhiza's `tests` bundle expects:

- Test files are named `test_*.py` (pytest default).
- The `tests/` directory does **not** need an `__init__.py` — pytest finds tests without it.
- `conftest.py` at the root of `tests/` is the right place for shared fixtures.

The pytest configuration in `pyproject.toml` (written by the `core` bundle) includes:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

## A complete project skeleton

```
my-project/
├── .github/
│   └── workflows/         # written by Rhiza (github bundle)
├── .rhiza/
│   └── template.yml       # Rhiza config
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── conftest.py
├── pyproject.toml         # PEP 621 metadata + tool config
├── .python-version        # written by Rhiza (core bundle)
├── Makefile               # written by Rhiza (core bundle)
└── ruff.toml              # written by Rhiza (core bundle)
```

Files that Rhiza writes are managed by the sync; everything else is yours.

## What if my project doesn't follow these conventions yet?

You can still adopt Rhiza, but you may need to adjust some tool configuration. The most common case is a project that has its package at the root (no `src/`) — in this case, update `testpaths` and the build backend config, then run `uv sync` again. Rhiza itself has no hard dependency on the src layout; it is the *tools it brings in* (pytest, coverage, mypy) that work best when the layout is standard.

---

**Next:** [Lesson 1b — The Repo Zoo Problem](./01b-the-repo-zoo.md)
