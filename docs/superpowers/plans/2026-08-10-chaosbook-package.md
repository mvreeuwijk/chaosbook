# chaosbook Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `chaosbook` package (sub-project ① of the vision spec `docs/superpowers/specs/2026-08-10-python-edition-vision-design.md`): the book's computational vocabulary as a pip-installable pure-python package, wired into the cookbook via "In the package" admonitions and a closing package section.

**Architecture:** src-layout package at the repo root (`pyproject.toml` + `src/chaosbook/`), one focused module per concern (maps, iterate, cobweb, bifurcation, flows, fractal), everything re-exported flat from `__init__` so the book can write `cb.cobweb(...)`. Implementations are copied from the cookbook's recipes — the package IS the cookbook code, packaged. pytest suite asserts qualitative/aggregate properties (fixed points, periods, dimension slopes), never exact chaotic trajectories.

**Tech Stack:** Python (≥3.9), numpy, matplotlib (plot helpers), setuptools src-layout, pytest.

## Global Constraints

- **APIs mirror the book's notation exactly**: parameter names `r`, `sigma`, `b`, `x0`; defaults match the cookbook recipes (logistic bifurcation: `nr=200, n=500, x0=0.57`; chaos game: `n=10000, seed=1`; box counting: `pmax=20`, `lmin = lmax/100`; Lorenz: `sigma=10, r=28, b=8/3`).
- **Dependencies**: at most numpy, scipy, matplotlib. This sub-project needs only numpy + matplotlib; scipy joins later (poincare module).
- **Clear simple code over sophisticated code**: plain loops where clearer; implementations match the cookbook cells they package (same variable names where sensible).
- **Nothing under `python/` may mention Maple.** The `maple/` tree is untouched.
- **The cookbook stays plain-code-first**: recipes unchanged; package references are *additions* (admonition cells + one closing section), never replacements.
- **Notebook hygiene** (from the cookbook plan): every cell has an `id`; no outputs stored; no mojibake (real UTF-8 em dashes); verify with `nbformat.validate` and a grep for `â€`.
- Windows/Git Bash; tooling lives in the venv `C:/Users/mvr/cbenv2` (`Scripts/python`, `Scripts/pip`, `Scripts/jupyter`, `Scripts/sphinx-build`). `make python` ≡ `sphinx-build -M html python build/python`. Build into short paths (deep nesting hits Windows MAX_PATH).
- Commit messages end with a blank line then `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: Package scaffold, maps and orbit

**Files:**
- Create: `pyproject.toml` (repo root)
- Create: `src/chaosbook/__init__.py`
- Create: `src/chaosbook/maps.py`
- Create: `src/chaosbook/iterate.py`
- Test: `tests/conftest.py`, `tests/test_maps.py`, `tests/test_iterate.py`

**Interfaces:**
- Produces: `chaosbook.logistic(x, r)` (works on scalars and numpy arrays); `chaosbook.orbit(f, x0, n, **params)` → numpy array `[x_0 … x_n]` of length `n + 1`; `__version__ = "0.1.0"`. Tasks 2–3 extend `__init__.py`; Task 4's notebook cells call these exact names via `import chaosbook as cb`.

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "chaosbook"
version = "0.1.0"
description = "Computational toolkit for the book 'From Stability to Chaos'"
authors = [
  {name = "Harmen J. Jonker"},
  {name = "Maarten van Reeuwijk"},
]
requires-python = ">=3.9"
dependencies = [
  "numpy",
  "matplotlib",
]
license = {text = "MIT"}

[tool.setuptools.packages.find]
where = ["src"]
```

- [ ] **Step 2: Create the empty package and install it editable**

Create `src/chaosbook/__init__.py` containing only:

```python
"""chaosbook - computational toolkit for 'From Stability to Chaos'.

Every function here is introduced in the book's cookbook, where the full
implementation is shown as plain code before being packaged.
"""

__version__ = "0.1.0"
```

Run: `"C:/Users/mvr/cbenv2/Scripts/pip" install -e . && "C:/Users/mvr/cbenv2/Scripts/pip" install pytest`
Expected: both exit 0; `"C:/Users/mvr/cbenv2/Scripts/python" -c "import chaosbook; print(chaosbook.__version__)"` prints `0.1.0`.

