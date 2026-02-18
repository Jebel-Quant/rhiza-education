# Lesson 7 — Customising Safely

Rhiza manages a set of files in your project. This raises an obvious question: what if you need to change something that Rhiza controls? This lesson covers the right ways to customise a Rhiza-managed project without getting into conflicts with the sync.

## The core rule

> If you edit a file that Rhiza manages, the next sync will overwrite your change.

This is intentional. Template-managed files are meant to stay consistent with the template. The right response to needing a customisation is not to edit the file — it is to use one of the extension mechanisms described below.

## Option 1: Use the Makefile extension hooks

The `core` bundle provides two files explicitly designed for local customisation:

- **`custom-task.mk`** — add your own `make` targets here. This file is not managed by the template, so you can edit it freely.
- **`custom-env.mk`** — set project-specific environment variables that Makefile targets will use.

Example: adding a custom `make` target to seed a local database.

```makefile
# custom-task.mk

.PHONY: seed-db
seed-db:  ## Seed the local development database
	python scripts/seed_db.py
```

After adding this, `make seed-db` will work alongside all the standard Rhiza targets, and it will never be touched by a sync.

## Option 2: Exclude a file and own it locally

If you need to diverge significantly from a template file — for example, your project needs a custom CI workflow that is incompatible with the template's version — add the file to `exclude:` in `.rhiza/template.yml`:

```yaml
exclude: |
  .github/workflows/rhiza_ci.yml
```

From that point on, the sync will never touch that file. You are responsible for maintaining it, including applying any relevant upstream changes manually.

> **Warning:** Be deliberate here. Excluded files are excluded permanently until you remove them from the list. Security fixes in the template will not reach excluded files automatically.

## Option 3: Fork the template for your organisation

This is the recommended approach for teams. Instead of pointing all your projects at `Jebel-Quant/rhiza`, you fork it into your own organisation:

```
Jebel-Quant/rhiza  →  your-org/rhiza
```

Your fork becomes your org's source of truth. You customise it to reflect your team's standards — different default Python version, additional CI steps, org-specific secrets, whatever you need. All your projects then point their `repository:` at `your-org/rhiza`.

When `Jebel-Quant/rhiza` releases a new version, you decide when and what to pull into your fork. You are in control of what flows downstream.

```yaml
# .rhiza/template.yml in a project from your org
repository: your-org/rhiza
ref: v1.2.0
```

This pattern scales well: one place to manage standards, automated propagation to all consuming repos, and full control over what gets adopted and when.

## What you should never do

**Don't edit template-managed files directly** unless you also add them to `exclude:`. You will lose your changes on the next sync.

**Don't disable the sync workflow** to avoid dealing with PRs. The PRs are the system working correctly. If you are getting too many PRs, the right answer is to use `exclude:` for files you own locally, or to reduce how often you sync.

**Don't diverge silently.** If you make a local change and do not exclude the file, the next sync PR will show the revert of your change. This is confusing for reviewers. Be explicit: if you own a file, exclude it.

## Summary of extension points

| Need | Mechanism |
|------|-----------|
| Custom `make` targets | Edit `custom-task.mk` |
| Custom environment variables for `make` | Edit `custom-env.mk` |
| Permanently own a specific file | Add to `exclude:` in `template.yml` |
| Customise the template itself for your whole org | Fork the template repo |

---

---

**Next:** [Lesson 8 — The Rhiza Ecosystem](./08-the-rhiza-ecosystem.md)
