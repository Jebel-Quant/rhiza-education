# Lesson 5 — Core Concepts

Before you run any commands, it helps to have a clear picture of the moving parts. This lesson walks through the key abstractions in Rhiza.

## The three actors

Every Rhiza setup involves three things:

**1. The template repository**

This is a GitHub repo that holds the canonical versions of shared infrastructure files: CI workflows, a Makefile, linting config, commit hooks, and so on. The canonical template repo is `Jebel-Quant/rhiza`, but you can fork it and use your own.

**2. The downstream project**

This is your actual project repo. It declares what it wants from the template repo via a config file (`.rhiza/template.yml`). The downstream project does not duplicate the template — it just consumes specific files from it.

**3. The syncer**

This is the sync engine, driven by `/rhiza:update` from the `rhiza-claude` Claude Code plugin. It reads the downstream project's config (`.rhiza/template.yml`), fetches the specified files from the template repo at the specified version, writes them into the project, and records what it synced — repository, ref, commit SHA, timestamp, strategy, and file paths — in `.rhiza/template.lock`.

## The config file: `.rhiza/template.yml`

Every downstream project has exactly one Rhiza config file. Here is what it looks like:

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza   # Which template repo to sync from
ref: v1.7.1                      # Which version of the template to use
language: python                 # Which language layer this repo uses

profiles:                         # Curated bundle preset (recommended)
  - github-project

