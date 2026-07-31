# Lesson 12 — Further Reading

The Rhiza repos contain detailed documentation beyond what fits in this curriculum. This lesson maps that material by topic so you can go deeper on whatever is most relevant to you.

Every link below was checked against the current `main` of each repo. Rhiza's own documentation moved into topic folders (`docs/guides/`, `docs/reference/`, `docs/development/`, `docs/ops/`) — if you have older bookmarks to flat `docs/*.md` paths, they will 404.

---

## Getting started and command usage

The primary interface is the `rhiza` plugin shipped by [`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude), documented on its [docs site](https://jebel-quant.github.io/rhiza-claude/) — a page per command.

| Document | What it covers |
|----------|---------------|
| [rhiza-claude docs](https://jebel-quant.github.io/rhiza-claude/) | Installing the marketplace and the full `/rhiza:*` command set, one page per command |
| [`jebel-quant/rhiza` README](https://github.com/Jebel-Quant/rhiza/blob/main/README.md) | The template repo itself — bundles, structure, and how the template files land in your project |
| [rhiza docs site](https://jebel-quant.github.io/rhiza/) | The same `docs/` tree below, rendered and searchable |

---

## Core reference

These live in [`rhiza/docs/`](https://github.com/Jebel-Quant/rhiza/tree/main/docs).

| Document | What it covers |
|----------|---------------|
| [guides/QUICK_REFERENCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/QUICK_REFERENCE.md) | Concise card of the most common Rhiza operations — good to bookmark |
| [reference/GLOSSARY.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/GLOSSARY.md) | Definitions of every term used in the Rhiza ecosystem |
| [reference/ARCHITECTURE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/ARCHITECTURE.md) | Visual diagrams of system components and how they interact |
| [reference/TOOLS_REFERENCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/TOOLS_REFERENCE.md) | Quick reference for all the external tools Rhiza-managed projects use (ruff, pytest, pre-commit, etc.) |
| [reference/BUNDLE_TAXONOMY.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/BUNDLE_TAXONOMY.md) | Every bundle and profile, how they layer, and which depends on which |
| [reference/DEPENDENCIES.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/DEPENDENCIES.md) | What the template depends on and why |
| [reference/WHY_NOT_COPIER_CRUFT.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/WHY_NOT_COPIER_CRUFT.md) | Why Rhiza is not Copier or Cruft — the design argument behind Lesson 4 |
| [troubleshooting.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/troubleshooting.md) | What to do when a sync, gate, or workflow misbehaves |

---

## Customisation and extension

| Document | Repo | What it covers |
|----------|------|---------------|
| [guides/CUSTOMIZATION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/CUSTOMIZATION.md) | rhiza | Makefile hooks, `custom-task.mk`, `custom-env.mk`, and the full menu of extension points |
| [guides/EXTENDING_RHIZA.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/EXTENDING_RHIZA.md) | rhiza | Comprehensive worked examples for extending Rhiza-based projects — patterns and best practices |
| [guides/DEMO.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/DEMO.md) | rhiza | A guided walkthrough of the template in action |

---

## Bundle-specific documentation

| Document | Bundle | What it covers |
|----------|--------|---------------|
| [development/DEVCONTAINER.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/DEVCONTAINER.md) | `devcontainer` | VS Code Dev Container and GitHub Codespaces configuration |
| [development/DOCKER.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/DOCKER.md) | `docker` | Dockerfile structure and container CI workflow |
| [development/MARIMO.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/MARIMO.md) | `marimo` | Marimo notebook conventions and folder layout |
| [development/PRESENTATION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/PRESENTATION.md) | `presentation` | Slide generation from Markdown using Marp |
| [development/TESTS.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/TESTS.md) | `tests` | The test layout the quality gate expects |
| [development/VSCODE_EXTENSIONS.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/development/VSCODE_EXTENSIONS.md) | `vscode` | The recommended editor extension set |
| [guides/BOOK.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/BOOK.md) | `book` | The MkDocs documentation site, its reports, and the coverage badge |
| [lfs/LFS.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/lfs/LFS.md) | `lfs` | Git LFS setup for repos carrying large files |

---

## Command reference

Each command has a dedicated page on the [rhiza-claude docs site](https://jebel-quant.github.io/rhiza-claude/). The eight below are the complete set as of `v0.6.1`.

| Document | Command | What it covers |
|----------|---------|---------------|
| [init](https://jebel-quant.github.io/rhiza-claude/commands/init/) | `/rhiza:init` | Make a folder rhiza-managed: write the pointer, add a skeleton and license, open PR #1. Syncs nothing |
| [update](https://jebel-quant.github.io/rhiza-claude/commands/update/) | `/rhiza:update` | Bump the ref, sync the template, resolve conflicts upstream-side, and open a PR of template-owned files |
| [quality](https://jebel-quant.github.io/rhiza-claude/commands/quality/) | `/rhiza:quality` | Run the code-quality gate and score the repo; optionally file findings as issues |
| [docs](https://jebel-quant.github.io/rhiza-claude/commands/docs/) | `/rhiza:docs` | Write or refresh `README.md`, `CLAUDE.md`, and `mkdocs.yml`, preserving hand-written prose |
| [release](https://jebel-quant.github.io/rhiza-claude/commands/release/) | `/rhiza:release` | Offer the legal next versions as a table, bump every declared location, regenerate `CHANGELOG.md`, commit and tag locally |
| [status](https://jebel-quant.github.io/rhiza-claude/commands/status/) | `/rhiza:status` | Validate the config and report the lock; `--files` for a tree, `--check` for whether you are behind |
| [uninstall](https://jebel-quant.github.io/rhiza-claude/commands/uninstall/) | `/rhiza:uninstall` | Delete every file the lock records and the lock itself; destructive, prompts unless `--force` |
| [maffay](https://jebel-quant.github.io/rhiza-claude/commands/maffay/) | `/rhiza:maffay` | A bonmot from a random Peter Maffay song |

> **Retired commands.** `/rhiza:validate` is now part of `/rhiza:status`, and `/rhiza:revisit` was renamed `/rhiza:docs`. `/rhiza:stats`, `/rhiza:repos` and `/rhiza:new` are gone. The version-matrix and coverage-badge logic that used to be user-run `rhiza-tools` commands lives inside the template's reusable CI workflows (`rhiza_ci.yml`), so there is nothing to invoke by hand.

---

## rhiza-hooks reference

| Document | What it covers |
|----------|---------------|
| [rhiza-hooks docs site](https://jebel-quant.github.io/rhiza-hooks/) | The hooks, rendered and searchable |
| [API reference](https://jebel-quant.github.io/rhiza-hooks/api-reference/) | A page per hook — `check_rhiza_config`, `check_makefile_targets`, `check_python_version`, `check_template_bundles`, `check_workflow_names`, `update_readme_help` — plus the shared internals |
| [rhiza-hooks README](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/README.md) | Installing the hooks and wiring them into `.pre-commit-config.yaml` |

---

## Operations and security

| Document | What it covers |
|----------|---------------|
| [operations/CI_ENFORCEMENT.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/operations/CI_ENFORCEMENT.md) | Which gates CI enforces, and what happens when one fails |
| [operations/CI_PERFORMANCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/operations/CI_PERFORMANCE.md) | Keeping the pipeline fast — caching and job layout |
| [ops/CHANGELOG_GUIDE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ops/CHANGELOG_GUIDE.md) | Conventional commits and how the changelog is generated |
| [ops/GLOBAL_PATCH.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ops/GLOBAL_PATCH.md) | Rolling one change across every managed repo at once |
| [ops/BRANCH_PROTECTION.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ops/BRANCH_PROTECTION.md) | The branch-protection settings the workflow assumes |
| [ops/TECHNICAL_DEBT.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ops/TECHNICAL_DEBT.md) | How debt is tracked rather than forgotten |
| [security/SECURITY_TESTING.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/security/SECURITY_TESTING.md) | The security scans in the template and how to read their output |

---

## Design decisions

Rhiza records its architectural decisions as ADRs, in [`docs/adr/`](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/README.md). They are the best available answer to "why is it like this?" — including several questions this curriculum raises.

| ADR | What it decides |
|-----|----------------|
| [0002](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0002-use-uv-for-python-package-management.md) | Use `uv` for Python package management — the background to Lesson 2 |
| [0004](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0004-adopt-modular-makefile-architecture.md) | Adopt a modular Makefile architecture — why `make.d/` exists |
| [0005](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0005-separate-rhiza-template-from-cli.md) | Separate the template from the CLI — the decision that eventually led to `rhiza-claude` |
| [0006](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0006-organise-templates-into-bundles.md) | Organise templates into bundles — the model taught in Lesson 5 |
| [0010](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0010-layered-bundle-profile-model.md) | The layered bundle and profile model |

---

## Cross-repo testing

| Document | Repo | What it covers |
|----------|------|---------------|
| [README.md](https://github.com/Jebel-Quant/rhiza-brainbug/blob/main/README.md) | rhiza-brainbug | The cross-repo test harness: how polling detects upstream commits and dispatches brainbug test runs |

---

## Day-to-day operations

Rhiza once shipped a `.rhiza/docs/` set — `WORKFLOWS.md`, `RELEASING.md`, `TOKEN_SETUP.md`, `PRIVATE_PACKAGES.md` — into every managed project. That folder is gone; the material that survived is in the template's own `docs/` tree, and the release mechanics are now the `/rhiza:release` command's business rather than a document you follow by hand.

| Document | What it covers |
|----------|---------------|
| [guides/QUICK_REFERENCE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/guides/QUICK_REFERENCE.md) | The common operations, releasing among them |
| [ops/CHANGELOG_GUIDE.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/ops/CHANGELOG_GUIDE.md) | Conventional commits, and how a release note is produced from them |
| [troubleshooting.md](https://github.com/Jebel-Quant/rhiza/blob/main/docs/troubleshooting.md) | Debugging a failed sync, gate, or workflow |
| [`/rhiza:release`](https://jebel-quant.github.io/rhiza-claude/commands/release/) | The release itself, start to finish |

---

## Contributing to Rhiza

Each repo keeps its contributor guide under `.rhiza/`, alongside the rest of its managed files — except `rhiza-claude`, which is a plugin marketplace rather than a managed project and keeps its own at the root.

| Document | Repo | What it covers |
|----------|------|---------------|
| [.rhiza/CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza/blob/main/.rhiza/CONTRIBUTING.md) | rhiza | How to contribute to the core template repo |
| [CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-claude/blob/main/CONTRIBUTING.md) | rhiza-claude | How to contribute to the `rhiza` plugin and its commands |
| [.rhiza/CONTRIBUTING.md](https://github.com/Jebel-Quant/rhiza-hooks/blob/main/.rhiza/CONTRIBUTING.md) | rhiza-hooks | How to contribute pre-commit hooks |

---

**Back to:** [Lesson 11 — The Rhiza Ecosystem](./11-the-rhiza-ecosystem.md) | [README](../README.md)
