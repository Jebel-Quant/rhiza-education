# Lesson 7 — Configuring Your Template

The file `.rhiza/template.yml` is the single source of configuration for Rhiza in your project. This lesson explains each field and the decisions you will make when setting it up.

## A complete example

The recommended approach is to use a **profile** — a curated preset that expands to a sensible bundle selection:

```yaml
# .rhiza/template.yml (profile-based — recommended)
repository: Jebel-Quant/rhiza
ref: v1.3.3
language: python

profiles:
  - github-project

exclude: |
  .rhiza/scripts/customisations/*
  Makefile.local
```

For finer control, you can list bundles explicitly:

```yaml
# .rhiza/template.yml (explicit bundles)
repository: Jebel-Quant/rhiza
ref: v1.3.3
language: python

templates:
  - core
  - python-core
  - tests
  - github
  - github-tests
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
ref: v1.3.3
```

This pins your project to a specific version of the template. It accepts:

- **A tag** (e.g. `v1.3.3`) — recommended. Gives you a stable, known version. Renovate can detect new releases and open version-bump PRs automatically.
- **A branch** (e.g. `main`) — always fetches the latest commit on that branch. Useful during active development of a template, but means your project can receive breaking changes without a PR review step.

For production projects, always pin to a tag.

## `language`

```yaml
language: python
```

Since template v1.3.0 Rhiza is multi-language, and this key records which of the three language layers your repo follows: `python`, `rust`, or `go`. `/rhiza:init` writes it for you from the language you pick during the interview, and it is what makes the `core` bundle able to stay language-neutral — `core` defines no `install` and no `all`, and the layer named here supplies them. That is why a shared CI workflow can call `make install` without knowing what it is building.

Pick exactly one. A repo with two language layers has two definitions of the same `make` targets.

## `profiles` — curated bundle presets

The `profiles` key selects a preset that expands to a curated list of bundles:

```yaml
profiles:
  - github-project
```

| Profile | What it includes |
|---------|-----------------|
| `github-project` | `core`, `python-core`, `github`, `tests`, `github-tests`, `book`, `github-book`, `marimo`, `github-marimo` — the standard setup for a Python project on GitHub |
| `gitlab-project` | `core`, `python-core`, `gitlab`, `tests`, `gitlab-tests`, `book`, `gitlab-book`, `marimo`, `gitlab-marimo` — the same for GitLab |
| `local` | `core`, `python-core`, `tests`, `book`, `marimo` — local tooling only, no hosted CI/CD |
| `rust-local` | `core`, `rust-core`, `book` — local-first Rust |
| `go-local` | `core`, `go-core`, `book` — local-first Go |

Using a profile means your bundle selection automatically stays consistent with what Rhiza recommends for that setup. You can still add extra bundles via `templates:` alongside a profile.

> **`renovate` is in no profile.** Automated dependency updates are opt-in — if you want them, add `renovate` to `templates:` yourself (Lesson 9). There are also no `rust-github-project` or `go-github-project` profiles: hosted CI for those languages has not shipped, and naming a profile the template does not define writes cleanly and then fails your *first* `/rhiza:update` with "Profile 'X' was not found".

## `templates` — explicit bundle selection

For finer control, the `templates` key lists bundles directly:

```yaml
templates:
  - core
  - python-core
  - tests
  - github
  - github-tests
```

Bundles come in three kinds. **`core`** is the required, language-neutral base. **Language layers** (`python-core`, `rust-core`, `go-core`) supply `install` and `all` — pick exactly one. **Feature bundles** contain local tooling only (`tests`, `book`, `marimo`, etc.), and **platform overlay bundles** layer CI/CD workflows on top (`github-tests`, `github-book`, `gitlab-tests`, etc.). When you want CI for a feature, you need both: for example, `tests` (pytest config) plus `github-tests` (the GitHub Actions workflow that runs it).

Dependencies resolve automatically, so listing `tests` already gives you `core`, `python-core`, and `book`. Browse the template repo's [`bundles/` directory](https://github.com/Jebel-Quant/rhiza/tree/main/bundles) to see every available bundle with its description and dependencies.

## `include` — explicit file patterns

For finer control, `include` accepts explicit glob patterns:

```yaml
include: |
  .github/workflows/*.yml
  ruff.toml
  Makefile
  pytest.ini
```

Use `include` when you want only specific files that are not covered by a bundle, or when you want to pull in individual files on top of your `templates` selection.

You can use `templates` and `include` together in the same config.

## `exclude` — protecting local files

The `exclude` block prevents Rhiza from overwriting files you own locally, even if they match an `include` pattern. Patterns match the **destination** path — where the file lands in your repo — not the path it has inside the template, so write `.github/workflows/rhiza_weekly.yml`, never `bundles/github/.github/workflows/rhiza_weekly.yml`:

```yaml
exclude: |
  .rhiza/scripts/customisations/*
  Makefile.local
  .env
```

This is how you customise a file that Rhiza would otherwise manage. Add it to `exclude`, make your local edits, and the next update will skip it.

> **Warning:** Be deliberate about what you put in `exclude`. Files you exclude will not receive upstream template updates. If the template fixes a security issue in a workflow you have excluded, you will not get that fix automatically.

## Choosing your starting bundles

For most projects, start with the `github-project` or `gitlab-project` profile and add feature bundles as needed:

| You want... | Add these |
|-------------|----------|
| A working GitHub project from day one | `profiles: [github-project]` |
| A working GitLab project from day one | `profiles: [gitlab-project]` |
| Interactive notebooks | `+ marimo` (local), `+ github-marimo` (with GitHub CI) |
| API documentation | `+ book` (local), `+ github-book` (with GitHub Pages publish) |
| Docker builds | `+ docker` (local), `+ github-docker` (with GitHub CI) |
| Slide decks from Markdown | `+ presentation` |
| A LaTeX paper built and published | `+ paper` (local), `+ github-paper` (with the PDF published from CI) |
| Licence headers and IP notices | `+ legal` |
| Git LFS support | `+ lfs` |
| Performance benchmarks | `+ benchmarks` |
| Automated dependency updates | `+ renovate` (in no profile — always opt-in) |
| An advisory Claude review on every PR | `+ github-quality-review` / `+ gitlab-quality-review` |

When in doubt, start with `profiles: [github-project]`. You can always add bundles later — add them to `templates:` and run `/rhiza:update`.

## Updating the config

After editing `template.yml`, always run:

```
/rhiza:update
```

This applies any changes — new bundles, updated include/exclude patterns, or a new `ref` — to your project, and opens a PR of template-owned files for review.

---

**Next:** [Lesson 8 — The Sync Lifecycle](./08-the-sync-lifecycle.md)
