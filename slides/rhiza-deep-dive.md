---
marp: true
theme: default
paginate: true
footer: "Rhiza — The Living Template System · jebel-quant.github.io/rhiza-education · rhiza {{ rhiza_version }} / rhiza-claude {{ rhiza_claude_version }}"
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

1. **The Repo Zoo Problem** — what goes wrong at scale and why it's structural
2. **Why existing tools fall short** — the Day 0 / Day 365 gap
3. **How Rhiza works** — config, bundles, the sync loop, and Renovate
4. **Getting started** — setup and the two bootstrap PRs
5. **Living with Rhiza** — sync PRs, customisation, and conflict resolution
6. **The ecosystem** — rhiza-claude, rhiza-hooks, and companion projects
7. **Adoption** — migrating existing repos and rolling out across a team

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

## The hidden tax

The problem is not just drift — it is the ongoing cost of managing inconsistency.

| Task | 1 repo | 20 repos |
|------|--------|----------|
| Update deprecated Actions runner | 15 min | 5 hours |
| Bump Python version across CI | 20 min | 7 hours |
| Apply security patch to linting config | 10 min | 3 hours |
| Rotate a shared API token | 5 min | 2 hours |

**Every shared infrastructure decision multiplies by your repo count.**

At 20 repos, a 15-minute task becomes an afternoon. At 50, it becomes a week.

---

## The coordination problem

Who owns shared infrastructure?

- DevOps pushes a new CI standard → who updates the 30 repos?
- Security mandates a new linting rule → how does it reach everyone?
- A CVE appears in a GitHub Actions dependency → who's responsible?

**There is no clean answer without a system.** Everyone assumes someone else is handling it.

The classic response — write a runbook, send a team email — doesn't scale.
Documentation tells people what to do. **Rhiza opens a pull request.**

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
  <div style="color:#2e86c1;font-size:0.95em;">↑ &nbsp;/rhiza:update</div>
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:8px;padding:0.7em 2.5em;text-align:center;min-width:52%;">
    <div style="font-weight:bold;color:#1a5276;">rhiza-claude</div>
    <div style="font-size:0.82em;color:#555;margin-top:0.2em;">the interface — <code>/rhiza:*</code> commands you run in Claude Code</div>
  </div>
</div>

---

## The config file: `.rhiza/template.yml`

```yaml
repository: Jebel-Quant/rhiza   # Which template repo to sync from
ref: v1.2.0                      # Which version (pinned tag — recommended)

profiles:                         # Curated bundle preset (recommended)
  - github-project

exclude: |                        # Files you own locally — never overwritten
  ruff.toml
  Makefile.local
```

One file, under version control. That's all Rhiza needs.

---

## Your org's fork

The canonical template is `Jebel-Quant/rhiza`. For most teams the right setup is:

<div style="display:flex;align-items:center;justify-content:center;gap:0.7em;margin:1em 0 1.2em;">
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:7px;padding:0.5em 1.1em;font-weight:bold;color:#1a5276;text-align:center;">Jebel-Quant/rhiza<div style="font-weight:normal;font-size:0.8em;color:#555;">upstream</div></div>
  <div style="color:#2e86c1;font-size:1.2em;">→</div>
  <div style="background:#eaf4fc;border:2px solid #1a5276;border-radius:7px;padding:0.5em 1.1em;font-weight:bold;color:#1a5276;text-align:center;">your-org/rhiza<div style="font-weight:normal;font-size:0.8em;color:#555;">your fork</div></div>
  <div style="color:#2e86c1;font-size:1.2em;">→</div>
  <div style="background:#eaf4fc;border:2px solid #2e86c1;border-radius:7px;padding:0.5em 1.1em;font-weight:bold;color:#1a5276;text-align:center;">your projects<div style="font-weight:normal;font-size:0.8em;color:#555;">subscribers</div></div>
</div>

1. **Fork** `Jebel-Quant/rhiza` into your organisation
2. **Customise** — add your org's runners, secrets, standards
3. **Point all projects** at `your-org/rhiza` in `template.yml`
4. **Pull upstream** when you're ready — nothing flows through without your review

---

## Bundles — named groups of files

**Feature bundles** (local tooling, no CI/CD):

| Bundle | What it includes |
|--------|-----------------|
| `core` | Makefile, ruff.toml, pre-commit config, editor config |
| `tests` | pytest config, coverage, type checking |
| `docker` | Dockerfile and container configuration |
| `marimo` | Interactive notebook support |
| `presentation` | Slide generation from Markdown (Marp) |
| `renovate` | Automated dependency update config |

