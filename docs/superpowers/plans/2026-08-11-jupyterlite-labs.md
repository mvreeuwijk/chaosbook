# JupyterLite + exercise labs — implementation plan

**Goal:** Implement sub-project ③ per
`docs/superpowers/specs/2026-08-11-jupyterlite-labs-design.md`.

Versions pinned by what was tested locally: jupyterlite-core 0.8.1,
jupyterlite-pyodide-kernel 0.8.2.

## Task 1 — build infrastructure

- `requirements-lite.txt`: `jupyterlite-core~=0.8`,
  `jupyterlite-pyodide-kernel~=0.8`, `ipywidgets`, `build`.
- `python/lite/jupyter_lite_config.json`: no CDN vendoring; contents come
  from the staging dir the build script passes on the command line.
- `python/lite/build_lite.py <output-dir>`:
  1. stage contents into `<output-dir>-stage/` (fresh dir): `files/*`,
     `data/set{1,2,3}.txt` from `python/_static/exercises/`, and
     `cookbook.ipynb` derived from `python/app_cookbook.ipynb` (insert
     `%pip install -q chaosbook ipywidgets` setup cell after the title
     cell; drop the PDF `button-link` block from the title cell).
  2. `python -m build --wheel` the repo into `<stage>/pypi-wheel/`, pass to
     `jupyter lite build --pypi-wheels` equivalent (0.8: wheels placed in
     the lite dir's `pypi/` folder are bundled into piplite; the script
     copies the built wheel there).
  3. `jupyter lite build --contents <stage> --output-dir <output-dir>`
     run with cwd `python/lite/`.
  No recursive deletes of pre-existing user dirs: the script refuses to
  write into a non-empty output dir unless it contains a prior lite build
  marker (`jupyter-lite.json`).
- Makefile: `python-lite` target → `build/lite`; gitignore
  `python/lite/pypi/`, `python/lite/.jupyterlite.doit.db`, `dist/`.

## Task 2 — lab notebooks

`python/lite/files/phenomenon_lab.ipynb` — sections:
intro (what/why, chapter link), setup cell, Lorenz explorer
(ipywidgets `interact`: sigma, r, b, epsilon, tend → twin series + 3D
phase portrait), starter cells per chapter exercise (Lorenz sensitivity
a–g; three-body a–…) with the chapter's own script prefilled and
`# your turn` markers.

`python/lite/files/disc1d_lab.ipynb` — sections: intro, setup, logistic
explorer (continuous r-slider → series + cobweb + return plot via
`cb.orbit`/`cb.cobweb`), then starters: classification (loads
`data/set1.txt` etc.), Newton–Raphson, cubic map, universality
revisited, discrete cubic map.

All package calls use the real API (`cb.orbit(f, x0, n, **params)`,
`cb.cobweb(..., xmin, xmax, ax=)`, `cb.lyapunov(f, dfdx, x0, ...)`,
`cb.bifurcation_diagram(f, rmin, rmax, ...)`, `cb.lorenz(t, xyz, ...)`,
`cb.threebody(t, state, G, m1, m2, R)`, `cb.corotating(x, y, t, omega)`).
Widget callbacks close figures properly (`plt.show()` inside `interact`
functions) so repeated slider moves don't leak figures.

## Task 3 — site wiring

- `python/_includes/phenomenon_exercises.md` + `disc1d_exercises.md`:
  under the `## Exercises` heading, an `{only} html` block with a
  sphinx-design `button-link` to `lite/lab/index.html?path=<chapter>_lab.ipynb`
  ("Launch the exercise lab — runs in your browser, nothing to install").
- `python/app_cookbook.ipynb` title cell: add a second button
  (`lite/lab/index.html?path=cookbook.ipynb`) next to the PDF download.
- `.github/workflows/pages.yml`: after the Python edition HTML build,
  `pip install -r requirements-lite.txt` and
  `python python/lite/build_lite.py build/maple/html/python/lite`.

## Task 4 — verification (evidence, not assertions)

1. `Scripts/python -m pytest tests/ -q` — all pass.
2. `jupyter nbconvert --execute` both labs (paste the cell error report;
   zero errors required).
3. `python python/lite/build_lite.py build/lite` — paste tail of output;
   confirm `build/lite/lab/index.html`, bundled wheel in output `pypi/`,
   contents `phenomenon_lab.ipynb`/`disc1d_lab.ipynb`/`cookbook.ipynb`/
   `data/set1.txt` in `build/lite/files/` (via `jupyter lite` contents API).
4. Serve `build/lite` + Playwright: open
   `lab/index.html?path=disc1d_lab.ipynb`, wait for the pyodide kernel,
   run the setup cell, confirm `chaosbook` imports (screenshot).
5. Sphinx python edition builds clean into a fresh dir (OneDrive
   jupyter-cache gotcha: fresh output dir).
6. Commit on main; push (publishes) after all of the above pass.
