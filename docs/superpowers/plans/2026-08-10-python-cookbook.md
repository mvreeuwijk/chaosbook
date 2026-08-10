# Python Cookbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the Python edition's first deliverable: a minimal `python/` Sphinx tree whose sole content page is `app_cookbook.ipynb`, a Jupyter-notebook conversion of the Maple cookbook, with an HTML site and a standalone `cookbook.pdf`.

**Architecture:** A new self-contained Sphinx source tree `python/` (parallel to `maple/`, sharing `../shared` resources via config) built with `myst-nb` in `cache` execution mode, so the notebook executes during the Sphinx build. The cookbook is one notebook following the Maple cookbook's recipe order with a Python-native intro. Spec: `docs/superpowers/specs/2026-08-10-python-cookbook-design.md`.

**Tech Stack:** Sphinx + myst-nb + sphinx-book-theme; numpy, scipy (solve_ivp), matplotlib, sympy; LaTeX (`howto` class) for the PDF.

## Global Constraints

- **Nothing in `python/` may mention Maple** — no words, links, or code. The Python site must read as fully independent.
- **Clear simple code over sophisticated code**: plain `for`-loops where they are clearer than vectorisation; no helper modules; each recipe self-contained and copy-pasteable.
- **Deterministic execution**: all randomness through `np.random.default_rng(seed=1)`.
- **Parameters match the Maple cookbook** (logistic map `r=0.5/3.8`, bifurcation `N=500, Nr=200, x0=0.57`, Lorenz `r=28, b=8/3, sigma=10`, chaos game `N=10000`, box counting `pmax=20, lmin=lmax/100`).
- The `maple/` tree is untouched; the only files modified outside `python/` are `requirements.txt`.
- Shell commands below are Git Bash syntax, run from the repo root. If `make` is unavailable, `make python` ≡ `sphinx-build -M html python build/python`.
- Notebook cells are listed in order; add them with the NotebookEdit tool (or Jupyter). "md" = markdown cell, "code" = code cell. Do not store outputs; myst-nb executes at build time.

---

### Task 1: Scaffold the `python/` Sphinx tree

**Files:**
- Create: `python/conf.py`
- Create: `python/index.md`
- Create: `python/app_cookbook.ipynb`
- Create: `python/_static/.gitkeep`
- Modify: `requirements.txt`

**Interfaces:**
- Produces: a green `make python` build; `python/app_cookbook.ipynb` with title/intro cells that Tasks 2–6 append to; `nb_execution_mode = "cache"`, `nb_execution_timeout = 300` in conf.py that all later builds rely on.

- [ ] **Step 1: Update requirements.txt**

Append to `requirements.txt`:

```text
myst-nb
ipykernel
numpy
scipy
matplotlib
sympy
```

- [ ] **Step 2: Install the new dependencies**

Run: `pip install -r requirements.txt`
Expected: exits 0. (`myst-nb` and the existing `myst-parser` must co-resolve; pip picks compatible versions since neither is pinned.)

- [ ] **Step 3: Write `python/conf.py`**

Derived from `maple/conf.py`: `myst_parser` → `myst_nb`, notebook execution config added; Maple lexer alias, custom navbar/sidebar templates, book `latex_documents` entry and `latex_appendices` all dropped.

