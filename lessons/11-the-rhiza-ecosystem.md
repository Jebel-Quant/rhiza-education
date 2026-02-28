# Lesson 11 — The Rhiza Ecosystem

The lessons so far have focused on the core workflow: configure `template.yml`, run `uvx rhiza sync`, review sync PRs. But Rhiza is one piece of a larger set of tools built around the same philosophy — automate the boring parts of running Python (and Go) projects at scale. This lesson maps the full ecosystem so you know what exists and when to reach for it.

## rhiza-cli — the CLI you have been using

[`rhiza-cli`](https://github.com/Jebel-Quant/rhiza-cli) is the package behind `uvx rhiza`. It is what you run directly:

| Command | What it does |
|---------|-------------|
| `uvx rhiza init` | Creates `.rhiza/template.yml` interactively |
| `uvx rhiza sync` | Fetches template files and writes them into the project |
| `uvx rhiza validate` | Validates `template.yml` syntax and checks that the referenced repo and ref exist |
| `uvx rhiza migrate` | Transitions projects from older Rhiza config layouts to the current `.rhiza/` folder structure |

You rarely need to install `rhiza-cli` globally — `uvx` handles it on demand. The Makefile target (`make sync`) calls `uvx rhiza` under the hood.

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

[`rhiza-tools`](https://github.com/Jebel-Quant/rhiza-tools) is a collection of utility commands that the Rhiza Makefile exposes as `make` targets. You can also call them directly with `uvx rhiza-tools <command>`:

| Command | What it does |
|---------|-------------|
| `bump` | Bumps the version in `pyproject.toml` (major, minor, or patch) |
| `release` | Pushes a version tag to trigger the release workflow |
| `update-readme` | Refreshes the `make help` section in `README.md` |
| `generate-coverage-badge` | Produces a coverage badge JSON file from pytest-cov output |
| `version-matrix` | Reads `requires-python` from `pyproject.toml` and emits a JSON matrix for GitHub Actions |
| `analyze-benchmarks` | Processes pytest-benchmark results and generates an interactive HTML report |

Most of the time you will reach these through `make bump`, `make release`, and so on rather than calling `uvx rhiza-tools` directly. But knowing the underlying tool exists means you can call it in custom scripts or extend it.

## rhiza-go — the same pattern for Go projects

[`rhiza-go`](https://github.com/Jebel-Quant/rhiza-go) is a parallel template repository for Go projects. It provides the same living-template contract — a `ref`-pinned template repo with a sync workflow — but tailored to Go tooling:

- `.golangci.yml` for linting
- GitHub Actions and GitLab CI workflows
- Makefile with Go-specific targets
- Dev container configuration

If your organisation runs both Python and Go projects, you can use `rhiza` and `rhiza-go` side by side, with each project's `.rhiza/template.yml` pointing at the appropriate template repo.

## rhiza-manager — multi-repo VS Code workspace

[`rhiza-manager`](https://github.com/Jebel-Quant/rhiza-manager) is a VS Code extension for teams that work across many repositories simultaneously. It adds a sidebar panel that shows the status of every repo in your workspace at a glance:

- Pending CI workflows
- Open PRs (including Rhiza sync PRs waiting for review)
- Branch status and commit counts
- Dependency update alerts from Renovate

The extension is useful once you have five or more Rhiza-managed repos: instead of checking each repo individually in GitHub, you see everything in one place inside your editor.

## repo-monitor — repository dashboard desktop app

[`repo-monitor`](https://github.com/Jebel-Quant/repo-monitor) is an Electron desktop application that surfaces the same multi-repo information as rhiza-manager but outside of VS Code. It connects to GitHub via a personal access token and displays a live dashboard covering:

- Workflow status across all configured repos
- Open PRs, issues, and code quality signals
- Renovate dependency update state

It is useful for team leads or platform engineers who want a persistent overview without having VS Code open, or who prefer a standalone window for the monitoring view.

## marimushka — notebook publishing

[`marimushka`](https://github.com/Jebel-Quant/marimushka) is covered in [Appendix A2](./A2-marimushka.md). In ecosystem terms, it is the publishing layer for the `marimo` bundle — it converts `.py` marimo notebooks to static HTML and WebAssembly for deployment to GitHub Pages.

## How the pieces fit together

```
                    ┌─────────────────────────────┐
                    │       template repo          │
                    │   (rhiza or rhiza-go)        │
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
```

At the top is the template repo (Rhiza or a fork of it). `rhiza-cli` is how you interact with it from inside a project. `rhiza-hooks` keeps the project valid on every commit. `rhiza-tools` handles the release and reporting tasks that the CI workflows call on. `rhiza-manager` and `repo-monitor` give you visibility across all of this at the organisation level.

---

**Next:** [Lesson 12 — Further Reading](./12-further-reading.md)
