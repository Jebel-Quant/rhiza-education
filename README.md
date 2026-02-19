# rhiza-education

Training for and with [Rhiza](https://github.com/Jebel-Quant/rhiza) — the living template system for Python projects.

The companion website (rendered, searchable) is at **https://jebel-quant.github.io/rhiza-education/**.

## Who this is for

Developers who are comfortable with Python, git, and basic CI/CD, and want to adopt Rhiza in a new or existing project.

## Curriculum

| # | Lesson | What you'll learn |
|---|--------|-------------------|
| 0 | [uv and uvx](lessons/00-uv-and-uvx.md) | The package manager and tool runner that underpins the Rhiza ecosystem |
| 1 | [Python Project Conventions](lessons/01-python-project-conventions.md) | src layout, PEP 621 `pyproject.toml`, and `tests/` structure |
| 2 | [Why Rhiza?](lessons/02-why-rhiza.md) | The problem with one-shot scaffolding and how Rhiza solves it |
| 3 | [Core Concepts](lessons/03-core-concepts.md) | The key abstractions: template repos, materialisation, and the sync loop |
| 4 | [Getting Started](lessons/04-getting-started.md) | Install Rhiza, initialise a project, and run your first materialise |
| 5 | [Configuring Your Template](lessons/05-configuring-your-template.md) | Anatomy of `template.yml`, bundles, include/exclude patterns |
| 6 | [The Sync Lifecycle](lessons/06-the-sync-lifecycle.md) | How automated sync PRs work and how to review them |
| 7 | [Customising Safely](lessons/07-customizing-safely.md) | Extend Rhiza-managed projects without fighting the sync |
| 8 | [The Rhiza Ecosystem](lessons/08-the-rhiza-ecosystem.md) | rhiza-cli, rhiza-hooks, rhiza-tools, rhiza-go, rhiza-manager, and repo-monitor |

Work through the lessons in order — each one builds on the last.

## Appendices

| # | Appendix | What you'll learn |
|---|----------|-------------------|
| A1 | [GitLab Users](lessons/A1-gitlab-users.md) | What changes when your project lives on GitLab instead of GitHub |
| A2 | [Marimushka](lessons/A2-marimushka.md) | Publishing marimo notebooks as a static site with the `marimo` bundle |
| A3 | [Projects Using Rhiza](lessons/A3-projects-using-rhiza.md) | Real repos using Rhiza — from Stanford's CVXGRP to Janus Henderson — with annotated `template.yml` files |
