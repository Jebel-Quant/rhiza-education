<p align="center">
  <img src="lessons/assets/rhiza-logo.svg" width="120" alt="Rhiza logo" />
</p>

# rhiza-education

Training for and with [Rhiza](https://github.com/Jebel-Quant/rhiza) — the living template system for Python projects.

The companion website (rendered, searchable) is at **https://jebel-quant.github.io/rhiza-education/**.

## Who this is for

Developers who are comfortable with Python, git, and basic CI/CD, and want to adopt Rhiza in a new or existing project.

## Curriculum

| # | Lesson | What you'll learn |
|---|--------|-------------------|
| — | [Preamble — The Repo Zoo Problem](lessons/preamble-repo-zoo.md) | What goes wrong at scale, why template systems can't fix it, and when Rhiza was born |
| 1 | [CI/CD Concepts](lessons/01-cicd-concepts.md) | Pipelines, jobs, triggers, GitHub Actions, matrix builds — the vocabulary the curriculum assumes |
| 2 | [uv and uvx](lessons/02-uv-and-uvx.md) | The package manager and tool runner that underpins the Rhiza ecosystem |
| 3 | [Python Project Conventions](lessons/03-python-project-conventions.md) | src layout, PEP 621 `pyproject.toml`, and `tests/` structure |
| 4 | [Why Rhiza?](lessons/04-why-rhiza.md) | The problem with one-shot scaffolding and how Rhiza solves it |
| 5 | [Core Concepts](lessons/05-core-concepts.md) | The key abstractions: template repos, materialisation, and the sync loop |
| 6 | [Getting Started](lessons/06-getting-started.md) | Install Rhiza, initialise a project, and run your first materialise |
| 7 | [Configuring Your Template](lessons/07-configuring-your-template.md) | Anatomy of `template.yml`, bundles, include/exclude patterns |
| 8 | [The Sync Lifecycle](lessons/08-the-sync-lifecycle.md) | How automated sync PRs work and how to review them |
| 9 | [Renovate](lessons/09-renovate.md) | How Renovate keeps your `ref:` pin current and why it is essential at scale |
| 10 | [Customising Safely](lessons/10-customizing-safely.md) | Extend Rhiza-managed projects without fighting the sync |
| 11 | [The Rhiza Ecosystem](lessons/11-the-rhiza-ecosystem.md) | rhiza-cli, rhiza-hooks, rhiza-tools, rhiza-go, rhiza-manager, and repo-monitor |
| 12 | [Further Reading](lessons/12-further-reading.md) | Direct links to every doc file across the Rhiza repos, organised by topic |

Work through the lessons in order — each one builds on the last.

## Appendices

| # | Appendix | What you'll learn |
|---|----------|-------------------|
| A1 | [GitLab Users](lessons/A1-gitlab-users.md) | What changes when your project lives on GitLab instead of GitHub |
| A2 | [Marimushka](lessons/A2-marimushka.md) | Publishing marimo notebooks as a static site with the `marimo` bundle |
| A3 | [Projects Using Rhiza](lessons/A3-projects-using-rhiza.md) | Real repos using Rhiza — from Stanford's CVXGRP to Janus Henderson — with annotated `template.yml` files |
| A4 | [Contributors](lessons/A4-contributors.md) | The people who built Rhiza and its ecosystem, with profiles and contribution counts |

Work through the appendices that apply to your setup — each is self-contained.
