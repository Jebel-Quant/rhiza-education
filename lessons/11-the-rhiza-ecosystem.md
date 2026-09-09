# Lesson 11 — The Rhiza Ecosystem

The lessons so far have focused on the core workflow: configure `template.yml`, run `/rhiza:update`, review the resulting PR. But Rhiza is one piece of a larger set of tools built around the same philosophy — automate the boring parts of running software projects at scale. This lesson maps that ecosystem so you know what exists and when to reach for it.

## rhiza-claude — the interface you have been using

[`rhiza-claude`](https://github.com/Jebel-Quant/rhiza-claude) is a [Claude Code](https://claude.com/claude-code) plugin marketplace. It ships the **`rhiza`** plugin — the set of slash commands that drive the whole init-sync-quality workflow from inside your AI coding assistant. It is the primary way you interact with Rhiza today: the commands wrap the underlying mechanics, and their bundled scripts are stdlib-only Python, so there is no separate CLI to install. The plugin reads `.rhiza/template.lock` and `.rhiza/template.yml` directly.

Install it once:

```
/plugin marketplace add Jebel-Quant/rhiza-claude
/plugin install rhiza@rhiza-claude
```

Pin a version by appending a git tag: `/plugin marketplace add Jebel-Quant/rhiza-claude#v0.14.0`. The only prerequisites are `uv`, `git`, and `make`.

> **You can run the mechanics without an LLM anywhere near them.** The plugin's central split is that deterministic work lives in tested code and judgement lives in markdown: parsing the lock, cloning a pinned ref, merging synced files and staging exactly what was delivered are stdlib-only Python under `plugin/scripts/`, and the markdown around them supplies the reading of your repo. Take the markdown away and the scripts still run — clone the repo, point `$RHIZA` at `plugin/scripts`, and invoke them through `uv run --python 3.12 --no-project python`. Most take `--json`, which is the surface to script against. This is not a second implementation: `/rhiza:update` shells out to the very same `sync.py`. Six of the ten commands are deterministic end to end and have an exact headless equivalent; the other four — `quality`, `docs`, `release`, `remote` — are the ones whose remaining half is irreducibly a judgement. The [headless guide](https://jebel-quant.github.io/rhiza-claude/headless/) has the mapping table.

The commands appear namespaced under the plugin, and since v0.7.0 each one ships as a **skill** rather than a bare command file — a change to how the plugin is packaged, not to how you invoke them. There are ten as of v0.14.0. Six drive the lifecycle of a project:

| Command | What it does |
|---------|-------------|
| `/rhiza:init` | Makes the current folder rhiza-managed: `git init` if needed, asks GitHub/GitLab, owner/name/visibility, language (Python, Rust, or Go) and template repo, then writes `.rhiza/template.yml` — the pointer at a template and a pinned ref — adds a skeleton for that language and license metadata, and opens a PR on a `rhiza_init_<date>` branch. It syncs nothing and runs no gates |
| `/rhiza:update` | Bumps the repo to the latest (or a given) template release, syncs, resolves conflicts by taking the upstream side, and opens a PR containing **only** template-owned files. This is how template content arrives, both the first time and every time after |
| `/rhiza:quality` | Runs the code-quality gates (lint, types, docs, `deps`, security, audit, tests, complexity, architecture) and scores the repo; can file findings as issues. It enumerates the tasks the repo's own `RHIZA_TASK` pin actually offers rather than assuming a fixed set, and on a repo that is *not* rhiza-managed or not yet synced it **degrades** rather than refusing — skipping the template-delivered gates and still scoring the design work. What it never does is report an unavailable gate as a failure |
| `/rhiza:docs` | Creates or refreshes the repo's `README.md`, `CLAUDE.md`, and `mkdocs.yml` — regenerating the badge block and correcting stale facts while preserving hand-written prose. Writes files only: no commit, no branch, no PR |
| `/rhiza:release` | Lays out the legal next versions as a table for you to choose from — it never picks one for you — then has `bump-my-version` write your choice into every location the repo declares in `[tool.bumpversion]` and regenerates `CHANGELOG.md`. Since v0.8.0 it lands that bump **through a PR**, and since v0.14.0 it opens that PR, waits for the merge and tags the merged commit in a single run (see below) |
| `/rhiza:remote` | New in v0.10.0. Reads what CI on the origin says about the repo's open pull/merge requests, then diagnoses and fixes the red ones **on their own branches** — reproducing the failure locally and pushing the fix to the request's branch, never to the default branch |

A second group works straight off the repo's own state. Three are read-only; one is destructive but explicit:

| Command | What it does |
|---------|-------------|
| `/rhiza:status` | Reports both halves of the repo's rhiza state: that `.rhiza/template.yml` exists, parses, and is well-typed, and what `.rhiza/template.lock` says was actually synced — repository, ref, commit SHA, timestamp, strategy, managed files. `--files` lists those as a tree, `--check` compares the pinned ref against the latest upstream release |
| `/rhiza:completions` | New in v0.11.0. Installs shell completions for the tasks the repo's pinned `rhiza-task` exposes, so `make <TAB>` and `rhiza-task <TAB>` list the real set. Owned by the plugin since the template stopped syncing `.rhiza/completions` |
| `/rhiza:maffay` | Prints one bonmot from a random Peter Maffay song. Read-only, needs no repo, works in any directory — the ecosystem's one deliberate frivolity |
| `/rhiza:detach` | Removes every file listed in `.rhiza/template.lock`, prunes emptied directories, and deletes the lock; destructive, so it prompts unless `--force`. Renamed from `/rhiza:uninstall` in v0.7.0 |

### `/rhiza:release` is one run, over two states

A tag must point at a commit that exists on the branch you publish from, and a squash-merge replaces a branch's commits with a new one. So a tag cut *before* the merge names a SHA that never lands. That constraint has not moved — but **since v0.14.0 the command bridges it itself** rather than asking you to run it twice.

One invocation now goes all the way: bump every declared location, regenerate the changelog, open the release PR, hand the merge to the forge (`gh pr merge --squash --auto`), **wait for the bump to appear on the default branch**, then tag the commit that actually landed — named by SHA, so another merge arriving in the same few seconds cannot decide what gets released.

The two phases are still there, but they are **states of the repository, not invocations of the command**:

| State | What it means | What the command does |
|-------|---------------|----------------------|
| **A** — declared version `==` highest tag, nothing pending | the declared version is already released | bump, changelog, PR, merge, tag |
| **B** — a committed version `>` highest tag | a merged bump that no tag names | tags the merged commit |
| neither — declared `<` highest tag, or two sources disagreeing | a reverted bump, a tag cut ahead, a PR edited before merge | stops and reports why |

An ordinary run starts in A, and *its own merge* is what puts the repo into B, which it then tags. A run that **starts** in B is one finishing a release whose wait ran out. You never declare which; `check_version_bump.py` reads it off the repo.

**The wait is bounded, and running out is an ordinary outcome, not a failure.** Each call waits nine minutes — what fits in one tool call — repeated at most three times, and only while the forge says the PR's checks are still running. A red check, or a green PR nobody has merged, ends the wait immediately, because neither is something more waiting fixes. Then you get the open PR reported with **no tag created**, and re-running `/rhiza:release` finishes it. That verdict is the only state carried between runs, so the merge can happen days later in a different session and the next run still knows what to do.

> **A repo with no required checks releases in one go, literally.** `--auto` defers to whatever branch protection actually enforces, so where nothing is required the PR is opened and merged inside the same run. That is not the command being hasty — it is the repo having no gate, which was equally true before and merely hidden behind the pause of waiting for a second invocation. If you want a longer look at your release PRs, make a check required. (On GitLab the flag differs in meaning too: `glab mr merge --auto-merge` defers only while a pipeline is *already* running.)

**Where the evidence lives when there is no number in a file.** State B is normally detected from the declared version exceeding the highest tag — `bump-my-version` wrote a number into a manifest, so it does. A repo whose version is *derived* from the tag has no such number ([Lesson 3](./03-python-project-conventions.md)): Go and Rust, whose synced `.bumpversion.toml` omits `current_version`, and any Python project on `hatch-vcs`. There the declared version is *read from* the highest tag, so it can never exceed it, and state B was unreachable by construction — the flow re-detected A after the merge and offered the same menu again. No tag was ever mis-cut, but the second half of the release could not be run. Since v0.14.0 `CHANGELOG.md` is the evidence instead: the new section is prepended on the release branch, so after the merge its newest heading names a version above every tag. On a tag-derived repo a missing heading makes the run **refuse** rather than assume nothing is pending, because there is no third source to fall back on.

Note also that `/rhiza:release` deliberately does **not** require `.rhiza/` — the version locations are repo-owned config, `git-cliff` reads conventional commits, and tags are tags — so it can release an unmanaged repo just as well as a rhiza-managed one. The wait needs no forge CLI either: it is a `git fetch` and a read of the merged `CHANGELOG.md`, so if `gh`/`glab` is missing or logged out you merge the PR in the browser and the same run tags what lands.

Reach for `/rhiza:status` first when something looks wrong: it answers both "is my config well-formed?" and "what did I actually get, and am I behind?" in one shot.

> **Commands you may read about elsewhere no longer exist under those names.** `/rhiza:uninstall` is now `/rhiza:detach`. `/rhiza:validate` was folded into `/rhiza:status`, which now validates the config *and* reports the lock — the two disagree often enough that reporting one alone misleads. `/rhiza:revisit` was renamed `/rhiza:docs`. Older material also mentions `/rhiza:stats`, `/rhiza:repos` and `/rhiza:new`; those have been retired.

> Historically the mechanics lived in two separate packages — `rhiza-cli` (the `uvx rhiza` command) and `rhiza-tools` (release and reporting utilities). Both are archived. `rhiza-claude` supersedes the CLI, and the reporting and version-matrix logic moved inside the template's reusable CI workflows. You no longer run `uvx rhiza` or `uvx rhiza-tools` for anything, and nothing in this curriculum asks you to. The reasoning behind splitting the template from its tooling is recorded in [ADR-0005](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0005-separate-rhiza-template-from-cli.md).

## rhiza-task — the tasks, as a pinned CLI

[`rhiza-task`](https://github.com/Jebel-Quant/rhiza-task) is the newest and most consequential piece: since template **v1.4.0** it holds every developer task — `install`, `test`, `fmt`, `typecheck`, `security`, `deps`, `book`, `benchmark`, the release helpers — that used to be synced into your repo as `.rhiza/rhiza.mk` and a `make.d/` fragment per bundle.

The documented interface is the CLI:

```bash
uv run rhiza-task list      # every task, its section, and what it needs
uv run rhiza-task test
```

`uvx` provisions it per invocation at the version your `Makefile` pins in `RHIZA_TASK`, so the version travels with the sync: a repo synced at a tag runs *that tag's* gates. The `Makefile` `core` still ships is a compatibility shim — it pins the CLI, bootstraps `uv` on a runner that has none, and forwards every unmatched target through a `%:` catch-all, which is why `make test` keeps working.

Why this was worth doing is the substance of [ADR-0011](https://github.com/Jebel-Quant/rhiza/blob/main/docs/adr/0011-replace-the-synced-make-layer-with-a-pinned-cli.md). The short version: **make cannot `include` a remote file**. So every consumer held a full copy of ~1,500 lines at whatever tag it last synced, "you are on v1.3.3" meant "these files were copied at v1.3.3 and nobody has edited them since" — which nothing verified — and a bug in a gate had to be found, fixed, released and re-synced into every consumer one at a time. One set of task names now spans Python, Rust and Go, and the recipes are testable Python rather than shell that only `make -n` could inspect.

The task layer is the only thing that moved. The bundle model is untouched: bundles still say which capabilities a project wants, and ADR-0006 and ADR-0010 still stand.

### Two tasks worth knowing about by name

Most of the registry is the gate set you would expect — `install`, `test`, `coverage`, `typecheck`, `security`, `deps`, `license`, `docs-coverage`, plus bundle-owned extras for Docker, LFS, papers and slides. Two later additions are less obvious and change how you work:

**`update` — the template sync as one command.** Added in v1.5.0, it runs four steps in order, reading their exit codes: bump `.rhiza/template.yml` if you asked for a ref, sync, resolve conflicts by taking the template's side, and stage exactly what was delivered.

```bash
TEMPLATE_REF=v1.8.0 uv run rhiza-task update    # or template-ref in [tool.rhiza-task]
uv run rhiza-task update                        # re-sync at the ref the file already names
```

It leaves the **commit** to you, printing the command that commits precisely that set, and it guards on `.rhiza/template.yml` existing — so a repo that is not rhiza-managed gets a skip rather than a failure. Taking the template's side of every conflict marker is right rather than merely convenient: a rhiza-managed file is the template's to own, so local divergence in one is drift to undo, not work to preserve. This is the same code path `/rhiza:update` drives; what the slash command adds is resolving *which* ref to move to and writing the PR body. If you want the sync in a `Makefile`, a shell script or a CI job, this is the entry point.

**`test-lowest` — the dependency floors, as a gate.** A declared floor is a claim: `typer>=0.15` says the package works with typer 0.15. With `--frozen` everywhere, nothing reads that claim back — the lock file resolves whatever is newest, so a floor can be years stale while every gate stays green. `test-lowest` (v1.6.0) runs the suite with every *direct* dependency resolved to its declared floor:

```bash
uv run rhiza-task test-lowest
```

It resolves `--isolated`, which matters more than it sounds: without it `uv` re-resolves the *project* environment in place and leaves both `.venv` and `uv.lock` downgraded when the gate finishes. On a runner that is invisible; on your machine it is a gate that silently rewrites a tracked file and changes what every later task runs against.

**Its being a task rather than a workflow step is the whole point.** rhiza had a `lowest-deps` job that called plain `uv`, because there was nothing to call — and a caller that bypasses the task graph bypasses `install`, and with it the `local-setup.sh` hook from [Lesson 10](./10-customizing-safely.md). So a repo whose setup hook provisions a native binary got a green `test` and a red `lowest-deps` on identical code, reporting a resolution problem that was really a missing `dot` on the runner. Arriving through `install` puts the gate back inside the single insertion point.

## pytest-rhiza — the repository checks, as a plugin

[`pytest-rhiza`](https://github.com/Jebel-Quant/pytest-rhiza) is the same move applied to the template's *conformance checks*. Up to v1.3.3 the template synced seven test modules plus a `conftest.py` into every consumer's `.rhiza/tests/`. Since **v1.3.4** they are a pytest plugin, run by the `rhiza-test` task:

```bash
uv run rhiza-task rhiza-test
```

Distributing them as a dependency removes the seven template-owned files, the `pythonpath` entry that let the synced suite import itself, and the template's own meta-tests re-running inside every project. The version is pinned by `pytest-rhiza` in `[tool.rhiza-task]`, so — as with the task CLI — the assertions a repo runs are those of a known release rather than of whatever the checks repo's `main` says today.

## rhiza-hooks — the commit hooks

[`rhiza-hooks`](https://github.com/Jebel-Quant/rhiza-hooks) is a pre-commit hook repository. Each language layer ships a `.pre-commit-config.yaml` that pulls from it — for Python that is `python-core`, not `core`, since v1.3.0 split the language layer out. The hooks run automatically on `git commit` and catch common mistakes before they hit CI:

| Hook | What it checks |
|------|---------------|
| `check-rhiza-config` | `template.yml` is valid and the referenced repo/ref can be resolved |
| `check-rhiza-workflow-names` | GitHub Actions workflow names carry the uppercase `(RHIZA)` prefix — and fixes them if not |
| `check-makefile-targets` | The Makefile front door still resolves the tasks CI depends on |
| `check-workflow-make-targets` | Every task CI actually invokes exists in the pinned `rhiza-task` |
| `check-test-layout` | Tests sit where the gates expect to find them |
| `check-python-version-consistency` | `.python-version`, `pyproject.toml`, and CI matrix all agree on the Python version |
| `check-rust-version-consistency` | The Rust toolchain versions agree across the repo |
| `check-go-version-consistency` | The Go versions agree across the repo |
| `check-bumpversion-config` | `bump-my-version` can find its config, so `/rhiza:release` will not stall |
| `check-template-bundles` | The bundles listed in `template.yml` exist in the remote template repo |
| `check-managed-files` | No template-owned file has been modified locally without being excluded |
| `check-license-metadata` | The licence declared in the manifest, the `LICENSE` file, and the classifiers agree |
| `update-readme-help` | Embeds the current `make help` output — now generated by `rhiza-task list` — into the README automatically |

The three version-consistency hooks are the visible edge of the multi-language split: a repo gets the one that matches its language layer.

These run locally on commit — through [`prek`](https://github.com/j178/prek) rather than `pre-commit` itself since template v1.3.2, a faster drop-in runner for the same config file, invoked by the `fmt` task as `uvx prek run --all-files`. Since v1.5.0 the shipped hooks also carry **prek groups**, so a subset can be run on its own rather than the whole file every time. The template's CI enforces the equivalent quality gates as well, so nothing slips through if someone bypasses the local hooks.

## rhiza-brainbug — cross-repo test harness

[`rhiza-brainbug`](https://github.com/Jebel-Quant/rhiza-brainbug) solves a problem that appears once you have many interdependent Rhiza projects: **contract and compatibility tests that span more than one repo**. Rather than duplicating an integration test in every consumer, you write it once in brainbug.

Brainbug watches a list of repositories on a cron. When any branch of a watched repo gets a new commit, brainbug checks out that repo at that SHA and runs its own tests ("brainbugs") against the code. Nothing is installed in the monitored repos — it is pure polling, comparing each branch head against a stored state file and self-dispatching a run on any change.

This makes it the ecosystem's answer to "did my change break a downstream repo?" without wiring webhooks or CI triggers into every project.

## How the pieces fit together

```
                    ┌──────────────────────────────┐
                    │       template repo          │
                    │           (rhiza)            │
                    │  core + python/rust/go-core  │
                    └─────────────┬────────────────┘
                                  │ config files only
                    ┌─────────────▼────────────────┐
                    │        rhiza-claude          │
                    │  init · update · quality     │
                    │  docs · release · remote     │
                    │  status · completions        │
                    │  detach · maffay             │
                    └─────────────┬────────────────┘
                                  │ drives
                    ┌─────────────▼────────────────┐
                    │        your project          │
                    │  .rhiza/template.yml + .lock │
                    │  Makefile shim → RHIZA_TASK  │
                    └──┬─────────────────────┬─────┘
                       │                     │ uvx, at the pinned version
          ┌────────────▼────────┐  ┌─────────▼──────────────┐
          │    rhiza-hooks      │  │      rhiza-task        │
          │     (via prek)      │  │  install · test · fmt  │
          └─────────────────────┘  │  … + pytest-rhiza      │
                                   └────────────────────────┘

   Cross-repo testing:   rhiza-brainbug → contract/compatibility runs on upstream commits
```

At the top is the template repo (Rhiza). Note what now flows down from it: **configuration files only**. `rhiza-claude` is the interface layer — its slash commands materialize those files into your project, run the quality gates, and keep the docs honest, all driven from Claude Code. The *executable* content comes from the right-hand branch instead: `rhiza-task` supplies the tasks and `pytest-rhiza` the conformance checks, both provisioned by `uvx` at the version your synced `Makefile` pins. `rhiza-hooks` keeps the project valid on every commit, and `rhiza-brainbug` runs the compatibility tests that span multiple Rhiza projects.

That split is the shape of the whole ecosystem in one line: **a template distributes configuration; a package manager distributes code.** Every piece that moved out of the template between v1.3.3 and v1.8.0 moved for that reason.

---

**Next:** [Lesson 12 — Further Reading](./12-further-reading.md)
