# Lesson 0 — uv and uvx

Rhiza is distributed as a `uvx` tool. Before you can run `uvx rhiza`, you need to understand what `uv` and `uvx` are and why the Rhiza ecosystem uses them.

## What is uv?

[uv](https://docs.astral.sh/uv/) is a Python package and project manager written in Rust. It replaces a sprawling collection of separate tools — `pip`, `pip-tools`, `virtualenv`, `pyenv`, `pipx` — with a single, very fast binary.

The two things you will use most often:

| Command | What it does |
|---------|-------------|
| `uv python install 3.12` | Download and manage Python versions |
| `uv sync` | Create a virtual environment and install dependencies from a lockfile |
| `uv run <command>` | Run a command inside the project's virtual environment |
| `uvx <tool>` | Run a tool in a temporary, isolated environment (no install step) |

uv is orders of magnitude faster than pip. A fresh install of a typical project that takes 30 seconds with pip takes under 2 seconds with uv.

## Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS you can also use Homebrew:

```bash
brew install uv
```

Verify the install:

```bash
uv --version
```

## What is uvx?

`uvx` is shorthand for `uv tool run`. It downloads a tool, runs it in an isolated throwaway environment, and discards the environment when done. You never need to install the tool globally or manage its dependencies.

```bash
uvx rhiza init
```

This is equivalent to:

1. Create a temporary virtual environment
2. Install `rhiza` and its dependencies into it
3. Run `rhiza init`
4. Delete the environment

The first run fetches from PyPI and takes a few seconds. Subsequent runs use a local cache and are nearly instant.

### Why not just `pip install rhiza`?

Global installs cause dependency conflicts. If two tools you install globally need different versions of the same library, one of them breaks. `uvx` sidesteps this entirely by giving every tool its own isolated environment.

### uvx vs pipx

`uvx` does the same job as `pipx` but is significantly faster because it shares uv's cache. If you already use `pipx`, `uvx` is a drop-in replacement.

## How the Rhiza ecosystem uses uv

All Rhiza-managed projects adopt uv as the standard package manager. When you run `uvx rhiza materialize`, one of the files it writes is `.python-version`, which tells uv which Python version the project targets. The Makefile it provides uses `uv sync` to set up the development environment.

In CI, Rhiza's template workflows install uv with the official `astral-sh/setup-uv` action and then call `uv sync` or `uvx` — no manual pip steps required.

## Quick reference

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run Rhiza without installing it
uvx rhiza --help

# Set up a project's development environment (inside a Rhiza-managed project)
uv sync

# Run a command inside the project environment
uv run pytest

# Install a specific Python version
uv python install 3.12
```

---

**Next:** [Lesson 1 — Why Rhiza?](./01-why-rhiza.md)
