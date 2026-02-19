# Appendix A1 — Rhiza on GitLab

Rhiza has full GitLab CI/CD support. If your project lives on GitLab rather than GitHub, this appendix covers what changes and what stays the same.

## What stays the same

Everything in lessons 1–6 applies equally to GitLab:

- The `.rhiza/template.yml` config file works identically.
- `uvx rhiza init` and `uvx rhiza materialize` work identically.
- The `templates:`, `include:`, and `exclude:` keys work identically.
- The sync lifecycle — materialize → diff → review → merge — is the same.
- The extension points (`custom-task.mk`, `custom-env.mk`, `exclude:`) are the same.

## What changes: use the `gitlab` bundle

When configuring your `template.yml`, replace the `github` bundle with `gitlab`:

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza
ref: v0.8.0

templates:
  - core
  - gitlab       # <-- instead of github
  - tests
  - renovate
```

The `gitlab` bundle provides GitLab CI/CD equivalents for all the workflows in the `github` bundle: CI testing, pre-commit, deptry, documentation, sync, and release.

> **Note:** Do not include both `github` and `gitlab` in the same project. Pick one.

## What you get from the `gitlab` bundle

After materialising, your project will have:

```
.gitlab-ci.yml                   # Main CI entrypoint — includes all workflow files
.gitlab/workflows/
  rhiza_ci.yml                   # Multi-version Python CI
  rhiza_pre-commit.yml           # Pre-commit hooks
  rhiza_deptry.yml               # Dependency checking
  rhiza_validate.yml             # Rhiza config validation
  rhiza_book.yml                 # Documentation (deploys to GitLab Pages)
  rhiza_sync.yml                 # Scheduled template sync
  rhiza_release.yml              # Release and PyPI publishing
  rhiza_renovate.yml             # Renovate dependency updates
```

## Required CI/CD variables

Set these in your GitLab project under **Settings > CI/CD > Variables**:

| Variable | Required for | Notes |
|----------|-------------|-------|
| `PAT_TOKEN` | Sync workflow | A Project or Group Access Token with `api` scope. Needed for two reasons: (1) GitLab's `CI_JOB_TOKEN` cannot create merge requests, so without PAT_TOKEN the sync runs but no MR is opened; (2) pushing changes to workflow files requires a PAT on both GitHub and GitLab — the default job token lacks that permission. |
| `PYPI_TOKEN` | Release workflow | Your PyPI API token. GitLab uses token-based authentication; OIDC Trusted Publishing is a GitHub-only feature. |

Mark both as **Masked** in the variable settings so they are not exposed in pipeline logs.

## Scheduling the sync pipeline

The GitHub bundle sets up a scheduled workflow automatically. On GitLab, you need to configure the schedule manually:

1. Go to **CI/CD > Schedules** in your GitLab project.
2. Click **New schedule**.
3. Set the cron expression (e.g. `0 9 * * 1` for every Monday at 09:00).
4. Set the target branch to `main`.
5. Save.

The `rhiza_sync.yml` workflow will then run on that schedule, materialise the latest template, and open a merge request if anything changed.

## Key differences from the GitHub setup

**Merge request creation on sync**

On GitHub, the sync workflow creates a pull request automatically using the built-in `GITHUB_TOKEN`. On GitLab, creating a merge request from CI requires a `PAT_TOKEN` with API scope. If this token is not set, the sync will still run and materialise changes, but it will not open an MR — you will need to create one manually from the resulting branch.

**PyPI publishing**

The GitHub release workflow uses OIDC Trusted Publishing — no token is stored, the trust is established between GitHub Actions and PyPI directly. On GitLab, this mechanism is not available, so you store a `PYPI_TOKEN` as a CI/CD variable instead.

**Documentation pages**

The `book` workflow deploys to GitLab Pages. GitLab requires that the output of the pages job is in a directory called `public/`. This is handled automatically by the `rhiza_book.yml` workflow — you do not need to configure anything extra, but you do need to ensure GitLab Pages is enabled for your project (**Settings > General > Visibility, project features, permissions > Pages**).

**Python version matrix**

The GitHub CI workflow uses a fully dynamic matrix (Python versions are read from `pyproject.toml` at runtime). GitLab has limited support for dynamic matrices, so the GitLab CI workflow uses a static list (`3.11`, `3.12`, `3.13`). If you need to test against a different set of versions, edit `.gitlab/workflows/rhiza_ci.yml` and add the file to `exclude:` in `template.yml` so the sync does not overwrite your change.

## Renovate on GitLab

The `renovate` bundle works on GitLab too. Renovate supports GitLab natively and will open merge requests to bump the `ref:` in your `template.yml` when a new template version is released. The configuration in `renovate.json` does not need to change.

---

**Back to:** [Lesson 9 — Customising Safely](./09-customizing-safely.md) | [README](../README.md)
