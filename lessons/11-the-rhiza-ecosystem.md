# Lesson 11 — The Rhiza Ecosystem

The lessons so far have focused on the core workflow: configure `template.yml`, run `/rhiza:update`, review the resulting PR. But Rhiza is one piece of a larger set of tools built around the same philosophy — automate the boring parts of running Python projects at scale. This lesson maps that ecosystem so you know what exists and when to reach for it.

## rhiza-claude — the interface you have been using

[`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude) is a [Claude Code](https://claude.com/claude-code) plugin marketplace. It ships the **`rhiza`** plugin — the set of slash commands that drive the whole init-sync-quality workflow from inside your AI coding assistant. It is the primary way you interact with Rhiza today: the commands wrap the underlying mechanics, and their bundled scripts are stdlib-only Python, so there is no separate CLI to install. The plugin reads `.rhiza/template.lock` and `.rhiza/template.yml` directly.

Install it once:

```
/plugin marketplace add Jebel-Quant/rhiza-claude
/plugin install rhiza@rhiza-claude
```

Pin a version by appending a git tag: `/plugin marketplace add Jebel-Quant/rhiza-claude#v0.4.1`. The only prerequisites are `uv`, `git`, and `make`.

The commands appear namespaced under the plugin. The primary ones drive the day-to-day lifecycle:

| Command | What it does |
|---------|-------------|
| `/rhiza:init` | Bootstraps a rhiza-managed repo in the current folder — `git init` if needed, asks GitHub/GitLab, owner/name/visibility, language (Python or Go) and template repo, optionally scaffolds `pyproject.toml` + `src/` + `tests/` + `mkdocs.yml` + a starter README, validates, and opens a PR on a `rhiza_init_<date>` branch |
| `/rhiza:update` | Bumps the repo to the latest (or a given) rhiza release, syncs the template, resolves conflicts, runs the quality gates, and opens a PR with a quality scorecard — this is how you apply template changes |
| `/rhiza:quality` | Runs the code-quality gate (lint, types, docs, deps, security, tests, test-layout, complexity, architecture) and scores the repo; can file findings as issues |
| `/rhiza:revisit` | Creates or refreshes the repo's `README.md`, `CLAUDE.md`, and `mkdocs.yml` — refreshing badges and correcting drift while preserving hand-written prose |
| `/rhiza:stats` | Read-only statistics dashboard for the repo (lines of code, test ratio, stars, coverage, complexity, dependencies, template status); writes `docs/stats.html` |
| `/rhiza:repos` | Lists GitHub repos tagged with a rhiza topic (default `rhiza`) as JSON |
| `/rhiza:release` | Derives the next semantic version from the conventional commits since the last tag (via git-cliff), bumps `pyproject.toml`, regenerates `CHANGELOG.md`, then commits and tags locally — stopping before pushing |
| `/rhiza:new` | Scaffolds `src/<pkg>/<name>.py` plus its mirrored `tests/<pkg>/test_<name>.py`, keeping the 1:1 layout parity that `/rhiza:quality` enforces; never overwrites |

A second group of repo utilities is read-only (or destructive but explicit) and works straight off the lock file:

| Command | What it does |
|---------|-------------|
| `/rhiza:status` | Shows the sync status — template repository, ref, synced commit SHA, timestamp, and strategy; `--files`/`--tree` lists managed files, `--check` compares the pinned ref against the latest upstream release |
| `/rhiza:validate` | Validates that `.rhiza/template.yml` parses and its fields are well-typed; exits non-zero on failure |
| `/rhiza:uninstall` | Removes every file listed in `.rhiza/template.lock`, prunes emptied directories, and deletes the lock; destructive, so it prompts unless `--force` |

Start with `/rhiza:status` and `/rhiza:validate` when something looks wrong — the first tells you what was synced and whether you are behind, the second confirms your config is well-formed.

> Historically, the mechanics lived in two separate packages — `rhiza-cli` (the `uvx rhiza` command) and `rhiza-tools` (release and reporting utilities). Both are now archived: `rhiza-claude` supersedes the CLI, and the reporting/matrix logic moved inside the template's reusable CI workflows. You no longer run `uvx rhiza` or `uvx rhiza-tools` for anything.

## rhiza-hooks — pre-commit hooks

[`rhiza-hooks`](https://github.com/Jebel-Quant/rhiza-hooks) is a pre-commit hook repository. The `core` bundle includes a `.pre-commit-config.yaml` that pulls from it. The hooks run automatically on `git commit` and catch common mistakes before they hit CI:

| Hook | What it checks |
|------|---------------|
| `check-rhiza-config` | `template.yml` is valid and the referenced repo/ref can be resolved |
| `check-rhiza-workflow-names` | GitHub Actions workflow files follow the expected naming convention |
| `check-makefile-targets` | The Makefile exposes the targets CI depends on |
| `check-python-version-consistency` | `.python-version`, `pyproject.toml`, and CI matrix all agree on the Python version |
| `check-template-bundles` | The bundles listed in `template.yml` exist in the remote template repo |
| `update-readme-help` | Embeds the current `make help` output into the README automatically |

These run locally on commit. The template's CI enforces the equivalent quality gates as well, so nothing slips through if someone bypasses the local hooks.

## rhiza-brainbug — cross-repo test harness

[`rhiza-brainbug`](https://github.com/Jebel-Quant/rhiza-brainbug) solves a problem that appears once you have many interdependent Rhiza projects: **contract and compatibility tests that span more than one repo**. Rather than duplicating an integration test in every consumer, you write it once in brainbug.

Brainbug watches a list of repositories on a cron. When any branch of a watched repo gets a new commit, brainbug checks out that repo at that SHA and runs its own tests ("brainbugs") against the code. Nothing is installed in the monitored repos — it is pure polling, comparing each branch head against a stored state file and self-dispatching a run on any change.

This makes it the ecosystem's answer to "did my change break a downstream repo?" without wiring webhooks or CI triggers into every project.

## How the pieces fit together

```
                    ┌─────────────────────────────┐
                    │       template repo          │
                    │          (rhiza)             │
                    └─────────────┬───────────────┘
                                  │ template files
                    ┌─────────────▼───────────────┐
                    │        rhiza-claude          │
                    │  init · update · quality     │
                    │  revisit · stats · release   │
                    │  status · validate · …       │
                    └─────────────┬───────────────┘
                                  │ drives
                    ┌─────────────▼───────────────┐
                    │       your project           │
                    │  .rhiza/template.yml + .lock │
                    └──┬───────────────────────────┘
                       │
          ┌────────────▼────────┐
          │   rhiza-hooks       │
          │   (pre-commit)      │
          └─────────────────────┘

   Cross-repo testing:   rhiza-brainbug → contract/compatibility runs on upstream commits
```

At the top is the template repo (Rhiza). `rhiza-claude` is the interface layer: its slash commands materialize template files into your project, run the quality gates, and keep the docs honest — all driven from Claude Code. `rhiza-hooks` keeps the project valid on every commit, and `rhiza-brainbug` runs the compatibility tests that span multiple Rhiza projects.

---

**Next:** [Lesson 12 — Further Reading](./12-further-reading.md)