**Platform overlay bundles** layer CI/CD on top: `github-tests`, `github-book`, `gitlab-tests`, etc.

**Profiles** (`github-project`, `gitlab-project`, `local`) expand to a sensible combination. Start here.

---

## What's in the `github` + `github-tests` bundles

The `github` overlay provides the base platform wiring:

| File | Purpose |
|------|---------|
| `rhiza_release.yml` | Build wheel, publish to PyPI via OIDC, create GitHub Release |
| `rhiza_codeql.yml` | CodeQL security scanning |
| `rhiza_scorecard.yml` | OpenSSF Scorecard supply-chain checks |

The `github-tests` overlay adds testing CI on top:

| File | Purpose |
|------|---------|
| `rhiza_ci.yml` | Test matrix across Python versions on push and PRs (matrix derived from `requires-python`) |

Other bundles layer in more workflows — benchmarks, mutation testing, fuzzing, a weekly dependency/link check, and a quality review. There is **no sync workflow**: template changes are applied by running `/rhiza:update`.

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
3. **Review** — if anything changed, opens a pull request with the diff (scoring is `/rhiza:quality`)
4. **Commit** — you review the PR and merge it (or close it if not relevant)

Run it on demand with **`/rhiza:update`** in Claude Code — it bumps the `ref`, syncs the files, resolves conflicts, runs the quality gates, and opens the PR.

---

## Renovate — closing the loop

Without Renovate, the `ref:` pin is frozen. Projects drift behind the template silently.

<div style="display:flex;flex-direction:column;gap:0.45em;margin:0.9em 0;font-size:0.93em;">
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    template repo publishes <strong>v1.2.0</strong>
  </div>
  <div style="padding-left:1.1em;color:#2e86c1;">↓</div>
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    Renovate opens PR: <code>ref: v1.1.0 → v1.2.0</code> &nbsp;<span style="color:#888;">(a notification — one line diff)</span>
  </div>
  <div style="padding-left:1.1em;color:#2e86c1;">↓ <span style="color:#888;font-size:0.88em;">you run <code>/rhiza:update</code></span></div>
  <div style="background:#eaf4fc;border-left:4px solid #2e86c1;border-radius:0 7px 7px 0;padding:0.6em 1.1em;">
    <code>/rhiza:update</code> applies the new CI files, linting config, etc. in a PR
  </div>
</div>

Two separate steps: **should we upgrade?** (the ref-bump PR) then **here's what changed** (the `/rhiza:update` PR).

---

## The `ref:` pin in depth

```yaml
ref: v1.2.0   # pinned tag — recommended for all production repos
ref: main     # tracks latest commit — useful during template development only
```

**Pinning to a tag gives you:**
- A known, auditable version — you can see exactly what each project is running
- Safe upgrades — Renovate proposes the bump, you review before it lands
- Easy rollback — if v1.2.0 breaks something, the cause is unambiguous

**Tracking `main`** delivers template changes immediately with no review step. Use only when actively developing the template. Never in repos others depend on.

---

<!-- _class: lead -->

# Part 4
## Getting Started

---

## Four commands

```bash
# 1. Install uv (skip if already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Make the repo rhiza-managed — writes .rhiza/template.yml, opens PR #1
/rhiza:init

# 3. After #1 merges: sync the template — this is where the files arrive (PR #2)
/rhiza:update

# 4. Install dev environment
make install
```

The `/rhiza:*` commands come from the rhiza Claude Code plugin — install it once with
`/plugin marketplace add Jebel-Quant/rhiza-claude` then `/plugin install rhiza@rhiza-claude`.

That's it. Your project is now Rhiza-managed.

---

## What `/rhiza:init` asks

Running `/rhiza:init` walks you through a few questions:

```
? Host and repo (GitHub or GitLab, owner/name):  Jebel-Quant/rhiza
? Template repo:                                  Jebel-Quant/rhiza
? Template ref (tag, branch, or commit):          v1.2.5
```

The template defaults to `Jebel-Quant/rhiza`; name any other `owner/repo` — a fork, or your own house template — and it is checked for reachability before being pinned.

The profile follows from the platform, so it is not asked. The result is `.rhiza/template.yml` — one file, under version control, that describes everything Rhiza will manage in this project.

