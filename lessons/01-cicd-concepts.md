# Lesson 1 — CI/CD Concepts

Rhiza exists to manage the files that make up a project's CI/CD pipeline. To get the most out of it, you need a solid mental model of what CI/CD is and how the pieces fit together. This lesson covers the concepts you will encounter throughout the curriculum.

If you already work with GitHub Actions daily, skim this as a vocabulary check. If you are newer to CI/CD, read it carefully — the rest of the lessons will assume it.

## What CI/CD is

**Continuous Integration (CI)** is the practice of automatically building and testing your code every time a change is pushed. The goal is to find problems immediately, when the context is fresh and the fix is small, rather than at the end of a sprint when changes have accumulated.

**Continuous Delivery (CD)** extends this: once code passes CI, it can be automatically delivered — published to PyPI, deployed to a server, pushed to a staging environment — without manual steps.

Together they form a pipeline:

```
developer pushes code
        │
        ▼
   CI: build & test
        │
        ▼ (if tests pass)
   CD: publish / deploy
```

The key word is *automatic*. CI/CD replaces the "works on my machine" problem with a reproducible, audited process that runs the same way every time.

## The pipeline model

Every CI/CD system organises work into the same basic hierarchy:

**Pipeline / Workflow**
The top-level unit. A pipeline is triggered by an event (a push, a pull request, a schedule) and runs one or more jobs.

**Job**
A self-contained unit of work that runs on a single machine (a *runner*). Jobs in the same pipeline can run in parallel or in sequence. A typical setup has a `test` job and a `publish` job, where `publish` only runs after `test` passes.

**Step**
A single command or action inside a job. Steps run sequentially within a job and share the same filesystem.

**Action / Task**
A reusable piece of step logic. In GitHub Actions these are published to the marketplace (e.g. `actions/checkout`, `astral-sh/setup-uv`). In GitLab CI they are called `includes` or referenced scripts.

```
Workflow
└── Job: test
│   ├── Step: checkout code
│   ├── Step: install uv
│   ├── Step: uv sync
│   └── Step: pytest
└── Job: publish
    ├── Step: checkout code
    ├── Step: build wheel
    └── Step: publish to PyPI
```

## GitHub Actions

GitHub Actions is the CI/CD system built into GitHub. Workflows are YAML files stored in `.github/workflows/`. Each file is one workflow.

### Triggers (`on:`)

The `on:` key defines what starts the workflow:

```yaml
on:
  push:
    branches: [main]        # runs on every push to main
  pull_request:             # runs on every PR
  schedule:
    - cron: '0 9 * * 1'    # runs every Monday at 09:00 UTC
  workflow_dispatch:        # allows manual triggering from the GitHub UI
```

Rhiza's CI workflow (`rhiza_ci.yml`) triggers on `push` and `pull_request`. The sync workflow (`rhiza_sync.yml`) uses `schedule`.

### Runners

Runners are the machines that execute jobs. GitHub provides hosted runners:

| Label | Machine |
|-------|---------|
| `ubuntu-latest` | Linux — fastest, cheapest, most common |
| `macos-latest` | macOS — needed for macOS-specific testing |
| `windows-latest` | Windows — slower, needed for cross-platform libraries |

Rhiza templates use `ubuntu-latest` by default.

### Jobs and dependencies

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - ...

  publish:
    runs-on: ubuntu-latest
    needs: test          # only runs if 'test' succeeds
    if: startsWith(github.ref, 'refs/tags/')  # only on tags
    steps:
      - ...
```

The `needs:` key creates a dependency. The `if:` key adds a condition. Together they express "run publish only when test passes and only when this is a tag push" — the standard release pattern.

### Matrix builds

A matrix lets you run the same job across multiple configurations simultaneously:

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

This runs three parallel jobs — one per Python version — and reports each as a separate check. Rhiza's `rhiza_ci.yml` builds this matrix dynamically from the `requires-python` field in `pyproject.toml` using `uvx rhiza-tools version-matrix`.

### Secrets and environment variables

Sensitive values (API tokens, passwords) are stored as *secrets* in the repository settings and injected into the workflow at runtime:

```yaml
- name: Publish to PyPI
  env:
    PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
  run: uv publish
```

Secrets are masked in logs — they never appear in plain text. Rhiza's release workflow uses `PYPI_TOKEN` for PyPI publishing on GitHub, and a `PAT_TOKEN` for the sync workflow (which needs permission to open pull requests).

### Artifacts and Pages

A job can upload files as *artifacts* that other jobs (or humans) can download:

```yaml
- uses: actions/upload-pages-artifact@v3
  with:
    path: site/
```

A subsequent deploy job then picks up that artifact and pushes it to GitHub Pages. This is the pattern used by Rhiza's `book` bundle (API docs), `marimo` bundle (notebooks), and by this very site.

### Permissions

By default, a workflow's `GITHUB_TOKEN` has read-only access. Jobs that need to write — opening PRs, pushing to Pages, creating releases — must declare their permissions explicitly:

```yaml
permissions:
  contents: write      # create releases, push tags
  pages: write         # deploy to GitHub Pages
  id-token: write      # OIDC for PyPI Trusted Publishing
  pull-requests: write # open sync PRs
```

Rhiza's templates set the minimal permissions needed for each workflow.

## The release pipeline in practice

A typical Rhiza-managed project has this release flow:

1. Developer runs `make bump` (calls `uvx rhiza-tools bump patch`) to increment the version in `pyproject.toml`.
2. Developer runs `make release` (calls `uvx rhiza-tools release`) to create and push a git tag (e.g. `v1.2.3`).
3. The tag push triggers the `rhiza_release.yml` workflow.
4. The workflow builds a wheel, publishes to PyPI using OIDC Trusted Publishing (no token stored), and creates a GitHub Release.

Every step is audited in the Actions tab. If a publish fails, the log shows exactly why.

## What Rhiza gives you

Rhiza's template bundles wire all of this up so you do not have to:

| Bundle | What it provides |
|--------|-----------------|
| `core` | Makefile with `make test`, `make lint`, `make bump`, `make release` |
| `github` | All workflow files: CI, pre-commit, sync, release, Renovate |
| `tests` | pytest config, coverage reporting, coverage badge publishing |
| `book` | API documentation build and Pages deployment |
| `marimo` | Notebook export and Pages deployment |
| `devcontainer` | Ready-to-use development environment for VS Code / Codespaces |

When you run `uvx rhiza sync`, you get a fully wired CI/CD pipeline committed to your repo. The rest of the curriculum explains how to configure, extend, and keep it up to date.

---

**Next:** [Lesson 2 — uv and uvx](./02-uv-and-uvx.md)
