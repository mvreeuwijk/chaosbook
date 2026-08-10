# Python edition vision: package, interactive figures, live layer — design

**Date:** 2026-08-10
**Status:** approved (umbrella vision; sub-projects get their own specs/plans)
**Builds on:** `2026-08-10-python-cookbook-design.md` (the cookbook notebook, implemented)

## Goal

Make the Python edition of *From Stability to Chaos* a cutting-edge
publication: a small chaos-specific package (`chaosbook`) introduced in the
cookbook and reused across the book, interactive figures embedded in the
site, and a zero-install live Jupyter layer for free exploration.

## Decisions made during brainstorming

1. **Serverless-first interactivity with a live escape hatch** — rich
   interactive figures are baked into the static HTML (no kernel needed to
   read); full free exploration happens in JupyterLite (Python in the
   browser via Pyodide), launched per page. (Rejected: fully live pages —
   reading would depend on a kernel booting; notebook-only — the site itself
   stays inert.)
2. **Small bespoke package** (`chaosbook`) built on numpy/scipy only,
   mirroring the book's notation. (Rejected: adopting pynamical/nolds/etc. —
   partial coverage, foreign notation, staleness risk; no package —
   repetitive chapter code.)
3. **Plotly** powers the serverless interactive figures (3D rotation,
   animations, precomputed sliders, zoom), with static twins exported for
   the PDF. (Rejected: bokeh — weak 3D; hand-rolled JS — bespoke
   engineering per figure.)
4. **Build order: package first, then a pilot chapter** (disc1d), then
   JupyterLite wiring, then rollout. (Rejected: pilot-chapter-first — API
   designed under pressure; infrastructure-first — nothing to show.)
5. **No platform migration** — the existing Sphinx + sphinx-book-theme +
   myst-nb stack supports all of the above; the mono-repo keeps one build
   system for both editions.

## The six interactive figure families

Walking the ~120 figures in the Maple chapters, the interactivity potential
falls into six families:

1. **Parameter-sweep panels → sliders.** The book's most repeated pattern is
   the same plot at several parameter values (logistic map at r = 1.5 / 3.2 /
   3.5 / 3.9 as series, return plots and cobwebs; Hopf at two μ; pitchfork /
   saddle / transcritical at three r each; Rössler at four period-doubling
   c values; ferromagnet at five temperatures). Each figure *set* collapses
   into one figure with a slider.
2. **Phase portraits → click-to-launch trajectories.** Lotka-Volterra, van
   der Pol, gradient systems, the standard map: click an initial condition,
   watch the trajectory grow; readers discover basins themselves.
3. **3D attractors → rotate/zoom.** Lorenz, Rössler, three-body trajectories.
4. **Sensitivity demos → play-button animations.** Twin Lorenz trajectories
   separating; the Hénon stretch-and-fold sequence (six static frames today).
5. **Bifurcation/fractal zooms.** The book already ships hand-made zoom
   insets; interactive pan/zoom over a precomputed fine grid shows
   self-similarity directly.
6. **Poincaré sections → linked views.** Drag the section plane / hover
   points to see them on the 3D trajectory.

Families 1 (precomputed grid), 3, 4, 5 work serverless via plotly. Families
2 and 6 (and family 1 at full parameter freedom) need a kernel and belong to
the JupyterLite layer.

## 1. Architecture

Three pillars on the existing Sphinx stack:

- **`chaosbook` package** — the book's computational vocabulary.
- **Interactive figures** — plotly, embedded in HTML chapters; every
  interactive figure has a static twin; the PDF remains first-class.
- **Live layer** — JupyterLite companion notebooks with the package
  pre-installed, launched from chapter pages, running in the reader's
  browser (no server, no install).

**Principle: progressive enhancement.** The site reads perfectly with JS
off and prints perfectly to PDF; interactivity is layered on top, never
load-bearing.

## 2. The `chaosbook` package

