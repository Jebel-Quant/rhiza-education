---
marp: true
theme: default
paginate: true
footer: "Rhiza — The Living Template System · jebel-quant.github.io/rhiza-education"
style: |
  :root {
    --color-brand: #1a5276;
    --color-accent: #2e86c1;
  }
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 1.15rem;
  }
  section.lead {
    text-align: center;
    justify-content: center;
  }
  section.lead h1 { font-size: 2.4rem; color: var(--color-brand); }
  section.lead h2 { font-size: 1.5rem; color: var(--color-accent); font-weight: normal; }
  section.lead p  { color: #555; }
  h1 { color: var(--color-brand); font-size: 1.8rem; }
  h2 { color: var(--color-accent); font-size: 1.4rem; }
  code { font-size: 0.82em; }
  pre  { font-size: 0.78em; }
  blockquote { border-left: 4px solid var(--color-accent); padding-left: 1em; color: #444; font-style: italic; }
  table { width: 100%; font-size: 0.9em; }
  footer { font-size: 0.65em; color: #888; }
---

<!-- _class: lead -->

# Rhiza

## The Living Template System

Keeping every Python repo in sync — automatically

---

## Agenda

1. **The Repo Zoo Problem** — what goes wrong at scale
2. **Why existing tools fall short** — the Day 0 / Day 365 gap
3. **How Rhiza works** — core concepts and the sync loop
4. **Getting started** — four commands
5. **Living with Rhiza** — sync PRs, customisation
6. **The ecosystem** — tooling and real-world users

---

<!-- _class: lead -->

# Part 1
## The Repo Zoo Problem

---

## How every team starts

A new project? Run the generator.

```bash
cookiecutter gh:my-org/python-template
```

✓ CI workflow — wired up
✓ Makefile — ready
✓ Linting config — configured
✓ Test harness — set

**Day 0 is great. Everything is consistent.**

---

## Then time passes.

*The backtesting repo got a pre-commit hook the risk model never received.*

*The data pipeline still pins Python 3.9 — EOL since October 2024.*

*Three repos use Black. Two use Ruff. One uses both.*

*The reporting dashboard references a GitHub Actions runner deprecated eight months ago.*

**Nobody did this on purpose. It just happens.**

---

## The Repo Zoo

> A collection of repositories that started identical and have since become
> a collection of unique, inconsistent snowflakes —
> each requiring its own maintenance.

Every change made to one repo is a change **not** made to the others.

---

## The real cost

**CVE in a GitHub Actions runner**
You need to update 17 repos. You do 12, get distracted. Five months later, five are still vulnerable.

**Python 3.9 reaches end-of-life**
You update the active repos. The legacy repos drift on, unpatched.

**Team decides to standardise on Ruff**
Active repos updated. Legacy repos still run Black. "Our standard" is now a fiction.

---

<!-- _class: lead -->

# Part 2
## Why Existing Tools Fall Short

---

## The tools we reach for

| Tool | What it does | The gap |
|------|-------------|---------|
| **Cookiecutter** | Generates files once | Template and project disconnect immediately — no update path |
| **Copier** | Records the template, supports `copier update` | Manual, per-repo command — no scheduling, no PRs, no org-wide trigger |
| **GitHub template repos** | One-click clone at a point in time | That's all. No sync, no version pinning, no update mechanism |

---

## The Day 0 / Day 365 gap

All of these tools were designed to solve the **Day 0 problem**:
> *Getting a new project off the ground with sensible defaults.*

None were designed for the **Day 365 problem**:
> *Keeping twenty existing projects aligned as shared infrastructure evolves.*

**Template systems treat configuration as something you set up once.**
But configuration is not a one-time decision — it is ongoing infrastructure.

---

## Where Rhiza came from

The idea came from lived experience at a **large sovereign wealth fund** — one of the largest pools of managed capital in the world.

Full, unfiltered exposure to a wild repo zoo at institutional scale:
dozens of Python repositories, multiple teams, different vintages, no mechanism to stay aligned.

The problem was not carelessness. It was **structural**: one-shot scaffolding is the default, and it produces drift by design.

> Rhiza was created in **December 2025** at Jebel-Quant.
> The name: ancient Greek **ῥίζα** *(ree-ZAH)* — *root*.

---

## The insight

**Treat the update as a pull request, not a push.**

Instead of forcing changes into downstream repos, Rhiza **opens a PR** in each one:

- Clean diff of what changed in the template
- Owner reviews, adapts if necessary, merges
- Opt-in at the individual PR level
- **Systematic** at the organisation level — every repo gets the PR, nothing is missed

The sync is not a bulldozer. It is a proposal.

---

<!-- _class: lead -->

# Part 3
## How Rhiza Works

---

## Three actors

```
┌──────────────────────────────┐
│        template repo          │  Jebel-Quant/rhiza (or your org's fork)
│  CI workflows · Makefile      │  The canonical source of truth
│  linting config · hooks       │
└──────────────┬───────────────┘
               │  sync PRs
┌──────────────▼───────────────┐
│        your project           │  Has .rhiza/template.yml
│                               │  Declares what it wants and at what version
└──────────────────────────────┘
               ▲
          uvx rhiza  ← the materialiser
```

---

## The config file: `.rhiza/template.yml`

```yaml
repository: Jebel-Quant/rhiza   # Which template repo to sync from
ref: v0.8.0                      # Which version (pinned tag — recommended)

templates:                        # Named bundles of files to include
  - core
  - github
  - tests
  - renovate

exclude: |                        # Files you own locally — never overwritten
  ruff.toml
  Makefile.local
```

One file. That's all Rhiza needs.

---

## Bundles — named groups of files

| Bundle | What it includes |
|--------|-----------------|
| `core` | Makefile, ruff.toml, pre-commit config, editor config |
| `github` | All GitHub Actions CI/CD workflows |
| `tests` | pytest config, coverage, security scanning |
| `docker` | Dockerfile and container CI workflow |
| `marimo` | Interactive notebook support |
| `presentation` | Slide generation from Markdown (Marp) |
| `renovate` | Automated dependency update config |

`core` is always required. All others are optional.

---

## The sync loop

```
fetch  →  diff  →  review  →  commit
```

1. **Fetch** — reads `template.yml`, pulls matching files from the template repo at `ref`
2. **Diff** — compares what was fetched against what's currently in your project
3. **Review** — if anything changed, opens a pull request with the diff
4. **Commit** — you review the PR and merge it (or close it if not relevant)

Runs automatically on a **weekly schedule** via GitHub Actions.
On-demand: `make sync` or `uvx rhiza materialize`.

---

## Version pinning + Renovate

```
ref: v0.7.1   →  Renovate opens PR  →  ref: v0.8.0
```

- `ref:` pins your project to a specific template version
- **Renovate** watches for new tags on the template repo
- When a new tag is published, Renovate opens a PR bumping your `ref`
- You review the Renovate PR and merge it
- The next scheduled sync applies whatever changed in that version

**Opt-in updates** — the template can evolve quickly without forcing anything on you.

---

<!-- _class: lead -->

# Part 4
## Getting Started

---

## Four commands

```bash
# 1. Install uv (skip if already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Initialise — writes .rhiza/template.yml interactively
uvx rhiza init

# 3. Materialise — fetches template files and writes them into the project
uvx rhiza materialize

# 4. Install dev environment
make install
```

That's it. Your project is now Rhiza-managed.

---

## What you get on day one

After materialising with `core + github + tests + renovate`:

```
.github/workflows/rhiza_ci.yml          ← CI: test on push and PRs
.github/workflows/rhiza_pre-commit.yml  ← Pre-commit checks in CI
.github/workflows/rhiza_sync.yml        ← Weekly template sync
.pre-commit-config.yaml                 ← Local commit hooks
ruff.toml                               ← Linting config
Makefile                                ← make test · make lint · make release
.python-version                         ← Pinned Python version
.editorconfig                           ← Editor consistency
```

None of this required manual configuration.

---

<!-- _class: lead -->

# Part 5
## Living with Rhiza

---

## Reading a sync PR

A sync PR is a standard git diff of template files that changed.

**Green (added)** — new template content your project doesn't have yet.
Usually safe to accept.

**Red (removed)** — content removed from the template.
Check whether anything you depend on is being removed.

**Changed** — read carefully. Could be a workflow version bump, a lint rule adjustment, or a security fix.

The PR description usually explains what changed at a high level.

---

## Accept, modify, or reject?

**Accept as-is** — CI workflow updates, runner version bumps, linting adjustments that apply cleanly and tests pass.

**Modify before merging** — the change applies but needs a small tweak for your project. Or: add a file to `exclude:` in `template.yml` before merging.

**Close without merging** — the change isn't relevant (e.g. Docker support in a project that won't use containers).

> Closing is fine. The next sync will re-open the PR
> if the template still differs from your project.

---

## Customising safely

| Need | Mechanism |
|------|-----------|
| Custom `make` targets | Edit `custom-task.mk` (never overwritten) |
| Project-specific env vars | Edit `custom-env.mk` (never overwritten) |
| Permanently own a specific file | Add to `exclude:` in `template.yml` |
| Custom standards for your whole org | Fork the template repo |

> **Never edit template-managed files directly** unless you also add them to `exclude:`.
> Your change will be overwritten on the next sync.

---

<!-- _class: lead -->

# Part 6
## The Ecosystem

---

## The Rhiza ecosystem

```
                ┌─────────────────────────────┐
                │       template repo          │
                │   (rhiza or rhiza-go)        │
                └─────────────┬───────────────┘
                              │ sync PRs
              ┌───────────────┴──────────────────┐
              │           your project            │
              └──┬───────────────┬───────────────┘
                 │               │
    ┌────────────▼──┐  ┌─────────▼──────────┐
    │   rhiza-cli   │  │    rhiza-hooks      │
    │  init         │  │  check-rhiza-config │
    │  materialize  │  │  check-py-versions  │
    │  validate     │  │  update-readme-help │
    └────────────┬──┘  └────────────────────┘
                 │
    ┌────────────▼──────────────────────────┐
    │            rhiza-tools                │
    │  bump · release · version-matrix      │
    │  coverage-badge · analyze-benchmarks  │
    └───────────────────────────────────────┘
```

---

## Who's using it

**The Rhiza tools themselves** — rhiza-cli, rhiza-hooks, and rhiza-tools all sync from rhiza. The system eats its own cooking.

**External projects:**

| Project | Organisation | Bundles |
|---------|-------------|---------|
| `simulator` | Stanford CVXGRP | `core + github + tests` |
| `jsharpe` | tschm | `core + github + marimo` |
| `loman` | Janus Henderson | `core + github + tests + renovate` |
| `chebpy` | chebpy | `core + github` |

---

## Key takeaways

1. **The repo zoo is structural** — drift is the default outcome of one-shot scaffolding, not a failure of discipline.

2. **Existing template tools solve Day 0.** Rhiza solves Day 365.

3. **The core insight:** treat updates as pull requests, not pushes. Systematic coverage, opt-in per repo.

4. **Setup is four commands.** Ongoing maintenance is reviewing a weekly PR.

5. **You stay in control.** `exclude:`, custom extension files, and org forks give full flexibility without fighting the sync.

---

<!-- _class: lead -->

# Get started today

```bash
uvx rhiza init
```

**Curriculum:** https://jebel-quant.github.io/rhiza-education/

**Template:** https://github.com/Jebel-Quant/rhiza

---

<!-- _class: lead -->

# Questions?

*ῥίζα (ree-ZAH) — root*

**https://jebel-quant.github.io/rhiza-education/**
