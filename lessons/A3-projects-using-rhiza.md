# Appendix A3 — Projects Using Rhiza

The best evidence that a tool works is that its authors use it themselves. This appendix lists the public projects that are already synced with Rhiza, so you can inspect real `.rhiza/template.yml` files, see what bundles teams actually choose, and observe how the sync PRs look in practice.

## The Rhiza tools themselves

The most direct proof of Rhiza's value is that the Rhiza ecosystem tools are all managed by Rhiza. Each one has a `.rhiza/template.yml` and receives sync PRs when the template is updated — the same workflow you set up in Lesson 4.

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

## What to look at in each repo

When you visit any of these projects, the following are worth inspecting:

| What to look at | Where to find it |
|-----------------|-----------------|
| Which bundles the team chose | `.rhiza/template.yml` → `templates:` key |
| What files Rhiza manages | `.github/workflows/rhiza_*.yml`, `Makefile`, `ruff.toml`, etc. |
| What they excluded or overrode | `.rhiza/template.yml` → `exclude:` key |
| What a sync PR looks like | Pull requests tab, filter by `rhiza-sync` label |
| How Renovate bumps the template version | Pull requests tab, filter by `renovate` label, look for `ref:` bumps in `template.yml` |

## A note on scale

These are all Jebel-Quant projects — Rhiza is still in early adoption beyond the organisation that built it. That is useful context: the patterns here are not theoretical. Every PR, every sync, every release in these repos went through the same workflow described in this curriculum. The rough edges are visible in the git history, and the solutions are there too.

---

**Back to:** [Lesson 8 — The Rhiza Ecosystem](./08-the-rhiza-ecosystem.md) | [README](../README.md)
