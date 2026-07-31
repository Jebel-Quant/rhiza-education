# Lesson 5 — Core Concepts

Before you run any commands, it helps to have a clear picture of the moving parts. This lesson walks through the key abstractions in Rhiza.

## The three actors

Every Rhiza setup involves three things:

**1. The template repository**

This is a GitHub repo that holds the canonical versions of shared infrastructure files: CI workflows, a Makefile, linting config, pre-commit hooks, and so on. The canonical template repo is `Jebel-Quant/rhiza`, but you can fork it and use your own.

**2. The downstream project**

This is your actual project repo. It declares what it wants from the template repo via a config file (`.rhiza/template.yml`). The downstream project does not duplicate the template — it just consumes specific files from it.

**3. The syncer**

This is the sync engine, driven by `/rhiza:update` from the `rhiza-claude` Claude Code plugin. It reads the downstream project's config (`.rhiza/template.yml`), fetches the specified files from the template repo at the specified version, writes them into the project, and records what it synced — repository, ref, commit SHA, timestamp, strategy, and file paths — in `.rhiza/template.lock`.

## The config file: `.rhiza/template.yml`

Every downstream project has exactly one Rhiza config file. Here is what it looks like:

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza   # Which template repo to sync from
ref: v1.2.5                      # Which version of the template to use

profiles:                         # Curated bundle preset (recommended)
  - github-project

exclude: |                        # Files to never overwrite locally
  .rhiza/scripts/customisations/*
```

- `repository` — any GitHub repo, not just the canonical Rhiza repo.
- `ref` — a tag or branch name. Tags are recommended because they enable automated version tracking (more on this in Lesson 8).
- `profiles` — a curated preset that expands to a sensible bundle selection. `github-project` gives you `core`, `github`, `tests`, `github-tests`, `book`, `github-book`, `marimo`, and `github-marimo`. This is the recommended starting point. There are three profiles — `github-project`, `gitlab-project`, and `local` — and `renovate` belongs to none of them, so projects that want automated dependency updates add that bundle by hand.
- `templates` — explicit list of named bundles, for when you need finer control than a profile offers.
- `include` — explicit glob patterns for files not covered by a bundle (optional).
- `exclude` — glob patterns that protect files from being overwritten by the sync.

## Bundles

Listing every file path in `include` by hand gets tedious. Rhiza provides **bundles**: named groups of files with sensible defaults. Bundles come in two kinds:

**Feature bundles** — local tooling only, no CI/CD. They work independently of any platform.

| Bundle | What it includes |
|--------|-----------------|
| `core` | Makefile, ruff.toml, pre-commit config, editor config, core scripts |
| `tests` | pytest config, coverage, type checking |
| `book` | API documentation generation |
| `marimo` | Interactive notebook support |
| `docker` | Dockerfile and container configuration |
| `devcontainer` | VS Code / GitHub Codespaces dev container |
| `presentation` | Slide generation from Markdown (via Marp) |
| `paper` | Academic paper/research publishing |
| `lfs` | Git Large File Storage configuration |
| `legal` | Licence headers and IP notice files |
| `renovate` | Automated dependency update config |
| `benchmarks` | Performance testing infrastructure |

**Platform overlay bundles** — layer CI/CD workflows on top of a feature bundle. Each overlay is named `<platform>-<feature>`:

| Bundle | What it adds |
|--------|-------------|
| `github` | Base GitHub Actions setup |
| `github-tests` | Testing and security scan workflows on GitHub |
| `github-book` | Documentation publication workflow on GitHub |
| `github-docker` | Docker image build and publish on GitHub |
| `github-marimo` | Notebook hosting workflow on GitHub |
| `github-devcontainer` | Dev container image build on GitHub |
| `gitlab` | Base GitLab CI/CD setup |
| `gitlab-tests` | Testing workflows on GitLab |
| `gitlab-book` | Documentation publication workflow on GitLab |
| `gitlab-marimo` | Notebook hosting workflow on GitLab |

**Profiles** are curated presets that expand to a sensible combination of bundles for common setups. For most projects, start with a profile rather than listing bundles individually:

| Profile | Expands to |
|---------|-----------|
| `github-project` | `core`, `github`, `tests`, `github-tests`, `book`, `github-book`, `marimo`, `github-marimo` |
| `gitlab-project` | `core`, `gitlab`, `tests`, `gitlab-tests`, `book`, `gitlab-book`, `marimo`, `gitlab-marimo` |
| `local` | `core`, `tests`, `book`, `marimo` — everything local, no hosted workflows |

Each platform profile is the `local` set plus that platform's CI overlays, which is why switching between GitHub and GitLab changes the workflows and nothing else. Note that `renovate` is in **no** profile: automated dependency updates are opt-in, added as a bundle when you want them (Lesson 9).

Browse the `bundles/` directory in the template repo, or the [bundle taxonomy](https://github.com/Jebel-Quant/rhiza/blob/main/docs/reference/BUNDLE_TAXONOMY.md), to see the full list with dependency information. The `core` bundle is required. All others are optional.

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

The `ref:` field in `template.yml` pins your project to a specific version of the template. When the template repo releases a new version, Renovate — a dependency automation tool — detects the new tag and opens a PR in your project that bumps `ref: v1.1.0` to `ref: v1.2.0`. That PR is a *notification* that a newer template exists; merging it no longer triggers a sync on its own. To actually apply the new version, run `/rhiza:update`, which bumps the `ref` and syncs the files in a single reviewable PR.

This gives you **opt-in updates**: the template can evolve quickly without forcing changes on you, but you can easily stay current when you choose to.

---

**Next:** [Lesson 6 — Getting Started](./06-getting-started.md)