```
src/chaosbook/
  maps.py         # logistic, sine, tent, henon, standard, circle — x_{n+1} = f(x_n, r)
  flows.py        # RHS functions: lorenz, rossler, vanderpol, lotka_volterra, duffing…
  iterate.py      # orbit(f, x0, n), orbit2d — iteration made one call
  cobweb.py       # cobweb(f, x0, n) → matplotlib axes
  bifurcation.py  # bifurcation_diagram(f, rmin, rmax, …), lyapunov(f, …)
  poincare.py     # sections via solve_ivp event functions
  fractal.py      # chaos_game, box_dimension
tests/            # pytest; qualitative/aggregate assertions (fixed points,
                  # Lyapunov signs, box-count slope ≈ 1.585), never exact
                  # chaotic trajectories
pyproject.toml    # pure-python wheel — installable locally, on PyPI (later),
                  # and in Pyodide/JupyterLite via piplite
```

- **The core of the package is the analysis and visualisation machinery**
  (orbit, cobweb, bifurcation, Lyapunov, Poincaré, box dimension): generic
  tools that operate on any user-supplied map or flow `f`. The bundled
  systems (`maps.py`, `flows.py` — logistic, Lorenz, …) are convenience
  examples of the kind readers define themselves; they are secondary, and
  the tools must never assume them.
- APIs mirror the book's notation exactly: parameter names (r, sigma, b),
  defaults, and conventions match the chapters and `creators/MODELS.md`.
- Dependencies: numpy and scipy only (matplotlib accepted in plotting
  helpers). Pure-python wheel so the same artifact installs everywhere,
  including in the browser.
- Deliberately small: modules and functions are added when a chapter or
  notebook needs them, not speculatively.
- Package name `chaosbook` is the working name; check PyPI availability
  before first release and fall back to an alternative (e.g. `stab2chaos`)
  if taken.

## 3. Cookbook integration

- Each cookbook recipe stays **plain-code-first**; where a package
  counterpart exists, the recipe closes with a short "In the package"
  admonition: *"This recipe is available ready-made:
  `chaosbook.cobweb(f, x0=0.1, n=50)` — the implementation is exactly the
  code above."*
- The cookbook gains one new section introducing the package
  (`pip install chaosbook`, import conventions).
- Chapters use the package in their code fragments, each linking back to
  the cookbook recipe that shows the internals. The package is the
  *vocabulary*; the cookbook is the *dictionary*.

## 4. Interactive figures & the PDF

- Plotly patterns per family: precomputed-frame slider (family 1),
  rotatable 3D scene (3), play-button animation (4), high-resolution
  pan/zoom (5).
- **Authoring workflow:** `creators/python/<chapter>/` scripts — the Python
  counterpart of the Maple worksheets — build each figure once from
  `chaosbook` functions and emit both the interactive asset (for HTML) and
  the static PNG/PDF twin (via kaleido). The porting manifest tracks both.
- Static-only figures stay pure matplotlib; plotly is used only where
  interaction earns its page weight (~3 MB JS on pages that use it).
- The LaTeX/PDF build consumes only the static twins; no interactive
  machinery in the print pipeline.

## 5. JupyterLite layer

- A JupyterLite deployment ships as a static asset folder built in CI, with
  numpy/scipy/matplotlib/ipywidgets and the `chaosbook` wheel pre-loaded.
- Each chapter gets a **companion notebook** (the "laboratory"): sliders at
  full parameter freedom, click-to-set initial conditions, Poincaré
  exploration — launched from a button on the chapter page.
- The cookbook notebook itself becomes launchable the same way.
- Requires no server: it is static files on GitHub Pages, running Python in
  the reader's browser.

## 6. Sequencing

Each step is its own spec → plan → implementation cycle:

1. **`chaosbook` package** + tests + cookbook integration (admonitions +
   install section).
2. **disc1d pilot chapter** — richest slider material; proves
   plotly + static twins + package end-to-end.
3. **JupyterLite wiring** + first companion notebook.
4. **Rollout** to the remaining chapters.

## Out of scope (deliberate)

- Migrating away from Sphinx (Jupyter Book 2 / Quarto / marimo) — revisit
  only if the current stack blocks a pillar.
- Custom d3/JS visualisations beyond what plotly provides.
- Binder/Colab as the primary live backend (JupyterLite is; launch links to
  Colab may be added later as a convenience).
- Publishing the package to PyPI (happens at first stable release of the
  Python edition).
