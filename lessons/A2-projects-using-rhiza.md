# Appendix A2 — Projects Using Rhiza

The best evidence that a tool works is that its authors use it themselves. This appendix lists the public projects that are already synced with Rhiza, so you can inspect real `.rhiza/template.yml` files, see what bundles teams actually choose, and observe how the sync PRs look in practice.

## The Rhiza tools themselves

The most direct proof of Rhiza's value is that the Rhiza ecosystem tools are all managed by Rhiza. Each one has a `.rhiza/template.yml` and receives an update PR when the template changes — the same `/rhiza:update` workflow you set up in Lesson 6.

### rhiza-claude

[github.com/Jebel-Quant/rhiza-claude](https://github.com/Jebel-Quant/rhiza-claude)

The Claude Code plugin marketplace that ships the `rhiza` plugin — the primary interface to Rhiza and the source of the `/rhiza:*` commands used throughout this curriculum. It is the instructive *partial* case: it has no `.rhiza/template.yml`, because a plugin marketplace is not a project the template can shape. What it did adopt, in v0.12.0, is the `Makefile` shim and the pinned `RHIZA_TASK`, with its own targets moved to `local.mk` — so it runs the same gates as a managed repo without being synced by one. That separation is only possible because the tasks left the template (Lesson 11).

### rhiza-hooks

[github.com/Jebel-Quant/rhiza-hooks](https://github.com/Jebel-Quant/rhiza-hooks)

The pre-commit hook repository, and the fullest example here: `profiles: [github-project]` plus `legal`, pinned at `v1.7.1`, with four annotated exclusions. Because it is a Python package with its own CI and release pipeline, it uses the same Rhiza template as any other project, and the `check-rhiza-config` hook it provides validates its own `template.yml` — so every commit to rhiza-hooks runs Rhiza validation on itself.

Its `exclude:` block is worth reading in full, because every entry carries a comment explaining the trade-off it accepts. One of them is a fossil of the migration this curriculum describes: `.rhiza/.env` is excluded with a note that it only ever restated two `?=` defaults, which is exactly the class of setting that moved into `[tool.rhiza-task]`.

### rhiza-task and pytest-rhiza

[github.com/Jebel-Quant/rhiza-task](https://github.com/Jebel-Quant/rhiza-task) · [github.com/Jebel-Quant/pytest-rhiza](https://github.com/Jebel-Quant/pytest-rhiza)

Neither is rhiza-managed, and that is the point rather than an oversight. They ship the content the template *stopped* syncing — the tasks and the conformance checks — so a sync relationship would be circular. They are ordinary published Python packages that every managed repo depends on by pin.

## A real-world library: jquantstats

[github.com/Jebel-Quant/jquantstats](https://github.com/Jebel-Quant/jquantstats)

**jQuantStats** is a Python library for portfolio performance analytics aimed at quantitative traders and portfolio managers. It provides:

- Performance metrics: Sharpe ratio, Sortino ratio, volatility, drawdown
- Risk analysis: Value at Risk (VaR), Conditional VaR
- Interactive Plotly visualisations for returns, drawdowns, and benchmarks
- Support for both pandas and polars DataFrames

jquantstats is a good example of adopting Rhiza for a scientific Python library — not a tooling project, but a domain library with its own test suite, docs, and release cycle:

```yaml
# .rhiza/template.yml (Jebel-Quant/jquantstats)
repository: "jebel-quant/rhiza"
ref: "v1.7.1"

profiles:
  - github-project
templates:
  - legal
  - github-paper

# Destination paths, as they land in this repo. Source-path entries
# (bundles/github/...) are inert since the exclude semantics were fixed.
exclude:
  - .github/workflows/rhiza_weekly.yml
  - .github/workflows/rhiza_scorecard.yml
```

The `exclude:` entries are the instructive part: the profile brings a full set of GitHub workflows, and this project opts out of two of them by naming the paths they land at. The comment above them records a real trap — template v1.3.0's predecessor matched `exclude:` against *source* paths, and entries written the old way became silently inert when that was fixed in rhiza-claude v0.7.0. If an exclusion stops working after an update, check which end of the path it names.

There used to be a third entry here, `.github/workflows/rhiza_fuzzing.yml`. Template v1.5.0 retired the fuzzing workflow outright, so the exclusion had nothing left to exclude and was dropped. That is the maintenance an `exclude:` block needs: an entry that matches nothing costs nothing at runtime and quietly misleads the next reader.

## External projects

The following projects live outside the Jebel-Quant organisation and have independently adopted Rhiza. Their `template.yml` files are public — they are among the most instructive examples of Rhiza in practice because they were written by people solving real problems, not by the team that built the tool.

### cvxgrp/simulator

[github.com/cvxgrp/simulator](https://github.com/cvxgrp/simulator) · PyPI: `cvxsimulator`

**cvxsimulator** is a backtesting framework for investment strategies, developed by the [Stanford CVXGRP](https://www.cvxgrp.org/) (the Convex Optimization Group behind CVXPY). Given a universe of assets and a time series of prices, it handles the accounting of a backtest — available cash, position sizing, P&L — leaving the strategy itself entirely up to you.

```yaml
# .rhiza/template.yml (cvxgrp/simulator)
repository: "jebel-quant/rhiza"
ref: "v1.7.1"

profiles:
  - github-project

templates:
  - legal

# Template-owned paths this repo declines to sync. Matched against *destination*
# paths, so entries are written as `.github/...`, never `bundles/github/...`,
# which matches nothing silently. A directory entry covers everything under it.
exclude:
  # The template's PAT_TOKEN and release-secret walkthrough — addressed to
  # whoever set the repository up. Upstream is where it belongs.
  - .github/CONFIG.md
  # The template's copy enumerates security measures generically; the accurate
  # list differs per repo. Excluding does not delete: an excluded path is never
  # treated as an orphan, so the existing file simply stops being overwritten.
  - SECURITY.md
  # Required checks and tag patterns are decided per repo.
  - .github/rulesets/main-branch-protection.json
  - .github/rulesets/tag-protection.json
```

Notable choice: everything that used to be listed by hand — `core`, `github`, `tests`, `book`, `marimo` — is now covered by the `github-project` profile, leaving one bundle to add explicitly. That bundle is `legal` (standard licence headers and notice files — common for projects from research institutions that need to be explicit about intellectual property).

The `exclude:` block is the model to copy, and not for its contents: every entry says *why*, and three of them turn on one fact worth internalising — **excluding a file does not delete it.** An excluded path is never treated as an orphan, so `SECURITY.md` stays exactly as this repo wrote it and merely stops being overwritten on each sync.

---

### tschm/jsharpe

[github.com/tschm/jsharpe](https://github.com/tschm/jsharpe) · PyPI: `jsharpe`

**jsharpe** provides rigorous statistical analysis of Sharpe ratios, based on the research of Marcos López de Prado. The central question it answers is: *is this strategy's performance statistically significant, or could it be due to chance?* Key features include the Probabilistic Sharpe Ratio (PSR), corrections for non-Gaussian returns (skewness, excess kurtosis), autocorrelation adjustment, and multiple testing corrections (FDR, FWER) for strategy selection.

```yaml
# .rhiza/template.yml (tschm/jsharpe)
repository: "jebel-quant/rhiza"
ref: "v1.6.0"

profiles:
  - github-project

templates:
  # Ships .github/workflows/rhiza_paper.yml, which compiles docs/paper/*.tex
  # into a PDF published as a workflow artifact (and, via the book, as a
  # docs-site asset). Pulls in the paper layout the workflow expects.
  - github-paper
  - legal

exclude:
  # SECURITY.md makes factual claims about THIS repo's security posture.
  # Only the repo knows which are true, so it is owned here.
  - SECURITY.md
  - .github/CONFIG.md
```

jsharpe has converged on nearly the same shape as `cvxgrp/simulator`, which is itself the point: two unrelated projects, independently maintained, arriving at the same profile-plus-extras pattern and the same two exclusions is what the mechanism is for. It once carried an `exclude: ruff.toml` entry for custom linting rules that diverged from Rhiza's defaults; that divergence has since been resolved upstream and the exclusion dropped. Dropping an `exclude:` once you no longer need it is as much a part of the pattern in [Lesson 10](./10-customizing-safely.md) as adding one.

Note also that it sits at `v1.6.0` while `cvxgrp/simulator` is at `v1.7.1`. Both are fine. Being a release behind is the normal resting state of a project that adopts updates deliberately rather than automatically — the `ref` is a decision, not a race.

---

### chebpy/chebpy

[github.com/chebpy/chebpy](https://github.com/chebpy/chebpy) · PyPI: `chebfun`

**ChebPy** is a Python implementation of [Chebfun](http://www.chebfun.org/), the MATLAB library for numerical computing with functions. It lets you work with mathematical functions as first-class objects — differentiating, integrating, finding roots, and composing them — with machine-precision accuracy via Chebyshev polynomial approximations.

```yaml
# .rhiza/template.yml (chebpy/chebpy)
repository: "jebel-quant/rhiza"
ref: "v1.6.0"

profiles:
  - github-project

templates:
  - devcontainer
  # Ships .github/workflows/rhiza_paper.yml, which compiles docs/paper/*.tex and
  # publishes the PDF both as a workflow artifact and on the `paper` branch.
  - github-paper

# `exclude:` is matched against DESTINATION paths — where a file lands here, not
# where it lives in the template clone. An entry spelled clone-relative
# (`bundles/github/.github/...`) matches nothing, silently.
exclude:
  # Generic community boilerplate; issue and discussion forms are a repo-owned
  # editorial choice rather than something the template should keep overwriting.
  - .github/CONFIG.md
```

This is the most extensive bundle selection of any external project here, and the best illustration of layering extras onto a profile. The `devcontainer` bundle adds a VS Code / GitHub Codespaces configuration — making it easy for contributors to open the project in a fully configured environment without any local setup. `github-paper` compiles the project's LaTeX paper in CI and publishes the PDF. Note the comment left in the config: annotating *why* a bundle is there is good practice, since the next person to read the file is usually not the one who added the line.

This config used to carry a second exclusion, `book/marimo/notebooks/rhiza.py`, and its removal is the most instructive line on this page. It had been there since v1.2.5 and **never matched anything** — no bundle in v1.3.4 or v1.4.2 ships a notebook to a consumer, and no such file existed in the tree. Nothing was un-excluded by deleting it. An `exclude:` entry that matches nothing does not announce itself; it just sits there looking like a decision someone made for a reason. Audit yours when you cross a template version that moves files around.

---

### janushendersonassetallocation/loman

[github.com/janushendersonassetallocation/loman](https://github.com/janushendersonassetallocation/loman) · PyPI: `loman`

**Loman** is a DAG-based computation manager for complex analytical workflows. It tracks the state of computations and their dependencies, enabling intelligent partial recalculations: when an input changes, only the downstream nodes that depend on it are rerun. It is designed for data pipelines, real-time pricing systems, and research workflows where recomputing everything on each change is too expensive.

```yaml
# .rhiza/template.yml (janushendersonassetallocation/loman)
template-repository: "jebel-quant/rhiza"
template-branch: "v0.10.3"

templates:
  - devcontainer
  - github
  - book
  - marimo
  - tests
```

Loman is the useful counter-example on this page, and it has become a sharper one with every release. It is the one project here still on the older `template-repository` / `template-branch` key names, still listing bundles by hand rather than using a profile, and pinned at `v0.10.3` — many releases behind the others. Both key formats are still accepted, so nothing is broken today.

But look at the bundle list against the 26 bundles that exist in v1.7.1: `book` still exists, and **`marimo` and `tests` do not** — they are not deprecated names, they are names the current template would reject. The config also predates the `core`/language-layer split, so it names no language layer. A `/rhiza:update` to a current `ref` is where all of that gets sorted out, and it would not be a quiet update: it crosses v1.4.0, which deletes the synced make layer this repo is still running on. Reading it next to the configs above is a good way to see how much the format has absorbed — and a fair picture of what deferring updates for a year actually costs.

When you visit any of these projects, the following are worth inspecting

| What to look at | Where to find it |
|-----------------|-----------------|
| Which bundles the team chose | `.rhiza/template.yml` → `templates:` key |
| What files Rhiza manages | `.rhiza/template.lock`, which lists them exactly — or `.github/workflows/rhiza_*.yml`, `Makefile`, `ruff.toml` by eye |
| Which task versions they run | `RHIZA_TASK` in the `Makefile`, and `[tool.rhiza-task]` in `pyproject.toml` |
| What they excluded or overrode | `.rhiza/template.yml` → `exclude:` key |
| What a sync PR looks like | Pull requests tab, filter by `rhiza-sync` label |
| How Renovate bumps the template version | Pull requests tab, filter by `renovate` label, look for `ref:` bumps in `template.yml` |

## A note on the configs you will find

Not every project here uses the current config format or best practices — and that is useful. You will find `template-repository` / `template-branch` alongside `repository` / `ref`; projects several releases behind the current template; `templates:` bundle lists rather than the `profiles:` shorthand; bundle names that no longer exist (`tests`, `marimo`, `paper`); configs written before the `core`/language-layer split that name no `language:` at all; and `exclude:` entries that reflect real customisation decisions — including one or two that stopped matching anything years ago. Reading these configs as an outsider — asking "why did they exclude that?" or "why are they still on that ref?" — is one of the best ways to build intuition for the trade-offs described in this curriculum.

The direction of travel is visible across the page: the projects that keep current have converged on a profile plus a short list of well-commented extras, and the ones that have not are the ones still carrying a hand-maintained bundle list. Note too what is *absent* from every current config on this page — nothing here configures the tasks. Since v1.4.0 that lives in `[tool.rhiza-task]` in each project's own `pyproject.toml`, outside Rhiza's reach entirely.

---

**Back to:** [Lesson 11 — The Rhiza Ecosystem](./11-the-rhiza-ecosystem.md) | [README](../README.md)