```python
# -*- coding: utf-8 -*-
#
# Sphinx configuration for the Python edition of "From Stability to Chaos".
# Parallel to maple/conf.py; shared resources (refs.bib, custom.sty,
# custom.css) come from ../shared via the settings below.

extensions = [
    'myst_nb',  # notebooks + MyST markdown (loads the MyST parser itself)
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.mathjax',
    'sphinx_design',
    'sphinxcontrib.proof',
    'sphinxcontrib.bibtex',
    'sphinx_subfigure',
    'sphinx_math_dollar',
]

autosectionlabel_prefix_document = True

master_doc = 'index'

project = u'From Stability to Chaos'
author = u'Harmen J. Jonker and Maarten van Reeuwijk'
copyright = u'2025, Harmen J. Jonker and Maarten van Reeuwijk'

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
mathjax3_config = {
    "tex": {
        "macros": {
            "d": r"\mathrm{d}",
        }
    }
}

import datetime as _datetime
_today = _datetime.date.today()
release = f'{_today:%B} {_today.day}, {_today.year}'
version = release
today = ''

exclude_patterns = []

pygments_style = 'sphinx'

proof_theorem_types = {
    "algorithm": "Algorithm",
    "conjecture": "Conjecture",
    "corollary": "Corollary",
    "definition": "Definition",
    "example": "Example",
    "lemma": "Lemma",
    "observation": "Observation",
    "proof": "Proof",
    "property": "Property",
    "theorem": "Theorem",
    "exercise": "Exercise",
    "tutorial": "Tutorial"
}
proof_latex_parent = "chapter"

# -- Notebook execution (myst-nb) ------------------------------------------
# "cache": execute during the Sphinx build, re-running only when the
# notebook changes (spec decision 5).
nb_execution_mode = "cache"
nb_execution_timeout = 300

# -- HTML ------------------------------------------------------------------

html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_url": "https://github.com/mvreeuwijk/chaosbook",
    "use_repository_button": True,
    "use_edit_page_button": False,
    "use_issues_button": False,
    "use_download_button": False,
    "home_page_in_toc": False,
    "collapse_navigation": True,
    "navigation_depth": 2,
    "show_nav_level": 1,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/mvreeuwijk/chaosbook",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
}
html_title = u'From Stability to Chaos'
html_static_path = ['../shared/_static', '_static']
html_css_files = ['custom.css']
html_use_smartypants = False
smartquotes = False

# -- LaTeX (the cookbook PDF) ----------------------------------------------

latex_additional_files = ['../shared/custom.sty']

latex_elements = {
    'papersize': 'a4paper',
    'fontpkg': '',
    'fncychap': '',
    'pointsize': '11pt',
    'releasename': "",
    'babel': '',
    'printindex': '',
    'fontenc': '',
    'inputenc': '',
    'classoptions': '',
    'utf8extra': '',
    'preamble': r'\usepackage{custom}\hypersetup{hypertexnames=false}',
    'figure_align': 'tbp',
}

# The cookbook is a standalone PDF built as a 'howto' (article-based)
# document: its top-level headings become sections rather than chapters, so
# they flow instead of each starting a new page.
latex_documents = [
  ('app_cookbook', 'cookbook.tex', u'The Python Cookbook',
   u'Harmen J. Jonker and Maarten van Reeuwijk', 'howto'),
]

numfig = True
numfig_format = {'figure': 'Figure %s', 'table': 'Table %s', 'section': '%s'}

bibtex_bibfiles = ['../shared/refs.bib']
suppress_warnings = ['bibtex.duplicate_citation']
bibtex_encoding = "iso-8859-1"
bibtex_default_style = "apa"
bibtex_reference_style = "author_year"

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
]
myst_dmath_double_inline = True
```

- [ ] **Step 4: Write `python/index.md`**

```markdown
# From Stability to Chaos

**A Hands-On Introduction to Nonlinear Dynamics** — Python edition.

The Python edition is under construction. The cookbook — a practical Python
reference for the techniques used throughout the book — is available now;
the chapters will follow.

```{toctree}
:hidden:
:numbered:
:caption: Cookbook

app_cookbook
```
```

(The outer fence must be a 4-backtick fence in the actual file so the inner toctree fence survives; write the file with the toctree as shown.)

- [ ] **Step 5: Create the notebook skeleton**

Write `python/app_cookbook.ipynb` with exactly this JSON:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": "(app:cookbook)=\n# The Python cookbook\n\n:::{only} html\n```{button-link} cookbook.pdf\n:color: primary\n:outline:\n\nDownload the cookbook (PDF)\n```\n:::\n\nThis Python cookbook contains various routines or 'recipes' for the analysis of non-linear and chaotic dynamical systems. The aim of this document is to provide you with a set of recipes that will enable you to analyze physical systems quickly and effectively. By no means is this document intended to be a sufficient introduction into Python, although it should give a reasonable impression of how Python works and what it can do in this field."
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

Also create the empty placeholder `python/_static/.gitkeep` (empty file).

- [ ] **Step 6: Build and verify**

Run: `make python`
Expected: exits 0; `build/python/html/index.html` and `build/python/html/app_cookbook.html` exist. Warnings about the (not yet existing) `cookbook.pdf` link target are acceptable; any ERROR is not.

Run: `grep -ri maple python/ --include='*.py' --include='*.md'; python -c "import json,sys; nb=json.load(open('python/app_cookbook.ipynb')); print(any('aple' in str(c) for c in nb['cells']))"`
Expected: no grep hits in index.md or conf.py prose visible to readers (the word may not appear at all outside pure config paths — it should appear nowhere), and `False` from the notebook check.

- [ ] **Step 7: Commit**

```bash
git add python/ requirements.txt
git commit -m "Scaffold the Python edition: minimal Sphinx tree with cookbook notebook"
```

---

### Task 2: Notebook basics — getting started through functions vs expressions

**Files:**
- Modify: `python/app_cookbook.ipynb` (append cells)

**Interfaces:**
- Consumes: notebook skeleton from Task 1.
- Produces: the shared import cell (`np`, `plt`, `sym`, `solve_ivp`) that ALL later code cells rely on; sympy symbols `x, y` defined in the "Functions vs expressions" section.

- [ ] **Step 1: Append the "Getting started" cells**

md:

```markdown
## Getting started

The recipes in this cookbook are written for the Jupyter notebook, the
standard interactive environment for scientific Python. The easiest way to
get everything at once is to install [Anaconda](https://www.anaconda.com);
alternatively install the packages directly with

    pip install numpy scipy matplotlib sympy jupyterlab

and start the environment with `jupyter lab`.

A notebook consists of *cells*. A cell contains either code or text
(Markdown), and a code cell is executed with Shift-Enter. All code in this
cookbook can be typed into a code cell and run directly.
```

md:

