# Python cookbook — design

**Date:** 2026-08-10
**Status:** approved
**Goal:** Start the Python edition of *From Stability to Chaos* by converting the
Maple cookbook (`maple/app_cookbook.md`) to a Python cookbook. The Python
edition must be entirely independent of the Maple edition — separate source
tree in the repo, separate built site on screen — and must prefer clear,
simple code over sophisticated code, even at some cost in speed.

## Decisions made during brainstorming

1. **Minimal `python/` tree** — a new Sphinx source tree containing only
   `conf.py`, a small `index.md` and the cookbook. Remaining chapters are added
   later as they are converted. (Rejected: copying the full `maple/` tree now,
   which would temporarily show Maple code on the Python site.)
2. **Jupyter notebook format** — the cookbook is `python/app_cookbook.ipynb`,
   rendered into the Sphinx site via `myst-nb`. (Rejected: a MyST `.md` page.)
3. **Stack: numpy/scipy/matplotlib + sympy** — numerical core, with sympy used
   only where symbolic work is the point (fixed points, derivatives,
   stability). (Rejected: purely numerical; sympy-centric.)
4. **Same recipes, Python-native intro** — the recipe sections keep the Maple
   cookbook's order, but Maple-specific intro material (Worksheet mode, Maple
   keys, `evalf`/`Digits`) is replaced with Python/Jupyter equivalents.
5. **Execution mode: `nb_execution_mode = "cache"`** — myst-nb executes the
   notebook during the Sphinx build and re-runs it only when it changes.
6. **One notebook** — a single `app_cookbook.ipynb`, matching the Maple
   cookbook's identity as one continuous reference document. (Rejected:
   notebook-per-theme; notebook + helper package.)

## 1. Repo layout

```
python/
  conf.py              # derived from maple/conf.py; myst-nb instead of myst-parser
  index.md             # minimal landing page: title + toctree (cookbook only, for now)
  app_cookbook.ipynb   # the Python cookbook, one notebook
  _static/             # edition-owned assets (empty for now)
```

- Nothing in `python/` mentions Maple. `make python` (already in the Makefile)
  builds to `build/python/html` — a fully separate site.
- `requirements.txt` gains `myst-nb`, `numpy`, `scipy`, `matplotlib`, `sympy`.
- The `maple/` tree is untouched.
- Shared resources come from `../shared` via config, exactly as the Maple
  edition does (`refs.bib`, `custom.sty`, `custom.css`).

## 2. Notebook content

Same recipe order as the Maple cookbook, with a Python-native opening:

| Maple section | Python counterpart |
|---|---|
| Settings & tips / Useful keys | Getting started with Jupyter: cells, running, keyboard shortcuts |
| Help | `help()` and IPython `?` |
| Comments | `#` comments |
| General | imports (`numpy`, `matplotlib`), assignment `=` vs comparison `==` |
| Floating point numbers | ints vs floats; exact answers via sympy when wanted |
| Functions vs expressions | `def` functions and lambdas; sympy expressions, `diff`, `solve`, `subs`, `lambdify` |
| Plotting | matplotlib basics |
| Lists, sets, sequences, Arrays, Matrices, Vectors | lists, tuples, numpy arrays, indexing/slicing, 2D arrays |
| For-loops | `for`, `range`, `while` |
| Plotting data points | markers and `scatter` |
| Plotting more than one function | multiple lines + legend |
| Implicitplot | `plt.contour(..., levels=[0])` |
| Iterative maps | logistic map iterated with a plain loop |
| Generate cobweb | cobweb plot built with a loop |
| Return plot | x[n] vs x[n+1] scatter |
| Bifurcation diagram | loop over r, discard transient, plot points |
| Non-linear ODEs, one variable | `scipy.integrate.solve_ivp` |
| Bifurcation diagram, continuous system | fixed points via sympy; integrate to large t for two initial conditions |
| ODEs in two dimensions | `solve_ivp`, phase portraits, several initial conditions |
| ODEs in three dimensions: chaos | sensitivity to initial conditions, time series, 3D trajectory |
| Manipulating solutions from dsolve | the `solve_ivp` result object: `t`, `y`, `t_eval`, dense output |
| Fractals | chaos-game Sierpinski gasket with a seeded random generator |
| Calculation box-dimension | box counting with an explicit grid loop and a log-log fit |

Every Maple section is either converted or its omission deliberately recorded
in the conversion (coverage cross-check, §4).

### Code style rules

- Plain loops over clever vectorisation whenever the loop is clearer; speed is
  secondary within reason.
- Each recipe self-contained and copy-pasteable; common imports appear once at
  the top of the notebook.
- Seeded randomness (`numpy.random.default_rng(seed)`) so re-execution is
  deterministic and cache-friendly.
- Default matplotlib styling; no custom style machinery.

## 3. Build integration

- `python/conf.py` starts from `maple/conf.py` with these changes:
  - `myst_parser` → `myst_nb` (myst-nb loads the MyST parser itself);
  - `nb_execution_mode = "cache"`;
  - drop the Maple lexer alias (`lexers["maple"]`) and the Maple-specific
    templates/sidebars (`navbar-center.html`, `exercises-nav.html`) — default
    book-theme navigation for now;
  - LaTeX configuration kept for the cookbook PDF: a `latex_documents` entry
    `('app_cookbook', 'cookbook.tex', 'The Python Cookbook', …, 'howto')`,
    mirroring the Maple edition's standalone cookbook PDF (article-based
    'howto' so top-level headings flow as sections). The book-level
    `latex_documents` entry and `latex_appendices` are dropped until those
    chapters exist.
- **Cookbook PDF is a first-class deliverable**: built via
  `sphinx-build -b latex python build/python/latex` + `latexmk -pdf
  cookbook.tex`, exactly parallel to the Maple cookbook's pipeline. The HTML
  cookbook page gets the same "Download the cookbook (PDF)" button as the
  Maple one, pointing at the Python edition's own `cookbook.pdf`.
- `python/index.md`: minimal landing page — book title, a line noting this is
  the Python edition (in progress), and a toctree containing the cookbook.
- No CI changes in this step: the deployed site remains the Maple edition; the
  Python site builds locally via `make python`. Publishing the Python site is
  a later, separate decision.

## 4. Verification

- The Sphinx build (`make python`) executes the notebook end-to-end; the build
  must be green with no new warnings.
- The LaTeX build produces `cookbook.pdf` cleanly (figures render, no missing
  characters or overfull disasters worth fixing).
- Visual sanity-check of the key figures: cobweb plot, bifurcation diagram,
  chaotic ODE trajectories, Sierpinski gasket, box-count slope ≈ log 3 / log 2
  ≈ 1.585.
- Coverage cross-check against `maple/app_cookbook.md`: every section accounted
  for (converted or deliberately omitted with a reason).

## Out of scope (deliberate)

- Converting the book chapters (`phenomenon.md` … `practice.md`) — later, one
  at a time.
- CI/deployment of the Python site and its PDF (the PDF builds locally for
  now; wiring it into the Pages workflow comes with deployment).
- A reusable `src/chaosbook/` package (ROADMAP §3) — the cookbook stays
  self-contained.
