# Lesson 8 — The Sync Lifecycle

Once Rhiza is set up, you largely stop thinking about it — until it is time to pull in a new template version. This lesson explains what drives an update, what the resulting PR contains, and how to handle it.

## How updates reach your project

There is no automated CI job that materialises template files into your repo. Template file changes are applied by a human running `/rhiza:update` in Claude Code. What you receive automatically is a *signal* that a new template version exists — and there are two ways that signal arrives.

**1. You run `/rhiza:update` yourself**

`/rhiza:update` is the update mechanism. When you run it in Claude Code, it:

1. Bumps your `ref:` to the latest (or a given) rhiza release.
2. Materialises the changed template files into your repo.
3. Resolves conflicts against the template upstream.
4. Opens a pull request containing **only** template-owned files — the paths `.rhiza/template.lock` records, never a blanket `git add --all`.

You can run it whenever you like. To check first whether you are behind the latest release, run `/rhiza:status --check` — it compares your pinned `ref:` against the latest upstream release.

Note what is *not* on that list: `/rhiza:update` runs no quality gates, produces no scorecard, and files no issues. The sync stays single-purpose so that exactly one code path writes template files. When you want the repo scored — before or after an update — run `/rhiza:quality`, which is built for it.

**2. Renovate opens a `ref:` bump PR**

Renovate watches the `ref: vX.Y.Z` line in your `.rhiza/template.yml`. When the template repository publishes a new release, Renovate opens a PR that bumps your `ref` to the new version — for example, changing `ref: v1.1.0` to `ref: v1.2.0`.

This PR is a **notification only**. Merging it changes one line in `template.yml`, but it does *not* apply the new template files — there is no sync workflow to do that. Treat the Renovate PR as a prompt: a new template version is available. When you are ready to adopt it, run `/rhiza:update`, which bumps the ref and materialises the changed files together in a single reviewable PR.

## Reading a `/rhiza:update` PR

A `/rhiza:update` PR shows you a standard git diff of the template files that changed, and nothing else. Here is how to read it:

- **Added lines (green)**: New content in the template that your project does not have yet. Usually safe to accept.
- **Removed lines (red)**: Content removed from the template. Check whether you depend on anything being removed.
- **Changed lines**: Modifications to existing files. Read these carefully — they may update a workflow version, change a lint rule, or fix a bug.

The PR branch's own CI tells you whether the update leaves your project green. For a fuller picture — lint, types, docs, deps, security, tests, test-layout, complexity, architecture — run `/rhiza:quality` on the branch; the update itself will not tell you. If you bumped across several versions, check the template repo's changelog for the versions you are upgrading through.

## When to accept, modify, or reject

**Accept the PR as-is** when:
- The changes are CI workflow updates, runner version bumps, or linting rule adjustments that apply cleanly to your project.
- The diff looks correct and your tests pass in the PR branch.

**Modify the PR before merging** when:
- A change applies to your project but needs a small adjustment (e.g. the template added a workflow that references a file your project names differently).
- You want to accept most of the changes but exclude one file going forward — add it to `exclude` in `template.yml` and push to the PR branch.

**Close the PR without merging** when:
- The change is not relevant to your project (e.g. the template added Docker support but your project will never use containers).
- You have intentionally diverged from the template for a file and want to keep your local version.

> **Note:** Closing an update PR is fine — nothing changes until you merge. When you next run `/rhiza:update`, it will produce a fresh PR against the current template. If you want to permanently silence a specific file from updates, add it to `exclude:` in `template.yml`.

## Handling conflicts

Occasionally an update will run into a conflict — usually because you edited a template-managed file locally. `/rhiza:update` resolves conflicts against the template upstream as it builds the PR, but you still decide what to keep. Your options:

1. **Accept the template version**: If the template's version is better, take it and discard your local change.
2. **Keep your local version and exclude the file**: Add the file to `exclude:` in `template.yml` so future updates skip it, then keep your version.
3. **Merge both sets of changes manually**: Edit the file to incorporate what you need from both the template and your local version, then push to the PR branch.

The cleanest long-term approach is to avoid editing template-managed files directly. If you need custom behaviour, use the extension points described in Lesson 10.

## Running an update

To pull in the latest template version at any time, run in Claude Code:

```
/rhiza:update
```

This bumps your `ref:` to the latest release, syncs the changed files, resolves conflicts, and opens a PR of template-owned files. Review the PR, then merge.

---

**Next:** [Lesson 9 — Renovate](./09-renovate.md)