```markdown
## Useful keys

- Shift-Enter: run cell, move to the next
- Ctrl-Enter: run cell, stay
- Alt-Enter: run cell, insert a new one below
- Esc / Enter: leave / enter a cell (command vs edit mode)
- A / B (in command mode): insert cell above / below
- D,D (in command mode): delete cell
- M / Y (in command mode): make cell Markdown / code
- Z (in command mode): undo cell operation

Try them now!
```

- [ ] **Step 2: Append the "Help" cells**

md:

```markdown
## Help

Help on any function is available with `help`, or — in the notebook — by
appending a question mark (`sum?`) or pressing Shift-Tab inside the
parentheses.
```

code:

```python
help(sum)
```

- [ ] **Step 3: Append the "Comments" cells**

md:

```markdown
## Comments
```

code:

```python
#
# the #-sign allows comments
#
```

- [ ] **Step 4: Append the "General" cells**

md:

```markdown
## General

A session normally starts with importing the packages we need: `numpy` for
numerical arrays, `matplotlib` for figures, `sympy` for symbolic
mathematics and `solve_ivp` from `scipy` for differential equations. The
short names `np`, `plt` and `sym` are conventional.
```

code:

```python
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from scipy.integrate import solve_ivp
```

md:

```markdown
Some important details:

- A cell displays the value of its **last** expression automatically.
- Ending a line with `;` suppresses that display.
- Assigning a value to a variable is done with `=`. A common mistake is to
  confuse it with `==`, which *compares* two values.
```

code:

```python
a = 1 / np.sqrt(2)   # assignment: a gets a value
a
```

code:

```python
a == 0.5             # comparison: is a equal to 0.5?
```

- [ ] **Step 5: Append the "Floating point numbers and exact answers" cells**

md:

```markdown
## Floating point numbers and exact answers

Python computes with floating point numbers, accurate to about 16
significant digits: `1/2` and `0.5` are the same thing. If an exact or
arbitrarily accurate answer is needed, `sympy` provides it: `sym.sqrt(2)`
stays exact, and `sym.N` evaluates to any number of digits.
```

code:

```python
1 / 2
```

code:

```python
a = 1 / sym.sqrt(2)
a
```

code:

```python
sym.N(a)
```

code:

```python
sym.N(sym.pi, 60)
```

- [ ] **Step 6: Append the "Functions vs expressions" cells**

md:

```markdown
## Functions vs expressions

A Python *function* computes numbers from numbers:
```

code:

```python
def f(x):
    return x**2

f(2)
```

md:

```markdown
A sympy *expression* is a formula containing symbols. It is not evaluated
until values are substituted with `subs`:
```

code:

```python
x, y = sym.symbols("x y")
q = x**2
q
```

code:

```python
q.subs(x, 2)
```

md:

```markdown
The command `sym.diff` differentiates an expression:
```

code:

```python
q = sym.sin(x**2)
dq = sym.diff(q, x)
dq
```

md:

```markdown
`sym.lambdify` converts an expression into an ordinary numerical function —
useful whenever a symbolic result (a derivative, say) is needed inside a
numerical recipe:
```

code:

```python
dg = sym.lambdify(x, dq)
dg(2.0)
```

md:

```markdown
Expressions of more variables work the same way, and partial derivatives
are taken by naming the variable:
```

code:

```python
r = sym.sqrt(x**2 + y**2)
sym.diff(r, x)
```

md:

```markdown
We prefer plain Python functions in the recipes that follow, and bring in
sympy expressions only where symbolic work (fixed points, derivatives,
stability) is the point.
```

- [ ] **Step 7: Execute the notebook to verify**

Run: `jupyter execute python/app_cookbook.ipynb`
Expected: exits 0, no cell errors.

- [ ] **Step 8: Commit**

```bash
git add python/app_cookbook.ipynb
git commit -m "Cookbook: basics — getting started, help, imports, floats, functions vs expressions"
```

---

### Task 3: Notebook plotting and data structures

**Files:**
- Modify: `python/app_cookbook.ipynb` (append cells)

**Interfaces:**
- Consumes: imports (`np`, `plt`, `sym`) from Task 2.
- Produces: nothing later tasks depend on (each recipe redefines its own variables).

- [ ] **Step 1: Append the "Plotting" cells**

md:

```markdown
## Plotting

Plotting a function means evaluating it on a fine grid of points and
drawing lines through the results. `np.linspace` creates the grid;
functions from `numpy` (`np.sin`, `np.sqrt`, ...) work on whole arrays at
once.
```

code:

```python
xs = np.linspace(-2, 2, 200)
plt.plot(xs, np.sin(xs**2), label="sin(x²)")
plt.plot(xs, 2 * xs**2, label="2x²")
plt.xlabel("x")
plt.ylabel("y")
plt.legend();
```

- [ ] **Step 2: Append the "Lists, tuples and arrays" cells**

md:

```markdown
## Lists, tuples and arrays

Python's basic container is the list, written with square brackets. Lists
preserve order and may contain doubles. **Indices start at 0.**
```

code:

```python
a = [1, 2, 3, 2, 1]
a[2]
```

md:

```markdown
Appending elements one at a time — which we will do frequently to collect
results in a loop — starts from an empty list:
```

code:

```python
c = []
c.append(1)
c.append(2)
c
```

md:

```markdown
A set, written with curly braces, discards doubles and order. `len` gives
the number of elements of any container.
```

code:

```python
set(a)
```

code:

```python
len(a)
```

md:

```markdown
A *list comprehension* generates a new list from a rule — we will need it
regularly:
```

code:

```python
[i**2 for i in range(1, 6)]
```

md:

```markdown
For numerical work the `numpy` array is the workhorse. Arrays can be
created filled with zeros or ones, from a list, or from a rule; arithmetic
acts on all elements at once.
```

code:

```python
np.zeros(10)
```

code:

```python
np.ones(5)
```

code:

```python
t = np.array([5, 3, 4, 1, 2])
t
```

code:

```python
t = np.arange(1, 6)      # the integers 1..5
t**2
```

md:

```markdown
Sums and products of the elements:
```

code:

```python
t2 = t**2
t2.sum(), t.prod()
```

md:

```markdown
Two-dimensional arrays are created the same way, with a pair of sizes:
```

code:

```python
np.zeros((5, 5))
```

code:

```python
i, j = np.indices((5, 5))
(i + 1)**2 + (j + 1)**2
```

md:

```markdown
Matrices and vectors are simply 2D and 1D arrays. `@` is the
matrix-vector product, and `np.linalg` contains the linear algebra
routines. Say we want to solve $A \mathbf{y} = \mathbf{b}$:
```

code:

```python
A = np.array([[1, 2],
              [3, 4]])
b = np.array([1, 2])
ysol = np.linalg.solve(A, b)
ysol
```

md:

```markdown
Which is indeed the solution, as verified below.
```

code:

```python
b - A @ ysol
```

md:

```markdown
(The inverse `np.linalg.inv(A)` exists too, but for solving a system
`np.linalg.solve` is the better tool.)
```

- [ ] **Step 3: Append the "For-loops" cells**

md:

```markdown
## For-loops

Frequently we will want to study the behavior of the equations over
complete parameter spaces, which can be done with for-loops. Here we
tabulate a sine function; `range(N)` runs `i` through `0, 1, ..., N-1`.
```

code:

```python
N = 25
X = np.zeros(N)
Y = np.zeros(N)
for i in range(N):
    X[i] = i * 2 * np.pi / (N - 1)
    Y[i] = np.sin(X[i])
X[:10]
```

md:

```markdown
The slice `X[:10]` shows the first ten elements. The same table can be made
without a loop (`X = np.linspace(0, 2*np.pi, N); Y = np.sin(X)`), which is
faster — but the loop form generalizes to the iterative recipes below,
where each value depends on the previous one and there is no way around a
loop.
```

- [ ] **Step 4: Append the "Plotting data points" cells**

md:

```markdown
## Plotting data points

To plot discrete data points rather than a line, give `plt.plot` a marker
style: `"o"` for circles, `"s"` for squares, `"d"` for diamonds, `","` for
single pixels.
```

code:

```python
plt.plot(X, Y, "o")
plt.xlabel("x")
plt.ylabel("y");
```

md:

```markdown
Lines and points combine naturally — a format string like `"r-"` (red
line) or `"ko"` (black circles) sets both color and style:
```

code:

```python
pts = np.arange(0, 5)
xfine = np.linspace(0, 4, 100)
plt.plot(xfine, xfine**2, "r-")
plt.plot(pts, pts**2, "ko")
plt.xlabel("x")
plt.ylabel("y");
```

- [ ] **Step 5: Append the "Plotting more than one function" cells**

md:

```markdown
## Plotting more than one function at the same time

Successive `plt.plot` calls draw into the same figure until the cell ends,
so a loop can overlay any number of curves. `label` and `plt.legend` handle
the legend.
```

code:

```python
def f(x, a):
    return np.sin(a * x)

xs = np.linspace(-np.pi, np.pi, 200)
for a in [1, 2, 3]:
    plt.plot(xs, f(xs, a), label=f"a={a}")
plt.xlabel("x")
plt.ylabel("y")
plt.legend();
```

- [ ] **Step 6: Append the "Implicit plot" cells**

md:

```markdown
## Implicit plots

A very useful trick is plotting *implicitly* defined data: the set of
points where some function is zero. `plt.contour` with the single contour
level 0 does exactly this — for example those $x$ for which
$x=\tanh(x/T)$, as a function of $T$:
```

code:

```python
T, x = np.meshgrid(np.linspace(0.01, 2, 400), np.linspace(-1.1, 1.1, 400))
F = -x + np.tanh(x / T)
plt.contour(T, x, F, levels=[0], colors="magenta")
plt.xlabel("T")
plt.ylabel("x");
```

- [ ] **Step 7: Execute the notebook to verify**

Run: `jupyter execute python/app_cookbook.ipynb`
Expected: exits 0, no cell errors.

- [ ] **Step 8: Commit**

```bash
git add python/app_cookbook.ipynb
git commit -m "Cookbook: plotting, containers, arrays, loops, implicit plots"
```

