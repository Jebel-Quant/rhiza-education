# Rhiza Education

Welcome to the Rhiza training curriculum. These lessons teach you how to adopt, configure, and work with **Rhiza** — the living template system that keeps Python project boilerplate consistent and up to date across all your repos.

## Curriculum

| Lesson | Title | What you will learn |
|--------|-------|---------------------|
| 0 | [uv and uvx](00-uv-and-uvx.md) | The package manager and tool runner that underpins the whole Rhiza ecosystem |
| 1 | [Python Project Conventions](01-python-project-conventions.md) | The src layout, pyproject.toml (PEP 621), and tests folder structure Rhiza assumes |
| 2 | [Why Rhiza?](02-why-rhiza.md) | The one-shot scaffolding problem and how Rhiza solves it |
| 3 | [Core Concepts](03-core-concepts.md) | Templates, projects, the sync mechanism, and key abstractions |
| 4 | [Getting Started](04-getting-started.md) | Setting up Rhiza in a new project from scratch |
| 5 | [Configuring Your Template](05-configuring-your-template.md) | Every field in `.rhiza/template.yml` explained |
| 6 | [The Sync Lifecycle](06-the-sync-lifecycle.md) | What triggers a sync PR, what it contains, and how to handle it |
| 7 | [Customising Safely](07-customizing-safely.md) | How to modify Rhiza-managed files without conflicting with future syncs |

## Appendices

| Appendix | Title | Audience |
|----------|-------|----------|
| A1 | [Rhiza on GitLab](A1-gitlab-users.md) | Teams whose projects live on GitLab rather than GitHub |

## How to use this curriculum

Work through lessons 0–7 in order on your first pass. Each lesson builds on the previous one. The appendices are self-contained — read whichever applies to your setup.

Lesson 4 is hands-on: you will need a GitHub (or GitLab) account and the ability to create a repository.
