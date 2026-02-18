# Lesson 2 — Core Concepts

Before you run any commands, it helps to have a clear picture of the moving parts. This lesson walks through the key abstractions in Rhiza.

## The three actors

Every Rhiza setup involves three things:

**1. The template repository**

This is a GitHub repo that holds the canonical versions of shared infrastructure files: CI workflows, a Makefile, linting config, pre-commit hooks, and so on. The canonical template repo is `Jebel-Quant/rhiza`, but you can fork it and use your own.

**2. The downstream project**

This is your actual project repo. It declares what it wants from the template repo via a config file (`.rhiza/template.yml`). The downstream project does not duplicate the template — it just consumes specific files from it.

**3. The materialiser**

This is Rhiza itself — the `uvx rhiza` CLI tool. It reads the downstream project's config, fetches the specified files from the template repo at the specified version, and writes them into the project.

## The config file: `.rhiza/template.yml`

Every downstream project has exactly one Rhiza config file. Here is what it looks like:

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza   # Which template repo to sync from
ref: v0.7.1                      # Which version of the template to use

templates:                        # Named bundles to include
  - core
  - github
  - tests

exclude: |                        # Files to never overwrite locally
  .rhiza/scripts/customisations/*
```

- `repository` — any GitHub repo, not just the canonical Rhiza repo.
- `ref` — a tag or branch name. Tags are recommended because they enable automated version tracking (more on this in Lesson 5).
- `templates` — named bundles of files to copy from the template (e.g. `core`, `github`, `tests`).
- `include` — explicit glob patterns for files not covered by a bundle (optional).
- `exclude` — glob patterns that protect files from being overwritten by the sync.

## Bundles

Listing every file path in `include` by hand gets tedious. Rhiza provides **bundles**: named groups of files with sensible defaults.

| Bundle | What it includes |
|--------|-----------------|
| `core` | Makefile, ruff.toml, pre-commit config, editor config, core scripts |
| `github` | All GitHub Actions CI/CD workflows |
| `tests` | pytest config, coverage, security scanning workflows |
| `marimo` | Interactive notebook support |
| `book` | API documentation generation |
| `docker` | Dockerfile and container CI workflow |
| `devcontainer` | VS Code / GitHub Codespaces dev container |
| `presentation` | Slide generation from Markdown (via Marp) |
| `renovate` | Automated dependency update config |

You reference a bundle by its name instead of listing files individually. You will see how this works in `template.yml` in Lesson 4.

The `core` bundle is required. All others are optional.

## The sync loop

The fundamental operation is:

```
fetch → diff → review → commit
```

1. **Fetch**: Rhiza reads your `template.yml` and pulls the matching files from the template repo at the specified `ref`.
2. **Diff**: It compares what it fetched against what is currently in your project.
3. **Review**: If anything changed, a pull request is opened with the diff (in automated mode) or the changes are written to disk (in manual mode).
4. **Commit**: You review the PR and merge it — or reject it if the change doesn't apply to your project.

This loop runs automatically on a schedule (via a GitHub Actions workflow included in the `github` bundle). You can also trigger it manually with `make sync` or `uvx rhiza materialize`.

## Version pinning and automated updates

The `ref:` field in `template.yml` pins your project to a specific version of the template. When the template repo releases a new version, Renovate — a dependency automation tool — detects the new tag and opens a PR in your project that bumps `ref: v0.7.1` to `ref: v0.8.0`. You review and merge that PR, then the next sync picks up whatever changed in the new template version.

This gives you **opt-in updates**: the template can evolve quickly without forcing changes on you, but you can easily stay current with a single merge.

---

**Next:** [Lesson 3 — Getting Started](./03-getting-started.md)