---

### Task 4: Notebook iterative-map recipes

**Files:**
- Modify: `python/app_cookbook.ipynb` (append cells)

**Interfaces:**
- Consumes: imports from Task 2.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Append the "Iterative maps" cells**

md:

```markdown
## Iterative maps

The logistic map $x_{n+1} = r\,x_n(1-x_n)$ iterated with a plain loop.
Each value depends on the previous one, so a loop is the natural tool.
```

code:

```python
def f(x):
    return r * x * (1 - x)   # define function

N = 50                       # define nr of points
X = np.zeros(N + 1)          # declare data array
r = 0.5                      # set parameter
X[0] = 0.1                   # set initial condition
for n in range(N):           # perform iterations
    X[n + 1] = f(X[n])
```

md:

```markdown
Plot the time series as points:
```

code:

```python
plt.plot(range(N + 1), X, "d")
plt.xlabel("n")
plt.ylabel("x[n]");
```

md:

```markdown
or as a line through circles:
```

code:

```python
plt.plot(range(N + 1), X, "-o")
plt.xlabel("n")
plt.ylabel("x[n]");
```

- [ ] **Step 2: Append the "Generate cobweb" cells**

md:

```markdown
## Generate cobweb

Create and plot a cobweb of the discrete data set: starting from
$(x_0, 0)$, repeatedly step vertically to the map and horizontally to the
diagonal.
```

code:

```python
px = [X[0]]
py = [0]
for n in range(N):
    px += [X[n], X[n]]
    py += [X[n], X[n + 1]]

xs = np.linspace(0, 1, 200)
plt.plot(xs, f(xs), "k")     # the map
plt.plot(xs, xs, "b")        # the diagonal
plt.plot(px, py, "r")        # the cobweb
plt.axis([0, 1, 0, 1])
plt.xlabel("x[n]")
plt.ylabel("x[n+1]");
```

- [ ] **Step 3: Append the "Return plot" cells**

md:

```markdown
## Return plot

First we need to create a data series, now in the chaotic regime:
```

code:

```python
def f(x):
    return r * x * (1 - x)

N = 200
r = 3.8
X = np.zeros(N + 1)
X[0] = 0.4
for n in range(N):
    X[n + 1] = f(X[n])
```

md:

```markdown
Now create a return plot from the $[x_n, x_{n+1}]$ pairs, removing the
transient by disregarding the first $N/2$ points:
```

code:

```python
xs = np.linspace(0, 1, 200)
plt.plot(X[N // 2 : N], X[N // 2 + 1 : N + 1], "ro")
plt.plot(xs, f(xs), "k")
plt.axis([0, 1, 0, 1])
plt.xlabel("x[n]")
plt.ylabel("x[n+1]");
```

- [ ] **Step 4: Append the "Bifurcation diagram" cells**

md:

```markdown
## Bifurcation diagram

For each value of $r$, iterate the map and keep only the second half of
the series (the part that has converged onto the attractor); plotting
those points against $r$ produces the bifurcation diagram. The `","`
marker plots single pixels.
```

code:

```python
def f(x):
    return r * x * (1 - x)

N = 500                      # iterations per r value
Nr = 200                     # number of r values
rmin, rmax = 0.1, 4
Nmin = N // 2                # discard the first half as transient

rs = []
xs = []
for i in range(Nr + 1):
    r = rmin + (rmax - rmin) * i / Nr
    X = np.zeros(N + 1)
    X[0] = 0.57
    for n in range(N):
        X[n + 1] = f(X[n])
    for n in range(Nmin, N + 1):
        rs.append(r)
        xs.append(X[n])

plt.plot(rs, xs, ",", color="blue")
plt.axis([rmin, rmax, 0, 1])
plt.xlabel("r")
plt.ylabel("x(r)");
```

- [ ] **Step 5: Execute the notebook to verify**

Run: `jupyter execute python/app_cookbook.ipynb`
Expected: exits 0, no cell errors.

- [ ] **Step 6: Commit**

```bash
git add python/app_cookbook.ipynb
git commit -m "Cookbook: iterative maps, cobweb, return plot, bifurcation diagram"
```

---

### Task 5: Notebook differential-equation recipes

**Files:**
- Modify: `python/app_cookbook.ipynb` (append cells)

**Interfaces:**
- Consumes: imports from Task 2 (`solve_ivp`, `sym`, `np`, `plt`).
- Produces: the `lorenz` right-hand-side function and parameters `r, b, sigma`, reused by the "Manipulating solutions" section within this task only.

- [ ] **Step 1: Append the "ODEs with one variable" cells**

md:

```markdown
## Non-linear differential equations with one variable

`solve_ivp` from `scipy.integrate` solves $\dot x = f(t, x)$ numerically.
Its first argument is the right-hand side as a function of $t$ and $x$
(in that order), then the time interval, then the initial condition —
always as a list, because `solve_ivp` handles systems of any dimension.
`t_eval` says at which times we want the solution reported.
```

code:

