# Lesson 9 — Renovate

[Renovate](https://docs.renovatebot.com/) is an open-source dependency update bot. It scans your repositories for version pins and opens pull requests whenever a newer version is available. For most projects that means bumping package versions in `requirements.txt` or `pyproject.toml`. For Rhiza-managed projects, it does one more thing: it watches the `ref:` in `.rhiza/template.yml` and tells you when a newer template release is available, so a new version never slips by unnoticed.

## The problem Renovate solves for Rhiza

Consider what happens after you first bring a project onto the template with `ref: v1.2.0` pinned in your `template.yml`. Everything is wired up — CI, linting, releases. Six months later the template has moved on with security fixes, updated runner versions, and a new linting rule. Your project is still on `v1.2.0`.

Without Renovate, nothing tells you. The template has moved, but your `ref:` is still pinned to the old version. You have to notice the new release yourself and run `/rhiza:update`. Across a handful of projects this is manageable. Across twenty or thirty it becomes the same problem Rhiza was built to solve in the first place: inconsistency through neglect.

Renovate closes this gap. It opens a PR whenever a new template release is tagged, so every project receives a signal that says: *there is a new version.* You still decide when to adopt it.

## The two-part update flow

Rhiza separates *knowing a new version exists* from *applying what changed in it*. Renovate handles the first part — the notification. You handle the second by running `/rhiza:update`.

```
template repo publishes v1.2.0
         │
         ▼
Renovate opens PR: ref: v1.1.0 → v1.2.0   (notification only)
         │
         ▼ (you learn a new version exists)
you run /rhiza:update in Claude Code
         │
         ▼
ref bump + updated CI files, linting config, etc. land in one PR
```

The Renovate PR contains a single line change in `template.yml`. Merging it on its own does **not** apply the new template files — there is no sync workflow that reacts to it. It is a prompt. When you are ready, `/rhiza:update` performs the real update: it bumps the ref and materialises the changed files together in one reviewable PR. (You can also skip the Renovate signal entirely and run `/rhiza:status --check` to see whether you are behind, then `/rhiza:update`.)

## What a Renovate PR looks like

When a new template release is published, Renovate opens a PR with a title like:

```
Update dependency Jebel-Quant/rhiza to v1.2.0
```

The diff is minimal:

```diff
# .rhiza/template.yml
 repository: Jebel-Quant/rhiza
-ref: v1.1.0
+ref: v1.2.0
```

The PR body includes a changelog summary (when the template repo provides one), a confidence indicator based on how many other repos have already merged this update, and links to the release notes.

When you see this PR:
1. Check the template repo's [releases page](https://github.com/Jebel-Quant/rhiza/releases) for the release notes of the new version.
2. Scan for breaking changes — especially if the bump spans multiple minor versions.
3. Run `/rhiza:update` to actually adopt the version. It opens a follow-up PR with the file changes. (You can close the Renovate notification PR — `/rhiza:update` sets the ref itself.)

## How Rhiza ships Renovate configuration

The `renovate` bundle in Rhiza provides a `renovate.json` file at the root of your project. This file is the Renovate configuration. It does two things:

**1. Extends a base configuration**

```json
{
  "extends": ["config:recommended"]
}
```

`config:recommended` is Renovate's maintained base preset. It sets sensible defaults: grouped minor/patch updates, separate major-version PRs, a reasonable schedule.

**2. Teaches Renovate to read `.rhiza/template.yml`**

Renovate does not know about `.rhiza/template.yml` by default — it is not a standard lockfile or manifest. The bundle includes a [custom regex manager](https://docs.renovatebot.com/modules/manager/regex/) that teaches Renovate to parse the file:

```json
{
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["/(^|/)\\.rhiza/template\\.yml$/"],
      "matchStrings": [
        "repository:\\s*(?<depName>[^\\n]+)\\nref:\\s*(?<currentValue>[^\\n]+)"
      ],
      "datasourceTemplate": "github-releases",
      "versioningTemplate": "semver"
    }
  ]
}
```

This tells Renovate:
- Look in `.rhiza/template.yml`
- Extract the `repository:` field as the dependency name (e.g. `Jebel-Quant/rhiza`)
- Extract the `ref:` field as the current version
- Check the GitHub releases API for newer semver releases
- Open a PR when one is found

You do not need to write or maintain this regex yourself — it ships with the `renovate` bundle and is kept up to date by Rhiza.

## Enabling Renovate

### Option 1 — The Renovate GitHub App (recommended for most teams)

The quickest way to start is the [Renovate GitHub App](https://github.com/apps/renovate). Install it, grant it access to your repositories, and it will start scanning for `renovate.json` on its next run (usually within a few hours). No self-hosting, no tokens to manage.

On first activation, Renovate opens a **Dependency Dashboard** issue in your repo. This issue lists every pending update and lets you trigger or silence individual PRs on demand. Keep it — it is the easiest way to see the state of all pending dependency updates at a glance.

### Option 2 — Self-hosted Renovate

For organisations that cannot or prefer not to grant third-party app access, Renovate can be self-hosted. The standard approach uses the [official Docker image](https://docs.renovatebot.com/getting-started/running/) inside a scheduled CI job:

```yaml
# .github/workflows/renovate.yml
name: Renovate
on:
  schedule:
    - cron: '0 3 * * 1'   # every Monday at 03:00 UTC
  workflow_dispatch:

jobs:
  renovate:
    runs-on: ubuntu-latest
    steps:
      - uses: renovatebot/github-action@v40
        with:
          token: ${{ secrets.RENOVATE_TOKEN }}
```

You control the token scope, run frequency, and log verbosity. The trade-off is that you manage the infrastructure and the workflow file yourself.

## Practical configuration options

The `renovate.json` in your project is yours to extend. A few commonly useful settings:

### Schedule

By default Renovate runs on the schedule configured by the app or your workflow. You can restrict update PRs to specific windows:

```json
{
  "schedule": ["before 5am on Monday"]
}
```

This is useful for teams who want to review updates in batch on Monday mornings rather than receiving PRs throughout the week.

### Automerge for patch updates

If you trust your test suite and want zero-touch patch updates:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    }
  ]
}
```

Only enable automerge once your CI is comprehensive. For the Rhiza `ref:` specifically, leave automerge off — the ref-bump PR is a notification, and merging it does not apply the new template files anyway. You want to read the release notes and then run `/rhiza:update` deliberately.

### Grouping updates

To receive one PR per week covering all dependencies rather than individual PRs:

```json
{
  "packageRules": [
    {
      "groupName": "all non-major dependencies",
      "matchUpdateTypes": ["minor", "patch"]
    }
  ]
}
```

### Limiting PR count

To avoid a flood of PRs on initial setup:

```json
{
  "prConcurrentLimit": 5
}
```

## Why this matters at Rhiza scale

Rhiza exists because letting boilerplate drift across many repos is expensive. Renovate closes the last gap in that argument: without it, the `ref:` pin is effectively invisible unless someone remembers to check for new releases.

With Renovate in place, the lifecycle runs with minimal manual scanning:

1. The template repo ships a new version.
2. Renovate opens a one-line notification PR in every subscriber repo.
3. A reviewer reads the release notes and decides whether to adopt it.
4. Running `/rhiza:update` bumps the ref, applies the file changes, and opens a PR of template-owned files.
5. The reviewer merges that update PR.

No manual scanning of the template repo. No new release left unnoticed. Every project stays within a few weeks of the latest template — or opts out deliberately via the `exclude:` mechanism.

For a team running ten or more Rhiza-managed repos, Renovate is not optional infrastructure. It is the notification layer that keeps the living-template model working at scale.

## Renovate on GitLab

Renovate supports GitLab natively. The `renovate.json` file does not need to change. The self-hosted workflow runs as a scheduled pipeline job. Renovate opens merge requests instead of pull requests, but the content and review process are identical. See [Appendix A1 — GitLab Users](./A1-gitlab-users.md) for the full GitLab setup.

---

**Next:** [Lesson 10 — Customising Safely](./10-customizing-safely.md)
