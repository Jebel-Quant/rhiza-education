# Lesson 4 — Configuring Your Template

The file `.rhiza/template.yml` is the single source of configuration for Rhiza in your project. This lesson explains each field and the decisions you will make when setting it up.

## A complete example

```yaml
# .rhiza/template.yml
repository: Jebel-Quant/rhiza
ref: v0.8.0

include: |
  templates:
    - core
    - github
    - tests
    - renovate

exclude: |
  .rhiza/scripts/customisations/*
  Makefile.local
```

## `repository`

```yaml
repository: Jebel-Quant/rhiza
```

This is the GitHub repository that Rhiza treats as your template source. It can be any GitHub repo — not just the canonical Rhiza repo. The most common choices are:

- **`Jebel-Quant/rhiza`** — the canonical upstream. Good for getting started; means you track Rhiza's own release cadence.
- **Your org's fork** — the recommended approach for teams. Fork `Jebel-Quant/rhiza` into your organisation, add your own customisations, and point all your projects at the fork. Your fork becomes the source of truth for your team's standards.

> **Note:** If you use your org's fork, you control when to pull upstream changes into your fork. This gives your team review control over what changes flow into all your projects.

## `ref`

```yaml
ref: v0.8.0
```

This pins your project to a specific version of the template. It accepts:

- **A tag** (e.g. `v0.8.0`) — recommended. Gives you a stable, known version. Renovate can detect new tags and open version-bump PRs automatically.
- **A branch** (e.g. `main`) — always fetches the latest commit on that branch. Useful during active development of a template, but means your project can receive breaking changes without a PR review step.

For production projects, always pin to a tag.

## `include` — file patterns

The `include` block tells Rhiza which files to copy from the template repository. You can write it two ways:

**Using templates (recommended):**

```yaml
include: |
  templates:
    - core
    - github
    - tests
```

Bundles are named groups of files defined in the template repo. They are the easiest way to get a meaningful set of files without enumerating every path.

**Using explicit glob patterns:**

```yaml
include: |
  .github/workflows/*.yml
  ruff.toml
  Makefile
  pytest.ini
```

Use explicit patterns when you want only specific files from a bundle, or when you want to include files that are not part of any bundle.

You can mix both styles in the same `include` block.

## `exclude` — protecting local files

The `exclude` block prevents Rhiza from overwriting files you own locally, even if they match an `include` pattern:

```yaml
exclude: |
  .rhiza/scripts/customisations/*
  Makefile.local
  .env
```

This is how you customise a file that Rhiza would otherwise manage. Add it to `exclude`, make your local edits, and the sync will skip it.

> **Warning:** Be deliberate about what you put in `exclude`. Files you exclude will not receive upstream template updates. If the template fixes a security issue in a workflow you have excluded, you will not get that fix automatically.

## Choosing your starting bundles

Here is a quick guide:

| You want... | Add these bundles |
|-------------|------------------|
| A working project from day one | `core`, `github`, `tests` |
| Automated dependency updates | `+ renovate` |
| Docker support | `+ docker` |
| Interactive notebooks | `+ marimo` |
| Slide decks from Markdown | `+ presentation` |
| GitLab instead of GitHub | replace `github` with `gitlab` |

When in doubt, start with `core`, `github`, and `tests`. You can always add bundles later — just add them to `include` and re-run `uvx rhiza materialize`.

## Updating the config

After editing `template.yml`, always re-run:

```bash
uvx rhiza materialize
```

This applies any changes — new bundles, updated include/exclude patterns, or a new `ref` — to your project.

---

**Next:** [Lesson 5 — The Sync Lifecycle](./05-the-sync-lifecycle.md)