exclude: |                        # Files to never overwrite locally
  .rhiza/scripts/customisations/*
```

- `repository` — any GitHub repo, not just the canonical Rhiza repo.
- `ref` — a tag or branch name. Tags are recommended because they enable automated version tracking (more on this in Lesson 8).
- `language` — `python`, `rust`, or `go`. Written by `/rhiza:init`, it records which language layer the repo follows. Since v1.3.0 the template is multi-language, and exactly one language layer belongs in a repo.
- `profiles` — a curated preset that expands to a sensible bundle selection. `github-project` gives you `core`, `python-core`, `github`, `book`, `github-book`, `github-marimo`, and `github-tests`. This is the recommended starting point. There are five profiles — `github-project`, `gitlab-project`, `local`, `rust-local`, and `go-local` — and `renovate` belongs to none of them, so projects that want automated dependency updates add that bundle by hand.
- `templates` — explicit list of named bundles, for when you need finer control than a profile offers.
- `include` — explicit glob patterns for files not covered by a bundle (optional).
- `exclude` — glob patterns that protect files from being overwritten by the sync. Patterns match **destination** paths — where a file lands in your repo — not the path it has inside the template.

## Bundles

Listing every file path in `include` by hand gets tedious. Rhiza provides **bundles**: named groups of files with sensible defaults. Bundles come in three kinds:

**`core` and the language layers.** Since v1.3.0, `core` is deliberately language-neutral: a thin `Makefile` front door, editor and changelog config, and `uv`/`uvx` as a tool runner. It defines no `install` and no `all`, so it is not a working repo on its own. Exactly one **language layer** supplies those, which is what lets a shared CI workflow ask for `install` without knowing what language it is building.

> **The tasks are no longer synced.** Up to v1.3.x, `core` shipped `.rhiza/rhiza.mk` plus a `make.d/` fragment per feature — around 1,500 lines of make copied into every consumer. Since **v1.4.0** those live in a pinned Python package, [`rhiza-task`](https://github.com/Jebel-Quant/rhiza-task), run per invocation by `uvx`. The documented interface is `uv run rhiza-task <task>`; the `Makefile` that `core` still ships is a 71-line compatibility shim that pins `RHIZA_TASK`, bootstraps `uv` if the runner has none, and forwards every unmatched target to the CLI. `make test` still works — because `test` is a *task*, not because anything in the file mentions it. The reasoning is [ADR-0011](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0011-replace-the-synced-make-layer-with-a-pinned-cli.md), which supersedes ADR-0004.

| Bundle | What it includes | Requires |
|--------|-----------------|----------|
| `core` | `Makefile` shim (pins `RHIZA_TASK`), `.editorconfig`, `cliff.toml`, uv as tool runner — language-neutral | — |
| `python-core` | Python layer: virtualenv and `uv sync`, `.python-version`, `ruff.toml`, `.bandit`, `.pre-commit-config.yaml`, deptry and licence scans | `core` |
| `rust-core` | Rust layer: rustup and `cargo fetch`, `rust-toolchain.toml`, `rustfmt.toml`, `clippy.toml`, `deny.toml`, clippy/nextest/llvm-cov gates | `core` |
| `go-core` | Go layer: `go mod download`, `.golangci.yml`, `revive.toml`, a `version.Version` constant for the release flow, go test/govulncheck gates | `core` |

**Feature bundles** — local tooling only, no CI/CD. They work independently of any platform.

| Bundle | What it includes | Requires |
|--------|-----------------|----------|
| `book` | The MkDocs documentation site, its reports, notebooks and the coverage badge | `core` |
| `benchmarks` | Performance testing infrastructure (`pytest-benchmark` and reporting) | `core`, `python-core` |
| `docker` | Dockerfile and container configuration | — |
| `devcontainer` | VS Code / GitHub Codespaces dev container | — |
| `vscode` | Recommended VS Code extensions and workspace settings | — |
| `presentation` | Slide generation from Markdown (via Marp) | — |
| `lfs` | Git Large File Storage configuration | — |
| `legal` | Licence headers and IP notice files | — |
| `renovate` | Automated dependency update config | — |

> **Bundles you may read about elsewhere are gone.** `tests`, `marimo` and `paper` no longer exist as standalone bundles. Their *configuration* moved into the bundle that already owned it — pytest and coverage settings are `python-core`'s, notebooks and the docs site are `book`'s — and their *tasks* were never files to begin with once the make layer retired. LaTeX papers are now the `github-paper` overlay alone. There are **26 bundles** in v1.7.1, down from the longer list earlier material shows.

**Platform overlay bundles** — layer CI/CD workflows on top of a feature bundle. Each overlay is named `<platform>-<feature>`:

| Bundle | What it adds |
|--------|-------------|
| `github` | Base GitHub Actions setup (sync, release, dependabot) |
| `github-tests` | Testing and security scan workflows on GitHub |
| `github-book` | Documentation publication workflow on GitHub |
| `github-docker` | Docker image build and publish on GitHub |
| `github-marimo` | Notebook hosting workflow on GitHub |
| `github-devcontainer` | Dev container image build on GitHub |
| `github-paper` | LaTeX compilation, and the PDF published to the `paper` branch |
| `github-quality-review` | Advisory Claude design review of PR diffs (opt-in) |
| `gitlab` | Base GitLab CI/CD setup |
| `gitlab-tests` | Testing workflows on GitLab |
| `gitlab-book` | Documentation publication workflow on GitLab |
| `gitlab-marimo` | Notebook hosting workflow on GitLab |
| `gitlab-quality-review` | Advisory Claude design review of MR diffs (opt-in) |

**Profiles** are curated presets that expand to a sensible combination of bundles for common setups. For most projects, start with a profile rather than listing bundles individually:

| Profile | Expands to |
|---------|-----------|
| `github-project` | `core`, `python-core`, `github`, `book`, `github-book`, `github-marimo`, `github-tests` |
| `gitlab-project` | `core`, `python-core`, `gitlab`, `book`, `gitlab-book`, `gitlab-marimo`, `gitlab-tests` |
| `local` | `core`, `python-core`, `book` — everything local, no hosted workflows |
| `rust-local` | `core`, `rust-core`, `book` |
| `go-local` | `core`, `go-core`, `book` |

Each Python platform profile is the `local` set plus that platform's CI overlays, which is why switching between GitHub and GitLab changes the workflows and nothing else. Rust and Go currently have local-only profiles: hosted CI for those languages is not yet part of the template, so `rust-github-project` and `go-github-project` do **not** exist. Note also that `renovate` is in **no** profile: automated dependency updates are opt-in, added as a bundle when you want them (Lesson 9).

Browse the `bundles/` directory in the template repo, or the [bundle taxonomy](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/BUNDLE_TAXONOMY.md), to see the full list with dependency information. Every bundle resolves its own dependencies, so selecting `github-tests` pulls in `core`, `python-core`, and `github` automatically. `core` plus one language layer is the minimum; all others are optional.

## The sync loop

The fundamental operation is:

```
fetch → diff → review → commit
```

1. **Fetch**: Rhiza reads your `template.yml` and pulls the matching files from the template repo at the specified `ref`.
2. **Diff**: It compares what it fetched against what is currently in your project.
3. **Review**: If anything changed, a pull request is opened with the diff. Scoring the repo is `/rhiza:quality`'s job, not the sync's.
4. **Commit**: You review the PR and merge it — or reject it if the change doesn't apply to your project.

This loop is human-initiated. You run `/rhiza:update` in Claude Code, which bumps the `ref` to the latest release, materializes the changed files, resolves conflicts against the template, and opens the PR for you to review. There is no longer an automated CI workflow that materializes template files — a person drives every update.

## Version pinning and automated updates

The `ref:` field in `template.yml` pins your project to a specific version of the template. When the template repo releases a new version, Renovate — a dependency automation tool — detects the new tag and opens a PR in your project that bumps `ref: v1.7.0` to `ref: v1.7.1`. That PR is a *notification* that a newer template exists; merging it no longer triggers a sync on its own. To actually apply the new version, run `/rhiza:update`, which bumps the `ref` and syncs the files in a single reviewable PR.

This gives you **opt-in updates**: the template can evolve quickly without forcing changes on you, but you can easily stay current when you choose to.

---

**Next:** [Lesson 6 — Getting Started](./06-getting-started.md)
