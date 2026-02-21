# Book Plan: Python DevOps

## Title

**Python DevOps: Building and Maintaining Software at Scale**

*Subtitle: From a clean repo to a production pipeline — and keeping it that way*

---

## Positioning

**Target reader:** A Python developer with 1–3 years of experience who writes working code but has not yet built or owned a CI/CD pipeline. They know how to push to GitHub. They do not know why their colleague's machine runs the tests differently, how releases happen, or what "production" actually means.

**What this book is not:** A cloud platform tutorial. A Docker manual. A general DevOps textbook. It is a Python-first, tool-specific guide to the practices and infrastructure that make Python projects maintainable at team scale.

**Distinguishing angle:** Most DevOps books treat Python as an incidental scripting language. Most Python books stop at "how to write good code." This one treats the *operational life* of a Python project — packaging, CI, releases, dependency hygiene, template maintenance — as a first-class topic.

---

## Structure Overview

| Part | Title | Chapters | Est. pages |
|------|-------|----------|-----------|
| I | Foundations | 1–2 | 30 |
| II | Local Discipline | 3–5 | 45 |
| III | CI and Release | 6–9 | 60 |
| IV | Keeping It Alive | 10–12 | 45 |
| Appendices | — | A–C | 20 |
| **Total** | | **12 + 3** | **~200** |

---

## Part I — Foundations

### Chapter 1: Project Anatomy

Everything needed to understand the rest of the book: how a Python project is structured, where configuration lives, and what tools expect to find where.

- `pyproject.toml` (PEP 621): project metadata, dependencies, tool configuration — the single source of truth
- The `src` layout: why it prevents a class of import bugs that flat layouts produce
- `tests/`, `.github/`, `.python-version` — the supporting cast
- What a complete, empty project looks like before a line of business logic is written
- Git as infrastructure: commits as intent, tags as release markers, PRs as the unit of review and automation

### Chapter 2: The DevOps Mindset

Why "DevOps" is not a job title and what it actually costs to skip these practices.

- The lifecycle of a Python project: from first commit to retired service
- "Works on my machine" as a process failure, not a mystery
- The repo zoo: what happens when twenty repos each drift from a shared standard
- Automation as a multiplier: one hour invested, ten saved
- The feedback loop: fast CI, no surprises on release day, boring deployments as the goal

---

## Part II — Local Discipline

### Chapter 3: Package Management with uv

`uv` has replaced pip, pip-tools, venv, and pyenv for most Python workflows.

- Managing Python versions with `uv`
- `uv sync`, `uv add`, `uv remove`: the dependency lifecycle
- `uv.lock`: what it is, why it matters, and when to commit it
- `uvx`: running tools without installing them globally
- Migrating a project from pip + requirements.txt

### Chapter 4: Code Quality — Linting, Formatting, and Hooks

Code style is a communication protocol. Enforce it at the commit boundary, not in review comments.

- Ruff: the single tool that replaces flake8, isort, pyupgrade, and more
- `ruff.toml`: choosing rule sets, disabling what doesn't fit, tuning for existing codebases
- Pre-commit: catching problems before they reach CI
- A minimal `.pre-commit-config.yaml`: Ruff, trailing whitespace, YAML/TOML validation, secret detection
- Running the same checks in CI: the pre-commit workflow

### Chapter 5: Testing with pytest

Tests are executable specifications that make refactoring safe. They are also the foundation of CI.

- pytest fundamentals: fixtures, parametrize, markers
- Test layout: `tests/unit/`, `tests/integration/`, `conftest.py`
- Coverage: what to measure and what not to target
- Testing side effects: patching, temporary files, environment variables
- Naming conventions: what a failing test should tell you without reading the source

---

## Part III — CI and Release

### Chapter 6: CI/CD Concepts and GitHub Actions

The vocabulary, mental model, and platform behind every workflow in this book.

- Pipelines, jobs, steps, triggers, runners — the universal model
- GitHub Actions: workflows as YAML files in `.github/workflows/`
- A complete, annotated minimal CI workflow: checkout, install, lint, test
- Secrets and environment variables: how sensitive values reach workflows safely
- Reading CI results: green, red, and the log that explains the difference

### Chapter 7: The Test Matrix and Security Scanning

Running tests across Python versions and catching vulnerabilities automatically.

- `strategy.matrix`: running the same job across multiple Python versions in parallel
- Dynamic matrices from `pyproject.toml` using `rhiza-tools version-matrix`
- Caching dependencies: making CI fast
- Dependency vulnerability scanning: `pip-audit` and Renovate
- Secret detection and static security analysis (Bandit, Semgrep) as blocking checks

### Chapter 8: Packaging and Publishing

Getting a package to users — and doing it safely and repeatably.

- What a wheel is and why it is the right distribution format
- `uv build`: building and inspecting the result locally
- PyPI and TestPyPI: when to use each
- OIDC Trusted Publishing: releasing without a stored token
- Yanking a bad release: the procedure and the etiquette

### Chapter 9: Release Pipelines

The automated path from merged PR to published software.

- Semantic versioning: what each part promises
- `rhiza-tools bump`: mechanical version increments without human error
- The tag-push trigger: why releases start with a git tag
- The release workflow: build → publish → GitHub Release, in one automated job
- Changelogs: conventional commits and automated generation

---

## Part IV — Keeping It Alive

### Chapter 10: Dependency Maintenance

Dependencies decay. Staying current is a process, not a task.

- The cost of outdated dependencies: CVEs, breaking changes, Python EOL
- `uv.lock` and reproducible installs across time
- Renovate: automated PRs for every dependency update
- `renovate.json`: the essential configuration — grouping, automerge, schedules
- The Dependency Dashboard: one view of all pending updates across all repos

### Chapter 11: Template Systems and the Repo Zoo

What to do when "update the CI workflow" means touching twenty repos.

- The Day 0 / Day 365 gap: scaffolding tools solve the wrong problem
- Drift as the default: how repos diverge without a sync mechanism
- The PR model: updates as proposals, not pushes
- Rhiza: `template.yml`, bundles, the sync loop, and the `exclude:` list
- Rolling out across an existing organisation: one repo at a time

### Chapter 12: Production Essentials

Visibility, secrets, and the minimum security posture a deployed Python project needs.

- Structured logging: what to emit, at what level, and where it goes
- The four golden signals: latency, traffic, errors, saturation
- Secrets management: never in code, never in logs, rotation schedules
- Least-privilege in CI: minimal permissions, OIDC everywhere, pinned action SHAs
- Responding to a security finding: disclosure → patch → publish

---

## Appendices

### Appendix A: Tool Quick-Reference Cards

One page per tool: `uv`, `ruff`, `pytest`, `pre-commit`, GitHub Actions, Renovate.

### Appendix B: `pyproject.toml` Reference

Every field used in this book, with examples and PEP cross-references.

### Appendix C: Checklists

**New project:** the complete sequence from `uv init` to first release.
**Existing project:** adopting these practices without disrupting what's already working.

---

## Relation to Rhiza Education

The Rhiza education curriculum covers a subset of this material from the Rhiza-first perspective. This book is the standalone treatment for readers who arrive without a Rhiza context. Chapters 2, 6, 10, and 11 correspond directly to existing curriculum material and can be developed in parallel.
