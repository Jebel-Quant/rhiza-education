# Appendix A2 — Publishing Notebooks with Marimushka

[Marimushka](https://pypi.org/project/marimushka/) is a tool that exports [marimo](https://marimo.io/) notebooks to static HTML and WebAssembly, then publishes them as a browsable site — no Python installation required for readers. It is the publishing layer for the `marimo` bundle in Rhiza.

## What marimo notebooks are

Marimo notebooks are pure Python files (`.py`) that behave like reactive notebooks: change a value and everything that depends on it re-executes automatically. Unlike Jupyter notebooks, they are stored as plain Python, diff cleanly in git, and can be run as scripts or deployed as interactive web apps.

The `marimo` bundle in Rhiza brings marimo into your project:

```yaml
# .rhiza/template.yml
templates:
  - core
  - github
  - tests
  - marimo      # <-- adds marimo support
```

After materialising, your project gains a CI workflow that uses marimushka to export and publish all notebooks on every push.

## Two kinds of output

Marimushka distinguishes two directories and exports them differently:

| Directory | Export mode | What the reader sees |
|-----------|-------------|----------------------|
| `notebooks/` | Edit mode (HTML) | Full notebook with visible code, editable in the browser |
| `apps/` | Run mode (WebAssembly) | App UI only — code is hidden, runs entirely in the browser |

Put exploratory or tutorial notebooks in `notebooks/`. Put polished interactive tools in `apps/`. Both land on the same published site with an auto-generated index page.

## Running marimushka locally

```bash
uvx marimushka export
```

By default this reads `notebooks/` and `apps/` from the current directory and writes output to `_site/`. Key options:

```bash
uvx marimushka export --notebooks notebooks/ --apps apps/ --output _site/
```

Open `_site/index.html` in a browser to preview the published site before pushing.

## Configuration file

Persistent options live in `.marimushka.toml` at the project root:

```toml
notebooks = "notebooks"
apps = "apps"
output = "_site"
```

You can also tune parallelism, timeouts, and sandbox behaviour here. Once this file exists, `uvx marimushka export` picks it up automatically — no flags needed.

## The GitHub Action

The `marimo` bundle includes a workflow that uses the [`jebel-quant/marimushka` GitHub Action](https://github.com/marketplace/actions/marimushka-export-action) to export notebooks and deploy them to GitHub Pages on every push to `main`:

```yaml
- name: Export notebooks
  uses: jebel-quant/marimushka@v0.2.1
  with:
    notebooks: notebooks
    apps: apps
```

The action produces a GitHub Pages artifact that a subsequent deploy job picks up — the same artifact-upload pattern used throughout the Rhiza CI stack.

> **Enabling GitHub Pages:** Go to **Settings → Pages → Source: GitHub Actions** in your project repo. You only need to do this once.

## Sandbox mode

By default, marimushka exports notebooks with `--sandbox`, which means each notebook runs in an isolated environment with its own dependencies declared in the notebook itself. This is the recommended approach: it keeps published notebooks reproducible and avoids environment bleed between notebooks.

If a notebook needs access to your project's installed packages, pass `--no-sandbox`. In that case, ensure `uv sync` has run before calling `marimushka export`, because the notebook will import from the project virtualenv.

## Worked example

A project with this layout:

```
my-project/
├── notebooks/
│   ├── exploratory_analysis.py    # marimo notebook
│   └── tutorial.py                # marimo notebook
├── apps/
│   └── dashboard.py               # marimo app
├── .marimushka.toml
└── ...
```

After `uvx marimushka export`, the `_site/` directory contains:

```
_site/
├── index.html                     # auto-generated listing
├── notebooks/
│   ├── exploratory_analysis.html
│   └── tutorial.html
└── apps/
    └── dashboard/
        └── index.html             # WebAssembly app
```

The published index page links to all of them. Readers can open notebooks in edit mode and run them interactively in the browser without installing anything.

---

**Back to:** [Lesson 7 — Customising Safely](./07-customizing-safely.md) | [README](../README.md)
