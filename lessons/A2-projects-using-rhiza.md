# Appendix A2 — Projects Using Rhiza

The best evidence that a tool works is that its authors use it themselves. This appendix lists the public projects that are already synced with Rhiza, so you can inspect real `.rhiza/template.yml` files, see what bundles teams actually choose, and observe how the sync PRs look in practice.

## The Rhiza tools themselves

The most direct proof of Rhiza's value is that the Rhiza ecosystem tools are all managed by Rhiza. Each one has a `.rhiza/template.yml` and receives an update PR when the template changes — the same `/rhiza:update` workflow you set up in Lesson 6.

### rhiza-claude

[github.com/Jebel-Quant/rhiza-claude](https://github.com/Jebel-Quant/rhiza-claude)

The Claude Code plugin marketplace that ships the `rhiza` plugin — the primary interface to Rhiza and the source of the `/rhiza:*` commands used throughout this curriculum. It is itself a rhiza-managed repository, so its `template.yml` is a useful reference for what a tooling project's setup looks like.

### rhiza-hooks

[github.com/Jebel-Quant/rhiza-hooks](https://github.com/Jebel-Quant/rhiza-hooks)

The pre-commit hook repository. Because it is a Python package with its own CI and release pipeline, it uses the same Rhiza template as any other project. Notably, the `check-rhiza-config` hook it provides also validates its own `template.yml` — so every commit to rhiza-hooks runs Rhiza validation on itself.

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
ref: "v1.3.3"

profiles:
  - github-project
templates:
  - legal
  - github-paper

# Destination paths, as they land in this repo. Source-path entries
# (bundles/github/...) are inert since the exclude semantics were fixed.
exclude:
  - .github/workflows/rhiza_fuzzing.yml
  - .github/workflows/rhiza_weekly.yml
  - .github/workflows/rhiza_scorecard.yml
```

The three `exclude:` entries are the instructive part: the profile brings a full set of GitHub workflows, and this project opts out of three of them by naming the paths they land at. The comment above them records a real trap — template v1.3.0's predecessor matched `exclude:` against *source* paths, and entries written the old way became silently inert when that was fixed in rhiza-claude v0.7.0. If an exclusion stops working after an update, check which end of the path it names.

## External projects

The following projects live outside the Jebel-Quant organisation and have independently adopted Rhiza. Their `template.yml` files are public — they are among the most instructive examples of Rhiza in practice because they were written by people solving real problems, not by the team that built the tool.

### cvxgrp/simulator

[github.com/cvxgrp/simulator](https://github.com/cvxgrp/simulator) · PyPI: `cvxsimulator`

**cvxsimulator** is a backtesting framework for investment strategies, developed by the [Stanford CVXGRP](https://www.cvxgrp.org/) (the Convex Optimization Group behind CVXPY). Given a universe of assets and a time series of prices, it handles the accounting of a backtest — available cash, position sizing, P&L — leaving the strategy itself entirely up to you.

```yaml
# .rhiza/template.yml (cvxgrp/simulator)
repository: "jebel-quant/rhiza"
ref: "v1.3.3"

profiles:
  - github-project

templates:
  - legal
```

Notable choice: everything that used to be listed by hand — `core`, `github`, `tests`, `book`, `marimo` — is now covered by the `github-project` profile, leaving just one bundle to add explicitly. That bundle is `legal` (standard licence headers and notice files — common for projects from research institutions that need to be explicit about intellectual property). This is the profile-plus-extras pattern in its cleanest form, and it is worth comparing against the long hand-written `templates:` list this project used to carry.

---

### tschm/jsharpe

[github.com/tschm/jsharpe](https://github.com/tschm/jsharpe) · PyPI: `jsharpe`

**jsharpe** provides rigorous statistical analysis of Sharpe ratios, based on the research of Marcos López de Prado. The central question it answers is: *is this strategy's performance statistically significant, or could it be due to chance?* Key features include the Probabilistic Sharpe Ratio (PSR), corrections for non-Gaussian returns (skewness, excess kurtosis), autocorrelation adjustment, and multiple testing corrections (FDR, FWER) for strategy selection.

```yaml
# .rhiza/template.yml (tschm/jsharpe)
repository: "jebel-quant/rhiza"
ref: "v1.3.3"

profiles:
  - github-project

templates:
  - legal
```

jsharpe has converged on exactly the same shape as `cvxgrp/simulator`, which is itself the point: two unrelated projects, independently maintained, ending up with an identical four-line config is what the profile mechanism is for. It once carried an `exclude: ruff.toml` entry for custom linting rules that diverged from Rhiza's defaults; that divergence has since been resolved upstream and the exclusion dropped. Dropping an `exclude:` once you no longer need it is as much a part of the pattern in [Lesson 10](./10-customizing-safely.md) as adding one.

---

### chebpy/chebpy

[github.com/chebpy/chebpy](https://github.com/chebpy/chebpy) · PyPI: `chebfun`

**ChebPy** is a Python implementation of [Chebfun](http://www.chebfun.org/), the MATLAB library for numerical computing with functions. It lets you work with mathematical functions as first-class objects — differentiating, integrating, finding roots, and composing them — with machine-precision accuracy via Chebyshev polynomial approximations.

```yaml
# .rhiza/template.yml (chebpy/chebpy)
repository: "jebel-quant/rhiza"
ref: "v1.3.3"

profiles:
  - github-project

templates:
  - devcontainer
  # Ships .github/workflows/rhiza_paper.yml, which compiles docs/paper/*.tex and
  # publishes the PDF both as a workflow artifact and on the `paper` branch.
  - github-paper

exclude:
  - book/marimo/notebooks/rhiza.py
```

This is the most extensive selection of any external project here, and the best illustration of layering extras onto a profile. The `devcontainer` bundle adds a VS Code / GitHub Codespaces configuration — making it easy for contributors to open the project in a fully configured environment without any local setup. `github-paper` compiles the project's LaTeX paper in CI and publishes the PDF. Note also the comment left in the config: annotating *why* a bundle is there is good practice, since the next person to read the file is usually not the one who added the line.

The `exclude:` entry names `book/marimo/notebooks/rhiza.py` — the path as it lands in the repo. Exclusions match destination paths, so a `bundles/marimo/...` source path there would silently do nothing.

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

Loman is the useful counter-example on this page: it is the one project here still on the older `template-repository` / `template-branch` key names, still listing bundles by hand rather than using a profile, and pinned many releases behind the others. Both key formats are still accepted, so nothing is broken — but the config predates the `core`/language-layer split, so it names no language layer at all, and a `/rhiza:update` to a current `ref` is where that would get sorted out. Reading it next to the four-line configs above is a good way to see how much the format has absorbed.

When you visit any of these projects, the following are worth inspecting

| What to look at | Where to find it |
|-----------------|-----------------|
| Which bundles the team chose | `.rhiza/template.yml` → `templates:` key |
| What files Rhiza manages | `.github/workflows/rhiza_*.yml`, `Makefile`, `ruff.toml`, etc. |
| What they excluded or overrode | `.rhiza/template.yml` → `exclude:` key |
| What a sync PR looks like | Pull requests tab, filter by `rhiza-sync` label |
| How Renovate bumps the template version | Pull requests tab, filter by `renovate` label, look for `ref:` bumps in `template.yml` |

## A note on the configs you will find

Not every project here uses the current config format or best practices — and that is useful. You will find `template-repository` / `template-branch` alongside `repository` / `ref`; projects several releases behind the current template; `templates:` bundle lists rather than the `profiles:` shorthand; configs written before the `core`/language-layer split that name no `language:` at all; and `exclude:` entries that reflect real customisation decisions. Reading these configs as an outsider — asking "why did they exclude that?" or "why are they still on that ref?" — is one of the best ways to build intuition for the trade-offs described in this curriculum.

The direction of travel is visible across the page: the projects that keep current have converged on a profile plus a short list of extras, and the ones that have not are the ones still carrying a hand-maintained bundle list.

---

**Back to:** [Lesson 11 — The Rhiza Ecosystem](./11-the-rhiza-ecosystem.md) | [README](../README.md)