```python
def f(t, x):
    return r * x - x**3

r = 1.2                      # set parameter value
x0 = 0.1                     # set initial condition
sol = solve_ivp(f, [0, 10], [x0], t_eval=np.linspace(0, 10, 200))
plt.plot(sol.t, sol.y[0])
plt.xlabel("t")
plt.ylabel("x");
```

- [ ] **Step 2: Append the "Bifurcation diagram continuous system" cells**

md:

```markdown
## Bifurcation diagram continuous system

Solve the equation up to a large time $t_\infty$ for a range of $r$ values
and two initial conditions, and record where the solution ends up — an
approximation of the stable fixed points.
```

code:

```python
rmin, rmax = -1, 1
N = 150
tinf = 200

for r in np.linspace(rmin, rmax, N + 1):
    for x0 in [-0.5, 0.5]:
        sol = solve_ivp(f, [0, tinf], [x0])
        plt.plot(r, sol.y[0, -1], "o", color="blue", markersize=3)
plt.xlabel("r")
plt.ylabel("x_inf");
```

- [ ] **Step 3: Append the "ODEs in two dimensions" cells**

md:

```markdown
## Non-linear differential equations with two dimensions

We will use an example of the Lotka-Volterra equations of competition.
```

code:

```python
def f1(x, y):
    return x * (3 - x - 2 * y)

def f2(x, y):
    return y * (2 - x - y)
```

md:

```markdown
Calculate the fixed points symbolically:
```

code:

```python
x, y = sym.symbols("x y")
fixed_points = sym.solve([f1(x, y), f2(x, y)], [x, y])
fixed_points
```

md:

```markdown
For the stability we need the Jacobian. Sympy computes it directly from
the vector of right-hand sides:
```

code:

```python
J = sym.Matrix([f1(x, y), f2(x, y)]).jacobian([x, y])
J
```

md:

```markdown
The Jacobian evaluated at the coexistence fixed point $(1, 1)$, and its
eigenvalues:
```

code:

```python
Jc = J.subs({x: 1, y: 1})
Jc
```

code:

```python
evs = list(Jc.eigenvals())
evs
```

code:

```python
[sym.N(ev) for ev in evs]
```

md:

```markdown
So the fixed point is a saddle node as $\lambda_1>0$ and $\lambda_2<0$.

### Phase portrait

A phase portrait combines the direction field (`plt.streamplot`) with a
few solution trajectories from different initial conditions:
```

code:

```python
def rhs(t, xy):
    x, y = xy
    return [f1(x, y), f2(x, y)]

X, Y = np.meshgrid(np.linspace(0, 4, 25), np.linspace(0, 4, 25))
plt.streamplot(X, Y, f1(X, Y), f2(X, Y), color="lightgray")
for x0, y0 in [(0.1, 0.15), (0.1, 0.3), (4, 2.5), (4, 3)]:
    sol = solve_ivp(rhs, [0, 50], [x0, y0], max_step=0.05)
    plt.plot(sol.y[0], sol.y[1])
plt.axis([0, 4, 0, 4])
plt.xlabel("x")
plt.ylabel("y");
```

- [ ] **Step 4: Append the "ODEs in three dimensions: chaos" cells**

md:

```markdown
## Non-linear differential equations with three dimensions: chaos

We will use the Lorenz equations as an example, with two initial
conditions very close to each other.
```

code:

```python
def lorenz(t, xyz):
    x, y, z = xyz
    return [sigma * (y - x),
            -x * z + r * x - y,
            x * y - b * z]

# define parameters
r, b, sigma = 28, 8 / 3, 10

# define two initial conditions close to each other
sol1 = solve_ivp(lorenz, [0, 40], [2, 5, 5], max_step=0.01)
sol2 = solve_ivp(lorenz, [0, 40], [2.0001, 5, 5], max_step=0.01)

# and plot the timeseries
plt.plot(sol1.t, sol1.y[0], "b", linewidth=0.8)
plt.plot(sol2.t, sol2.y[0], "r", linewidth=0.8)
plt.xlabel("t")
plt.ylabel("x");
```

md:

```markdown
A phase-space plot is created by:
```

code:

```python
ax = plt.figure().add_subplot(projection="3d")
ax.plot(sol1.y[0], sol1.y[1], sol1.y[2], "b", linewidth=0.5)
ax.plot(sol2.y[0], sol2.y[1], sol2.y[2], "r", linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z");
```

- [ ] **Step 5: Append the "Manipulating solutions" cells**

md:

```markdown
## Manipulating solutions from solve_ivp

Often one would like to manipulate the data returned by `solve_ivp`. The
result object contains the sample times in `sol.t` and the solution in
`sol.y`, one row per variable. `t_eval` controls exactly when the solution
is sampled:
```

code:

```python
sol = solve_ivp(lorenz, [0, 25], [2, 5, 5],
                t_eval=np.arange(0, 25, 0.01), max_step=0.01)
T = sol.t
X = sol.y[0]
Y = sol.y[1]
Z = sol.y[2]
T.shape, X.shape
```

md:

