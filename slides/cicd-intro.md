---
marp: true
theme: default
paginate: true
footer: "CI/CD for Complete Beginners · jebel-quant.github.io/rhiza-education"
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
---

<!-- _class: lead -->

# CI/CD

## For Complete Beginners

What it is, why it matters, and how it works

---

## Agenda

1. **The problem** — "works on my machine"
2. **What CI is** — catching problems automatically
3. **What CD is** — shipping automatically
4. **How it works** — pipelines, jobs, and steps
5. **GitHub Actions** — CI/CD built into GitHub
6. **What you gain** — why teams adopt it

---

<!-- _class: lead -->

# Part 1
## The Problem

---

## "It works on my machine"

You write code. It runs perfectly on your laptop.

Your colleague pulls the changes. It crashes.

The server gets the update. It crashes differently.

**What went wrong?**

- Different Python version
- Missing dependency
- An environment variable not set
- A file only you have locally

**Every "works on my machine" moment is a gap in process.**

---

## The manual release nightmare

Before CI/CD, shipping code looked like this:

1. Developer finishes a feature
2. Emails the team: *"Ready to test"*
3. Tester runs it manually on their machine — different to prod
4. Finds a bug — back to developer
5. Two weeks pass
6. Someone runs a script to deploy — forgets a step
7. Production is down at 11pm

**This is expensive, slow, and fragile.**
Every step is a chance for human error.

---

<!-- _class: lead -->

# Part 2
## What CI Is

---

## Continuous Integration (CI)

> Every time someone pushes code, automatically build it and run the tests.

**Continuous** — it happens on *every* push, not once a week before a release.

**Integration** — it integrates your change with the rest of the codebase and checks that everything still works together.

**The goal:** find problems *immediately*, when the fix is small and the context is fresh — not three weeks later when no one remembers what changed.

---

## What CI does

When you push code, CI automatically:

1. **Checks out** your code on a clean machine (not your laptop)
2. **Installs** dependencies from scratch
3. **Runs the tests**
4. **Reports** pass or fail — in your pull request, in your inbox

<br>

✅ **Tests pass** → the change is safe to review and merge

❌ **Tests fail** → the problem is caught before it reaches anyone else

---

## Why "clean machine" matters

CI runs on a fresh virtual machine every time.

No leftover files. No special settings. No "I have it installed globally".

If your code works in CI, it works **anywhere** — because CI has nothing your colleagues don't have.

> This is how you permanently retire "works on my machine."

---

<!-- _class: lead -->

# Part 3
## What CD Is

---

## Continuous Delivery (CD)

> Once code passes CI, automatically deliver it — no manual steps.

**Delivery** means publishing or deploying: pushing a package to PyPI, deploying to a web server, publishing documentation.

**The insight:** if the tests passed on a clean machine, the software is ready. Why wait for a human to press a button?

---

## CI vs CD — the full pipeline

```
developer pushes code
        │
        ▼
   CI: install & test        ← runs on every push
        │
        │  (if tests pass and this is a release)
        ▼
   CD: build & publish       ← runs automatically
        │
        ▼
   users get the update
```

Together, CI and CD form a **pipeline** — a repeatable, automated path from code change to running software.

---

<!-- _class: lead -->

# Part 4
## How It Works

---

## Three concepts: workflow, job, step

Every CI/CD system organises work the same way:

<br>

| Concept | What it is | Analogy |
|---------|-----------|---------|
| **Workflow** | The full automated process | A recipe |
| **Job** | A unit of work on one machine | A cooking station |
| **Step** | One command inside a job | One instruction in the recipe |

---

## What a workflow looks like

```
Workflow: "CI"
│
├── Job: test
│   ├── Step: check out the code
│   ├── Step: install Python and dependencies
│   ├── Step: run the linter
│   └── Step: run the tests
│
└── Job: publish          (only runs if 'test' passed)
    ├── Step: check out the code
    ├── Step: build the package
    └── Step: upload to PyPI
```

Jobs can run in **parallel** (faster) or in **sequence** (when one depends on another).