- [ ] **Step 3: Write the failing tests**

`tests/conftest.py`:

```python
import matplotlib

matplotlib.use("Agg")
```

`tests/test_maps.py`:

```python
import numpy as np

from chaosbook import logistic


def test_logistic_fixed_points():
    r = 2.5
    assert logistic(0, r) == 0
    xstar = 1 - 1 / r
    assert np.isclose(logistic(xstar, r), xstar)


def test_logistic_works_on_arrays():
    x = np.array([0.0, 0.5, 1.0])
    assert np.allclose(logistic(x, 4.0), [0.0, 1.0, 0.0])
```

`tests/test_iterate.py`:

```python
import numpy as np

from chaosbook import logistic, orbit


def test_orbit_length_and_start():
    X = orbit(logistic, 0.1, 50, r=2.5)
    assert len(X) == 51
    assert X[0] == 0.1


def test_orbit_converges_to_fixed_point():
    X = orbit(logistic, 0.1, 200, r=2.5)
    assert np.isclose(X[-1], 1 - 1 / 2.5)
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: FAIL — `ImportError: cannot import name 'logistic'`.

- [ ] **Step 5: Implement `maps.py` and `iterate.py`**

`src/chaosbook/maps.py`:

```python
"""Iterated maps: x_{n+1} = f(x_n, parameters).

Every map takes the current state as its first argument and its
parameters after it, so it can be passed directly to orbit() and the
plotting helpers.
"""


def logistic(x, r):
    """The logistic map x_{n+1} = r x (1 - x)."""
    return r * x * (1 - x)
```

`src/chaosbook/iterate.py`:

```python
"""Iterating maps into orbits."""

import numpy as np


def orbit(f, x0, n, **params):
    """Iterate the map x_{k+1} = f(x_k, **params) starting from x0.

    Returns the numpy array [x_0, x_1, ..., x_n] of length n + 1.
    """
    X = np.zeros(n + 1)
    X[0] = x0
    for k in range(n):
        X[k + 1] = f(X[k], **params)
    return X
```

Replace `src/chaosbook/__init__.py` with:

```python
"""chaosbook - computational toolkit for 'From Stability to Chaos'.

Every function here is introduced in the book's cookbook, where the full
implementation is shown as plain code before being packaged.
"""

from .maps import logistic
from .iterate import orbit

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "orbit",
]
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 4 passed.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml src/chaosbook/ tests/
git commit -m "chaosbook: package scaffold with logistic map and orbit"
```

---

### Task 2: Cobweb and bifurcation modules

**Files:**
- Create: `src/chaosbook/cobweb.py`
- Create: `src/chaosbook/bifurcation.py`
- Modify: `src/chaosbook/__init__.py`
- Test: `tests/test_cobweb.py`, `tests/test_bifurcation.py`

**Interfaces:**
- Consumes: `chaosbook.orbit(f, x0, n, **params)` and `chaosbook.logistic(x, r)` from Task 1.
- Produces: `chaosbook.cobweb(f, x0, n, xmin=0.0, xmax=1.0, ax=None, **params)` → matplotlib Axes (draws map, diagonal, cobweb path — three lines in that order); `chaosbook.bifurcation_diagram(f, rmin, rmax, nr=200, n=500, x0=0.57, ax=None)` → `(rs, xs)` numpy arrays, plotted on `ax` with pixel markers. Task 4's notebook demo cell calls `cb.cobweb(cb.logistic, x0=0.1, n=50, r=0.5)`.

- [ ] **Step 1: Write the failing tests**

`tests/test_cobweb.py`:

```python
import matplotlib.pyplot as plt

from chaosbook import cobweb, logistic


def test_cobweb_draws_three_lines_on_given_axes():
    fig, ax = plt.subplots()
    out = cobweb(logistic, 0.1, 50, ax=ax, r=0.5)
    assert out is ax
    assert len(ax.lines) == 3
    plt.close(fig)


def test_cobweb_path_starts_at_x0_on_the_x_axis():
    fig, ax = plt.subplots()
    cobweb(logistic, 0.3, 10, ax=ax, r=2.5)
    path = ax.lines[2]
    assert path.get_xdata()[0] == 0.3
    assert path.get_ydata()[0] == 0
    plt.close(fig)
