# Lesson 10 — Customising Safely

Rhiza manages a set of files in your project. This raises an obvious question: what if you need to change something that Rhiza controls? This lesson covers the right ways to customise a Rhiza-managed project without getting into conflicts when you update.

## The core rule

> If you edit a file that Rhiza manages, the next `/rhiza:update` will overwrite your change.

This is intentional. Template-managed files are meant to stay consistent with the template. Since template v1.5.0 it is also *enforced* rather than merely advised: the `check-managed-files` hook refuses a commit that touches a file the lock records, so a local edit fails at commit time instead of surfacing as a surprise revert in the next update PR. (`/rhiza:update`'s own sync commit bypasses it — that commit is the one thing allowed to write those files.)

The right response to needing a customisation is not to edit the file — it is to use one of the extension mechanisms below.

## Option 1: Add your own targets in `local.mk`

The `Makefile` is template-owned and `-include`s **`local.mk`**, which no sync touches and `core` deliberately does not gitignore. Commit it: anything CI invokes has to be in the repository.

```makefile
# local.mk — committed, never synced

seed-db:  ## Seed the local development database
	@uv run python scripts/seed_db.py
```

Targets carrying a `##` comment are listed by `make help` under *Repo-owned targets*, so they stay discoverable next to the template's tasks.

> **`custom-task.mk` and `custom-env.mk` are gone.** They were fragments of the synced make layer that retired in template v1.4.0 (see Lesson 5 and [ADR-0011](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0011-replace-the-synced-make-layer-with-a-pinned-cli.md)). `local.mk` replaces the first; `[tool.rhiza-task]` replaces the second.

### Extending a template task

The old `pre-install::` / `post-install::` hooks are gone too — the tasks now live in the pinned `rhiza-task` CLI, which knows nothing about make targets. The replacement is to **shadow** the target from `local.mk`: an explicit rule always beats the shim's `%:` catch-all, so your rule can call the task and then do the extra work.

```makefile
# local.mk
report: $(UVX)
	@$(UVX) $(RHIZA_TASK) test
	@./scripts/publish-test-report.sh
```

`RHIZA_TASK` and `UVX` are defined by the `Makefile` above the `-include`, so a shadowing rule runs the same pinned CLI as the rest of the project, and naming `$(UVX)` as a prerequisite keeps the bootstrap that installs `uv` on a runner without one.

**Shadowing only reaches a task make itself resolves.** It wins when you type the name, or when another make rule names it as a prerequisite. It does not win when the CLI reaches a task internally — `test` needs `install`, but the shim forwards the goal `test` to `rhiza-task`, which resolves `install` in its own task graph, consulting no make rule. And CI never invokes make at all: every workflow calls `uvx "$RHIZA_TASK" <gate>` directly. So shadowing adds work around a task *you* invoke; work that must happen before every gate belongs in the setup hook below.

## Option 2: Set task behaviour in `[tool.rhiza-task]`

Settings that used to be make variables are now a table in your `pyproject.toml`, which the template never overwrites:

```toml
[tool.rhiza-task]
source-folder = "lib"          # default: "src"
typechecker = "both"           # ty | mypy | both (default: ty)
coverage-fail-under = 85       # default: 90
mkdocs-extra-packages = ["mkdocstrings[python]"]
```

`source-folder` is the load-bearing one. The scoped gates — `typecheck`, `security`, `deps`, `docs-coverage`, `semgrep` — all read it, and if it points at nothing they exit **green having measured nothing**. A standard `src/` layout needs no setting at all; a project whose code lives elsewhere must say so, or its gates quietly stop being gates. Rhiza's own repo hit exactly this and fixed it by naming the folder.

For per-developer overrides that should not be committed, `.rhiza/.env` still works — and since the template stopped shipping the `.gitignore` negation that kept it tracked, it is now genuinely developer-local: a CI checkout never contains it.

The full resolution order, lowest precedence first, is explicit and testable:

| # | Source | Committed? |
|---|--------|------------|
| 1 | Built-in defaults | — |
| 2 | `.rhiza/.env` | No |
| 3 | `rhiza.toml` | Yes |
| 4 | `[tool.rhiza-task]` in `pyproject.toml` / `Cargo.toml` | Yes |
| 5 | `RHIZA_*` environment variables | — |
| 6 | Command-line flags | — |

Two files at layers 3 and 4 because neither alone covers all three languages: `pyproject.toml` is Python-only, and a Go module has no manifest to hide a table in. **Rust and Go projects use `rhiza.toml`.** It ranks *below* the manifest deliberately, so adding one to a Python repo cannot silently outrank the table already there. Layer 5 is what lets CI override anything without editing a file.

## Option 3: Install system dependencies in `local-setup.sh`

New in template v1.7.0. If your project needs a native binary before any gate can run — graphviz for a docs plugin, `libpq` for psycopg, pandoc — put it in an executable `local-setup.sh` at the repository root:

```bash
#!/usr/bin/env bash
set -euo pipefail

if ! command -v dot >/dev/null 2>&1; then
    sudo apt-get update && sudo apt-get install -y graphviz
fi
```

Every language layer's `install` runs it first, and `install` is a prerequisite of essentially every gate — so one file covers a local `make test`, GitHub Actions, GitLab CI and the devcontainer, with no workflow edit anywhere. Guard the expensive part yourself: the hook runs on every fresh CI job. A hook that exists but is not executable **fails** with a `chmod +x` hint, on the principle that a provisioning step someone believes is running must not pass quietly; having no hook at all simply succeeds.

## Option 4: Exclude a file and own it locally

If you need to diverge significantly from a template file — for example, your project needs a custom CI workflow that is incompatible with the template's version — add the file to `exclude:` in `.rhiza/template.yml`:

```yaml
exclude: |
  .github/workflows/rhiza_ci.yml
```

From that point on, `/rhiza:update` will never touch that file. You are responsible for maintaining it, including applying any relevant upstream changes manually.

> **Warning:** Be deliberate here. Excluded files are excluded permanently until you remove them from the list. Security fixes in the template will not reach excluded files automatically.

## Option 5: Fork the template for your organisation

This is the recommended approach for teams. Instead of pointing all your projects at `Jebel-Quant/rhiza`, you fork it into your own organisation:

```
Jebel-Quant/rhiza  →  your-org/rhiza
```

Your fork becomes your org's source of truth. You customise it to reflect your team's standards — different default Python version, additional CI steps, org-specific secrets, whatever you need. All your projects then point their `repository:` at `your-org/rhiza`.

When `Jebel-Quant/rhiza` releases a new version, you decide when and what to pull into your fork. You are in control of what flows downstream.

```yaml
# .rhiza/template.yml in a project from your org
repository: your-org/rhiza
ref: v1.7.1
```

This pattern scales well: one place to manage standards, automated propagation to all consuming repos, and full control over what gets adopted and when.

## What you should never do

**Don't edit template-managed files directly** unless you also add them to `exclude:`. You will lose your changes the next time you run `/rhiza:update`.

**Don't work around updates** to avoid dealing with PRs. The `/rhiza:update` PR is the system working correctly. If an update surfaces too many changes you don't want, the right answer is to use `exclude:` for files you own locally, not to stop updating.

**Don't diverge silently.** If you make a local change and do not exclude the file, the next `/rhiza:update` PR will show the revert of your change. This is confusing for reviewers. Be explicit: if you own a file, exclude it.

## Summary of extension points

| Need | Mechanism | Committed? |
|------|-----------|------------|
| Your own `make` targets, or extending a task you invoke | `local.mk` at the repo root | Yes |
| Change how a template task behaves (folders, typechecker, thresholds) | `[tool.rhiza-task]` in `pyproject.toml` | Yes |
| A native binary every gate needs | Executable `local-setup.sh` at the repo root | Yes |
| A per-developer override of one setting | `.rhiza/.env` | No — gitignored |
| Permanently own a specific file | Add to `exclude:` in `template.yml` | Yes |
| Customise the template itself for your whole org | Fork the template repo | — |

---

**Next:** [Lesson 11 — The Rhiza Ecosystem](./11-the-rhiza-ecosystem.md)
