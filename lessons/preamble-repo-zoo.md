# Preamble — The Repo Zoo Problem

Before understanding what Rhiza does, you need to understand the problem it was built to solve. That problem is not "how do I start a new Python project" — there are plenty of tools for that. The problem is what happens *after* you have started many Python projects.

## The zoo

A team of quantitative developers typically accumulates repositories the way a zoo accumulates animals. There is one for backtesting, one for data ingestion, one for the risk model, one for the reporting dashboard, several experimental notebooks that became production systems, a couple of internal libraries, and a handful of one-off tools that nobody can quite bring themselves to delete.

Each of these started well. Someone ran a project generator, answered a few questions, and got a clean repo with a CI workflow, a Makefile, a linting config, and a test harness. On day one, everything was consistent.

Then the repos started to diverge — and each became an exemplar of its kind.

The backtesting repo got a new pre-commit hook that the risk model repo never received. The data ingestion repo still pins Python 3.9 because nobody got around to updating the CI matrix after 3.9 went end-of-life. Three repos use Black, two use Ruff, one uses both. The CI workflow in the reporting dashboard references a GitHub Actions runner version that was deprecated eight months ago. The Makefile in the experimental repo has targets that the main repo dropped two releases ago — and vice versa.

Nobody did this on purpose. It just happens. Every change made to one repo is a change not made to the others.

This is the **repo zoo problem**: a collection of repositories that started identical and have since become a collection of unique, inconsistent snowflakes, each requiring its own maintenance.

## The real cost

The cost is not usually visible on any given day. It becomes visible in moments:

**A CVE is disclosed in a GitHub Actions runner.** You need to bump the runner version across all your repos. You have seventeen. You do twelve, get distracted, and three months later the other five are still vulnerable.

**Python 3.9 reaches end-of-life.** Your CI matrices should drop it. You update the ones you work in regularly. The others drift on, running against a Python version that no longer receives security patches.

**The team decides to standardise on Ruff.** You update the active repos. The legacy repos keep running Black. Now you have a split standard, and nobody is quite sure which one applies to the repo they are looking at.

**A new security scanning workflow is added to the template.** It lands in the repos whose owners happened to be paying attention. The others never get it.

Each individual failure is small. Cumulatively they mean that "our standard" is a fiction — there is no single standard, only a collection of local deviations from a standard that existed at the moment each repo was created.

## Why template systems cannot solve this

The instinctive response is to reach for a template tool. If all the repos were created from the same template, can't the template tool push updates?

No. This is the fundamental limitation that motivated Rhiza.

**Cookiecutter** generates files once from a template. Once generation is complete, the template and the project are completely disconnected. There is no mechanism to propagate a change in the template back to any project it generated. You can re-run it, but that means overwriting everything and resolving conflicts by hand, one repo at a time.

**Copier** is the closest prior art. It records which template was used and supports an `update` command that replays template changes. But `copier update` is a manual command you run inside a single repo. There is no facility to trigger it across all your repos simultaneously, no automated PR for review, and no scheduling. It solves the one-repo case; it does not scale to the zoo.

**GitHub template repositories** are one-shot. Click "use this template," get a copy of the repo at a point in time. That is all. There is no sync, no version pinning, no update mechanism.

The deeper issue is that all of these tools were designed to solve the **Day 0 problem**: getting a new project off the ground with sensible defaults. None of them were designed to solve the **Day 365 problem**: keeping twenty existing projects aligned as their shared infrastructure evolves.

Template systems treat configuration as something you set up once. The repo zoo problem proves that configuration is not a one-time decision — it is ongoing infrastructure, and infrastructure requires ongoing maintenance.

## When Rhiza was born

The idea for Rhiza came directly from lived experience. The author spent time embedded in the engineering organisation of a **large sovereign wealth fund** — one of the largest pools of managed capital in the world — and had full, unfiltered exposure to what a wild repo zoo looks like at institutional scale. Dozens of Python repositories, each maintained by different teams, each with its own vintage of CI configuration, its own pinned tool versions, its own informal conventions that had diverged from whatever standard had existed when the repo was created. The problem was not that people were careless. It was structural: there was no mechanism to keep the repositories aligned as the organisation's standards evolved.

That experience made clear that the problem was not unique to any one team or any one firm. It is the default outcome whenever a growing engineering organisation relies on one-shot scaffolding. The question was whether there was a better approach.

Rhiza was created in **December 2025** at Jebel-Quant, a quantitative asset management firm. The repo was initialised on December 13, 2025; the first public release (v0.0.1) followed three days later on December 16.

The name is from the ancient Greek **ῥίζα** (*ree-ZAH*), meaning *root*. The metaphor is intentional: a root system connects and sustains many things from a single source, invisibly, continuously. That is what Rhiza does for your repos.

## The insight

The insight that separates Rhiza from template tools is simple: **treat the update as a pull request, not a push**.

Instead of trying to force changes into downstream repos, Rhiza opens a PR in each one. The PR contains a clean diff of what changed in the template. The owner of the downstream repo reviews it, adapts it if necessary, and merges it. The change is opt-in at the individual PR level, but *systematic* at the organisation level — every repo gets the PR, nothing is missed, and the git history shows exactly what changed and when.

This also means Rhiza respects the fact that repos are not identical. The `exclude:` mechanism lets each project opt out of specific files. Custom extension points let projects add behaviour without touching managed files. The sync is not a bulldozer — it is a proposal.

The result: a zoo that stays in sync without becoming a monoculture.

---

**Next:** [Lesson 1 — CI/CD Concepts](./01-cicd-concepts.md)
