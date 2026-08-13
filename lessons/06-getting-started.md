# Lesson 6 — Getting Started

This lesson walks you through setting up Rhiza in a new project from scratch.

## Prerequisites

You need:

- **[uv](https://docs.astral.sh/uv/)** — Rhiza's bundled scripts run on `uv`, and it is the tool runner behind every gate regardless of language. `/rhiza:init` also uses it to scaffold the project. Install it with:
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
/plugin marketplace add Jebel-Quant/rhiza-claude#v0.8.2
```

The plugin's bundled scripts are stdlib-only Python — there is no separate `rhiza` CLI to install. Everything you need beyond `uv`, `git`, and `make` comes from the plugin.

Once installed, you have the full `/rhiza:*` command set available. Getting running takes both of the first two: `/rhiza:init` makes the repo rhiza-managed, and `/rhiza:update` brings the template content in.

> **Bootstrapping is two pull requests, not one.** `/rhiza:init` writes the pointer that says which template you follow; `/rhiza:update`, run after that PR merges, is what actually delivers the CI workflows, the `Makefile` and the rest. The split is deliberate: it keeps `/rhiza:init` from re-implementing the sync and drifting from it, so there is exactly one code path that materializes template files. Expect PR #1 to look almost empty — that is correct.

## Step 2: Bootstrap your project (PR #1)

Navigate to your project directory and, in Claude Code, run:

```
/rhiza:init
```

`/rhiza:init` makes the current folder a rhiza-managed repo. If the folder already has an `origin`, it derives the host and slug from that URL. Otherwise it will ask you:

- **GitHub or GitLab** — this picks your project's profile, so a GitLab repo gets GitLab's CI
- **Owner, name, and visibility** for the repo
- **Language** — `python` (the default), `rust`, or `go`. This chooses both the language layer you sync and the profile you get: Python repos get `github-project`/`gitlab-project`, Rust gets `rust-local`, and Go gets `go-local`
- **Template repository** — `Jebel-Quant/rhiza` by default, or any `owner/repo` you name. That one template serves all three languages, layering `python-core`, `rust-core`, or `go-core` on the neutral `core`. It checks the template is reachable — and that it actually defines the profile it is about to write — before pointing at it, and pins its latest release as your starting `ref`

It then writes `.rhiza/template.yml` — the pointer, and the only Rhiza config file your project needs — adds a skeleton for the language you chose (`uv init --lib` plus the `pyproject.toml` shape the template's gates require, or a `Cargo.toml`, or a `go.mod`) and license metadata, and opens a PR on a `rhiza_init_<date>` branch titled `chore: make repo rhiza-managed`. It never pushes to your default branch.

The skeleton is not optional, and not decoration: the template ships no manifest of any kind, so without one the gates in step 4 fail outright — every `make` target that builds or tests needs a `pyproject.toml`, `Cargo.toml`, or `go.mod` to work with, and on Python the synced `.rhiza/tests/test_pyproject.py` asserts a specific `[project]` shape.

**What is deliberately not in PR #1:** no CI workflows, no `Makefile`, no `.rhiza/rhiza.mk`, no docs, and no gates were run. Your package is empty by design. Review the PR and merge it.

## Step 3: Pull in the template content (PR #2)

Once PR #1 is merged, run:

```
/rhiza:update
```

This is the sync. It reads `.rhiza/template.yml`, fetches every file the profile matches at the pinned ref, writes them into your project, records exactly what it materialized in `.rhiza/template.lock`, and opens a second PR — containing **only** template-owned files, never a blanket `git add --all`.

PR #2 is where the infrastructure shows up:

```
.github/workflows/rhiza_ci.yml
.pre-commit-config.yaml
ruff.toml
Makefile
.rhiza/rhiza.mk
.python-version
.editorconfig
```

Review that diff and merge it too. From here on, the same command is how you take every later template release — the mechanism described in Lesson 8.

## Step 4: Choose your bundles or profile

`/rhiza:init` picks your profile from the platform and language you chose, so there is nothing extra to select. `github-project` is the default for a Python repo on GitHub, and it expands to:

- `core` (always required, and language-neutral)
- `python-core` (the Python language layer: `install`/`all`, virtualenv, ruff, bandit, deptry)
- `github` (base GitHub Actions setup)
- `tests` (pytest, coverage — local tooling)
- `github-tests` (testing and security scan workflows on GitHub)
- `book` and `github-book` (the MkDocs documentation site and its publishing workflow)
- `marimo` and `github-marimo` (Marimo notebooks and their workflow)

GitLab projects get `gitlab-project`, the same shape with GitLab's CI. There is also a `local` profile — `core`, `python-core`, `book`, `marimo`, `tests` — for experiments and early-stage work with no hosted automation at all. Rust and Go repos get `rust-local` and `go-local`, which pair `core` with that language's layer and `book`; hosted CI for those two languages has not shipped yet.

Anything outside your profile is opt-in by editing `template.yml` and running `/rhiza:update`. `renovate`, for automated dependency updates, is the one most projects add first — it is a bundle in its own right, not part of any profile. To see every available bundle with its description and dependencies, browse the template repo's [`bundles/` directory](https://github.com/Jebel-Quant/rhiza/tree/main/bundles) or the [bundle taxonomy](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/BUNDLE_TAXONOMY.md).

## Step 5: Verify your setup

To check what Rhiza synced and confirm your configuration, ask in Claude Code:

```
/rhiza:status
```

One command answers both halves of the question. It validates that `.rhiza/template.yml` exists, parses, and is well-typed, then reports what `.rhiza/template.lock` says you actually got: template repository, pinned `ref`, synced commit SHA, timestamp, strategy, and the files materialized. Add `--files` to see those as a tree, or `--check` to find out whether a newer template release is out. Start here whenever something seems wrong — intent and outcome can disagree, and this is the command that shows you both.

Run `make help` to see all the Makefile targets now available — grouped by category: testing, quality, docs, releasing, and more.

Run `make install` to set up your development environment:

```bash
make install
```

This installs your project dependencies, wires up the commit hooks, and gets you ready to work. The hooks themselves are run by [`prek`](https://github.com/j178/prek) — a faster drop-in runner for the same `.pre-commit-config.yaml` — which `make fmt` invokes as `uvx prek run --all-files`.

## Applying later template updates

`/rhiza:init` is a one-time bootstrap; `/rhiza:update` is forever. Every later template release comes in exactly the way PR #2 did:

```
/rhiza:update
```

It bumps your `ref:` to the latest release (or one you name), syncs the changed template files, resolves conflicts by taking the upstream side, and opens a PR of template-owned files. This is the mechanism described in Lesson 8 — it replaces any older `sync` command.

`/rhiza:update` deliberately does **not** score your repo. It runs no quality gates, produces no scorecard, and files no issues; keeping the sync single-purpose is what lets it stay the one code path that writes template files. Those jobs belong to other commands:

| You want | Run |
|----------|-----|
| A quality scorecard, optionally filed as issues | `/rhiza:quality` |
| `README.md`, `CLAUDE.md`, `mkdocs.yml` written or refreshed | `/rhiza:docs` |
| To know what you have and whether you are behind | `/rhiza:status` |

## What you just got

Your project now has:

- **CI/CD workflows** that run on push and pull requests — automatically testing your code across multiple Python versions.
- **A modular Makefile** with targets for testing, linting, releasing, and more.
- **Commit hooks** that enforce code quality on every commit, run through `prek`.
- **A living-template link** to the upstream, kept current by running `/rhiza:update` when a new template version ships.

None of this required manual configuration. It came from the template, and it stays up to date via the update mechanism described in Lesson 8.

---

**Next:** [Lesson 7 — Configuring Your Template](./07-configuring-your-template.md)