```

`tests/test_bifurcation.py`:

```python
import matplotlib.pyplot as plt
import numpy as np

from chaosbook import bifurcation_diagram, logistic


def test_stable_branch_follows_fixed_point():
    fig, ax = plt.subplots()
    rs, xs = bifurcation_diagram(logistic, 2.0, 2.8, nr=8, n=400, ax=ax)
    for r in np.unique(rs):
        branch = xs[rs == r]
        assert np.allclose(branch, 1 - 1 / r, atol=1e-3)
    plt.close(fig)


def test_period_two_beyond_first_doubling():
    fig, ax = plt.subplots()
    rs, xs = bifurcation_diagram(logistic, 3.2, 3.2, nr=0, n=1000, ax=ax)
    values = np.unique(np.round(xs, 6))
    assert len(values) == 2
    plt.close(fig)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/test_cobweb.py tests/test_bifurcation.py -v`
Expected: FAIL — `ImportError: cannot import name 'cobweb'`.

- [ ] **Step 3: Implement `cobweb.py` and `bifurcation.py`**

`src/chaosbook/cobweb.py`:

```python
"""Cobweb diagrams for one-dimensional maps."""

import matplotlib.pyplot as plt
import numpy as np

from .iterate import orbit


def cobweb(f, x0, n, xmin=0.0, xmax=1.0, ax=None, **params):
    """Draw a cobweb diagram of x_{k+1} = f(x_k, **params) from x0.

    Plots the map, the diagonal and the cobweb path on ax (the current
    axes if not given) and returns the axes.
    """
    if ax is None:
        ax = plt.gca()
    X = orbit(f, x0, n, **params)
    px = [X[0]]
    py = [0]
    for k in range(n):
        px += [X[k], X[k]]
        py += [X[k], X[k + 1]]
    xs = np.linspace(xmin, xmax, 200)
    ax.plot(xs, f(xs, **params), "k")
    ax.plot(xs, xs, "b")
    ax.plot(px, py, "r")
    ax.set_xlabel("x[n]")
    ax.set_ylabel("x[n+1]")
    return ax
```

`src/chaosbook/bifurcation.py`:

```python
"""Bifurcation diagrams for one-dimensional maps."""

import matplotlib.pyplot as plt
import numpy as np

from .iterate import orbit


def bifurcation_diagram(f, rmin, rmax, nr=200, n=500, x0=0.57, ax=None):
    """Compute and plot the bifurcation diagram of x_{k+1} = f(x_k, r).

    For nr + 1 parameter values r between rmin and rmax the map is
    iterated n times from x0, and the second half of every orbit (the
    part that has converged onto the attractor) is plotted against r.
    Returns the arrays (rs, xs) that make up the diagram.
    """
    nmin = n // 2
    rs = []
    xs = []
    for i in range(nr + 1):
        if nr == 0:
            r = rmin
        else:
            r = rmin + (rmax - rmin) * i / nr
        X = orbit(f, x0, n, r=r)
        for x in X[nmin:]:
            rs.append(r)
            xs.append(x)
    rs = np.array(rs)
    xs = np.array(xs)
    if ax is None:
        ax = plt.gca()
    ax.plot(rs, xs, ",")
    ax.set_xlabel("r")
    ax.set_ylabel("x(r)")
    return rs, xs
```

In `src/chaosbook/__init__.py`, extend the imports and `__all__`:

```python
from .maps import logistic
from .iterate import orbit
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "orbit",
    "cobweb",
    "bifurcation_diagram",
]
```

- [ ] **Step 4: Run the full suite to verify it passes**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add src/chaosbook/ tests/
git commit -m "chaosbook: cobweb and bifurcation-diagram helpers"
```

---

### Task 3: Flows and fractal modules

**Files:**
- Create: `src/chaosbook/flows.py`
- Create: `src/chaosbook/fractal.py`
- Modify: `src/chaosbook/__init__.py`
- Test: `tests/test_flows.py`, `tests/test_fractal.py`

**Interfaces:**
- Consumes: nothing beyond numpy.
- Produces: `chaosbook.lorenz(t, xyz, sigma=10.0, r=28.0, b=8.0/3.0)` → list of three derivatives (solve_ivp-compatible signature); `chaosbook.chaos_game(n=10000, seed=1)` → `(X, Y)` numpy arrays of length `n + 1`; `chaosbook.box_dimension(X, Y, pmax=20)` → `(dimension, boxsize, boxcount)` where `dimension` is minus the log-log slope. Task 4's admonition cells cite these exact names.