`/rhiza:init` opens a PR on a `rhiza_init_<date>` branch. It syncs **nothing**: no CI, no `Makefile`, no gates. Merge it, then run `/rhiza:update` for the content.

---

## What you get on day one

After syncing with `core + github + tests + renovate`:

```
.github/workflows/rhiza_ci.yml          ← CI: test matrix on push and PRs
.github/workflows/rhiza_release.yml     ← Build + publish to PyPI on a tag
.pre-commit-config.yaml                 ← Local commit hooks (rhiza-hooks)
ruff.toml                               ← Linting config
Makefile                                ← make test · make lint
.python-version                         ← Pinned Python version
.editorconfig                           ← Editor consistency
```

None of this required manual configuration.

---

## The one manual step — `PAT_TOKEN`

Rhiza's automation (Renovate, releases) opens pull requests. GitHub requires a Personal Access Token for PRs that touch `.github/workflows/` files.

**Create a fine-grained token:**
> GitHub → Settings → Developer settings → Personal access tokens (fine-grained)

Required permissions: `contents: write`, `pull-requests: write`, `workflows: write`

Add it as `PAT_TOKEN` in your repository secrets — or as an org secret to cover all repos at once.

> Without `PAT_TOKEN`, automation falls back to `GITHUB_TOKEN`, which cannot write workflow files. PRs that touch workflow files will silently fail to open.

---

## PyPI publishing — OIDC Trusted Publishing

The release workflow publishes to PyPI **without a stored token**, using OpenID Connect:

```yaml
permissions:
  id-token: write   # required for OIDC — no PYPI_TOKEN needed
```

On PyPI: **Publishing → Trusted Publishers → Add**
Specify the repo name, workflow filename, and environment name. PyPI issues a short-lived credential at publish time.

**Benefits:**
- No token to rotate or accidentally expose
- Publish permission is tied to the specific workflow, not a person
- Revocation is instant — remove the trusted publisher on PyPI

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

The PR description explains what changed at a high level. If Renovate bumped the `ref`, check the template repo's release notes for the version you're upgrading to.

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

## Handling conflicts

A sync PR conflicts when you have edited a template-managed file locally.

**Option 1 — Accept the template version**
Discard your local change. Clean, but you lose your customisation.

**Option 2 — Keep your version and exclude**
Add the file to `exclude:` in `template.yml`, resolve the conflict in your favour. You now own that file permanently.

**Option 3 — Merge both changes manually**
Take what's useful from the template update and your local edit. Most effort, cleanest long-term result.

> If you find yourself regularly in option 2 or 3 for the same file, that file belongs in `exclude:`.

---

## The exclude list in practice

```yaml
exclude: |
  ruff.toml                            # our lint rules differ from template defaults
  .github/workflows/rhiza_ci.yml       # we use a custom test matrix
  Makefile.local                       # project-specific targets
```

**Exclude deliberately, not defensively.**

Every excluded file is a file you are now responsible for — including applying security fixes the template would otherwise deliver automatically.

Audit your exclude list when bumping the template version. Ask: *"Does the new template version of this file contain anything I should merge in manually?"*

---

<!-- _class: lead -->

# Part 6
## The Ecosystem

---

## rhiza-hooks — pre-commit checks

`rhiza-hooks` ships pre-commit hooks that catch config errors before they reach CI:

| Hook | What it checks |
|------|---------------|
| `check-rhiza-config` | `template.yml` is valid; repo and ref resolve |
| `check-rhiza-workflow-names` | Workflow files follow naming conventions |
| `check-makefile-targets` | `make test`, `make lint`, `make release` are present |
| `check-python-version-consistency` | `.python-version`, `pyproject.toml`, and CI matrix agree |
| `update-readme-help` | Embeds `make help` output into `README.md` |

Runs on every `git commit` — catching config errors locally, before anything reaches CI.

---

## Releasing — `/rhiza:release`

`/rhiza:release` prepares a release straight from your conventional-commit history:

| Step | What it does |
|------|-------------|
| Derive version | Reads the conventional commits since the last tag (via git-cliff) to pick the next semver |
| Bump | Updates the version in `pyproject.toml` |
| Changelog | Regenerates `CHANGELOG.md`, folding the unreleased commits under the new tag |
| Commit + tag | Commits and tags locally — then stops before pushing |

You review, then push the tag yourself. The pushed tag triggers `rhiza_release.yml`, which builds and publishes.

