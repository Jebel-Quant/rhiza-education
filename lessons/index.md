# Rhiza Education

Welcome to the Rhiza training curriculum. These lessons teach you how to adopt, configure, and work with **Rhiza** — the living template system that keeps Python project boilerplate consistent and up to date across all your repos.

## Curriculum

| Lesson | Title | What you will learn |
|--------|-------|---------------------|
| Preamble | [The Repo Zoo Problem](preamble-repo-zoo.md) | What goes wrong when you have many repos, why template systems can't fix it, and when Rhiza was born |
| 1 | [CI/CD Concepts](01-cicd-concepts.md) | Pipelines, jobs, triggers, GitHub Actions, secrets, matrix builds — the vocabulary Rhiza assumes |
| 2 | [uv and uvx](02-uv-and-uvx.md) | The package manager and tool runner that underpins the whole Rhiza ecosystem |
| 3 | [Python Project Conventions](03-python-project-conventions.md) | The src layout, pyproject.toml (PEP 621), and tests folder structure Rhiza assumes |
| 4 | [Why Rhiza?](04-why-rhiza.md) | The one-shot scaffolding problem and how Rhiza solves it |
| 5 | [Core Concepts](05-core-concepts.md) | Templates, projects, the sync mechanism, and key abstractions |
| 6 | [Getting Started](06-getting-started.md) | Setting up Rhiza in a new project from scratch |
| 7 | [Configuring Your Template](07-configuring-your-template.md) | Every field in `.rhiza/template.yml` explained |
| 8 | [The Sync Lifecycle](08-the-sync-lifecycle.md) | What triggers a sync PR, what it contains, and how to handle it |
| 9 | [Customising Safely](09-customizing-safely.md) | How to modify Rhiza-managed files without conflicting with future syncs |
| 10 | [The Rhiza Ecosystem](10-the-rhiza-ecosystem.md) | rhiza-cli, rhiza-hooks, rhiza-tools, rhiza-go, rhiza-manager, and repo-monitor |
| 11 | [Further Reading](11-further-reading.md) | Direct links to every doc file across the Rhiza repos, organised by topic |

## Appendices

| Appendix | Title | Audience |
|----------|-------|----------|
| A1 | [Rhiza on GitLab](A1-gitlab-users.md) | Teams whose projects live on GitLab rather than GitHub |
| A2 | [Publishing Notebooks with Marimushka](A2-marimushka.md) | Exporting marimo notebooks to a static site with the `marimo` bundle |
| A3 | [Projects Using Rhiza](A3-projects-using-rhiza.md) | Real repos using Rhiza — from Stanford's CVXGRP to Janus Henderson — with annotated `template.yml` files |
| A4 | [Contributors](A4-contributors.md) | The people who built Rhiza and its ecosystem, with profiles and contribution counts |

## How to use this curriculum

Start with the Preamble if the repo-at-scale problem is new to you, then work through lessons 1–11 in order. Each lesson builds on the previous one. The appendices are self-contained — read whichever applies to your setup.

Lesson 6 is hands-on: you will need a GitHub (or GitLab) account and the ability to create a repository.