- [ ] **Step 1: Write the failing tests**

`tests/test_flows.py`:

```python
import numpy as np

from chaosbook import lorenz


def test_origin_is_a_fixed_point():
    assert lorenz(0, [0, 0, 0]) == [0, 0, 0]


def test_nontrivial_fixed_point():
    r, b = 28.0, 8.0 / 3.0
    q = np.sqrt(b * (r - 1))
    assert np.allclose(lorenz(0, [q, q, r - 1]), [0, 0, 0], atol=1e-12)
```

`tests/test_fractal.py`:

```python
import numpy as np

from chaosbook import box_dimension, chaos_game


def test_chaos_game_is_reproducible_and_bounded():
    X1, Y1 = chaos_game(n=2000, seed=1)
    X2, Y2 = chaos_game(n=2000, seed=1)
    assert np.array_equal(X1, X2) and np.array_equal(Y1, Y2)
    assert len(X1) == 2001
    assert X1.min() >= 0 and X1.max() <= 1
    assert Y1.min() >= 0 and Y1.max() <= 1


def test_gasket_dimension_is_log3_over_log2():
    X, Y = chaos_game(n=10000, seed=1)
    dim, boxsize, boxcount = box_dimension(X, Y)
    assert abs(dim - np.log(3) / np.log(2)) < 0.1
    assert len(boxsize) == 21 and len(boxcount) == 21


def test_straight_line_has_dimension_one():
    X = np.linspace(0, 1, 5000)
    Y = np.zeros(5000)
    dim, _, _ = box_dimension(X, Y)
    assert abs(dim - 1) < 0.1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/test_flows.py tests/test_fractal.py -v`
Expected: FAIL — `ImportError: cannot import name 'lorenz'`.

- [ ] **Step 3: Implement `flows.py` and `fractal.py`**

`src/chaosbook/flows.py`:

```python
"""Right-hand sides of the book's flows, in solve_ivp form f(t, state)."""


def lorenz(t, xyz, sigma=10.0, r=28.0, b=8.0 / 3.0):
    """The Lorenz equations."""
    x, y, z = xyz
    return [sigma * (y - x), -x * z + r * x - y, x * y - b * z]
```

`src/chaosbook/fractal.py`:

```python
"""Chaos-game fractals and box-counting dimension."""

import numpy as np


def chaos_game(n=10000, seed=1):
    """Play the chaos game whose attractor is the Sierpinski gasket.

    Returns the point arrays (X, Y), each of length n + 1.
    """
    rng = np.random.default_rng(seed=seed)
    X = np.zeros(n + 1)
    Y = np.zeros(n + 1)
    X[0], Y[0] = 1, 0
    for k in range(n):
        dice = rng.integers(3)
        if dice == 0:
            X[k + 1] = 0.5 * X[k]
            Y[k + 1] = 0.5 * Y[k]
        elif dice == 1:
            X[k + 1] = 0.5 * X[k] + 0.25
            Y[k + 1] = 0.5 * Y[k] + 0.5
        else:
            X[k + 1] = 0.5 * X[k] + 0.5
            Y[k + 1] = 0.5 * Y[k]
    return X, Y


def box_dimension(X, Y, pmax=20):
    """Estimate the box-counting dimension of the point set (X, Y).

    Covers the points with square boxes whose size shrinks from the
    extent of the data down to 1/100th of it in pmax logarithmic steps,
    counts the occupied boxes at every size, and fits a straight line to
    log(count) against log(size). Returns (dimension, boxsize, boxcount),
    where dimension is minus the fitted slope.
    """
    xmin, ymin = X.min(), Y.min()
    lmax = max(X.max() - xmin, Y.max() - ymin)
    lmin = lmax / 100
    b = np.exp(np.log(lmax / lmin) / pmax)

    boxsize = np.zeros(pmax + 1)
    boxcount = np.zeros(pmax + 1)
    for p in range(pmax + 1):
        boxsize[p] = lmin * b**p
        gridsize = int(lmax / boxsize[p]) + 1
        grid = np.zeros((gridsize, gridsize))
        for x, y in zip(X, Y):
            i = int((x - xmin) / boxsize[p])
            j = int((y - ymin) / boxsize[p])
            grid[i, j] = 1
        boxcount[p] = grid.sum()
    slope, _ = np.polyfit(np.log(boxsize), np.log(boxcount), 1)
    return -slope, boxsize, boxcount
```

