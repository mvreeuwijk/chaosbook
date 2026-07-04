# `shared/` - resources common to every language edition

Each language edition (`maple/`, and later `python/`) is a self-contained Sphinx
source tree with its own `conf.py`, `index.md` and chapter `.md` files. Anything
that is genuinely identical across editions lives here and is pulled in via
config, so it is maintained once.

## What's shared here

| File | Wired into each edition's `conf.py` via |
|------|------------------------------------------|
| `refs.bib`          | `bibtex_bibfiles = ['../shared/refs.bib']` |
| `custom.sty`        | `latex_additional_files = ['../shared/custom.sty']` |
| `_static/custom.css`| `html_static_path = ['../shared/_static', '_static']` |

These three share **losslessly through config** because Sphinx resolves them by
configuration, not by document-relative path.

## Adding the Python edition

1. Copy `maple/` to `python/` (prose is duplicated by design - see the repo
   `README.md`). The copy already points at `../shared`, so it builds green
   immediately, still showing Maple code.
2. Swap each ` ```{code-block} maple ` snippet for its Python equivalent. Use
   `creators/README.md` (Maple->Python cheat-sheet) and `creators/MODELS.md`
   (canonical equations & parameters) as the recipe.
3. Regenerate the **computed** figures into `python/_static/` with matplotlib,
   keeping the same basenames so the image references resolve unchanged.
4. `make python`.

## Figures the Python edition does NOT regenerate (hand-drawn schematics)

These have no Maple worksheet - they are xfig/TikZ schematics (confidence `n/a`
in `creators/figure_maple_map.csv`). The Python edition should **copy** them from
`maple/_static/`, not redraw them:

    maple/_static/phenomenon/3body.{png,pdf}
    maple/_static/cont2d/cont2d_phasespace.{png,pdf}
    maple/_static/cont2d/cont2d_phase_r1.{png,pdf}
    maple/_static/cont2d/cont2d_phase_r2.{png,pdf}
    maple/_static/cont2d/cont2d_phase_r3.{png,pdf}
    maple/_static/cont2d/cont2d_phase_i1.{png,pdf}
    maple/_static/cont2d/cont2d_phase_i2.{png,pdf}
    maple/_static/cont2d/cont2d_phase_i3.{png,pdf}
    maple/_static/cont2d/cont2d_classification.{png,pdf}

Likely a 10th (flagged `REVIEW`, "no maple script found" - confirm before
relying on it):

    maple/_static/cont2d/cont2d_zoo.{png,pdf}

Note: these are referenced by `{figure}` / `![]()` directives, which Sphinx
resolves relative to the source document - so they cannot be shared purely via
config the way the CSS/bib/sty above are. They must physically exist in each
edition's `_static/`. Since they are immutable, the simplest approach when
`python/` is created is a one-time copy (or a `make` copy step); decide then.
