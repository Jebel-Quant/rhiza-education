# Lesson 11 — The Rhiza Ecosystem

The lessons so far have focused on the core workflow: configure `template.yml`, run `uvx rhiza sync`, review sync PRs. But Rhiza is one piece of a larger set of tools built around the same philosophy — automate the boring parts of running Python projects at scale. This lesson maps that ecosystem so you know what exists and when to reach for it.

## rhiza-cli — the CLI you have been using

[`rhiza-cli`](https://github.com/Jebel-Quant/rhiza-cli) is the package behind `uvx rhiza`. It is what you run directly:

| Command | What it does |
|---------|-------------|
| `uvx rhiza init` | Creates `.rhiza/template.yml` interactively |
| `uvx rhiza sync` | Fetches template files and writes them into the project |
| `uvx rhiza validate` | Validates `template.yml` syntax and checks that the referenced repo and ref exist |
| `uvx rhiza migrate` | Transitions projects from older Rhiza config layouts to the current `.rhiza/` folder structure |

You rarely need to install `rhiza-cli` globally — `uvx` handles it on demand. The Makefile target (`make sync`) calls `uvx rhiza` under the hood.

The `core` bundle also ships two Makefile targets that are useful for everyday diagnostics:

| Target | What it does |
|--------|-------------|
| `make doctor` | Validates your project and environment — required tools, Python version consistency, `.rhiza/` config |
| `make explain-bundles` | Lists all available bundles with descriptions, dependency relationships, and platform grouping |

Start with `make doctor` when something is wrong. Run `make explain-bundles` when you are planning which bundles to add.

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

These run locally on commit. The same checks also run in CI via the `rhiza_pre-commit.yml` workflow, so nothing slips through if someone bypasses the local hooks.

## rhiza-tools — release and project utilities

[`rhiza-tools`](https://github.com/Jebel-Quant/rhiza-tools) is a collection of utility commands that the Rhiza Makefile exposes as `make` targets. It installs as a plugin for `rhiza-cli`, so you can also call the commands directly as `rhiza tools <command>` (via `uvx "rhiza[tools]" tools <command>`), or standalone with `uvx rhiza-tools <command>`:

| Command | What it does |
|---------|-------------|
| `bump` | Bumps the version in `pyproject.toml` (major, minor, or patch) |
| `release` | Pushes a version tag to trigger the release workflow |
| `update-readme` | Refreshes the `make help` section in `README.md` |
| `generate-coverage-badge` | Produces a coverage badge JSON file from pytest-cov output |
| `version-matrix` | Reads `requires-python` from `pyproject.toml` and emits a JSON matrix for GitHub Actions |
| `analyze-benchmarks` | Processes pytest-benchmark results and generates an interactive HTML report |

Most of the time you will reach these through `make bump`, `make release`, and so on rather than calling `uvx rhiza-tools` directly. But knowing the underlying tool exists means you can call it in custom scripts or extend it.

## rhiza-config — Rhiza commands for Claude Code

[`rhiza-config`](https://github.com/Jebel-Quant/rhiza-config) is a [Claude Code](https://claude.com/claude-code) plugin marketplace. It ships the **`rhiza`** plugin — a set of slash commands that drive the whole sync-and-quality workflow from inside your AI coding assistant, so you do not have to remember the underlying `make` and `uvx` invocations.

Install it once:

```
/plugin marketplace add Jebel-Quant/rhiza-config
/plugin install rhiza@rhiza-config
```

The commands then appear namespaced under the plugin:

| Command | What it does |
|---------|-------------|
| `/rhiza:boost` | Bumps the repo to the latest (or a given) rhiza release, syncs the template, resolves conflicts, runs the quality gates, and opens a PR with a quality scorecard |
| `/rhiza:quality` | Runs the code-quality gate (lint, types, docs, deps, security, tests, complexity, architecture) and scores the repo |
| `/rhiza:revisit` | Creates or refreshes the repo's `README.md`, `CLAUDE.md`, and `mkdocs.yml` — refreshing badges and correcting drift while preserving hand-written prose |
| `/rhiza:stats` | Read-only statistics dashboard for the repo (lines of code, test ratio, stars, coverage, complexity, template status) |

Where `rhiza-cli` automates the mechanics of syncing, `rhiza-config` automates the *judgement* around it — deciding when to bump, scoring quality, and keeping docs honest — by handing those tasks to Claude Code with the right context baked in. It is optional: everything the plugin does can also be done by hand with the CLI and Makefile targets.

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
                                  │ sync PRs
                    ┌─────────────▼───────────────┐
                    │       your project           │
                    │  .rhiza/template.yml         │
                    └──┬──────────┬───────────────┘
                       │          │
          ┌────────────▼──┐  ┌───▼────────────────┐
          │  rhiza-cli    │  │   rhiza-hooks       │
          │  init         │  │   (pre-commit)      │
          │  sync         │  └────────────────────┘
          │  validate     │
          └────────────┬──┘
                       │
          ┌────────────▼──────────────────────────┐
          │            rhiza-tools                │
          │  bump · release · version-matrix      │
          │  coverage-badge · analyze-benchmarks  │
          └───────────────────────────────────────┘

   AI layer (optional):  rhiza-config   → /rhiza:boost · quality · revisit · stats
   Cross-repo testing:   rhiza-brainbug → contract/compatibility runs on upstream commits
```

At the top is the template repo (Rhiza). `rhiza-cli` is how you interact with it from inside a project. `rhiza-hooks` keeps the project valid on every commit. `rhiza-tools` handles the release and reporting tasks that the CI workflows call on. `rhiza-config` layers Claude Code slash commands over that workflow when you want the assistant to drive it, and `rhiza-brainbug` runs the compatibility tests that span multiple Rhiza projects.

---

**Next:** [Lesson 12 — Further Reading](./12-further-reading.md)
