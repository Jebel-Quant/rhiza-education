# Lesson 11 — The Rhiza Ecosystem

The lessons so far have focused on the core workflow: configure `template.yml`, run `/rhiza:update`, review the resulting PR. But Rhiza is one piece of a larger set of tools built around the same philosophy — automate the boring parts of running software projects at scale. This lesson maps that ecosystem so you know what exists and when to reach for it.

## rhiza-claude — the interface you have been using

[`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude) is a [Claude Code](https://claude.com/claude-code) plugin marketplace. It ships the **`rhiza`** plugin — the set of slash commands that drive the whole init-sync-quality workflow from inside your AI coding assistant. It is the primary way you interact with Rhiza today: the commands wrap the underlying mechanics, and their bundled scripts are stdlib-only Python, so there is no separate CLI to install. The plugin reads `.rhiza/template.lock` and `.rhiza/template.yml` directly.

Install it once:

```
/plugin marketplace add Jebel-Quant/rhiza-claude
/plugin install rhiza@rhiza-claude
```

Pin a version by appending a git tag: `/plugin marketplace add Jebel-Quant/rhiza-claude#v0.8.2`. The only prerequisites are `uv`, `git`, and `make`.

The commands appear namespaced under the plugin, and since v0.7.0 each one ships as a **skill** rather than a bare command file — a change to how the plugin is packaged, not to how you invoke them. Five drive the lifecycle of a project:

| Command | What it does |
|---------|-------------|
| `/rhiza:init` | Makes the current folder rhiza-managed: `git init` if needed, asks GitHub/GitLab, owner/name/visibility, language (Python, Rust, or Go) and template repo, then writes `.rhiza/template.yml` — the pointer at a template and a pinned ref — adds a skeleton for that language and license metadata, and opens a PR on a `rhiza_init_<date>` branch. It syncs nothing and runs no gates |
| `/rhiza:update` | Bumps the repo to the latest (or a given) template release, syncs, resolves conflicts by taking the upstream side, and opens a PR containing **only** template-owned files. This is how template content arrives, both the first time and every time after |
| `/rhiza:quality` | Runs the code-quality gates (lint, types, docs, deps, security, audit, tests, test-layout, complexity, architecture) and scores the repo; can file findings as issues. On a repo that is *not* rhiza-managed or not yet synced it **degrades** rather than refusing — it skips the template-delivered gates, discovers the repo's own `make` targets, and still scores the design work. What it never does is report an unavailable gate as a failure |
| `/rhiza:docs` | Creates or refreshes the repo's `README.md`, `CLAUDE.md`, and `mkdocs.yml` — regenerating the badge block and correcting stale facts while preserving hand-written prose. Writes files only: no commit, no branch, no PR |
| `/rhiza:release` | Lays out the legal next versions as a table for you to choose from — it never picks one for you — then has `bump-my-version` write your choice into every location the repo declares in `[tool.bumpversion]` and regenerates `CHANGELOG.md`. Since v0.8.0 it lands that bump **through a PR** and tags only after you merge (see below) |

A second group works straight off the lock file. Two are read-only; one is destructive but explicit:

| Command | What it does |
|---------|-------------|
| `/rhiza:status` | Reports both halves of the repo's rhiza state: that `.rhiza/template.yml` exists, parses, and is well-typed, and what `.rhiza/template.lock` says was actually synced — repository, ref, commit SHA, timestamp, strategy, managed files. `--files` lists those as a tree, `--check` compares the pinned ref against the latest upstream release |
| `/rhiza:maffay` | Prints one bonmot from a random Peter Maffay song. Read-only, needs no repo, works in any directory — the ecosystem's one deliberate frivolity |
| `/rhiza:detach` | Removes every file listed in `.rhiza/template.lock`, prunes emptied directories, and deletes the lock; destructive, so it prompts unless `--force`. Renamed from `/rhiza:uninstall` in v0.7.0 |

### `/rhiza:release` is two phases, not one

A tag must point at a commit that exists on the branch you publish from, and a squash-merge replaces a branch's commits with a new one. So a tag cut *before* the merge names a SHA that never lands. There is no ordering of a single invocation that fixes this, and the fix is to run the command twice:

| Phase | You run | It ends with |
|-------|---------|--------------|
| **A — the release PR** | `/rhiza:release` on a clean default branch | a pushed branch and an open PR. **No tag** |
| **B — the tag** | `/rhiza:release` again, once that PR merges | the merged commit tagged and the tag pushed — release CI running |

The command works out which phase it is in from the repo's own state; you do not declare it. The human decision is the merge, and there is exactly one of it. Note also that `/rhiza:release` deliberately does **not** require `.rhiza/` — the version locations are repo-owned config, `git-cliff` reads conventional commits, and tags are tags — so it can release an unmanaged repo just as well as a rhiza-managed one.

Reach for `/rhiza:status` first when something looks wrong: it answers both "is my config well-formed?" and "what did I actually get, and am I behind?" in one shot.

> **Commands you may read about elsewhere no longer exist under those names.** `/rhiza:uninstall` is now `/rhiza:detach`. `/rhiza:validate` was folded into `/rhiza:status`, which now validates the config *and* reports the lock — the two disagree often enough that reporting one alone misleads. `/rhiza:revisit` was renamed `/rhiza:docs`. Older material also mentions `/rhiza:stats`, `/rhiza:repos` and `/rhiza:new`; those have been retired.

> Historically the mechanics lived in two separate packages — `rhiza-cli` (the `uvx rhiza` command) and `rhiza-tools` (release and reporting utilities). Both are archived. `rhiza-claude` supersedes the CLI, and the reporting and version-matrix logic moved inside the template's reusable CI workflows. You no longer run `uvx rhiza` or `uvx rhiza-tools` for anything, and nothing in this curriculum asks you to. The reasoning behind splitting the template from its tooling is recorded in [ADR-0005](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0005-separate-rhiza-template-from-cli.md).

## rhiza-hooks — the commit hooks

[`rhiza-hooks`](https://github.com/Jebel-Quant/rhiza-hooks) is a pre-commit hook repository. Each language layer ships a `.pre-commit-config.yaml` that pulls from it — for Python that is `python-core`, not `core`, since v1.3.0 split the language layer out. The hooks run automatically on `git commit` and catch common mistakes before they hit CI:

| Hook | What it checks |
|------|---------------|
| `check-rhiza-config` | `template.yml` is valid and the referenced repo/ref can be resolved |
| `check-rhiza-workflow-names` | GitHub Actions workflow names carry the uppercase `(RHIZA)` prefix — and fixes them if not |
| `check-makefile-targets` | The Makefile exposes the targets CI depends on |
| `check-workflow-make-targets` | Every `make` target CI actually invokes exists |
| `check-python-version-consistency` | `.python-version`, `pyproject.toml`, and CI matrix all agree on the Python version |
| `check-rust-version-consistency` | The Rust toolchain versions agree across the repo |
| `check-go-version-consistency` | The Go versions agree across the repo |
| `check-bumpversion-config` | `bump-my-version` can find its config, so `/rhiza:release` will not stall |
| `check-template-bundles` | The bundles listed in `template.yml` exist in the remote template repo |
| `check-managed-files` | No template-owned file has been modified locally without being excluded |
| `check-license-metadata` | The licence declared in the manifest, the `LICENSE` file, and the classifiers agree |
| `update-readme-help` | Embeds the current `make help` output into the README automatically |

The three version-consistency hooks are the visible edge of the multi-language split: a repo gets the one that matches its language layer.

These run locally on commit — through [`prek`](https://github.com/j178/prek) rather than `pre-commit` itself since template v1.3.2, a faster drop-in runner for the same config file, invoked by `make fmt` as `uvx prek run --all-files`. The template's CI enforces the equivalent quality gates as well, so nothing slips through if someone bypasses the local hooks.

## rhiza-brainbug — cross-repo test harness

[`rhiza-brainbug`](https://github.com/Jebel-Quant/rhiza-brainbug) solves a problem that appears once you have many interdependent Rhiza projects: **contract and compatibility tests that span more than one repo**. Rather than duplicating an integration test in every consumer, you write it once in brainbug.

Brainbug watches a list of repositories on a cron. When any branch of a watched repo gets a new commit, brainbug checks out that repo at that SHA and runs its own tests ("brainbugs") against the code. Nothing is installed in the monitored repos — it is pure polling, comparing each branch head against a stored state file and self-dispatching a run on any change.

This makes it the ecosystem's answer to "did my change break a downstream repo?" without wiring webhooks or CI triggers into every project.

## How the pieces fit together

```
                    ┌─────────────────────────────┐
                    │       template repo          │
                    │          (rhiza)             │
                    │  core + python/rust/go-core  │
                    └─────────────┬───────────────┘
                                  │ template files
                    ┌─────────────▼───────────────┐
                    │        rhiza-claude          │
                    │  init · update · quality     │
                    │  docs · release · status     │
                    │  detach · maffay             │
                    └─────────────┬───────────────┘
                                  │ drives
                    ┌─────────────▼───────────────┐
                    │       your project           │
                    │  .rhiza/template.yml + .lock │
                    └──┬───────────────────────────┘
                       │
          ┌────────────▼────────┐
          │   rhiza-hooks       │
          │   (via prek)        │
          └─────────────────────┘

   Cross-repo testing:   rhiza-brainbug → contract/compatibility runs on upstream commits
```

At the top is the template repo (Rhiza). `rhiza-claude` is the interface layer: its slash commands materialize template files into your project, run the quality gates, and keep the docs honest — all driven from Claude Code. `rhiza-hooks` keeps the project valid on every commit, and `rhiza-brainbug` runs the compatibility tests that span multiple Rhiza projects.

---

**Next:** [Lesson 12 — Further Reading](./12-further-reading.md)
