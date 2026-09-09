# Lesson 3 — Python Project Conventions

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
| `version` | Current version — a literal string, or omitted in favour of `dynamic = ["version"]` (see below) |
| `requires-python` | Minimum Python version; sets expectations for CI |
| `dependencies` | Runtime dependencies; what gets installed by `uv sync` |
| `[project.optional-dependencies]` | Groups like `dev`, `test`, `docs` installed with `uv sync --extra dev` |

> `pyproject.toml` also carries configuration for tools like `ruff`, `pytest`, and `mypy`. Rhiza's `python-core` bundle writes sensible defaults for these into the file (or alongside it) when you first sync. It is also where you put `[tool.rhiza-task]`, the table that tells the task runner which folder to measure — that one stays yours (see [Lesson 10](./10-customizing-safely.md)).

## Two legal shapes for the version

`version = "0.1.0"` above is one of two shapes a Rhiza-managed Python project may use. The other is to **not write the number down at all** and let the build backend derive it from the git tag:

```toml
[project]
name = "my-project"
dynamic = ["version"]
requires-python = ">=3.11"

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"
```

This is recent, and it is recent in a specific way: until `pytest-rhiza` v0.6.0 the `test_pyproject` check **rejected** it. `version` sat among the required `[project]` fields and was matched against a semver pattern, so the conformance check Rhiza ships failed any project that adopted the shape. Six of that check's assertions are about a *written* version and now skip on a derived one, which costs nothing — every one of them catches a disagreement between a number in a file and a number in git, and a version derived from git cannot disagree with git. Declaring neither, or both, is still an error.

**What it buys is the version existing in exactly one place.** `rhiza-task` itself used to carry it in three — `[project].version`, `__version__`, and `uv.lock` — and a release had to update all three before tagging. v1.0.0 shipped with `uv.lock` left behind, and every gate failed, because `uv lock --check` is the first thing `install` runs. With a derived version there is no copy left to fall behind, and `uv` stops recording a version for the root package at all.

Two things do **not** follow from it, and both are worth knowing before you reach for it:

- **It does not make a release one step.** Anything the repo pins to *its own* version — a `rhiza-task@X.Y.Z` in a README, a `@vX.Y.Z` in a self-referencing CI workflow — is a documentation pin that has to be correct in the commit the tag names, so it cannot be derived from a tag that does not exist yet. Those keep their `[[tool.bumpversion.files]]` entries.
- **The failure mode gets quieter, not louder.** `hatch-vcs` and `setuptools-scm` fall back rather than fail. A clone with no tags derives `0.1.dev1+g<sha>`, so a distribution built from a shallow checkout gets published at a version nobody asked for — green build, no error anywhere. **Any job that builds a distribution needs `fetch-depth: 0`**, and since template v1.8.0 the release workflow checks that rather than only documenting it: a `Verify built distribution matches the tag` step parses the version out of what `uv build` actually wrote into `dist/`.

Rhiza itself derives its version this way as of v1.8.0. Rust and Go have always worked like this — their synced `.bumpversion.toml` deliberately omits `current_version`, so the newest tag answers instead — which makes the Python shape the odd one out finally catching up rather than a new idea. [Lesson 11](./11-the-rhiza-ecosystem.md) covers what it means for `/rhiza:release`, which had to learn to tell its phases apart without a written number to compare against.

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

Conventions the `python-core` bundle's pytest configuration expects:

- Test files are named `test_*.py` (pytest default).
- The `tests/` directory does **not** need an `__init__.py` — pytest finds tests without it.
- `conftest.py` at the root of `tests/` is the right place for shared fixtures.

The pytest configuration in `pyproject.toml` (written by the `python-core` bundle) includes:

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
├── pyproject.toml         # PEP 621 metadata + tool config + [tool.rhiza-task]
├── local.mk               # your own make targets — never synced
├── .python-version        # written by Rhiza (python-core bundle)
├── Makefile               # written by Rhiza (core bundle) — the task-runner shim
└── ruff.toml              # written by Rhiza (python-core bundle)
```

Files that Rhiza writes are managed by the sync; everything else is yours. `local.mk` is optional — add it when you have targets of your own.

## What if my project doesn't follow these conventions yet?

You can still adopt Rhiza, but you may need to adjust some tool configuration. The most common case is a project that has its package at the root (no `src/`) — in this case, update `testpaths` and the build backend config, then run `uv sync` again. Rhiza itself has no hard dependency on the src layout; it is the *tools it brings in* (pytest, coverage, mypy) that work best when the layout is standard.

---

**Next:** [Lesson 4 — Why Rhiza?](./04-why-rhiza.md)
