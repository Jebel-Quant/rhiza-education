# Lesson 12 — Further Reading

The Rhiza repos contain detailed documentation beyond what fits in this curriculum. This lesson maps that material by topic so you can go deeper on whatever is most relevant to you.

All links point directly to the Markdown source on GitHub. Every file listed here has been verified to exist.

---

## Getting started and command usage

The primary interface is the `rhiza` plugin shipped by [`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude), documented on its [docs site](https://jebel-quant.github.io/rhiza-claude/) — a page per command.

| Document | What it covers |
|----------|---------------|
| [rhiza-claude docs](https://jebel-quant.github.io/rhiza-claude/) | Installing the marketplace and the full `/rhiza:*` command set, one page per command — the reference for `init`, `update`, `quality`, and the rest |
| [`jebel-quant/rhiza` README](https://github.com/Jebel-Quant/rhiza/blob/main/README.md) | The template repo itself — bundles, structure, and how the template files land in your project |

---

## Core reference

These live in [`rhiza/docs/`](https://github.com/Jebel-Quant/rhiza/tree/main/docs).

| Document | What it covers |
|----------|---------------|
| [QUICK_REFERENCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/QUICK_REFERENCE.md) | Concise card of the most common Rhiza operations — good to bookmark |
| [GLOSSARY.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/GLOSSARY.md) | Definitions of every term used in the Rhiza ecosystem |
| [ARCHITECTURE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ARCHITECTURE.md) | Visual diagrams of system components and how they interact |
| [TOOLS_REFERENCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/TOOLS_REFERENCE.md) | Quick reference for all the external tools Rhiza-managed projects use (ruff, pytest, pre-commit, etc.) |

---

## Customisation and extension

| Document | Repo | What it covers |
|----------|------|---------------|
| [CUSTOMIZATION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/CUSTOMIZATION.md) | rhiza | Makefile hooks, `custom-task.mk`, `custom-env.mk`, and the full menu of extension points |
| [EXTENDING_RHIZA.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/EXTENDING_RHIZA.md) | rhiza | Comprehensive worked examples for extending Rhiza-based projects — patterns and best practices |
| [CUSTOMIZATION.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/docs/CUSTOMIZATION.md) | rhiza-hooks | How to write and register your own pre-commit hooks alongside the built-in Rhiza hooks |

---

## Bundle-specific documentation

Each bundle has its own guide in [`rhiza/docs/`](https://github.com/Jebel-Quant/rhiza/tree/main/docs).

| Document | Bundle | What it covers |
|----------|--------|---------------|
| [DEVCONTAINER.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/DEVCONTAINER.md) | `devcontainer` | VS Code Dev Container and GitHub Codespaces configuration |
| [DOCKER.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/DOCKER.md) | `docker` | Dockerfile structure and container CI workflow |
| [MARIMO.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/MARIMO.md) | `marimo` | Marimo notebook conventions and folder layout |
| [PRESENTATION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/PRESENTATION.md) | `presentation` | Slide generation from Markdown using Marp |
| [GH_AW.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/GH_AW.md) | — | GitHub Agentic Workflows: AI-driven repository automation built into the Rhiza template |

---

## Command reference

Each `/rhiza:*` command has a dedicated page on the [rhiza-claude docs site](https://jebel-quant.github.io/rhiza-claude/).

| Document | Command | What it covers |
|----------|---------|---------------|
| [update](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:update` | Bump to the latest release, sync the template, resolve conflicts, and open a scorecard PR |
| [quality](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:quality` | Run the code-quality gate and score the repo |
| [release](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:release` | Derive the next semver from conventional commits, bump `pyproject.toml`, regenerate `CHANGELOG.md`, commit and tag locally |
| [stats](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:stats` | Read-only statistics dashboard; writes `docs/stats.html` |
| [status](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:status` | Show sync status from `.rhiza/template.lock`; `--check` reports whether you are behind |
| [new](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:new` | Scaffold a source module and its mirrored test file |

> The version-matrix and coverage-badge logic that used to be user-run `rhiza-tools` commands now lives inside the template's reusable CI workflows (`rhiza_ci.yml`), so there is nothing to invoke by hand.

---

## rhiza-hooks reference

| Document | What it covers |
|----------|---------------|
| [ARCHITECTURE.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/docs/ARCHITECTURE.md) | How the hooks are structured and how they interact with pre-commit |
| [QUICK_REFERENCE.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/docs/QUICK_REFERENCE.md) | All available hooks, their IDs, and what they check |

---

## Claude Code integration

The [`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude) plugin marketplace ships the `rhiza` plugin — the slash commands that drive the whole init, sync, and quality workflow from Claude Code. The full reference lives on its [docs site](https://jebel-quant.github.io/rhiza-claude/).

| Document | Command | What it covers |
|----------|---------|---------------|
| [rhiza-claude README](https://github.com/Jebel-Quant/rhiza-claude/blob/main/README.md) | — | Installing the marketplace and the full command list |
| [update](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:update` | Bump to the latest release, sync, resolve conflicts, and open a scorecard PR |
| [quality](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:quality` | Run the code-quality gate and score the repo |
| [revisit](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:revisit` | Refresh `README.md`, `CLAUDE.md`, and `mkdocs.yml` |
| [stats](https://jebel-quant.github.io/rhiza-claude/) | `/rhiza:stats` | Read-only statistics dashboard for the repo |

---

## Cross-repo testing

| Document | Repo | What it covers |
|----------|------|---------------|
| [README.md](https://github.com/Jebel-Quant/rhiza-brainbug/blob/main/README.md) | rhiza-brainbug | The cross-repo test harness: how polling detects upstream commits and dispatches brainbug test runs |

---

## Day-to-day operations

These live in `.rhiza/docs/` and are synced into every Rhiza-managed project via the `core` bundle. You will find them in your own repo after syncing.

| Document | What it covers |
|----------|---------------|
| [WORKFLOWS.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/WORKFLOWS.md) | Recommended day-to-day development workflows: branching, dependency updates, debugging CI |
| [RELEASING.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/RELEASING.md) | Full release process: from `/rhiza:release` to a published PyPI package |
| [TOKEN_SETUP.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/TOKEN_SETUP.md) | How to create and configure a `PAT_TOKEN` for the release workflow and PR automation |
| [PRIVATE_PACKAGES.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/PRIVATE_PACKAGES.md) | Using private GitHub packages as dependencies in Rhiza-managed projects |

---

## Contributing to Rhiza

| Document | Repo | What it covers |
|----------|------|---------------|
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza/blob/main/CONTRIBUTING.md) | rhiza | How to contribute to the core template repo |
| [rhiza-claude README](https://github.com/Jebel-Quant/rhiza-claude/blob/main/README.md) | rhiza-claude | How to contribute to the `rhiza` plugin and its commands |
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/CONTRIBUTING.md) | rhiza-hooks | How to contribute pre-commit hooks |

---

**Back to:** [Lesson 11 — The Rhiza Ecosystem](./11-the-rhiza-ecosystem.md) | [README](../README.md)
