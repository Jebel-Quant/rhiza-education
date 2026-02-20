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
  section::before {
    content: '';
    position: absolute;
    top: 18px;
    right: 24px;
    width: 52px;
    height: 52px;
    background-image: url(assets/rhiza-logo.svg);
    background-size: contain;
    background-repeat: no-repeat;
  }
  section.lead::before { display: none; }
---

<!-- _class: lead -->

![w:120](assets/rhiza-logo.svg)

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

Each repo drifted into a different breed — incompatible with the others, living in its own enclosure, expensive to maintain on its own terms.

---

## The real cost

> Every change made to one repo is a change **not** made to the others.

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

## The insight

Born from experience at a **large sovereign wealth fund**: dozens of Python repos, multiple teams, no mechanism to stay aligned. The problem was not carelessness — it was **structural**. One-shot scaffolding produces drift by design.

**Treat the update as a pull request, not a push.**

Instead of forcing changes into downstream repos, Rhiza **opens a PR** in each one:

- Clean diff of what changed in the template
- Owner reviews, adapts if necessary, merges
- Opt-in per repo — **systematic** across the organisation

The sync is not a bulldozer. It is a proposal.

---

<!-- _class: lead -->

# Part 3
## How Rhiza Works

---

## Three actors

<div style="display:flex;flex-direction:column;align-items:center;gap:0.8em;margin-top:1em;">
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:8px;padding:0.7em 2.5em;text-align:center;min-width:52%;">
    <div style="font-weight:bold;color:#1a5276;">template repo</div>
    <div style="font-size:0.82em;color:#555;margin-top:0.2em;">Jebel-Quant/rhiza &nbsp;·&nbsp; or your org's fork</div>
  </div>
  <div style="color:#2e86c1;font-size:0.95em;">↓ &nbsp;sync PRs</div>
  <div style="background:#eaf4fc;border:2px solid #1a5276;border-radius:8px;padding:0.7em 2.5em;text-align:center;min-width:52%;">
    <div style="font-weight:bold;color:#1a5276;">your project</div>
    <div style="font-size:0.82em;color:#555;margin-top:0.2em;">.rhiza/template.yml</div>
  </div>
  <div style="color:#2e86c1;font-size:0.95em;">↑ &nbsp;materialise</div>
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:8px;padding:0.7em 2.5em;text-align:center;min-width:52%;">
    <div style="font-weight:bold;color:#1a5276;">uvx rhiza</div>
    <div style="font-size:0.82em;color:#555;margin-top:0.2em;">the materialiser — runs locally or in CI</div>
  </div>
</div>

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

<div style="display:flex;align-items:center;justify-content:center;gap:0.7em;margin:1em 0 1.2em;">
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:7px;padding:0.45em 1.1em;font-weight:bold;color:#1a5276;">fetch</div>
  <div style="color:#2e86c1;font-size:1.2em;">→</div>
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:7px;padding:0.45em 1.1em;font-weight:bold;color:#1a5276;">diff</div>
  <div style="color:#2e86c1;font-size:1.2em;">→</div>
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:7px;padding:0.45em 1.1em;font-weight:bold;color:#1a5276;">review</div>
  <div style="color:#2e86c1;font-size:1.2em;">→</div>
  <div style="background:#1a5276;border-radius:7px;padding:0.45em 1.1em;font-weight:bold;color:#fff;">commit</div>
</div>

1. **Fetch** — reads `template.yml`, pulls matching files from the template repo at `ref`
2. **Diff** — compares what was fetched against what's currently in your project
3. **Review** — if anything changed, opens a pull request with the diff
4. **Commit** — you review the PR and merge it (or close it if not relevant)

Runs automatically on a **weekly schedule** via GitHub Actions.
On-demand: `make sync` or `uvx rhiza materialize`.

---

## Renovate — closing the loop

Without Renovate, the `ref:` pin is frozen. Projects drift behind the template silently.

<div style="display:flex;flex-direction:column;gap:0.45em;margin:0.9em 0;font-size:0.93em;">
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    template repo publishes <strong>v0.9.0</strong>
  </div>
  <div style="padding-left:1.1em;color:#2e86c1;">↓</div>
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    Renovate opens PR: <code>ref: v0.8.0 → v0.9.0</code> &nbsp;<span style="color:#888;">(one line diff)</span>
  </div>
  <div style="padding-left:1.1em;color:#2e86c1;">↓ <span style="color:#888;font-size:0.88em;">you merge</span></div>
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    sync workflow applies updated CI files, linting config, etc.
  </div>
</div>

Two separate PRs: **should we upgrade?** then **here's what changed.**
Opt-in per repo. Systematic across the organisation.

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

| Tool | What it does |
|------|-------------|
| **rhiza-cli** | `uvx rhiza init / materialize / validate` — the tool you run |
| **rhiza-hooks** | Pre-commit hooks: validate config, check version consistency |
| **rhiza-tools** | `bump`, `release`, `version-matrix`, `coverage-badge` |
| **rhiza-go** | The same living-template pattern for Go projects |
| **repo-monitor** | Desktop dashboard: workflow status, open PRs, Renovate state |

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

# Get started

```bash
uvx rhiza init
```

*ῥίζα (ree-ZAH) — root*

**https://jebel-quant.github.io/rhiza-education/**
