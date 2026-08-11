# JupyterLite + exercise labs — design

**Date:** 2026-08-11
**Status:** approved (executed same day)
**Builds on:** `2026-08-10-python-edition-vision-design.md` (sub-project ③);
the pilot chapters (phenomenon, disc1d) and the `chaosbook` package are live
at `https://mvreeuwijk.github.io/chaosbook/python/`.

## Goal

Ship the live layer: a zero-install JupyterLite deployment (Python in the
browser via Pyodide) with the `chaosbook` wheel pre-loaded, and a companion
**exercise lab** notebook per pilot chapter — full parameter freedom where
the serverless figures were limited to precomputed frames, plus scaffolded
starter cells for every chapter exercise, with the exercise datasets already
in the lab's filesystem.

## Decisions

1. **Static deployment under `/python/lite/`** — `jupyter lite build`
   output is copied into the Pages artifact next to the Python edition;
   no server. Pyodide itself loads from the JupyterLite CDN defaults at
   runtime (NOT vendored: vendoring adds ~200 MB to every deploy for no
   functional gain; the reader is online anyway).
2. **The `chaosbook` wheel is built in CI and bundled via piplite** — the
   pure-python wheel (guarded since the package plan) is placed in the lite
   `pypi/` folder, so `%pip install chaosbook` resolves locally inside the
   browser with no PyPI dependency. ipywidgets installs from PyPI via
   piplite at runtime.
3. **Labs are exercise-first** ("exercise labs"): each lab opens with a
   free-exploration section (the widgets the serverless figures could not
   provide — continuous-r logistic explorer, Lorenz/three-body at full
   parameter freedom), then one scaffolded section per chapter exercise:
   a one-line restatement linking to the chapter for the full text, plus
   starter cells using the book's own code style. Exercise text is NOT
   duplicated into the notebooks (single source of truth stays in
   `python/_includes/`).
4. **Datasets pre-seeded**: the classification exercise's `set1/2/3.txt`
   ship inside the lab filesystem under `data/`, so `np.loadtxt` works
   immediately — no download/upload dance in the browser. They are
   committed copies in `files/data/` (26 kB each), not staged from
   `_static` at build time, so local nbconvert execution of the labs sees
   the same filesystem the browser does.
5. **One build entry point**: `python/lite/build_lite.py` stages the
   contents (lab notebooks + datasets + a launchable copy of the cookbook
   notebook with an inserted `%pip install` setup cell), builds the wheel,
   and runs `jupyter lite build`. The Makefile (`make python-lite`) and CI
   both call this script; nothing is staged by hand and no generated
   contents are committed.
6. **Launch buttons, not link rewrites**: each chapter gets a
   sphinx-design `button-link` (inside `{only} html`) at the Exercises
   section, and the cookbook page's button row gains a launch button.
   The "Code behind this figure" links STAY GitHub links — deviating from
   the pilot spec's "upgraded to a JupyterLite launch" remark: JupyterLite
   opens a `.py` file in a text editor with no run affordance, which is a
   worse reading experience than GitHub and not a lab. Figure scripts are
   for reading; labs are for running.
7. **Lab notebooks live in `python/lite/files/`** and are executed by
   nbconvert in local verification (the `%pip` setup cell is a no-op noise
   locally since the venv already has everything) — the labs' code is
   CI-testable without a browser.

## Layout

```
python/lite/
  jupyter_lite_config.json   # contents dir + output opts
  build_lite.py              # stage contents, build wheel, jupyter lite build
  files/
    phenomenon_lab.ipynb
    disc1d_lab.ipynb
    data/set{1,2,3}.txt      # committed copies of the exercise datasets
requirements-lite.txt        # jupyterlite-core, jupyterlite-pyodide-kernel,
                             # jupyter-server (contents addon), ipywidgets
                             # (bundles the widget labextension), build
```

Staged at build time (never committed): `cookbook.ipynb` =
`python/app_cookbook.ipynb` with a setup cell inserted after the title cell
(and the PDF button block dropped — it is site chrome, not notebook content).

## Out of scope (deliberate)

- Labs for chapters beyond the pilot two — rollout chapters bring their own
  labs (same pattern) with each chapter conversion.
- Vendoring pyodide / offline use.
- ipympl-based click-to-set initial conditions — revisit if a rollout
  chapter needs it; sliders + editable ICs cover the pilot exercises.
- Colab/Binder alternates.