Replace the import block and `__all__` in `src/chaosbook/__init__.py` (final form):

```python
from .maps import logistic
from .iterate import orbit
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram
from .flows import lorenz
from .fractal import chaos_game, box_dimension

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "orbit",
    "cobweb",
    "bifurcation_diagram",
    "lorenz",
    "chaos_game",
    "box_dimension",
]
```

- [ ] **Step 4: Run the full suite to verify it passes**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 13 passed.

- [ ] **Step 5: Commit**

```bash
git add src/chaosbook/ tests/
git commit -m "chaosbook: Lorenz flow, chaos game and box dimension"
```

---

### Task 4: Cookbook integration

**Files:**
- Modify: `python/app_cookbook.ipynb` (insert 6 admonition cells; append 1 closing section: 2 markdown + 1 code cell)
- Modify: `requirements.txt` (append `pytest` and `-e .`)

**Interfaces:**
- Consumes: the full `chaosbook` API from Tasks 1–3 (`cb.logistic`, `cb.orbit`, `cb.cobweb`, `cb.bifurcation_diagram`, `cb.lorenz`, `cb.chaos_game`, `cb.box_dimension`), installed editable in the build venv.
- Produces: the cookbook pattern the chapters will follow — recipes link to `{ref}` target `cookbook:package`.

All inserted cells are **markdown** cells except the one demo **code** cell. Insert each admonition cell *directly after* the last cell of the recipe it refers to. Use NotebookEdit; keep ids on every cell; store no outputs; write real UTF-8 (em dashes; grep for `â€` must find nothing afterwards).

- [ ] **Step 1: Insert the six "In the package" admonition cells**

After the last cell of **Iterative maps** (the `"-o"` line+points plot cell):

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `cb.orbit(cb.logistic, x0=0.1, n=50, r=0.5)` returns exactly this series — the implementation is the loop above. See {ref}`cookbook:package`.
:::
```

After the **Generate cobweb** code cell:

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `cb.cobweb(cb.logistic, x0=0.1, n=50, r=0.5)` draws this diagram in one call. See {ref}`cookbook:package`.
:::
```

After the **Bifurcation diagram** code cell:

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `cb.bifurcation_diagram(cb.logistic, rmin=0.1, rmax=4)` computes and plots this diagram, and returns the `(rs, xs)` data. See {ref}`cookbook:package`.
:::
```

After the last cell of **Non-linear differential equations with three dimensions: chaos** (the 3D phase-space plot cell):

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `cb.lorenz` is this right-hand side with the parameters as keyword arguments — `solve_ivp(cb.lorenz, [0, 40], [2, 5, 5], max_step=0.01)`. See {ref}`cookbook:package`.
:::
```

After the **Fractals** code cell:

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `X, Y = cb.chaos_game(n=10000, seed=1)` produces exactly these points. See {ref}`cookbook:package`.
:::
```

After the final markdown cell of **Calculation box-dimension** (the "fitted slope is close to −log 3/log 2" cell):

```markdown
:::{admonition} In the package
:class: tip
Ready-made: `dim, boxsize, boxcount = cb.box_dimension(X, Y)` runs this whole analysis and returns the dimension (minus the fitted slope) with the underlying data. See {ref}`cookbook:package`.
:::
```

- [ ] **Step 2: Append the closing package section (three cells)**

md:

```markdown
(cookbook:package)=
## The chaosbook package

Every recipe in this cookbook is plain code that you can copy, adapt and
build on. The ones you will reach for again and again are also packaged:
the `chaosbook` package contains them as ready-made functions whose
implementations are exactly the code shown in this cookbook. Install it
from the book's repository with

    pip install git+https://github.com/mvreeuwijk/chaosbook

and import it as `import chaosbook as cb`. The recipes and their packaged
counterparts:

| Recipe | In the package |
|---|---|
| Iterative maps | `cb.orbit(f, x0, n, **params)` |
| Generate cobweb | `cb.cobweb(f, x0, n, **params)` |
| Bifurcation diagram | `cb.bifurcation_diagram(f, rmin, rmax)` |
| ODEs in three dimensions | `cb.lorenz(t, xyz)` |
| Fractals | `cb.chaos_game(n, seed)` |
| Calculation box-dimension | `cb.box_dimension(X, Y)` |

The map argument `f` is any function of the form `f(x, **params)`, such as
`cb.logistic(x, r)`. As a demonstration, the cobweb recipe in one line:
```

code:

```python
import chaosbook as cb

cb.cobweb(cb.logistic, x0=0.1, n=50, r=0.5);
```

md:

```markdown
The rest of the book uses these functions freely; whenever you want to see
inside one, come back to the recipe in this cookbook that builds it.
```

- [ ] **Step 3: Update `requirements.txt`**

Append two lines:

```text
pytest
-e .
```

- [ ] **Step 4: Execute and validate the notebook**

Run: `"C:/Users/mvr/cbenv2/Scripts/jupyter" execute python/app_cookbook.ipynb`
Expected: exit 0 (the demo cell imports the editable-installed package).

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -c "import nbformat; nbformat.validate(nbformat.read('python/app_cookbook.ipynb', as_version=4)); print('ok')"` and `grep -c 'â€' python/app_cookbook.ipynb || true`
Expected: `ok`; grep finds 0 occurrences.

- [ ] **Step 5: Rebuild the HTML to confirm the cross-references resolve**

Run: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -M html python build/python`
Expected: exit 0; no new warnings about `cookbook:package` (the pre-existing `cookbook.pdf` button warning remains acceptable).

- [ ] **Step 6: Commit**

```bash
git add python/app_cookbook.ipynb requirements.txt
git commit -m "Cookbook: introduce the chaosbook package after the plain-code recipes"
```

---

### Task 5: Full verification

**Files:**
- Modify: none expected (fixes only if verification fails)

**Interfaces:**
- Consumes: everything from Tasks 1–4.

- [ ] **Step 1: Run the full test suite**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 13 passed.

- [ ] **Step 2: Full HTML build from a clean slate**

Run: `rm -rf build/python && "C:/Users/mvr/cbenv2/Scripts/sphinx-build" -M html python build/python`
Expected: exit 0; the notebook re-executes (cache is gone) including the `import chaosbook` demo cell; `build/python/html/app_cookbook.html` contains the "The chaosbook package" section, six "In the package" admonitions, and one more figure than before (the demo cobweb).

- [ ] **Step 3: PDF build**

Run: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -b latex python build/python/latex`, then in `build/python/latex`: `latexmk -pdf cookbook.tex` (MiKTeX; on PATH or at `C:/Program Files/MiKTeX/miktex/bin/x64`).
Expected: `cookbook.pdf` produced; the closing section and admonitions render.

- [ ] **Step 4: Fresh-environment smoke test of the package build**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pip install --dry-run .`
Expected: exit 0 (the sdist/wheel metadata resolves standalone — guards the pure-python-wheel requirement for the later JupyterLite sub-project).

- [ ] **Step 5: Commit any fixes**

```bash
git status
git add -A src/ tests/ python/ requirements.txt
git commit -m "chaosbook: final verification fixes"   # only if there are changes
```

---

## Self-review notes

- **Spec coverage** (vision spec §2–3 / sub-project ①): package layout (Tasks 1–3 — `poincare.py` deliberately deferred until a chapter needs it, per the spec's YAGNI rule; scipy joins with it), notation-matching defaults (Global Constraints), qualitative tests (each test asserts fixed points, periods, bounds or slopes — never exact chaotic values), pure-python wheel viability (Task 5 Step 4), cookbook plain-code-first pattern with admonitions + closing section (Task 4), chapters-reference-cookbook pattern documented by the closing cell.
- **Placeholder scan:** all code and cell contents are complete; all commands carry expected outcomes.
- **Type consistency:** `cb.orbit(f, x0, n, **params)` signature is identical in Task 1 (definition), Task 2 (cobweb/bifurcation consume it), and Task 4 (admonition text); `box_dimension` returns `(dimension, boxsize, boxcount)` in Task 3 and is cited that way in Task 4.
