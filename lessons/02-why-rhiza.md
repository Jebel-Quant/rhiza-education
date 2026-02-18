# Lesson 2 — Why Rhiza?

## The one-shot scaffolding problem

Most project generators work like this: you run a command, answer a few questions, and the tool writes a bunch of files into your new repo — CI workflows, a Makefile, linting config, a test harness. Day 0 is great. Everything is consistent, up to date, and wired together correctly.

Then time passes.

A security vulnerability is discovered in one of the GitHub Actions runners. You update the workflow in one repo but forget the other four. Six months later your CI configurations have diverged: some repos pin an old Python version, others have a newer linting rule set, one still uses a deprecated workflow syntax. The template was a one-time snapshot, not a contract.

This is called **template drift**, and it's the rule, not the exception, for teams that run more than a couple of Python projects.

## The usual workarounds don't scale

You could manually update every repo every time the template changes. But that's tedious, error-prone, and it only works if someone is responsible for doing it. You could write a script to push changes across repos — but now you're maintaining that script, and it breaks every time a repo deviates from the expected structure.

The real problem is that one-shot generators treat project configuration as something you set up once. But **configuration is infrastructure**, and infrastructure needs ongoing maintenance.

## What Rhiza does differently

Rhiza treats the template as a **living contract** between a central template repository and your downstream projects. Instead of generating files once, Rhiza continuously synchronises them.

Here is the core idea:

1. You (or your organisation) maintain a **template repository** — this is where your canonical CI workflows, Makefile, linting config, and other shared files live.
2. Each downstream project has a small config file (`.rhiza/template.yml`) that declares which files it wants from the template and which version of the template to use.
3. When the template changes, Rhiza opens a **pull request** in each downstream project with the diff. You review it, merge it, and the project is updated.

The template is the source of truth. The downstream projects are consumers. The sync is automatic.

## What Rhiza is not

Rhiza is not a framework. It has no opinion about how you structure your Python code, which libraries you use, or how you architect your application.

Rhiza only manages **project infrastructure files** — the scaffolding around your code, not the code itself. Your business logic, your tests, your application code — none of that is touched.

It is also not a one-time generator like cookiecutter or copier. If you want a tool that generates files once and then leaves you alone, Rhiza is the wrong choice. Rhiza is for teams that want their project infrastructure to stay consistent and up to date over time.

## The payoff

Once Rhiza is set up:

- A security fix in a CI workflow propagates to all consuming repos automatically, as a PR.
- A team decision to switch linters is applied everywhere, not just in the repo where someone remembered to do it.
- New repos get a full, up-to-date CI/CD setup in minutes, not hours.
- The configuration across all your repos stays consistent — not because you enforced it manually, but because the system does.

---

**Next:** [Lesson 3 — Core Concepts](./03-core-concepts.md)