```markdown
(With the option `dense_output=True`, `solve_ivp` instead returns a
continuous interpolant `sol.sol(t)` that can be evaluated at any time.)

Make a 3D plot of the Lorenz attractor:
```

code:

```python
ax = plt.figure().add_subplot(projection="3d")
ax.plot(X, Y, Z, linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z");
```

- [ ] **Step 6: Execute the notebook to verify**

Run: `jupyter execute python/app_cookbook.ipynb`
Expected: exits 0, no cell errors. (This run is noticeably longer — the Lorenz integrations dominate; well under the 300 s build timeout.)

- [ ] **Step 7: Commit**

```bash
git add python/app_cookbook.ipynb
git commit -m "Cookbook: ODE recipes in one, two and three dimensions"
```

---

### Task 6: Notebook fractal recipes

**Files:**
- Modify: `python/app_cookbook.ipynb` (append cells)

**Interfaces:**
- Consumes: imports from Task 2.
- Produces: arrays `X`, `Y` (the chaos-game points) that the box-dimension section reuses within this task.

- [ ] **Step 1: Append the "Fractals" cells**

md:

```markdown
## Fractals

First we have to generate a fractal object. We will do this with a
discrete mapping (a *chaos game*) whose attractor is the Sierpinski
gasket, the triangular fractal of dimension $\log 3/\log 2$ met in the
fractals chapter. A seeded random generator makes the run reproducible.
```

code:

```python
rng = np.random.default_rng(seed=1)
N = 10000

X = np.zeros(N + 1)
Y = np.zeros(N + 1)
X[0], Y[0] = 1, 0
for n in range(N):
    dice = rng.integers(3)         # random integer from [0, 1, 2]
    # depending on the dice, jump to a new point
    if dice == 0:
        X[n + 1] = 0.5 * X[n]
        Y[n + 1] = 0.5 * Y[n]
    elif dice == 1:
        X[n + 1] = 0.5 * X[n] + 0.25
        Y[n + 1] = 0.5 * Y[n] + 0.5
    else:
        X[n + 1] = 0.5 * X[n] + 0.5
        Y[n + 1] = 0.5 * Y[n]

plt.plot(X[1:], Y[1:], ",", color="blue")
plt.gca().set_aspect("equal")
plt.xlabel("x")
plt.ylabel("y");
```

- [ ] **Step 2: Append the "Calculation box-dimension" cells**

md:

```markdown
## Calculation box-dimension

Cover the object with square boxes of size $\ell$ and count how many boxes
contain at least one point; repeating this for a range of box sizes
$\ell_p = \ell_{\min} b^p$ gives the box dimension as (minus) the slope of
$\log(\text{count})$ against $\log(\ell)$.

Determine the extrema of the data, the largest and smallest box size, and
the growth factor $b$:
```

code:

```python
xmin, xmax = X.min(), X.max()
ymin, ymax = Y.min(), Y.max()

lmax = max(xmax - xmin, ymax - ymin)   # maximum box size
lmin = lmax / 100                      # minimum box size
pmax = 20                              # number of box sizes
b = np.exp(np.log(lmax / lmin) / pmax) # so that l[pmax] = lmax
```

md:

```markdown
Loop over all resolutions; at each resolution, mark which grid boxes are
occupied and count them:
```

code:

```python
boxsize = np.zeros(pmax + 1)
boxcount = np.zeros(pmax + 1)
print("p, gridsize, boxsize")
for p in range(pmax, -1, -1):
    boxsize[p] = lmin * b**p
    gridsize = int(lmax / boxsize[p]) + 1
    print(p, gridsize, boxsize[p])

    # construct the grid with all boxes initially unoccupied
    grid = np.zeros((gridsize, gridsize))

    # mark which boxes are occupied
    for n in range(1, N + 1):
        i = int((X[n] - xmin) / boxsize[p])
        j = int((Y[n] - ymin) / boxsize[p])
        grid[i, j] = 1

    # count the number of occupied boxes
    boxcount[p] = grid.sum()
```

md:

```markdown
Plot the results in log-log fashion:
```

code:

```python
plt.plot(np.log(boxsize), np.log(boxcount), "o-")
plt.xlabel("log(boxsize)")
plt.ylabel("log(boxcount)");
```

md:

```markdown
Calculate the box dimension by fitting a straight line with `np.polyfit`;
the box dimension is minus the slope.
```

code:

```python
slope, intercept = np.polyfit(np.log(boxsize), np.log(boxcount), 1)
slope, intercept
```

code:

```python
ls = np.linspace(np.log(lmin / 2), np.log(lmax * 2), 50)
plt.plot(ls, intercept + slope * ls, "r", label="fit")
plt.plot(np.log(boxsize), np.log(boxcount), "bo", label="data")
plt.xlabel("log(boxsize)")
plt.ylabel("log(boxcount)")
plt.legend();
```

md:

```markdown
The fitted slope is close to $-\log 3/\log 2 \approx -1.585$: the box
dimension of the Sierpinski gasket.
```

- [ ] **Step 3: Execute the notebook and check the slope**

Run: `jupyter execute python/app_cookbook.ipynb`
Expected: exits 0. Then run the box-count check standalone:

```bash
jupyter nbconvert --to notebook --execute python/app_cookbook.ipynb --output executed.ipynb --output-dir "$TMPDIR"
python - <<'EOF'
import json, os, re
nb = json.load(open(os.path.join(os.environ["TMPDIR"], "executed.ipynb")))
text = json.dumps(nb)
m = re.search(r"\(-1\.5[0-9]+", text)
print("slope found:", m.group(0) if m else "NOT FOUND")
EOF
```

Expected: `slope found: (-1.5...` — i.e. the fitted slope lies between −1.5 and −1.7. (If `$TMPDIR` is unset, substitute any scratch directory.)

- [ ] **Step 4: Commit**

```bash
git add python/app_cookbook.ipynb
git commit -m "Cookbook: chaos-game Sierpinski gasket and box-dimension calculation"
```

---

### Task 7: Full build, PDF, and coverage cross-check

**Files:**
- Modify: none expected (fixes only if verification fails)
- Test: `build/python/html/`, `build/python/latex/cookbook.pdf`

**Interfaces:**
- Consumes: the complete notebook and conf.py from Tasks 1–6.
- Produces: the verified deliverables (HTML site + cookbook.pdf).

- [ ] **Step 1: Full HTML build**

Run: `make python`
Expected: exits 0. The notebook executes (first build) or comes from cache. No ERRORs; the only acceptable warning is the unresolved `cookbook.pdf` button link (it resolves once the PDF is deployed alongside the site, as for the other edition).

- [ ] **Step 2: Visual sanity-check of the HTML**

Open `build/python/html/app_cookbook.html` and confirm, per the spec's verification section:
- cobweb plot shows map, diagonal and red cobweb path;
- bifurcation diagram shows the period-doubling cascade;
- Lorenz time series shows the red/blue trajectories separating after t ≈ 25;
- Sierpinski gasket is clearly triangular/self-similar;
- box-count fit reports a slope ≈ −1.585.

- [ ] **Step 3: Build the PDF**

```bash
sphinx-build -b latex python build/python/latex
cd build/python/latex && latexmk -pdf cookbook.tex && cd ../../..
```

Expected: `build/python/latex/cookbook.pdf` exists; headings flow as sections (howto class); all figures render.

- [ ] **Step 4: Coverage cross-check against the Maple cookbook**

Confirm every section of `maple/app_cookbook.md` is accounted for:

| Maple section | Status |
|---|---|
| Settings & tips | replaced: "Getting started" (Jupyter) |
| Useful keys | replaced: Jupyter keys |
| Help | converted |
| Comments | converted |
| General | converted (imports, `=` vs `==`, `;` suppression) |
| Floating point numbers | converted (floats + sympy `N`) |
| Functions vs expressions | converted (def/lambdify/diff/subs) |
| Plotting | converted |
| Lists, sets, sequences, Arrays, Matrices and Vectors | converted (lists/sets/comprehensions/arrays/linalg) |
| For-loops | converted |
| Plotting data points | converted |
| Plotting more than one function | converted |
| Implicitplot | converted (contour level 0) |
| Iterative maps | converted |
| Generate cobweb | converted |
| Return plot | converted |
| Bifurcation diagram | converted |
| ODEs one variable | converted (solve_ivp) |
| Bifurcation diagram continuous system | converted |
| ODEs two dimensions (+ phase portrait) | converted (sympy fixed points/Jacobian/eigenvalues, streamplot) |
| ODEs three dimensions: chaos | converted (Lorenz) |
| Manipulating solutions from dsolve | converted (solve_ivp result object) |
| Fractals | converted (seeded chaos game) |
| Calculation box-dimension | converted (loop + polyfit) |

Deliberately not carried over (Maple-specific, no Python counterpart needed): Worksheet/Document mode, `restart`/`with(...)` package loading (covered by imports), `Digits` (covered by sympy `N`), sequences vs lists vs sets distinction (Python lists/sets cover it), `add`/`mul` oddity, `unapply`/`D` (covered by `lambdify`), obsolete `array`/`matrix`/`vector` types warning, `op`/`nops` (covered by `len`), Maple's `%` last-result operator.

If any row fails this check, add the missing cells (following the patterns of Tasks 2–6) before proceeding.

- [ ] **Step 5: Commit any fixes and finish**

```bash
git status
git add -A python/
git commit -m "Cookbook: final build fixes after verification"   # only if there are changes
```

---

## Self-review notes

- **Spec coverage:** layout (Task 1), notebook content mapping (Tasks 2–6 cover every row of the spec's table), execute-with-cache (Task 1 conf.py), PDF deliverable (Task 1 latex config + Task 7 build), verification incl. slope check and coverage cross-check (Tasks 6–7). Out-of-scope items (chapters, CI) appear in no task.
- **Placeholder scan:** every cell's full content is present; commands have expected outcomes.
- **Consistency:** all code cells assume only the Task 2 import cell (`np`, `plt`, `sym`, `solve_ivp`); each recipe redefines its own `f`, `X`, `r` locally, matching the "self-contained recipes" constraint.
