# Appendix A1 — Rhiza on GitLab

Rhiza has full GitLab CI/CD support. If your project lives on GitLab rather than GitHub, this appendix covers what changes and what stays the same.

## What stays the same

Everything in lessons 1–6 applies equally to GitLab:

- The `.rhiza/template.yml` config file works identically.
- The rhiza-claude plugin commands (`/rhiza:init`, `/rhiza:update`) work identically — `/rhiza:init` asks whether your project is on GitHub or GitLab, and picks the matching profile from your answer.
- The `templates:`, `include:`, `exclude:`, and `language:` keys work identically.
- `core` plus one language layer is the base on either platform; only the CI overlays differ.
- The update lifecycle — `/rhiza:update` → diff → review → merge — is the same.
- The extension points (`local.mk`, `[tool.rhiza-task]`, `local-setup.sh`, `exclude:`) are the same.
- The tasks come from the same pinned `rhiza-task` CLI, so `uv run rhiza-task test` means the same thing on either platform.

## What changes: use the `gitlab` bundle

When configuring your `template.yml`, replace the `github` bundle with `gitlab`:

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza
ref: v1.8.0
language: python

templates:
  - core
  - python-core
  - gitlab       # <-- instead of github
  - gitlab-tests
  - renovate
```

Or, more simply, use the `gitlab-project` profile, which expands to exactly the GitLab shape:

```yaml
repository: Jebel-Quant/rhiza
ref: v1.8.0
language: python

profiles:
  - gitlab-project
```

The `gitlab` bundle provides GitLab CI/CD equivalents for the workflows in the `github` bundle: CI testing, the code-quality gates, documentation, releases, and Renovate.

> **Note:** Do not include both `github` and `gitlab` in the same project. Pick one.

## What you get from the `gitlab` bundle

After syncing, your project will have:

```
.gitlab-ci.yml                   # Main CI entrypoint — includes all workflow files
.gitlab/workflows/
  rhiza_ci.yml                   # Multi-version Python CI
  rhiza_quality.yml              # Code-quality gates (lint, types, deps, security)
  rhiza_book.yml                 # Documentation (deploys to GitLab Pages)
  rhiza_release.yml              # Release and PyPI publishing
  rhiza_renovate.yml             # Renovate dependency updates
  rhiza_weekly.yml               # Weekly dependency-compatibility and link checks
```

There is no `rhiza_sync.yml` — GitLab has no automated template-sync pipeline any more than GitHub does. Template updates are applied by running `/rhiza:update`. Commit hooks run locally via [rhiza-hooks](https://github.com/Jebel-Quant/rhiza-hooks), through `prek`, rather than as a CI workflow.

GitLab also has a `gitlab-quality-review` overlay — an opt-in advisory Claude design review of merge-request diffs, the counterpart to `github-quality-review`. It is in no profile; add the bundle if you want it.

> **Rust and Go are local-only for now.** The template's Rust and Go layers ship no hosted CI on either platform, so there is no `rust-gitlab-project` or `go-gitlab-project`. `/rhiza:init` writes `rust-local` or `go-local` regardless of host.

## Required CI/CD variables

Set these in your GitLab project under **Settings > CI/CD > Variables**:

| Variable | Required for | Notes |
|----------|-------------|-------|
| `PAT_TOKEN` | Renovate MRs | A Project or Group Access Token with `api` scope. GitLab's `CI_JOB_TOKEN` cannot create merge requests, so without `PAT_TOKEN` the `rhiza_renovate.yml` job runs but no MR is opened. |
| `PYPI_TOKEN` | Release workflow | Your PyPI API token. GitLab uses token-based authentication; OIDC Trusted Publishing is a GitHub-only feature. |

Mark both as **Masked** in the variable settings so they are not exposed in pipeline logs.

## Keeping the template up to date

There is no scheduled sync pipeline on GitLab (or on GitHub). To pull the latest template changes into your project, run `/rhiza:update` from Claude Code — it works identically regardless of platform, bumps the `ref:`, applies the changed files, and opens a merge request containing only template-owned files. It produces no scorecard; if you want the repo scored, run `/rhiza:quality` separately. Run `/rhiza:status --check` any time to see whether your pinned `ref:` is behind the latest release.

Renovate (via the shipped `rhiza_renovate.yml` job) still opens a merge request bumping the `ref:` when a new template release is tagged, but that MR is only a notification that a new version exists — you apply the actual file changes with `/rhiza:update`.

## Key differences from the GitHub setup

**Merge request creation**

On GitHub, Renovate and the release automation open pull requests using the built-in `GITHUB_TOKEN`. On GitLab, creating a merge request from CI requires a `PAT_TOKEN` with API scope. If this token is not set, the `rhiza_renovate.yml` job still runs but will not open an MR — you will need to create one manually from the resulting branch.

**PyPI publishing**

The GitHub release workflow uses OIDC Trusted Publishing — no token is stored, the trust is established between GitHub Actions and PyPI directly. On GitLab, this mechanism is not available, so you store a `PYPI_TOKEN` as a CI/CD variable instead.

**Documentation pages**

The `book` workflow deploys to GitLab Pages. GitLab requires that the output of the pages job is in a directory called `public/`. This is handled automatically by the `rhiza_book.yml` workflow — you do not need to configure anything extra, but you do need to ensure GitLab Pages is enabled for your project (**Settings > General > Visibility, project features, permissions > Pages**).

**Python version matrix**

The GitHub CI workflow uses a fully dynamic matrix (Python versions are read from `pyproject.toml` at runtime). GitLab has limited support for dynamic matrices, so the GitLab CI workflow uses a static list (`3.11`, `3.12`, `3.13`). If you need to test against a different set of versions, edit `.gitlab/workflows/rhiza_ci.yml` and add the file to `exclude:` in `template.yml` so the sync does not overwrite your change.

## Renovate on GitLab

The `renovate` bundle works on GitLab too. Renovate supports GitLab natively and will open merge requests to bump the `ref:` in your `template.yml` when a new template version is released. The configuration in `renovate.json` does not need to change.

---

**Back to:** [Lesson 10 — Customising Safely](./10-customizing-safely.md) | [README](../README.md)
