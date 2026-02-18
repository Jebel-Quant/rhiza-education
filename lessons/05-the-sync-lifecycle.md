# Lesson 5 — The Sync Lifecycle

Once Rhiza is set up, you largely stop thinking about it — until a sync PR appears. This lesson explains what drives those PRs, what they contain, and how to handle them.

## Two triggers for sync

Your project will receive sync-related PRs from two sources:

**1. The sync workflow (`rhiza_sync.yml`)**

This GitHub Actions workflow runs on a schedule (typically weekly) and does the following:

1. Runs `uvx rhiza materialize` inside a temporary branch.
2. Compares the result against your current `main` branch.
3. If any files changed, opens a pull request with the diff.
4. If nothing changed, exits silently.

You can also trigger it manually from the GitHub Actions tab.

**2. Renovate**

Renovate watches the `ref: vX.Y.Z` line in your `.rhiza/template.yml`. When the template repository publishes a new tag, Renovate opens a PR that bumps your `ref` to the new version — for example, changing `ref: v0.7.1` to `ref: v0.8.0`.

These two PRs work together: Renovate bumps the version, the sync workflow applies what changed in that new version.

## Reading a sync PR

A sync PR shows you a standard git diff of the template files that changed. Here is how to read it:

- **Added lines (green)**: New content in the template that your project does not have yet. Usually safe to accept.
- **Removed lines (red)**: Content removed from the template. Check whether you depend on anything being removed.
- **Changed lines**: Modifications to existing files. Read these carefully — they may update a workflow version, change a lint rule, or fix a bug.

The PR description usually explains what changed at a high level. If you pinned to a tag and Renovate bumped it, check the template repo's changelog for the version you are upgrading to.

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

> **Note:** Closing a sync PR is fine. The next scheduled sync will open a new PR if the template still differs from your project. If you want to permanently silence a specific file from sync, add it to `exclude:` in `template.yml`.

## Handling conflicts

Occasionally a sync PR will have a merge conflict — usually because you edited a template-managed file locally. Your options:

1. **Accept the template version**: If the template's version is better, take it and discard your local change.
2. **Keep your local version and exclude the file**: Add the file to `exclude:` in `template.yml` so future syncs skip it. Resolve the conflict in favour of your version.
3. **Merge both sets of changes manually**: Edit the file to incorporate what you need from both the template and your local version, then mark the conflict resolved.

The cleanest long-term approach is to avoid editing template-managed files directly. If you need custom behaviour, use the extension points described in Lesson 6.

## Triggering sync manually

To run a sync without waiting for the schedule:

```bash
# Via the Makefile
make sync

# Or directly via the CLI
uvx rhiza materialize
```

This writes updated files to disk. Review the changes with `git diff`, commit them, and push.

---

**Next:** [Lesson 6 — Customising Safely](./06-customizing-safely.md)
