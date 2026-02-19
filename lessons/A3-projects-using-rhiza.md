# Appendix A3 — Projects Using Rhiza

The best evidence that a tool works is that its authors use it themselves. This appendix lists the public projects that are already synced with Rhiza, so you can inspect real `.rhiza/template.yml` files, see what bundles teams actually choose, and observe how the sync PRs look in practice.

## The Rhiza tools themselves

The most direct proof of Rhiza's value is that the Rhiza ecosystem tools are all managed by Rhiza. Each one has a `.rhiza/template.yml` and receives sync PRs when the template is updated — the same workflow you set up in Lesson 6.

### rhiza-cli

[github.com/Jebel-Quant/rhiza-cli](https://github.com/Jebel-Quant/rhiza-cli)

The CLI package that provides `uvx rhiza`. Being a Python tool with CI, tests, and a release workflow, it is a natural consumer of its own template. Its `template.yml` is a useful reference for what a typical `core + github + tests + renovate` setup looks like.

### rhiza-hooks

[github.com/Jebel-Quant/rhiza-hooks](https://github.com/Jebel-Quant/rhiza-hooks)

The pre-commit hook repository. Because it is a Python package with its own CI and release pipeline, it uses the same Rhiza template as any other project. Notably, the `check-rhiza-config` hook it provides also validates its own `template.yml` — so every commit to rhiza-hooks runs Rhiza validation on itself.

### rhiza-tools

[github.com/Jebel-Quant/rhiza-tools](https://github.com/Jebel-Quant/rhiza-tools)

The utility command package. Its CI pipeline uses `version-matrix` (from rhiza-tools) to generate the Python test matrix and `generate-coverage-badge` to publish the coverage badge — tools built by the project, consumed by its own CI, all wired together by the Rhiza template.

### marimushka

[github.com/Jebel-Quant/marimushka](https://github.com/Jebel-Quant/marimushka)

The notebook export tool (covered in [Appendix A2](./A2-marimushka.md)). It uses the `marimo` bundle from Rhiza to publish its own documentation notebooks to GitHub Pages — again, the tool consuming its own output.

## A real-world library: jquantstats

[github.com/Jebel-Quant/jquantstats](https://github.com/Jebel-Quant/jquantstats)

**jQuantStats** is a Python library for portfolio performance analytics aimed at quantitative traders and portfolio managers. It provides:

- Performance metrics: Sharpe ratio, Sortino ratio, volatility, drawdown
- Risk analysis: Value at Risk (VaR), Conditional VaR
- Interactive Plotly visualisations for returns, drawdowns, and benchmarks
- Support for both pandas and polars DataFrames

jquantstats is a good example of adopting Rhiza for a scientific Python library — not a tooling project, but a domain library with its own test suite, docs, and release cycle. Its `template.yml` is worth reading if you work on that kind of project.

## External projects

The following projects live outside the Jebel-Quant organisation and have independently adopted Rhiza. Their `template.yml` files are public — they are among the most instructive examples of Rhiza in practice because they were written by people solving real problems, not by the team that built the tool.

### cvxgrp/simulator

[github.com/cvxgrp/simulator](https://github.com/cvxgrp/simulator) · PyPI: `cvxsimulator`

**cvxsimulator** is a backtesting framework for investment strategies, developed by the [Stanford CVXGRP](https://www.cvxgrp.org/) (the Convex Optimization Group behind CVXPY). Given a universe of assets and a time series of prices, it handles the accounting of a backtest — available cash, position sizing, P&L — leaving the strategy itself entirely up to you.

```yaml
# .rhiza/template.yml (cvxgrp/simulator)
template-repository: "jebel-quant/rhiza"
template-branch: "v0.8.0"

templates:
  - core
  - github
  - legal
  - tests
  - book
  - marimo
```

Notable choices: the `legal` bundle (adds standard licence headers and notice files — common for projects from research institutions that need to be explicit about intellectual property) and the `marimo` bundle (interactive notebook demos of backtesting strategies published to GitHub Pages). The `book` bundle deploys API documentation on every push.

> **Config format note:** This project uses the older `template-repository` / `template-branch` key names rather than the current `repository` / `ref`. The tool accepts both; `uvx rhiza migrate` can update the format automatically.

---

### tschm/jsharpe

[github.com/tschm/jsharpe](https://github.com/tschm/jsharpe) · PyPI: `jsharpe`

**jsharpe** provides rigorous statistical analysis of Sharpe ratios, based on the research of Marcos López de Prado. The central question it answers is: *is this strategy's performance statistically significant, or could it be due to chance?* Key features include the Probabilistic Sharpe Ratio (PSR), corrections for non-Gaussian returns (skewness, excess kurtosis), autocorrelation adjustment, and multiple testing corrections (FDR, FWER) for strategy selection.

```yaml
# .rhiza/template.yml (tschm/jsharpe)
repository: "jebel-quant/rhiza"
ref: "v0.8.0"

templates:
  - core
  - github
  - tests
  - legal
  - book
  - marimo

exclude:
  - ruff.toml
```

The `exclude: ruff.toml` is the most instructive part of this config. The project has custom linting rules that diverge from Rhiza's defaults — rather than fighting the sync, the author added `ruff.toml` to `exclude:` and manages it locally. This is exactly the pattern described in [Lesson 9](./09-customizing-safely.md).

---

### chebpy/chebpy

[github.com/chebpy/chebpy](https://github.com/chebpy/chebpy) · PyPI: `chebfun`

**ChebPy** is a Python implementation of [Chebfun](http://www.chebfun.org/), the MATLAB library for numerical computing with functions. It lets you work with mathematical functions as first-class objects — differentiating, integrating, finding roots, and composing them — with machine-precision accuracy via Chebyshev polynomial approximations.

```yaml
# .rhiza/template.yml (chebpy/chebpy)
repository: "jebel-quant/rhiza"
ref: "v0.8.0"

templates:
  - devcontainer
  - core
  - github
  - book
  - marimo
  - tests
  - presentation
```

This is the most extensive bundle selection of any external project here. The `devcontainer` bundle adds a VS Code / GitHub Codespaces configuration — making it easy for contributors to open the project in a fully configured environment without any local setup. The `presentation` bundle generates slide decks from Markdown, used to produce shareable talks about the library. Worth looking at if you are building a project intended for community contribution.

---

### janushendersonassetallocation/loman

[github.com/janushendersonassetallocation/loman](https://github.com/janushendersonassetallocation/loman) · PyPI: `loman`

**Loman** is a DAG-based computation manager for complex analytical workflows, developed by [Janus Henderson Asset Allocation](https://www.janushenderson.com/) — a global asset management firm. It tracks the state of computations and their dependencies, enabling intelligent partial recalculations: when an input changes, only the downstream nodes that depend on it are rerun. It is designed for data pipelines, real-time pricing systems, and research workflows where recomputing everything on each change is too expensive.

```yaml
# .rhiza/template.yml (janushendersonassetallocation/loman)
template-repository: jebel-quant/rhiza
template-branch: main

templates:
  - devcontainer
  - github
  - core
  - book
  - marimo
  - tests

exclude:
  - book/marimo/notebooks/rhiza.py
```

Two things stand out. First, `template-branch: main` — this project tracks the template's `main` branch rather than a pinned tag, meaning it receives template changes as they land rather than via a Renovate version-bump PR. This gives faster access to fixes but removes the review step before changes arrive. Second, the `exclude` entry for `book/marimo/notebooks/rhiza.py` — this is a specific notebook inside the docs that the team manages locally, likely a Rhiza integration demo they have customised for their workflow.

Most significantly: **Loman is a production tool at a real asset management firm.** Its adoption is the clearest signal that Rhiza works at professional scale.

## What to look at in each repo

When you visit any of these projects, the following are worth inspecting:

| What to look at | Where to find it |
|-----------------|-----------------|
| Which bundles the team chose | `.rhiza/template.yml` → `templates:` key |
| What files Rhiza manages | `.github/workflows/rhiza_*.yml`, `Makefile`, `ruff.toml`, etc. |
| What they excluded or overrode | `.rhiza/template.yml` → `exclude:` key |
| What a sync PR looks like | Pull requests tab, filter by `rhiza-sync` label |
| How Renovate bumps the template version | Pull requests tab, filter by `renovate` label, look for `ref:` bumps in `template.yml` |

## A note on the configs you will find

Not every project here uses the current config format or best practices — and that is useful. You will find `template-repository` / `template-branch` alongside `repository` / `ref`; projects tracking `main` rather than a pinned tag; and `exclude:` entries that reflect real customisation decisions. Reading these configs as an outsider — asking "why did they exclude that?" or "why are they on `main`?" — is one of the best ways to build intuition for the trade-offs described in this curriculum.

---

**Back to:** [Lesson 10 — The Rhiza Ecosystem](./10-the-rhiza-ecosystem.md) | [README](../README.md)
