# Lesson 6 — Getting Started

This lesson walks you through setting up Rhiza in a new project from scratch.

## Prerequisites

You need:

- **[uv](https://docs.astral.sh/uv/)** — Rhiza's bundled scripts run on `uv`, and `/rhiza:init` uses it to scaffold the project. Install it with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **[Claude Code](https://docs.claude.com/en/docs/claude-code)** — Rhiza is driven from Claude Code via the `rhiza` plugin. This is the primary interface.
- **A GitHub account** with access to the template repository (`Jebel-Quant/rhiza` or your org's fork). Rhiza also supports GitLab.
- **A project directory** — a new or empty folder where you want Rhiza's config to land. `/rhiza:init` will run `git init` for you if the folder is not a repo yet.

## Step 1: Install the Rhiza plugin

Rhiza ships as a Claude Code plugin from the `rhiza-claude` marketplace. Inside Claude Code, add the marketplace and install the plugin once:

```
/plugin marketplace add Jebel-Quant/rhiza-claude
/plugin install rhiza@rhiza-claude
```

To pin a specific version, append a git tag when you add the marketplace:

```
/plugin marketplace add Jebel-Quant/rhiza-claude#v0.4.1
```

The plugin's bundled scripts are stdlib-only Python — there is no separate `rhiza` CLI to install. Everything you need beyond `uv`, `git`, and `make` comes from the plugin.

Once installed, you have the full `/rhiza:*` command set available. The two commands you will use to get running are `/rhiza:init` (first-time bootstrap) and `/rhiza:update` (later template updates).

## Step 2: Bootstrap your project

Navigate to your project directory and, in Claude Code, run:

```
/rhiza:init
```

`/rhiza:init` bootstraps a rhiza-managed repo in the current folder. It will ask you a few questions:

- **GitHub or GitLab** (it auto-detects an existing remote if there is one)
- **Owner, name, and visibility** for the repo
- **Language and template repository** — Python (default, `Jebel-Quant/rhiza`) or Go (`Jebel-Quant/rhiza-go`)

For a new Python project, it then scaffolds the standard skeleton — `pyproject.toml`, `src/<pkg>/`, `tests/`, a starter module and test, and optionally `mkdocs.yml` and a README — and writes `.rhiza/template.yml`, the single Rhiza config file your project needs.

## Step 3: Choose your bundles or profile

During `init`, you will be asked what to include. For most projects, choose the `github-project` profile — it expands to `core`, `github`, `tests`, `github-tests`, and `renovate`, which covers CI/CD, testing, and automated dependency updates in one step.

If you prefer to select bundles individually, the essentials are:

- `core` (always required)
- `github` (base GitHub Actions setup)
- `tests` (pytest, coverage — local tooling)
- `github-tests` (testing and security scan workflows on GitHub)
- `renovate` (automated dependency updates)

You can add more bundles later by editing `template.yml` and running `/rhiza:update`. To see every available bundle with its description and dependencies, browse the template repo's [`bundles/` directory](https://github.com/Jebel-Quant/rhiza/tree/main/bundles).

## Step 4: The first sync and its PR

`/rhiza:init` does the first template sync for you. It reads your `.rhiza/template.yml`, fetches all matching files from the template repository, writes them into your project, validates the config, and runs the test suite.

Crucially, it does **not** push these changes to your default branch. Instead it puts the scaffold and first sync on a `rhiza_init_<date>` branch and opens a pull request. This gives you a review step before any Rhiza-managed files land on `main`.

The PR will introduce files like:

```
.github/workflows/rhiza_ci.yml
.pre-commit-config.yaml
ruff.toml
Makefile
.python-version
.editorconfig
```

Review the PR diff, then merge it when you are happy.

## Step 5: Verify your setup

To check what Rhiza synced and confirm your configuration, use the plugin's read-only utilities in Claude Code:

```
/rhiza:status
/rhiza:validate
```

`/rhiza:status` shows the template repository, pinned `ref`, the synced commit SHA, the sync timestamp, and the files that were materialized (it reads `.rhiza/template.lock`). `/rhiza:validate` confirms your `.rhiza/template.yml` parses and its fields are well-typed. Start here whenever something seems wrong.

Run `make help` to see all the Makefile targets now available — grouped by category: testing, quality, docs, releasing, and more.

Run `make install` to set up your development environment:

```bash
make install
```

This installs your project dependencies, sets up pre-commit hooks, and gets you ready to work.

## Applying later template updates

`/rhiza:init` is a one-time bootstrap. Once your repo is rhiza-managed, you pull in new template versions with:

```
/rhiza:update
```

`/rhiza:update` bumps your `ref:` to the latest rhiza release, syncs the changed template files, resolves conflicts against the template upstream, runs the quality gates, and opens a PR with a quality scorecard. This is the mechanism described in Lesson 8 — it replaces any older `sync` command.

## What you just got

Your project now has:

- **CI/CD workflows** that run on push and pull requests — automatically testing your code across multiple Python versions.
- **A modular Makefile** with targets for testing, linting, releasing, and more.
- **Pre-commit hooks** that enforce code quality on every commit.
- **A living-template link** to the upstream, kept current by running `/rhiza:update` when a new template version ships.

None of this required manual configuration. It came from the template, and it stays up to date via the update mechanism described in Lesson 8.

---

**Next:** [Lesson 7 — Configuring Your Template](./07-configuring-your-template.md)
