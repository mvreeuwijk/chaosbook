# Contributing

Thanks for your interest in *From Stability to Chaos*. Corrections and
suggestions are genuinely valued — because the exercises and figures are central
to the book, errata reports are especially useful.

## Reporting errata, typos and issues

Please [open an issue](https://github.com/mvreeuwijk/chaosbook/issues). An
**erratum** template is provided for reporting mistakes in the text, maths,
figures or exercises; there is also a general template for questions and
suggestions. When reporting an erratum, please include the chapter/section (or
figure/equation label) so it is easy to locate.

## Making changes

1. Fork and branch off `main`.
2. Edit the relevant source. The prose lives in the per-edition trees
   (`maple/`, later `python/`); shared resources are in `shared/`; figure
   sources and the figure → worksheet mapping are in `creators/`.
3. Build locally and check your change renders (see below).
4. Open a pull request describing what you changed and why.

Keep pull requests focused — a single erratum or a single topic per PR is easier
to review than a sweeping change.

## Building locally

```
pip install -r requirements.txt
make maple                 # HTML -> build/maple/html
```

For the PDF:

```
sphinx-build -b latex maple build/maple/latex
cd build/maple/latex && latexmk -pdf main.tex
```

The `build/` directory is generated output and is git-ignored — never edit or
commit files under `build/` (or the copies under `build/**/_sources/`); change
the source in `maple/` (or `shared/`) instead. GitHub Actions rebuilds and
deploys the site on every push to `main` (see
[`.github/workflows/pages.yml`](.github/workflows/pages.yml)).

## Conventions

The book uses [MyST Markdown](https://myst-parser.readthedocs.io/) with Sphinx.
A few house rules keep the source consistent:

- **Cross-references** use roles/labels, e.g. `` {numref}`fig:...` ``,
  `` {eq}`eq:...` ``, `` {cite:t}`Key` `` — not hard-coded numbers.
- **Math** is written with `$...$` / `$$...$$` and MyST `{math}` blocks.
- **Differentials** use an upright `d`: write `\mathrm{d}` for derivative and
  integral differentials — `\frac{\mathrm{d}x}{\mathrm{d}t}`, `\int f \,\mathrm{d}x`
  — never a plain italic `d`. (This does **not** apply to variable names inside
  Maple/Python code fragments, e.g. a timestep `dt`.)
- **Figures** are generated from the sources catalogued in `creators/`; if you
  change a figure, update the corresponding worksheet and the manifest rather
  than editing the image.

## Editions

This is a mono-repo hosting multiple editions of the same book. Shared
mathematical and textual material should live in `shared/` (or be factored so it
can be); edition-specific material (code fragments, figure workflows, notebooks)
stays inside that edition's tree. See [ROADMAP.md](ROADMAP.md) for how the
Python edition is expected to slot in alongside the Maple one.