---

## Triggers — what starts a workflow

Workflows don't run constantly. They are triggered by **events**:

| Trigger | When it fires |
|---------|--------------|
| **Push** | Every time code is pushed to the repo |
| **Pull request** | When a PR is opened or updated |
| **Schedule** | On a timer — e.g. every Monday at 9am |
| **Manual** | A button click in the GitHub UI |

A typical setup: run tests on every push and PR, publish only on a tagged release.

---

<!-- _class: lead -->

# Part 5
## GitHub Actions

---

## GitHub Actions

GitHub Actions is CI/CD built directly into GitHub.

- **No separate service to sign up for**
- **Free** for public repos, generous free tier for private repos
- **Workflows live in your repo** — in `.github/workflows/`
- **Every workflow is a YAML file**

When you push code, GitHub reads your workflow files and runs them automatically on its servers.

---

## A real (minimal) workflow

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4        # download the code

      - uses: actions/setup-python@v5    # install Python
        with:
          python-version: '3.12'

      - run: pip install -e ".[dev]"     # install dependencies

      - run: pytest                      # run the tests
```

Push this file. GitHub runs it automatically on every push and PR.

---

## Reading the results

After a push, GitHub shows a status on the commit and in the PR:

<br>

**✅ All checks passed**
Every job succeeded. Safe to merge.

**❌ Some checks failed**
At least one job failed. Click through to see which step failed and the exact error output.

<br>

The output is the same as running the commands locally — but on a clean machine, with a full log you can share with anyone.

---

## Runners — where jobs run

A **runner** is the machine that executes a job. GitHub provides hosted runners:

| Runner | OS | When to use |
|--------|----|------------|
| `ubuntu-latest` | Linux | Almost always — fastest and cheapest |
| `macos-latest` | macOS | macOS-specific code or tests |
| `windows-latest` | Windows | Cross-platform libraries |

Each job gets a **fresh, clean machine** — installed, used, and discarded.

You can also host your own runners on your own hardware if you need custom specs or private network access.

---

<!-- _class: lead -->

# Part 6
## What You Gain

---

## The benefits

**Confidence**
Every merged PR has passed the same test suite on a clean machine. You know the code works.

**Speed**
Problems are caught in minutes, not at the end of a sprint. The fix is always small.

**Consistency**
The release process is identical every time. No forgotten steps, no "who knows how to deploy this?"

**Visibility**
Every build has a log. You can see exactly what ran, when it ran, and what it produced — permanently.

---

## Before and after

| Without CI/CD | With CI/CD |
|---------------|-----------|
| "Works on my machine" | Tested on a clean machine, every time |
| Manual test runs (sometimes) | Automated test runs on every push |
| Deployment is a ceremony | Deployment is a tag push |
| Bugs found in production | Bugs found in the pull request |
| "Who broke this?" | Exact commit, exact error, exact line |
| Friday deploys are scary | Friday deploys are boring |

**Boring deployments are the goal.**

---

## Getting started

You don't need to write workflow files from scratch.

**Rhiza** provides a ready-made CI/CD setup for Python projects:

```bash
uvx rhiza init        # creates .rhiza/template.yml
uvx rhiza materialize # writes CI workflow files into your repo
```

You get: CI on every push, linting, test coverage, automated releases, and a weekly sync to keep everything up to date.

> Learn more: **https://jebel-quant.github.io/rhiza-education/**

---

## Key takeaways

1. **CI/CD automates the boring, error-prone parts** of software development — testing and shipping.

2. **CI** runs your tests on a clean machine every time you push. "Works on my machine" becomes "works everywhere."

3. **CD** ships your software automatically once tests pass. No manual steps, no forgotten procedures.

4. **GitHub Actions** is CI/CD built into GitHub — workflows are YAML files in your repo.

5. **You don't need to build this from scratch.** Tools like Rhiza wire it up for you in four commands.

---

<!-- _class: lead -->

# That's it

Push code. Tests run. Ship with confidence.

*Start with one workflow file. Build from there.*
