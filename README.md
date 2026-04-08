# ols-mcdocs

Documentation / website for **Optimal Living Systems**, built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Local dev

```bash
./serve.sh     # live-reload preview at http://localhost:8000
./build.sh     # strict production build into ./site
```

Python virtualenv lives at `.venv/`. If recreating:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Editing content

All pages live under `docs/`. Nav order is defined in `mkdocs.yml`.

## Deploy

Pushes to `main` build and publish to GitHub Pages via `.github/workflows/gh-pages.yml`.