The old `version-matrix` and `coverage-badge` helpers are no longer user commands — that logic now lives **inside the reusable CI workflows** (`rhiza_ci.yml` derives the test matrix from `requires-python`; the coverage badge is generated during CI).

---

## The Rhiza ecosystem

| Tool | What it does |
|------|-------------|
| **rhiza-claude** | Claude Code plugin — the `/rhiza:*` command set (`init`, `update`, `quality`, `docs`, `release`, `status`, `uninstall`, `maffay`). The primary interface. |
| **rhiza-hooks** | Pre-commit hooks: validate config, check version consistency |
| **rhiza-brainbug** | Cross-repo test harness: runs contract tests on upstream commits |

---

## Who's using it

**The Rhiza tools themselves** — rhiza-claude and rhiza-hooks all sync from rhiza. The system eats its own cooking.

**External projects:**

| Project | Organisation | Bundles |
|---------|-------------|---------|
| `simulator` | Stanford CVXGRP | `core + github + tests` |
| `jsharpe` | tschm | `core + github + marimo` |
| `loman` | Janus Henderson | `core + github + tests + renovate` |
| `chebpy` | chebpy | `core + github` |

---

## GitLab support

Rhiza works on GitLab with the `gitlab` bundle replacing `github`:

```yaml
templates:
  - core
  - gitlab     # instead of github
  - tests
  - renovate
```

**What changes:** CI workflows become `.gitlab-ci.yml` pipeline files. Renovate opens merge requests. `PAT_TOKEN` → GitLab Personal Access Token with `api` scope.

**What doesn't change:** `template.yml`, `renovate.json`, the tooling (`rhiza-claude`, `rhiza-hooks`), and how you sync — you still run `/rhiza:update` in Claude Code.

---

<!-- _class: lead -->

# Part 7
## Adoption

---

## Starting fresh vs. migrating

**New project — the easy case:**

```bash
/rhiza:init      # config + skeleton, PR #1
/rhiza:update    # after #1 merges: the template content, PR #2
make install
```

Done. Rhiza-managed from day one.

**Existing project:**

```bash
/rhiza:init      # detects the existing repo from its origin and asks
                 # nothing; opens PR #1 on rhiza_init_<date>
/rhiza:update    # the first sync — this is the PR that needs review
```

PR #1 is nearly empty on an existing repo. The sync in PR #2 is where the diff appears: some files may already match, others may have local customisations — preserve those via `exclude:` in `template.yml` before merging.

---

## The migration path

1. **Audit your current setup** — list your CI files, linting configs, and Makefiles
2. **Start conservative** — begin with `core` only; add `github` once you've reviewed the workflow files
3. **Exclude what you own** — add locally-maintained files to `exclude:` before syncing
4. **Review the first sync PR carefully** — that is PR #2, from `/rhiza:update`; treat it as a code review, not a forced update
5. **Add Renovate** — add the `renovate` bundle and install the GitHub App
6. **Expand bundles gradually** — add `tests`, `docker`, etc. as your team gains confidence

> Don't try to adopt everything at once. The goal of the first PR is to get Rhiza in place with minimal disruption.

---

## Rolling out across a team

**Week 1** — Pick one low-risk repo as your pilot. Adopt Rhiza, run a sync cycle, review the process with the team.

**Weeks 2–3** — Add Rhiza to active projects. Fork the template into your org if you need custom standards.

**Month 2** — Add Renovate org-wide. Enable the Dependency Dashboard. Review the first round of version-bump PRs together.

**Ongoing** — New projects start with `/rhiza:init`. Legacy repos migrate at their next maintenance window.

**Governance** — One person or platform team owns the org's template fork. Changes go through PRs on the fork — reviewed before they propagate to all subscriber repos.

---

## Key takeaways

1. **Drift is structural** — it is the default outcome of one-shot scaffolding, not a failure of discipline.

2. **Existing template tools solve Day 0.** Rhiza solves Day 365.

3. **The PR model is the key insight.** Systematic coverage, opt-in per repo, auditable history.

4. **Setup is four commands.** Ongoing maintenance is reviewing a weekly PR.

5. **You stay in control.** `exclude:`, extension files, and org forks give full flexibility.

6. **Renovate closes the loop.** Without it, the `ref:` pin is frozen and drift returns.

7. **Adoption is gradual.** One repo at a time, one bundle at a time.

---

<!-- _class: lead -->

# Get started

```bash
/rhiza:init
```

*ῥίζα (ree-ZAH) — root*

**https://jebel-quant.github.io/rhiza-education/**
