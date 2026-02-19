# Lesson 9 — Further Reading

The Rhiza repos contain detailed documentation beyond what fits in this curriculum. This lesson maps that material by topic so you can go deeper on whatever is most relevant to you.

All links point directly to the Markdown source on GitHub. Every file listed here has been verified to exist.

---

## Getting started and CLI usage

These live in [`rhiza-cli`](https://github.com/Jebel-Quant/rhiza-cli) alongside the source code.

| Document | What it covers |
|----------|---------------|
| [GETTING_STARTED.md](https://github.com/Jebel-Quant/rhiza-cli/blob/main/GETTING_STARTED.md) | End-to-end walkthrough of adopting Rhiza in a new project — the narrative version of Lesson 4 |
| [CLI.md](https://github.com/Jebel-Quant/rhiza-cli/blob/main/CLI.md) | One-page command reference: every flag and subcommand with examples |
| [USAGE.md](https://github.com/Jebel-Quant/rhiza-cli/blob/main/USAGE.md) | Practical tutorials and real-world usage patterns, including edge cases |

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
| [MARIMO.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/MARIMO.md) | `marimo` | Marimo notebook conventions, folder layout, and publishing via marimushka |
| [PRESENTATION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/PRESENTATION.md) | `presentation` | Slide generation from Markdown using Marp |
| [GH_AW.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/GH_AW.md) | — | GitHub Agentic Workflows: AI-driven repository automation built into the Rhiza template |

---

## rhiza-tools command reference

Each command in [`rhiza-tools`](https://github.com/Jebel-Quant/rhiza-tools) has a dedicated doc in [`docs/commands/`](https://github.com/Jebel-Quant/rhiza-tools/tree/main/docs/commands).

| Document | Command | What it covers |
|----------|---------|---------------|
| [bump.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/bump.md) | `rhiza-tools bump` | Semantic version bumping in `pyproject.toml` |
| [release.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/release.md) | `rhiza-tools release` | Pushing a release tag to trigger the release workflow |
| [version_matrix.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/version_matrix.md) | `rhiza-tools version-matrix` | Extracting Python versions from `pyproject.toml` for CI matrices |
| [generate_coverage_badge.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/generate_coverage_badge.md) | `rhiza-tools generate-coverage-badge` | Producing a shields.io-compatible badge from coverage output |
| [analyze_benchmarks.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/analyze_benchmarks.md) | `rhiza-tools analyze-benchmarks` | Processing pytest-benchmark results into an interactive HTML report |
| [update_readme.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/update_readme.md) | `rhiza-tools update-readme` | Embedding `make help` output into `README.md` |
| [rollback.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/commands/rollback.md) | `rhiza-tools rollback` | Rolling back a release tag |
| [configuration.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/docs/configuration.md) | — | The `.rhiza/.cfg.toml` configuration file and bump-my-version integration |

---

## rhiza-hooks reference

| Document | What it covers |
|----------|---------------|
| [ARCHITECTURE.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/docs/ARCHITECTURE.md) | How the hooks are structured and how they interact with pre-commit |
| [QUICK_REFERENCE.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/docs/QUICK_REFERENCE.md) | All available hooks, their IDs, and what they check |

---

## Day-to-day operations

These live in `.rhiza/docs/` and are synced into every Rhiza-managed project via the `core` bundle. You will find them in your own repo after materialising.

| Document | What it covers |
|----------|---------------|
| [WORKFLOWS.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/WORKFLOWS.md) | Recommended day-to-day development workflows: branching, dependency updates, debugging CI |
| [RELEASING.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/RELEASING.md) | Full release process: from `make bump` to a published PyPI package |
| [TOKEN_SETUP.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/TOKEN_SETUP.md) | How to create and configure a `PAT_TOKEN` for the sync and release workflows |
| [PRIVATE_PACKAGES.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/docs/PRIVATE_PACKAGES.md) | Using private GitHub packages as dependencies in Rhiza-managed projects |

---

## Contributing to Rhiza

| Document | Repo | What it covers |
|----------|------|---------------|
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza/blob/main/CONTRIBUTING.md) | rhiza | How to contribute to the core template repo |
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-cli/blob/main/CONTRIBUTING.md) | rhiza-cli | How to contribute to the CLI |
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-tools/blob/main/CONTRIBUTING.md) | rhiza-tools | How to contribute utilities |
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/CONTRIBUTING.md) | rhiza-hooks | How to contribute pre-commit hooks |

---

**Back to:** [Lesson 8 — The Rhiza Ecosystem](./08-the-rhiza-ecosystem.md) | [README](../README.md)
