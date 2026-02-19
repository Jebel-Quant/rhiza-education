# Lesson 6 — Getting Started

This lesson walks you through setting up Rhiza in a new project from scratch.

## Prerequisites

You need:

- **[uv](https://docs.astral.sh/uv/)** — Rhiza is distributed as a `uvx` tool. Install it with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **A GitHub account** with access to the template repository (`Jebel-Quant/rhiza` or your org's fork).
- **A new project repo** — an empty git repository on GitHub where you want Rhiza's config to land.

## Step 1: Initialise Rhiza in your project

Navigate to your project directory and run:

```bash
uvx rhiza init
```

Rhiza will ask you a few questions:

- Which template repository to use (default: `Jebel-Quant/rhiza`)
- Which version (ref) to pin to
- Which bundles you want

After you answer, it writes `.rhiza/template.yml` to your project. This is the only Rhiza config file your project needs.

> **Note:** `uvx rhiza init` does not write any template files yet. It only creates the config that tells Rhiza what to fetch. The next step does the actual fetching.

## Step 2: Choose your bundles

During `init`, you will be asked which bundles to include. For a typical Python project, a good starting point is:

- `core` (always required)
- `github` (CI/CD workflows — highly recommended)
- `tests` (pytest, coverage)
- `renovate` (automated dependency updates)

You can add more bundles later by editing `template.yml` and re-running `materialize`.

## Step 3: Materialise

Now fetch and apply the template files:

```bash
uvx rhiza materialize
```

Rhiza reads your `.rhiza/template.yml`, fetches all matching files from the template repository, and writes them into your project.

This will create files like:

```
.github/workflows/rhiza_ci.yml
.github/workflows/rhiza_pre-commit.yml
.github/workflows/rhiza_sync.yml
.pre-commit-config.yaml
ruff.toml
Makefile
.python-version
.editorconfig
```

Review the changes with `git diff --stat`, then commit them:

```bash
git add .
git commit -m "chore: initialise rhiza template"
```

## Step 4: Verify your setup

Run `make help` to see all the Makefile targets now available in your project. You should see targets grouped by category: testing, quality, docs, releasing, and more.

Run `make install` to set up your development environment:

```bash
make install
```

This installs your project dependencies, sets up pre-commit hooks, and gets you ready to work.

## What you just got

Your project now has:

- **CI/CD workflows** that run on push and pull requests — automatically testing your code across multiple Python versions.
- **A modular Makefile** with targets for testing, linting, releasing, and more.
- **Pre-commit hooks** that enforce code quality on every commit.
- **A sync workflow** (`rhiza_sync.yml`) that runs on a schedule and opens PRs when the template is updated.

None of this required manual configuration. It came from the template, and it will stay up to date via the sync mechanism described in Lesson 8.

---

**Next:** [Lesson 7 — Configuring Your Template](./07-configuring-your-template.md)
