# Rhiza Education

Welcome to the Rhiza training curriculum. These lessons teach you how to adopt, configure, and work with **Rhiza** — the living template system that keeps project boilerplate consistent and up to date across all your repos.

The examples are Python throughout, which is where the template is most complete. Since template `v1.3.0` Rhiza is multi-language — `core` is language-neutral, and a language layer (`python-core`, `rust-core`, or `go-core`) supplies the build and test tasks — so everything you learn here about config, bundles, and the sync lifecycle carries over to a Rust or Go repo unchanged.

This edition is current for **rhiza `v1.7.1`** and **rhiza-claude `v0.13.0`**. If you are coming from material written against v1.3.x, the change to read first is v1.4.0: the synced make layer was replaced by a pinned CLI, [`rhiza-task`](https://github.com/Jebel-Quant/rhiza-task). Lesson 5 introduces it, Lesson 10 covers what that means for customisation, and Lesson 11 explains why.

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
| 9 | [Renovate](09-renovate.md) | How Renovate keeps your `ref:` pin current, the two-part update flow, and how to configure it |
| 10 | [Customising Safely](10-customizing-safely.md) | `local.mk`, `[tool.rhiza-task]`, `local-setup.sh` and `exclude:` — extending a project without fighting the sync |
| 11 | [The Rhiza Ecosystem](11-the-rhiza-ecosystem.md) | rhiza-claude, rhiza-task, pytest-rhiza, rhiza-hooks, and rhiza-brainbug |
| 12 | [Further Reading](12-further-reading.md) | Direct links to every doc file across the Rhiza repos, organised by topic |

## Appendices

| Appendix | Title | Audience |
|----------|-------|----------|
| A1 | [Rhiza on GitLab](A1-gitlab-users.md) | Teams whose projects live on GitLab rather than GitHub |
| A2 | [Projects Using Rhiza](A2-projects-using-rhiza.md) | Real repos using Rhiza — from Stanford's CVXGRP to Janus Henderson — with annotated `template.yml` files |
| A3 | [Contributors](A3-contributors.md) | The people who built Rhiza and its ecosystem, with profiles and contribution counts |

## How to use this curriculum

Start with the Preamble if the repo-at-scale problem is new to you, then work through lessons 1–11 in order. Each lesson builds on the previous one. The appendices are self-contained — read whichever applies to your setup.

Lesson 6 is hands-on: you will need a GitHub (or GitLab) account and the ability to create a repository.
