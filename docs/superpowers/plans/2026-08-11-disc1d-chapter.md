# disc1d Chapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert chapter 2 ("Chaos in Iterative Maps") to the Python edition per `docs/superpowers/specs/2026-08-11-pilot-chapters-design.md`, completing the pilot: package additions (sine/tent/shift maps, Lyapunov tools, bifurcation transient control), creators scripts regenerating all 23 figures, three interactive companions (logistic explorer, bifurcation deep zoom, bifurcation+Λ(r) linked view), and the converted chapter + exercises.

**Architecture:** Same pipeline as the phenomenon chapter: package additions first (TDD), then `creators/python/disc1d/` scripts emitting committed static PNGs (Maple basenames) plus plotly HTML assets (self-hosted `../../plotly.min.js`), then the chapter as a verbatim copy of `maple/disc1d.md` with enumerated edits (Python admonitions, code links on every script-generated figure, `{raw} html` iframes), then exercises/index/manifest/publish. The chapter conversion is split into two tasks (front half / back half) because of its size (1372 lines, 15 code blocks).

**Tech Stack:** numpy, scipy (brentq), sympy (fixed-point algebra), mpmath (extended-precision shift/tent iteration — already installed as a sympy dependency), matplotlib, plotly.

## Global Constraints

- **Nothing under `python/` may mention Maple.** Prose and math copied verbatim from `maple/disc1d.md` except the enumerated edits.
- **Figure basenames identical to the Maple edition** under `python/_static/disc1d/`; static twins must visually match `maple/_static/disc1d/*.png` (same systems, same qualitative content).
- **Model parameters are fixed** (map definitions, r values, x0=0.57 for bifurcation diagrams, N=1000 with 0.8 transient discard, r∞ = 3.56994537 logistic / 0.86557928 sine, chapter-quoted numeric results). **Presentation parameters** (number of plotted points, view ranges, marker sizes, grid resolutions, figure sizes) may be adjusted to match the Maple originals visually — record every adjustment in the task report.
- **Floating-point honesty:** the shift and tent maps shift one binary digit per iteration, so IEEE-double iteration collapses to exactly 0 after ~52 steps. Their 400-step figures use mpmath extended precision (`mp.dps = 150`), and the chapter gains one explanatory sentence (edit F7) — this is the chapter's own round-off lesson, made visible.
- **Code links on EVERY script-generated figure** (`:::{only} html` paragraph directly after the figure/subfigure block — the pattern recorded in the pilot spec's implementation notes). Interactive iframes via `{raw} html` (emits nothing in LaTeX).
- Creators scripts are reader-facing: package-based, short, header comment listing outputs.
- Package tools stay generic over user-supplied `f`; parameter-name-`r` assumptions documented in docstrings.
- Windows/Git Bash; tooling `C:/Users/mvr/cbenv2/Scripts/{python,pip,sphinx-build}`. No `rm -rf`.
- Commits end with a blank line then `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: Package additions — maps, Lyapunov tools, bifurcation transient control

**Files:**
- Modify: `src/chaosbook/maps.py`, `src/chaosbook/bifurcation.py`, `src/chaosbook/__init__.py`
- Create: `src/chaosbook/lyapunov.py`
- Test: `tests/test_maps.py`, `tests/test_bifurcation.py` (extend), `tests/test_lyapunov.py` (new)

**Interfaces:**
- Produces: `chaosbook.sine(x, r)` (= r·sin(πx)), `chaosbook.tent(x)` (= 1 − 2|x − 1/2|; the book's tent map has no parameter, overriding the spec's sketch), `chaosbook.shift(x)` (= 2x mod 1); `chaosbook.lyapunov(f, dfdx, x0, n=1000, nskip=100, **params)` → float; `chaosbook.lyapunov_sweep(f, dfdx, rmin, rmax, nr=500, n=1000, x0=0.57, nskip=100)` → `(rs, lams)`; `bifurcation_diagram(..., discard=0.5, ...)` new keyword (fraction of each orbit dropped as transient). All later tasks use these exact names.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_maps.py`:

```python
from chaosbook import shift, sine, tent


def test_sine_tent_shift_definitions():
    assert np.isclose(sine(0.5, 0.5), 0.5)
    assert tent(0.25) == 0.5
    assert tent(0.5) == 1.0
    assert np.isclose(shift(0.75), 0.5)
    assert np.isclose(shift(0.3), 0.6)
```

Append to `tests/test_bifurcation.py`:

```python
def test_bifurcation_discard_fraction():
    fig, ax = plt.subplots()
    rs, xs = bifurcation_diagram(logistic, 3.2, 3.2, nr=0, n=1000,
                                 discard=0.8, ax=ax)
    assert len(xs) == 1000 - 800 + 1
    plt.close(fig)
```

Create `tests/test_lyapunov.py`:

```python
import numpy as np

from chaosbook import logistic, lyapunov, lyapunov_sweep


def dlogistic(x, r):
    return r * (1 - 2 * x)


def test_logistic_r4_has_lyapunov_log2():
    lam = lyapunov(logistic, dlogistic, 0.3, n=5000, r=4.0)
    assert abs(lam - np.log(2)) < 0.05


def test_stable_fixed_point_has_negative_lyapunov():
    # at r=2.5 the orbit sits on x*=1-1/r where sigma = 2-r = -0.5
    lam = lyapunov(logistic, dlogistic, 0.3, n=2000, r=2.5)
    assert np.isclose(lam, np.log(0.5), atol=1e-6)


def test_sweep_is_negative_before_first_bifurcation():
    rs, lams = lyapunov_sweep(logistic, dlogistic, 2.5, 3.5, nr=100)
    assert lams[rs < 2.95].max() < 0
```

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: FAIL — `ImportError: cannot import name 'sine'` (and friends).

- [ ] **Step 2: Implement**

Append to `src/chaosbook/maps.py` (and add `import numpy as np` at the top of the module):

```python
def sine(x, r):
    """The sine map x_{n+1} = r sin(pi x)."""
    return r * np.sin(np.pi * x)


def tent(x):
    """The tent map x_{n+1} = 1 - 2 |x - 1/2|."""
    return 1 - 2 * np.abs(x - 0.5)


def shift(x):
    """The shift map x_{n+1} = 2 x mod 1."""
    return (2 * x) % 1.0
```

Create `src/chaosbook/lyapunov.py`:

```python
"""Lyapunov exponents of one-dimensional maps."""

import numpy as np

from .iterate import orbit


def lyapunov(f, dfdx, x0, n=1000, nskip=100, **params):
    """Estimate the Lyapunov exponent of x_{k+1} = f(x_k, **params).

    Iterates the map from x0, discards the first nskip points as
    transient, and returns the mean of log|f'(x_k)| over the next n
    points. dfdx is the derivative of the map, with the same signature
    as f.
    """
    X = orbit(f, x0, nskip + n, **params)
    with np.errstate(divide="ignore"):
        return np.mean(np.log(np.abs(dfdx(X[nskip:-1], **params))))


def lyapunov_sweep(f, dfdx, rmin, rmax, nr=500, n=1000, x0=0.57, nskip=100):
    """The Lyapunov exponent as a function of the parameter r.

    Assumes the map's varying parameter is named r, i.e. f(x, r).
    Returns the arrays (rs, lams).
    """
    rs = np.linspace(rmin, rmax, nr + 1)
    lams = np.array([lyapunov(f, dfdx, x0, n=n, nskip=nskip, r=r)
                     for r in rs])
    return rs, lams
```

In `src/chaosbook/bifurcation.py`, change the signature to
`def bifurcation_diagram(f, rmin, rmax, nr=200, n=500, x0=0.57, discard=0.5, ax=None):`
and replace `nmin = n // 2` with `nmin = int(discard * n)`; in the docstring replace "the second half of every orbit" with "the last (1 - discard) fraction of every orbit".

Update `src/chaosbook/__init__.py` (final form of the import block and `__all__`):

```python
from .maps import logistic, sine, tent, shift
from .iterate import orbit
from .cobweb import cobweb
from .bifurcation import bifurcation_diagram
from .lyapunov import lyapunov, lyapunov_sweep
from .flows import lorenz, threebody, corotating
from .fractal import chaos_game, box_dimension

__version__ = "0.1.0"

__all__ = [
    "logistic",
    "sine",
    "tent",
    "shift",
    "orbit",
    "cobweb",
    "bifurcation_diagram",
    "lyapunov",
    "lyapunov_sweep",
    "lorenz",
    "threebody",
    "corotating",
    "chaos_game",
    "box_dimension",
]
```

- [ ] **Step 3: Run the full suite**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 20 passed.

- [ ] **Step 4: Commit**

```bash
git add src/chaosbook/ tests/
git commit -m "chaosbook: sine/tent/shift maps, Lyapunov tools, bifurcation transient control"
```

---

### Task 2: Creators — series, cobwebs, return plots, unknown mappings + logistic explorer

**Files:**
- Create: `creators/python/disc1d/fig_series_cobweb_return.py`
- Create (generated, committed): `python/_static/disc1d/disc1d_logist_series_r{1_5,3_2,3_5,3_9}.png`, `disc1d_logist_cobweb_r{2_7,3_2,3_9}.png`, `disc1d_logist_return_r{1_5,3_2,3_5,3_9}.png`, `disc1d_unknownmapping_{series,return}_{henon,noise,sin3map}.png`, `python/_static/disc1d/interactive/logistic_explorer.html`

**Interfaces:**
- Consumes: `cb.logistic`, `cb.orbit`, `cb.cobweb`.
- Produces: 17 asset files with the exact names above; the chapter (Tasks 6–7) references them.

- [ ] **Step 1: Write `creators/python/disc1d/fig_series_cobweb_return.py`**

```python
"""Series, cobweb and return-plot figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_series_r{1_5,3_2,3_5,3_9}.png
  disc1d_logist_cobweb_r{2_7,3_2,3_9}.png
  disc1d_logist_return_r{1_5,3_2,3_5,3_9}.png
  disc1d_unknownmapping_{series,return}_{henon,noise,sin3map}.png
  interactive/logistic_explorer.html
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def tag(r):
    return str(r).replace(".", "_")


# -- logistic time series ----------------------------------------------------
for r in [1.5, 3.2, 3.5, 3.9]:
    X = cb.orbit(cb.logistic, x0=0.1, n=30, r=r)
    plt.figure(figsize=(4.2, 3))
    plt.plot(range(len(X)), X, "o", markersize=4)
    plt.xlabel("n")
    plt.ylabel("xn")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_series_r{tag(r)}.png", dpi=150)
    plt.close()

# -- cobwebs -----------------------------------------------------------------
for r in [2.7, 3.2, 3.9]:
    fig, ax = plt.subplots(figsize=(4, 4))
    cb.cobweb(cb.logistic, x0=0.1, n=30, ax=ax, r=r)
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_cobweb_r{tag(r)}.png", dpi=150)
    plt.close()

# -- return plots (gray map line + points, transient dropped) ---------------
for r in [1.5, 3.2, 3.5, 3.9]:
    X = cb.orbit(cb.logistic, x0=0.1, n=200, r=r)
    xs = np.linspace(0, 1, 200)
    plt.figure(figsize=(4.2, 3.6))
    plt.plot(xs, cb.logistic(xs, r), color="gray")
    plt.plot(X[50:-1], X[51:], "ko", markersize=4)
    plt.xlabel("x[n]")
    plt.ylabel("x[n+1]")
    plt.axis([0, 1, 0, 1])
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_return_r{tag(r)}.png", dpi=150)
    plt.close()

# -- three unknown data sets: henon, noise, sin3 -----------------------------
rng = np.random.default_rng(seed=1)
N = 200

hx, hy = np.zeros(N + 1), np.zeros(N + 1)
hx[0], hy[0] = 0.1, 0.1
for n in range(N):
    hx[n + 1] = 1 - 1.4 * hx[n] ** 2 + hy[n]
    hy[n + 1] = 0.3 * hx[n]

noise = rng.uniform(-1, 1, N + 1)

s3 = np.zeros(N + 1)
s3[0] = 0.3
for n in range(N):
    s3[n + 1] = -4 * s3[n] ** 3 + 3 * s3[n]

for name, data in [("henon", hx), ("noise", noise), ("sin3map", s3)]:
    plt.figure(figsize=(4.6, 2.6))
    plt.plot(range(len(data)), data, "k", linewidth=0.7)
    plt.xlabel("n")
    plt.ylabel("x[n]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_unknownmapping_series_{name}.png", dpi=150)
    plt.close()

    plt.figure(figsize=(3.4, 3.4))
    plt.plot(data[:-1], data[1:], "ko", markersize=3)
    plt.xlabel("x[n]")
    plt.ylabel("x[n+1]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_unknownmapping_return_{name}.png", dpi=150)
    plt.close()

# -- interactive: logistic explorer (series + cobweb + return, r slider) -----
rgrid = np.round(np.arange(0.5, 4.0001, 0.1), 2)
frames = []
for r in rgrid:
    X = cb.orbit(cb.logistic, x0=0.1, n=100, r=r)
    xs = np.linspace(0, 1, 100)
    px, py = [X[0]], [0.0]
    for k in range(40):
        px += [X[k], X[k]]
        py += [X[k], X[k + 1]]
    frames.append(go.Frame(name=f"{r}", data=[
        go.Scatter(x=list(range(41)), y=X[:41], mode="lines+markers",
                   marker=dict(size=4), line=dict(color="steelblue")),
        go.Scatter(x=xs, y=cb.logistic(xs, r), mode="lines",
                   line=dict(color="black")),
        go.Scatter(x=xs, y=xs, mode="lines", line=dict(color="royalblue")),
        go.Scatter(x=px, y=py, mode="lines",
                   line=dict(color="crimson", width=1)),
        go.Scatter(x=X[50:-1], y=X[51:], mode="markers",
                   marker=dict(color="crimson", size=4)),
    ]))
fig = make_subplots(rows=1, cols=3,
                    subplot_titles=("series x[n]", "cobweb", "return plot"))
for tr, (row, col) in zip(frames[0].data,
                          [(1, 1), (1, 2), (1, 2), (1, 2), (1, 3)]):
    fig.add_trace(tr, row=row, col=col)
# route every frame's traces to the same subplots as the initial data
for fr in frames:
    fr.traces = [0, 1, 2, 3, 4]
fig.frames = frames
fig.update_layout(
    showlegend=False, margin=dict(l=40, r=10, t=40, b=40),
    sliders=[dict(
        currentvalue=dict(prefix="r = "),
        steps=[dict(label=f"{r}", method="animate",
                    args=[[f"{r}"], dict(mode="immediate",
                                         frame=dict(duration=0, redraw=False))])
               for r in rgrid],
    )],
)
fig.update_yaxes(range=[0, 1])
fig.update_xaxes(range=[0, 1], row=1, col=2)
fig.update_xaxes(range=[0, 1], row=1, col=3)
fig.write_html(OUT / "interactive" / "logistic_explorer.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_series_cobweb_return: assets written to", OUT)
```

- [ ] **Step 2: Run and verify visually**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" creators/python/disc1d/fig_series_cobweb_return.py`
Expected: exit 0, 17 files. Read each PNG beside its Maple original (`maple/_static/disc1d/<same name>.png`): series show fixed point / period-2 / period-4 / chaos; cobwebs converge / 2-cycle / tangle; return plots show 1 / 2 / 4 points / the parabola filled; unknown-mapping panels: henon return plot is structured-but-not-a-curve, noise is a shapeless cloud, sin3map lies on the cubic. Open `logistic_explorer.html` as text: slider steps r = 0.5 … 4.0, script src `../../plotly.min.js`, no CDN. Adjust presentation parameters if a panel visibly mismatches the original; record adjustments.

- [ ] **Step 3: Commit**

```bash
git add creators/python/disc1d/ python/_static/disc1d/
git commit -m "Creators: disc1d series, cobweb, return-plot figures and logistic explorer"
```

---

### Task 3: Creators — fixed points, periodic-solution graphs

**Files:**
- Create: `creators/python/disc1d/fig_fixedpoints.py`
- Create (generated, committed): `python/_static/disc1d/disc1d_logist_attractor_r1_5.png`, `disc1d_logist_attractor_local_r2_0.png`, `disc1d_logist_attractor_local_r1_5.png`, `disc1d_logist_p2graph.png`, `disc1d_logist_p3graph_r380.png`, `disc1d_logist_p3graph_r384.png`

**Interfaces:**
- Consumes: `cb.logistic`, `cb.orbit`.
- Produces: 6 asset files above.

- [ ] **Step 1: Write `creators/python/disc1d/fig_fixedpoints.py`**

```python
"""Fixed-point and periodic-solution figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_attractor_r1_5.png        many x0 converge to x*=1/3
  disc1d_logist_attractor_local_r2_0.png  superstable convergence (sigma=0)
  disc1d_logist_attractor_local_r1_5.png  ordinary convergence
  disc1d_logist_p2graph.png               f, g=f(f(x)), y=x at r=3.2
  disc1d_logist_p3graph_r380.png          f, f^(3), y=x at r=3.80
  disc1d_logist_p3graph_r384.png          f, f^(3), y=x at r=3.84
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- global attraction: many initial conditions at r = 1.5 -------------------
plt.figure(figsize=(5.2, 3.4))
for x0 in [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    X = cb.orbit(cb.logistic, x0=x0, n=20, r=1.5)
    plt.plot(range(len(X)), X, "-o", markersize=3)
plt.axhline(1 / 3, color="gray", linewidth=0.8)
plt.xlabel("n")
plt.ylabel("xn")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_attractor_r1_5.png", dpi=150)
plt.close()

# -- local convergence: superstable (r=2) vs ordinary (r=1.5) ----------------
for r, xstar in [(2.0, 0.5), (1.5, 1 / 3)]:
    plt.figure(figsize=(4.2, 3.2))
    X = cb.orbit(cb.logistic, x0=xstar + 0.2, n=12, r=r)
    plt.plot(range(len(X)), X, "-o", markersize=4)
    plt.axhline(xstar, color="gray", linewidth=0.8)
    plt.xlabel("n")
    plt.ylabel("xn")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_attractor_local_r{str(r).replace('.', '_')}.png",
                dpi=150)
    plt.close()


def compose(f, m, x, r):
    for _ in range(m):
        x = f(x, r)
    return x


def periodic_points(m, r, exclude=()):
    """Real solutions of x = f^(m)(x) on [0,1], minus the excluded points."""
    xs = np.linspace(0, 1, 4001)
    h = compose(cb.logistic, m, xs, r) - xs
    roots = []
    for i in range(len(xs) - 1):
        if h[i] == 0 or h[i] * h[i + 1] < 0:
            root = brentq(lambda x: compose(cb.logistic, m, x, r) - x,
                          xs[i], xs[i + 1])
            if all(abs(root - e) > 1e-6 for e in exclude + tuple(roots)):
                roots.append(root)
    return roots


def sigma(points, r):
    """Stability of a periodic orbit: product of f' along the orbit."""
    return np.prod([r * (1 - 2 * x) for x in points])


# -- f, g = f(f(x)), y = x at r = 3.2 with period-2 and fixed points ---------
r = 3.2
xs = np.linspace(0, 1, 400)
plt.figure(figsize=(4.4, 4.4))
plt.plot(xs, cb.logistic(xs, r), "k", label="f(x)")
plt.plot(xs, compose(cb.logistic, 2, xs, r), "k--", label="g(x)=f(f(x))")
plt.plot(xs, xs, color="gray", linewidth=0.8)
fixed = [0, 1 - 1 / r]
p2 = periodic_points(2, r, exclude=tuple(fixed))
plt.plot(p2, p2, "ko", markersize=7)
plt.plot(fixed, fixed, "o", color="gray", markersize=9)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_p2graph.png", dpi=150)
plt.close()

# -- f, f^(3), y = x at r = 3.80 and 3.84 ------------------------------------
for r, name in [(3.80, "r380"), (3.84, "r384")]:
    plt.figure(figsize=(4.4, 4.4))
    plt.plot(xs, cb.logistic(xs, r), "k")
    plt.plot(xs, compose(cb.logistic, 3, xs, r), "k--")
    plt.plot(xs, xs, color="gray", linewidth=0.8)
    fixed = [0, 1 - 1 / r]
    plt.plot(fixed, fixed, "o", color="gray", markersize=10)
    p3 = periodic_points(3, r, exclude=tuple(fixed))
    if p3:
        # split the six points into the stable and the unstable 3-cycle
        orbit_a = [p3[0]]
        for _ in range(2):
            orbit_a.append(cb.logistic(orbit_a[-1], r))
        orbit_b = [p for p in p3
                   if all(abs(p - q) > 1e-6 for q in orbit_a)]
        for orb in [orbit_a, orbit_b]:
            color = "k" if abs(sigma(orb, r)) < 1 else "gray"
            plt.plot(orb, orb, "o", color=color, markersize=5)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_p3graph_{name}.png", dpi=150)
    plt.close()

print("fig_fixedpoints: assets written to", OUT)
```

- [ ] **Step 2: Run and verify visually**

Run the script; expect exit 0, 6 files. Compare each against the Maple original: attractor figure shows all series converging to 1/3; superstable panel converges dramatically faster than r=1.5; p2graph's black dots sit near 0.513/0.799; p3graph r=3.80 has no extra crossings, r=3.84 shows two 3-cycles, black set stable (|σ| ≈ 0.875 < 1), gray set unstable (σ ≈ 2.744). Record any presentation adjustments.

- [ ] **Step 3: Commit**

```bash
git add creators/python/disc1d/fig_fixedpoints.py python/_static/disc1d/
git commit -m "Creators: disc1d fixed-point and periodic-solution figures"
```

---

### Task 4: Creators — bifurcation diagrams + deep-zoom companion

**Files:**
- Create: `creators/python/disc1d/fig_bifurcation.py`
- Create (generated, committed): `python/_static/disc1d/disc1d_logist_bifur_theo.png`, `disc1d_logist_stability_p3both.png`, `disc1d_bifurcation_implicit_sin.png`, `disc1d_logist_series_bifurcation.png`, `disc1d_logist_series_bifurcation_zoom_doubling.png`, `disc1d_logist_series_bifurcation_zoom_p3.png`, `python/_static/disc1d/interactive/bifurcation_zoom.html`

**Interfaces:**
- Consumes: `cb.logistic`, `cb.sine`, `cb.orbit`, `cb.bifurcation_diagram` (with `discard=0.8`), plus `compose`/`periodic_points`/`sigma` re-declared locally (each creators script is self-contained).
- Produces: 7 asset files above.

- [ ] **Step 1: Write `creators/python/disc1d/fig_bifurcation.py`**

```python
"""Bifurcation-diagram figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_bifur_theo.png            analytical branches (period 1,2,4)
  disc1d_logist_stability_p3both.png      period-3 stable/unstable branches
  disc1d_bifurcation_implicit_sin.png     implicit x = f^(4)(x), sine map
  disc1d_logist_series_bifurcation.png    numerical bifurcation diagram
  disc1d_logist_series_bifurcation_zoom_doubling.png
  disc1d_logist_series_bifurcation_zoom_p3.png
  interactive/bifurcation_zoom.html       high-resolution pan/zoom diagram
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import brentq

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def compose(f, m, x, r):
    for _ in range(m):
        x = f(x, r)
    return x


def periodic_points(m, r, exclude=()):
    xs = np.linspace(0, 1, 4001)
    h = compose(cb.logistic, m, xs, r) - xs
    roots = []
    for i in range(len(xs) - 1):
        if h[i] == 0 or h[i] * h[i + 1] < 0:
            root = brentq(lambda x: compose(cb.logistic, m, x, r) - x,
                          xs[i], xs[i + 1])
            if all(abs(root - e) > 1e-6 for e in exclude + tuple(roots)):
                roots.append(root)
    return roots


def sigma_of(points, r):
    return np.prod([r * (1 - 2 * x) for x in points])


# -- analytical branches: periods 1, 2 and 4 ---------------------------------
plt.figure(figsize=(5.4, 3.8))
rs = np.linspace(0.5, 3.6, 500)
plt.plot(rs, np.where(rs < 1, 0, np.nan), "k")            # x*=0 stable
plt.plot(rs, np.where(rs >= 1, 0, np.nan), "gray")         # x*=0 unstable
x1 = 1 - 1 / rs
plt.plot(rs, np.where((rs > 1) & (rs < 3), x1, np.nan), "k")
plt.plot(rs, np.where(rs >= 3, x1, np.nan), color="gray")
r2 = np.linspace(3.0, 3.6, 400)
disc = np.sqrt(r2**2 - 2 * r2 - 3)
for sign in [+1, -1]:
    branch = (r2 + 1 + sign * disc) / (2 * r2)
    stable = r2 < 1 + np.sqrt(6)
    plt.plot(r2[stable], branch[stable], "k")
    plt.plot(r2[~stable], branch[~stable], color="gray")
for r in np.linspace(1 + np.sqrt(6) + 1e-4, 3.56, 120):   # period-4, numeric
    pts = periodic_points(4, r, exclude=tuple(
        [0, 1 - 1 / r] + periodic_points(2, r, exclude=(0, 1 - 1 / r))))
    for p in pts:
        plt.plot(r, p, "k.", markersize=2)
plt.xlabel("r")
plt.ylabel("x*(r)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_bifur_theo.png", dpi=150)
plt.close()

# -- period-3 stable and unstable branches -----------------------------------
plt.figure(figsize=(5.0, 3.8))
for r in np.linspace(3.8284, 3.856, 140):
    pts = periodic_points(3, r, exclude=(0, 1 - 1 / r))
    if len(pts) >= 6:
        orbit_a = [pts[0]]
        for _ in range(2):
            orbit_a.append(cb.logistic(orbit_a[-1], r))
        orbit_b = [p for p in pts
                   if all(abs(p - q) > 1e-6 for q in orbit_a)]
        for orb in [orbit_a, orbit_b]:
            color = "k" if abs(sigma_of(orb, r)) < 1 else "gray"
            for p in orb:
                plt.plot(r, p, ".", color=color, markersize=2)
plt.xlabel("r")
plt.ylabel("x*(r)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_stability_p3both.png", dpi=150)
plt.close()

# -- implicit plot x = f^(4)(x) for the sine map -----------------------------
R, Xg = np.meshgrid(np.linspace(0.0, 1, 400), np.linspace(0, 1, 400))
plt.figure(figsize=(5.2, 3.8))
plt.contour(R, Xg, compose(cb.sine, 4, Xg, R) - Xg, levels=[0],
            colors="black", linewidths=1.5)
plt.axis([0, 1, -0.1, 1])
plt.xlabel("r")
plt.ylabel("x(r)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_bifurcation_implicit_sin.png", dpi=150)
plt.close()

# -- numerical bifurcation diagram + zooms -----------------------------------
for rmin, rmax, name in [
    (3.3, 4.0, "disc1d_logist_series_bifurcation"),
    (2.8, 3.6, "disc1d_logist_series_bifurcation_zoom_doubling"),
    (3.82, 3.86, "disc1d_logist_series_bifurcation_zoom_p3"),
]:
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    cb.bifurcation_diagram(cb.logistic, rmin, rmax, nr=500, n=1000,
                           x0=0.57, discard=0.8, ax=ax)
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()

# -- interactive: high-resolution pan/zoom bifurcation diagram ---------------
rs, xs = [], []
for r in np.linspace(2.5, 4.0, 2001):
    X = cb.orbit(cb.logistic, x0=0.57, n=1000, r=r)
    rs.extend([r] * 150)
    xs.extend(X[-150:])
fig = go.Figure(go.Scattergl(x=rs, y=xs, mode="markers",
                             marker=dict(size=1, color="darkblue")))
fig.update_layout(
    xaxis_title="r", yaxis_title="x(r)",
    margin=dict(l=40, r=10, t=10, b=40),
    dragmode="zoom",
)
fig.write_html(OUT / "interactive" / "bifurcation_zoom.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_bifurcation: assets written to", OUT)
```

- [ ] **Step 2: Run and verify visually**

Run the script (the period-4 numeric continuation and the interactive grid take a couple of minutes). Compare each PNG with its Maple original: bifur_theo shows the fork at r=3 and period-4 onset near 3.45; p3both shows the stable/unstable pair splitting from the saddle-node at r≈3.8284; implicit_sin reproduces the closed loops near r=1; the numerical diagram and zooms match. Open the zoom HTML: Scattergl, ~300k points, no CDN. Record adjustments.

- [ ] **Step 3: Commit**

```bash
git add creators/python/disc1d/fig_bifurcation.py python/_static/disc1d/
git commit -m "Creators: disc1d bifurcation figures and deep-zoom companion"
```

---

### Task 5: Creators — Lyapunov, shift/tent, analytical, statistical, universality + Λ-link companion

**Files:**
- Create: `creators/python/disc1d/fig_lyapunov.py`, `creators/python/disc1d/fig_shift_tent.py`, `creators/python/disc1d/fig_analytical_statistical.py`, `creators/python/disc1d/fig_universality.py`, `creators/python/disc1d/roundoff_table.py`
- Create (generated, committed): `python/_static/disc1d/disc1d_logist_lyap_r39_lin.png`, `disc1d_logist_lyap_r39_log.png`, `disc1d_logist_lyap_bifurcation.png`, `disc1d_shiftmap_series.png`, `disc1d_shiftmap_returnplot.png`, `disc1d_tentmap_series.png`, `disc1d_tentmap_returnplot.png`, `disc1d_logist_analytical.png`, `disc1d_tanh_analytical.png`, `disc1d_logist_pdf.png`, `disc1d_sin3map_pdf.png`, `disc1d_doubling_logist.png`, `disc1d_doubling_sinmap.png`, `disc1d_universality_logist.png`, `disc1d_universality_sinmap.png`, `disc1d_not_so_universal.png`, `python/_static/disc1d/interactive/lyapunov_link.html`

**Interfaces:**
- Consumes: `cb.logistic`, `cb.sine`, `cb.tent`, `cb.shift`, `cb.orbit`, `cb.bifurcation_diagram`, `cb.lyapunov`, `cb.lyapunov_sweep`.
- Produces: 16 PNGs + 1 HTML above, plus `roundoff_table.py` whose printed output Task 7 pastes into the chapter.

- [ ] **Step 1: Write `creators/python/disc1d/fig_lyapunov.py`**

```python
"""Lyapunov-exponent figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_lyap_r39_lin.png     two series, eps=1e-9, linear scale
  disc1d_logist_lyap_r39_log.png     ln|y-x| with slope-0.6 guide line
  disc1d_logist_lyap_bifurcation.png bifurcation diagram + Lambda(r)
  interactive/lyapunov_link.html     linked bifurcation/Lambda slider view
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def dlogistic(x, r):
    return r * (1 - 2 * x)


# -- two series at r=3.9, eps = 1e-9 -----------------------------------------
N, eps = 60, 1e-9
X = cb.orbit(cb.logistic, x0=0.1, n=N, r=3.9)
Y = cb.orbit(cb.logistic, x0=0.1 + eps, n=N, r=3.9)
plt.figure(figsize=(6.4, 3.2))
plt.plot(range(N + 1), X, "-o", markersize=3, label="x")
plt.plot(range(N + 1), Y, "-s", markersize=3, label="y")
plt.xlabel("n")
plt.ylabel("x, y")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_r39_lin.png", dpi=150)
plt.close()

plt.figure(figsize=(5.4, 3.4))
plt.plot(range(N + 1), np.log(np.abs(Y - X)), "o", markersize=3)
n = np.arange(0, 36)
plt.plot(n, np.log(eps) + 0.6 * n, "k--")
plt.xlabel("n")
plt.ylabel("ln|y[n]-x[n]|")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_r39_log.png", dpi=150)
plt.close()

# -- combined bifurcation + Lambda(r) ----------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6),
                               sharex=True, height_ratios=[2, 1])
cb.bifurcation_diagram(cb.logistic, 2.5, 4.0, nr=800, n=1000,
                       x0=0.57, discard=0.8, ax=ax1)
rs, lams = cb.lyapunov_sweep(cb.logistic, dlogistic, 2.5, 4.0, nr=800)
ax2.plot(rs, lams, "k", linewidth=0.7)
ax2.axhline(0, color="gray", linewidth=0.8)
ax2.set_xlabel("r")
ax2.set_ylabel("Lambda(r)")
ax2.set_ylim(-2.5, 1)
ax1.set_xlim(2.5, 4)
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_bifurcation.png", dpi=150)
plt.close()

# -- interactive: bifurcation + Lambda(r) with a linked r-cursor -------------
rs_b, xs_b = [], []
for r in np.linspace(2.5, 4.0, 1001):
    X = cb.orbit(cb.logistic, x0=0.57, n=1000, r=r)
    rs_b.extend([r] * 100)
    xs_b.extend(X[-100:])
rs_l, lams_l = cb.lyapunov_sweep(cb.logistic, dlogistic, 2.5, 4.0, nr=1000)

rcursor = np.round(np.arange(2.5, 4.0001, 0.05), 3)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.65, 0.35],
                    vertical_spacing=0.05)
fig.add_trace(go.Scattergl(x=rs_b, y=xs_b, mode="markers",
                           marker=dict(size=1, color="darkblue")), row=1, col=1)
fig.add_trace(go.Scatter(x=rs_l, y=np.clip(lams_l, -3, None), mode="lines",
                         line=dict(color="black", width=1)), row=2, col=1)
fig.add_trace(go.Scatter(x=[3.0, 3.0], y=[0, 1], mode="lines",
                         line=dict(color="crimson", width=1.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=[3.0, 3.0], y=[-3, 1], mode="lines",
                         line=dict(color="crimson", width=1.5)), row=2, col=1)
frames = []
for r in rcursor:
    lam = np.interp(r, rs_l, np.clip(lams_l, -3, None))
    frames.append(go.Frame(name=f"{r}", traces=[2, 3], data=[
        go.Scatter(x=[r, r], y=[0, 1]),
        go.Scatter(x=[r, r], y=[-3, 1]),
    ], layout=dict(title=f"r = {r:.2f},  Lambda = {lam:+.3f}")))
fig.frames = frames
fig.update_layout(
    showlegend=False, margin=dict(l=50, r=10, t=40, b=40),
    yaxis_title="x(r)", yaxis2_title="Lambda(r)", xaxis2_title="r",
    sliders=[dict(
        currentvalue=dict(prefix="r = "),
        steps=[dict(label=f"{r}", method="animate",
                    args=[[f"{r}"], dict(mode="immediate",
                                         frame=dict(duration=0, redraw=True))])
               for r in rcursor],
    )],
)
fig.write_html(OUT / "interactive" / "lyapunov_link.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_lyapunov: assets written to", OUT)
```

- [ ] **Step 2: Write `creators/python/disc1d/fig_shift_tent.py`**

```python
"""Shift-map and tent-map figures for "Chaos in Iterative Maps".

The shift and tent maps discard one binary digit per iteration, so
double-precision orbits collapse to exactly 0 after ~52 steps — itself a
neat illustration of the chapter's round-off story. To draw 400
meaningful steps we iterate in extended precision with mpmath.

Produces (in python/_static/disc1d/):
  disc1d_shiftmap_series.png / disc1d_shiftmap_returnplot.png
  disc1d_tentmap_series.png  / disc1d_tentmap_returnplot.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpmath import mp, mpf

mp.dps = 150  # enough digits for 400 doublings

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

N = 400


def run_map(f, y0):
    Y = np.zeros(N + 1)
    y = y0
    for n in range(N + 1):
        Y[n] = float(y)
        y = f(y)
    return Y


shift = lambda y: (2 * y) - int(2 * y)
tent = lambda z: 1 - 2 * abs(z - mpf(1) / 2)

for name, f, y0, label in [
    ("shiftmap", shift, 1 / mp.pi, "y"),
    ("tentmap", tent, 1 / mp.pi, "z"),
]:
    Y = run_map(f, y0)
    plt.figure(figsize=(5.6, 2.8))
    plt.plot(range(N + 1), Y, "o", markersize=2)
    plt.xlabel("n")
    plt.ylabel(f"{label}[n]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_{name}_series.png", dpi=150)
    plt.close()

    plt.figure(figsize=(3.6, 3.6))
    plt.plot(Y[:-1], Y[1:], "o", markersize=2)
    plt.xlabel(f"{label}[n]")
    plt.ylabel(f"{label}[n+1]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_{name}_returnplot.png", dpi=150)
    plt.close()

print("fig_shift_tent: assets written to", OUT)
```

- [ ] **Step 3: Write `creators/python/disc1d/fig_analytical_statistical.py`**

```python
"""Closed-form-solution and pdf figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_analytical.png  x_n = sin^2(2^n theta) vs the iterated map
  disc1d_tanh_analytical.png    x_n = tanh(2^n theta) vs the iterated map
  disc1d_logist_pdf.png         histogram vs 1/(pi sqrt(x(1-x)))
  disc1d_sin3map_pdf.png        histogram vs 1/(pi sqrt(1-x^2))
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- analytical solution of the r=4 logistic map -----------------------------
x0 = 0.36
theta = np.arcsin(np.sqrt(x0))
t = np.linspace(0, 7, 400)
plt.figure(figsize=(6.4, 3))
plt.plot(t, np.sin(2**t * theta) ** 2, "gray", linewidth=1)
X = cb.orbit(cb.logistic, x0=x0, n=7, r=4)
plt.plot(range(8), X, "ko", markersize=6)
plt.xlabel("n")
plt.ylabel("x[n]")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_analytical.png", dpi=150)
plt.close()

# -- analytical solution of the tanh map -------------------------------------
x0 = 0.05
theta = np.arctanh(x0)
t = np.linspace(0, 14, 400)
plt.figure(figsize=(6.4, 3))
plt.plot(t, np.tanh(2**t * theta), "gray", linewidth=1)
X = np.zeros(15)
X[0] = x0
for n in range(14):
    X[n + 1] = 2 * X[n] / (1 + X[n] ** 2)
plt.plot(range(15), X, "ko", markersize=6)
plt.xlabel("n")
plt.ylabel("x[n]")
plt.tight_layout()
plt.savefig(OUT / "disc1d_tanh_analytical.png", dpi=150)
plt.close()

# -- pdfs --------------------------------------------------------------------
X = cb.orbit(cb.logistic, x0=0.1, n=8192, r=4)
plt.figure(figsize=(4.8, 3.4))
plt.hist(X, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(0.005, 0.995, 300)
plt.plot(xs, 1 / (np.pi * np.sqrt(xs * (1 - xs))), "k", linewidth=2.5)
plt.axis([0, 1, 0, 2])
plt.xlabel("x")
plt.ylabel("p(x)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_pdf.png", dpi=150)
plt.close()

S = np.zeros(8193)
S[0] = 0.3
for n in range(8192):
    S[n + 1] = -4 * S[n] ** 3 + 3 * S[n]
plt.figure(figsize=(4.8, 3.4))
plt.hist(S, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(-0.995, 0.995, 300)
plt.plot(xs, 1 / (np.pi * np.sqrt(1 - xs**2)), "k", linewidth=2.5)
plt.axis([-1, 1, 0, 2])
plt.xlabel("x")
plt.ylabel("p(x)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_sin3map_pdf.png", dpi=150)
plt.close()

print("fig_analytical_statistical: assets written to", OUT)
```

(Note: the sin3-map orbit in doubles degrades like the shift map but only via rounding noise, which merely re-randomises the chaotic orbit — the histogram is unaffected; no mpmath needed here.)

- [ ] **Step 4: Write `creators/python/disc1d/fig_universality.py`**

```python
"""Universality / Feigenbaum figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_doubling_logist.png / disc1d_doubling_sinmap.png
  disc1d_universality_logist.png / disc1d_universality_sinmap.png
  disc1d_not_so_universal.png   delta(eta) for f = r(1-|2x-1|^eta)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

RC_LOGIST, RC_SINE = 3.56994537, 0.86557928

# -- plain bifurcation diagrams with the accumulation point marked -----------
for f, rmin, rmax, rc, name in [
    (cb.logistic, 2.8, 4.0, RC_LOGIST, "disc1d_doubling_logist"),
    (cb.sine, 0.6, 1.0, RC_SINE, "disc1d_doubling_sinmap"),
]:
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    cb.bifurcation_diagram(f, rmin, rmax, nr=600, n=1000,
                           x0=0.57, discard=0.8, ax=ax)
    ax.annotate("", xy=(rc, 0.02), xytext=(rc, 0.14),
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()

# -- rescaled diagrams: a = -ln(r_inf - r) -----------------------------------
for f, rc, rmin, amax, name in [
    (cb.logistic, RC_LOGIST, 2.8, 10.2, "disc1d_universality_logist"),
    (cb.sine, RC_SINE, 0.3, 10.2, "disc1d_universality_sinmap"),
]:
    amin = -np.log(rc - rmin)
    plt.figure(figsize=(5.4, 3.8))
    for a in np.linspace(amin, amax, 501):
        r = rc - np.exp(-a)
        X = cb.orbit(f, x0=0.57, n=1000, r=r)
        plt.plot([a] * 201, X[800:], ",", color="black")
    plt.xlim(amin, amax)
    plt.ylim(0.33, 0.9)
    plt.xlabel("a")
    plt.ylabel("x(a)")
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


# -- delta(eta) via Newton-Raphson on superstable orbits ---------------------
def superstable_r(f, df, p_max, r_start):
    """r_p of superstable 2^p cycles via Newton-Raphson from x0 = 1/2."""
    rc = {}
    for p in range(p_max + 1):
        m = 2**p
        if p >= 3:
            delta = (rc[p - 2] - rc[p - 3]) / (rc[p - 1] - rc[p - 2])
            r = rc[p - 1] + (rc[p - 1] - rc[p - 2]) / delta
        else:
            r = r_start
        for _ in range(100):
            X = np.zeros(m + 1)
            X[0] = 0.5
            for n in range(m):
                X[n + 1] = f(X[n], r)
            dg = 0.0
            for n in range(1, m + 1):
                dg = X[n] / r + df(X[n - 1], r) * dg
            rnew = r - (X[m] - X[0]) / dg
            if abs(rnew - r) < 1e-13:
                r = rnew
                break
            r = rnew
        rc[p] = r
    return rc


etas, deltas = [], []
for eta in np.arange(1.2, 4.01, 0.2):
    f = lambda x, r, e=eta: r * (1 - np.abs(2 * x - 1) ** e)
    df = lambda x, r, e=eta: (-r * e * np.abs(2 * x - 1) ** (e - 1)
                              * np.sign(2 * x - 1) * 2)
    try:
        rc = superstable_r(f, df, 8, 0.9)
        deltas.append((rc[6] - rc[5]) / (rc[7] - rc[6]))
        etas.append(eta)
    except (ZeroDivisionError, FloatingPointError, OverflowError):
        pass

plt.figure(figsize=(5.2, 3.6))
plt.plot(etas, deltas, "ko-", markersize=5)
plt.axhline(4.6692, color="gray", linewidth=0.8)
plt.xlabel("eta")
plt.ylabel("delta")
plt.tight_layout()
plt.savefig(OUT / "disc1d_not_so_universal.png", dpi=150)
plt.close()

print("fig_universality: assets written to", OUT)
```

- [ ] **Step 5: Write `creators/python/disc1d/roundoff_table.py`**

```python
"""Prints the round-off comparison table for the chapter: two
algebraically identical implementations of the logistic map,
r x (1 - x) versus r x - r x^2, iterated from the same x0."""

import numpy as np

N, r = 50, 3.9
X = np.zeros(N)
Y = np.zeros(N)
X[0] = Y[0] = 0.1
for n in range(N - 1):
    X[n + 1] = r * X[n] * (1 - X[n])
    Y[n + 1] = r * Y[n] - r * Y[n] ** 2

print("    n       X[n]          Y[n]        n      X[n]           Y[n]")
for n in range(25):
    print(f"   {n:2d}  {X[n]:12.10f}  {Y[n]:12.10f}    "
          f"{n + 25:2d}  {X[n + 25]:12.10f}  {Y[n + 25]:12.10f}")
```

- [ ] **Step 6: Run everything and verify**

Run all five scripts with `"C:/Users/mvr/cbenv2/Scripts/python"`. `fig_universality.py` takes several minutes (Newton-Raphson over an η grid). Verify against the Maple originals: the log-divergence points follow the dashed 0.6-slope line; Λ(r) is negative below r=3, zero at bifurcations, first positive near 3.57; the shift/tent series stay chaotic for all 400 points (no collapse — that's the mpmath working) and their return plots show the two-branch line and the tent; analytical figures show the continuous curve threading the iterates; pdfs match the U-shaped curves; δ(η) passes through ≈4.67 at η=2. Verify `roundoff_table.py` prints 25 rows and the two columns diverge visibly in the n=25–49 half. Open `lyapunov_link.html` as text: slider present, no CDN. Record adjustments.

- [ ] **Step 7: Commit**

```bash
git add creators/python/disc1d/ python/_static/disc1d/
git commit -m "Creators: disc1d Lyapunov, shift/tent, analytical, pdf and universality figures"
```

---

### Task 6: Chapter conversion, front half (intro through Bifurcation-diagrams)

**Files:**
- Create: `python/disc1d.md` (copy of `maple/disc1d.md` with the front-half edits applied; back-half edits follow in Task 7)

Copy `maple/disc1d.md` to `python/disc1d.md` (`cp`), then apply EXACTLY these edits (F1–F17). Everything else stays byte-identical. All "Python admonition" replacements use the same fence pattern as the phenomenon chapter: ````{admonition} Python` / `:class: python` outer fence with a ```{code-block} python` inner fence. Every `:::{only} html` code-link block has the form:

```markdown
:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/disc1d/<script>.py)*
:::
```

- [ ] **F1** — In the paragraph before the first code block, replace "Instead let us resort to a numerical approach and write a small `maple` program to calculate and plot the series for some values of $r$. Take for example $r=3.9$ and $0 < x_0 < 1$. Execute the `maple` program and observe the chaos!" with "Instead let us resort to a numerical approach and write a small Python program to calculate and plot the series for some values of $r$. Take for example $r=3.9$ and $0 < x_0 < 1$. Run the program and observe the chaos!"

- [ ] **F2** — Replace the first Maple admonition (the series program) with a Python admonition containing:

```python
import numpy as np
import matplotlib.pyplot as plt
import chaosbook as cb

# generate and plot the time series
X = cb.orbit(cb.logistic, x0=0.1, n=20, r=0.5)
plt.plot(range(len(X)), X, "o")
plt.xlabel("n")
plt.ylabel("xn")
```

- [ ] **F3** — After the `fig:disc1d:some_series_logist` subfigure block, insert the code link (`fig_series_cobweb_return.py`).

- [ ] **F4** — After the `fig:disc1d:some_cobwebs_logist` subfigure block, insert the code link (`fig_series_cobweb_return.py`). Then, in the paragraph "One can study the cobweb method in more detail by running the `maple` program below and changing the value of $r$ and/or looking at other mappings like $f(x)=r\sin(\pi x)$.", replace "`maple` program" with "Python program" and append " (`cb.sine`)" after "$f(x)=r\sin(\pi x)$". Replace the cobweb Maple admonition with a Python admonition containing:

```python
cb.cobweb(cb.logistic, x0=0.1, n=20, r=3.9)
```

(with one preceding comment line `# the cookbook shows the cobweb construction written out in plain code`).

- [ ] **F5** — In the Return-plot section, replace "Here is the `maple` -code to make a return-plot." with "Here is the Python code to make a return-plot." and replace the Maple admonition with:

```python
X = cb.orbit(cb.logistic, x0=0.1, n=200, r=3.9)
nmin = 50
plt.plot(X[nmin:-1], X[nmin + 1:], "o")
plt.xlabel("x[n]")
plt.ylabel("x[n+1]")
plt.axis([0, 1, 0, 1])
```

- [ ] **F6** — After the `fig:disc1d:returnplots_logist` subfigure block, insert the code link (`fig_series_cobweb_return.py`) and then the logistic-explorer iframe:

````markdown
```{raw} html
<p><em>All three views under one slider — drag r yourself:</em></p>
<iframe src="_static/disc1d/interactive/logistic_explorer.html" width="100%" height="420" style="border:none;"></iframe>
```
````

- [ ] **F7** — After the `fig:disc1d:unknownmappings` subfigure block, insert the code link (`fig_series_cobweb_return.py`).

- [ ] **F8** — After the `fig:disc1d:logist_attractor` figure block and after the `fig:disc1d:logist_attractor_local` subfigure block, insert code links (`fig_fixedpoints.py`).

- [ ] **F9** — After the `fig:disc1d:plot_of_g` figure block, insert the code link (`fig_fixedpoints.py`). In the period-2 Example admonition, replace "In the following maple program we determine the true period-2 solutions for the logistic map." with "In the following Python program we determine the true period-2 solutions for the logistic map, using sympy for the algebra." and replace its first code block with:

```python
import sympy as sym

x, r = sym.symbols("x r")
f = lambda x: r * x * (1 - x)
g = lambda x: f(f(x))
fp2 = sym.solve(sym.Eq(x, g(x)), x)
```

Replace "`maple` returns the general solution to $x=g(x)$, where $g$ is given by {eq}`eq:disc1d:p2_g_logisticmap`; we have added the curly bars to store the solution in the form of a *set*:" with "sympy returns the general solution to $x=g(x)$, where $g$ is given by {eq}`eq:disc1d:p2_g_logisticmap`, as a list:". Replace "we calculate the period-1 solutions separately and exclude this set of solutions from the former set by issuing the `maple` command `minus`:" with "we calculate the period-1 solutions separately and exclude them:" and replace the second code block with:

```python
fp1 = sym.solve(sym.Eq(x, f(x)), x)
truefp2 = [s for s in fp2 if s not in fp1]
```

- [ ] **F10** — In the period-2 stability Example, replace "we extend the maple-code of the previous example by the following commands" with "we extend the code of the previous example by the following commands" and replace its first code block with:

```python
dg = sym.diff(g(x), x)
sigma2 = sym.simplify(dg.subs(x, truefp2[0]))
```

Replace the second code block ("solve(abs(...)...") with:

```python
sym.solve(sym.Eq(sigma2, 1), r), sym.solve(sym.Eq(sigma2, -1), r)
```

(the surrounding prose "which, ignoring negative solutions, yields" stays).

- [ ] **F11** — After the `fig:disc1d:plot_of_f3` subfigure block, insert the code link (`fig_fixedpoints.py`). In the period-3 Example, replace its first code block with:

```python
f3 = lambda x: f(f(f(x)))
fp1 = sym.solve(sym.Eq(x, f(x)), x)
poly = sym.Poly(sym.expand(f3(x) - x).subs(r, 3.84), x)
roots = sym.nroots(poly)
tfp3 = sorted(ro for ro in roots
              if all(abs(ro - s.subs(r, 3.84)) > 1e-6 for s in fp1))
tfp3
```

Replace "The latter command yields" and its `tfp3 := ...` code block with "The last line yields" and:

```{code-block} text
[0.149406, 0.169433, 0.488004, 0.540387, 0.953736, 0.959447]
```

Replace "We determine the derivative $g'$ by the `maple` command `D(g)`, which directly yields the derivative as a function. Next we use the `seq` command to enumerate all the values" with "We determine the derivative $g'$ with sympy and evaluate it at all six points" and its code block with:

```python
df3 = sym.lambdify(x, sym.diff(f3(x), x).subs(r, 3.84))
[round(df3(ro), 6) for ro in tfp3]
```

followed by a `text` code block `[-0.875276, 2.74407, -0.875276, 2.74407, 2.74407, -0.875276]`. Replace the final code block (the `..` / `df := D(f)` chain method) with:

```python
df = sym.lambdify(x, sym.diff(f(x), x).subs(r, 3.84))
for k in [0, 1]:
    x3a = float(tfp3[k])
    x3b = 3.84 * x3a * (1 - x3a)
    x3c = 3.84 * x3b * (1 - x3b)
    print(round(df(x3a) * df(x3b) * df(x3c), 6))
```

followed by a `text` code block with the two printed values `-0.875276` and `2.74407`.

- [ ] **F12** — In the Bifurcation-diagrams section, replace "With use of `maple` it is not impossible but surely it is rather cumbersome." with "It is not impossible to push this further, but surely it is rather cumbersome." Replace "We mention in passing that `maple` does provide a fast *numerical* way to get a quick glance of the bifurcations of a map." with "We mention in passing that there is a fast *numerical* way to get a quick glance of the bifurcations of a map." Replace "We do this by employing the `maple` command `implicitplot`." with "We do this with an implicit plot — a single zero contour." Replace the sine-map Maple admonition with:

```python
def f4(x, r):
    for _ in range(4):
        x = cb.sine(x, r)
    return x

R, X = np.meshgrid(np.linspace(0, 1, 300), np.linspace(0, 1, 300))
plt.contour(R, X, f4(X, R) - X, levels=[0], colors="black")
plt.xlabel("r")
plt.ylabel("x(r)")
```

- [ ] **F13** — In the caption of `fig:disc1d:bifurcation_implicit_sin`, replace "calculated and plotted by using the `maple` command `implicitplot`" with "calculated and plotted as a zero contour". After the figure block, insert the code link (`fig_bifurcation.py`). Also insert code links after the `fig:disc1d:theobifurcationdiagram` subfigure block (`fig_bifurcation.py`).

- [ ] **F14** — Replace the numerical-bifurcation Maple admonition with:

```python
cb.bifurcation_diagram(cb.logistic, 3.3, 4, nr=500, n=1000,
                       x0=0.57, discard=0.8)
```

(with one preceding comment line `# the cookbook shows this construction written out in plain code`).

- [ ] **F15** — After the `fig:disc1d:series_bifurcation_logist` figure block, insert the code link (`fig_bifurcation.py`). After the `fig:disc1d:series_bifurcation_logist_zooms` subfigure block, insert the code link (`fig_bifurcation.py`) and then the deep-zoom iframe:

````markdown
```{raw} html
<p><em>Zoom in yourself — the structure repeats at every scale:</em></p>
<iframe src="_static/disc1d/interactive/bifurcation_zoom.html" width="100%" height="440" style="border:none;"></iframe>
```
````

- [ ] **F16** — Sanity-diff check: run `git diff --no-index maple/disc1d.md python/disc1d.md` and confirm every hunk so far maps to one of F1–F15 (the back half is still identical).

- [ ] **F17** — Commit:

```bash
git add python/disc1d.md
git commit -m "Python edition: disc1d chapter, front half converted"
```

---

### Task 7: Chapter conversion, back half + exercises + index + build

**Files:**
- Modify: `python/disc1d.md` (back-half edits B1–B12)
- Create: `python/_includes/disc1d_exercises.md`
- Copy: `maple/_static/exercises/ex0093r00.png` → `python/_static/exercises/`
- Modify: `python/index.md` (add `disc1d` to the Text toctree after `phenomenon`)

- [ ] **B1** — In the Lyapunov section, replace "see the maple code below." with "see the code below." and replace the two-series Maple admonition with:

```python
r, N = 3.9, 100
epsilon = 1e-9
X = cb.orbit(cb.logistic, x0=0.1, n=N, r=r)
Y = cb.orbit(cb.logistic, x0=0.1 + epsilon, n=N, r=r)
```

Insert code links after `fig:disc1d:logist_lyap_two_sets`, `fig:disc1d:logist_lyap_r39_log` and `fig:disc1d:lyapunovdiagram` figure blocks (`fig_lyapunov.py`), and after the `fig:disc1d:lyapunovdiagram` code link add the linked-view iframe:

````markdown
```{raw} html
<p><em>Slide r and watch the diagram and Lambda(r) move together:</em></p>
<iframe src="_static/disc1d/interactive/lyapunov_link.html" width="100%" height="520" style="border:none;"></iframe>
```
````

- [ ] **B2** — Replace "See the `maple` -code below:" (round-off example) with "See the code below:" and the Maple admonition with:

```python
N, r = 50, 3.9
X = np.zeros(N)
Y = np.zeros(N)
X[0] = Y[0] = 0.1
for n in range(N - 1):
    X[n + 1] = r * X[n] * (1 - X[n])
    Y[n + 1] = r * Y[n] - r * Y[n] ** 2
    print(f"{n:2d}  {X[n]:12.10f}  {Y[n]:12.10f}")
```

- [ ] **B3** — Replace the entire `{code-block} text` output table with the actual output of `"C:/Users/mvr/cbenv2/Scripts/python" creators/python/disc1d/roundoff_table.py` (run it, paste verbatim). Then, in the paragraph after the table, replace "At step $n=45$ the difference between the two series is as large as the values themselves." with the same sentence using the first $n$ at which $|X_n - Y_n| > 0.1$ in YOUR generated table (inspect the pasted output; e.g. "At step $n=38$ …"). Record the observed value in the task report.

- [ ] **B4** — In the shift-map section, replace "See the maple-code below. Note that we first define the modulo-function `modf`, since it is not a standard function of `maple` ." with: "See the code below. A subtlety: an ordinary double-precision number stores $y$ in *binary*, and the shift map shifts one bit out per step — so a naive iteration collapses to exactly zero after about 52 steps, a perfect illustration of the round-off mechanism discussed above (and of {numref}`table:shiftmapconcept` below). To iterate meaningfully for 400 steps we therefore use extended-precision arithmetic." Replace the shift-map Maple admonition with:

```python
from mpmath import mp, mpf

mp.dps = 150          # plenty of binary digits for 400 doublings
f = lambda y: 2 * y - int(2 * y)
N = 400
Y = np.zeros(N + 1)
y = 1 / mp.pi
for n in range(N + 1):
    Y[n] = float(y)
    y = f(y)
plt.plot(range(N + 1), Y, "o", markersize=2)
plt.xlabel("n")
plt.ylabel("y[n]")
```

Insert code links after the `fig:disc1d:shiftmapseriesreturnplot` and `fig:disc1d:tentmapseriesreturnplot` subfigure blocks (`fig_shift_tent.py`).

- [ ] **B5** — Insert code links after the `fig:disc1d:logist_analytical` and `fig:disc1d:tanh_analytical` figure blocks (`fig_analytical_statistical.py`).

- [ ] **B6** — In the statistical Example, replace "The `maple` code below determines the pdf" with "The code below determines the pdf" and its code block with:

```python
X = cb.orbit(cb.logistic, x0=0.1, n=8192, r=4)
plt.hist(X, bins=32, density=True, color="gray")
xs = np.linspace(0.025, 0.975, 200)
plt.plot(xs, 1 / (np.pi * np.sqrt(xs * (1 - xs))), "k", linewidth=3)
plt.axis([0, 1, 0, 2])
plt.xlabel("x")
plt.ylabel("p(x)")
```

Insert the code link after the `fig:disc1d:pdfs` subfigure block (`fig_analytical_statistical.py`).

- [ ] **B7** — Insert code links after the `fig:disc1d:universality` and `fig:disc1d:universality_regular` subfigure blocks and the `fig:disc1d:not_so_universal` figure block (`fig_universality.py`). Replace "The plots, which were generated with a `maple` -code similar to the one shown below, now nicely reveal" with "The plots, generated with code like that shown below, now nicely reveal" and replace the rescaled-diagram Maple admonition with:

```python
rc = 0.86557928
amin, amax = -np.log(rc - 0.3), 10.2
for a in np.linspace(amin, amax, 501):
    r = rc - np.exp(-a)
    X = cb.orbit(cb.sine, x0=0.57, n=1000, r=r)
    plt.plot([a] * 201, X[800:], ",", color="black")
plt.axis([amin, amax, 0.33, 0.9])
plt.xlabel("a")
plt.ylabel("x(a)")
```

- [ ] **B8** — Replace "Execution of the simple maple commands below" with "Execution of the simple commands below" and the fsolve Maple admonition with:

```python
from scipy.optimize import brentq

def F(r):
    x = 0.5
    for _ in range(8):
        x = cb.logistic(x, r)
    return x - 0.5

rs = np.linspace(2, 3.56, 2000)
vals = [F(r) for r in rs]
[round(brentq(F, rs[i], rs[i + 1]), 9)
 for i in range(len(rs) - 1) if vals[i] * vals[i + 1] < 0]
```

- [ ] **B9** — Replace "Below find the maple implementation. First we define $f(x,r)$, $f'(x,r)$ and $h(r)$, which the right-hand side of {eq}`eq:feigennewtonraphson`; next we loop" with "Below find the Python implementation. First we define $f(x,r)$, $f'(x,r)$ and $h(r)$, which is the right-hand side of {eq}`eq:feigennewtonraphson`; next we loop". Replace "The `maple` code will give numbers such as given in table {numref}`table:disc1d:feigenbaum_numbers`; for the sine-map one should replace $r[0]$ by an appropriate number ($r[0] =  0.9$ works)" with "The code will give numbers such as given in table {numref}`table:disc1d:feigenbaum_numbers`; for the sine-map one should replace the start value 3.57 by an appropriate number (0.9 works)". Replace the Newton-Raphson Maple admonition with:

```python
f = lambda x, r: r * x * (1 - x)
df = lambda x, r: r * (1 - 2 * x)

def h(r, m):
    X = np.zeros(m + 1)
    X[0] = 0.5
    for n in range(m):
        X[n + 1] = f(X[n], r)
    dg = 0.0
    for n in range(1, m + 1):
        dg = X[n] / r + df(X[n - 1], r) * dg
    return r - (X[m] - X[0]) / dg

P = 11                      # calculations until period 2^11 = 2048
rc = {}
for p in range(P + 1):
    m = 2**p
    if p >= 3:              # smart start value from the previous delta
        delta = (rc[p - 2] - rc[p - 3]) / (rc[p - 1] - rc[p - 2])
        r = rc[p - 1] + (rc[p - 1] - rc[p - 2]) / delta
    else:
        r = 3.57
    for _ in range(100):    # Newton-Raphson iteration
        rnew = h(r, m)
        if abs(rnew - r) < 1e-13:
            break
        r = rnew
    rc[p] = rnew

for p in range(1, P):
    print(p, round(rc[p], 8), round((rc[p] - rc[p - 1]) / (rc[p + 1] - rc[p]), 6))
```

- [ ] **B10** — Replace "Adapting the `maple` code slightly gives the data-points plotted in" with "Adapting the code slightly gives the data-points plotted in".

- [ ] **B11** — Write `python/_includes/disc1d_exercises.md`: copy `maple/_includes/disc1d_exercises.md` and apply exactly these edits: (1) delete all four "**Downloads:** …" lines (the linked Maple worksheets have no Python counterpart yet; the exercise figure stays); (2) in Newton-Raphson (a), replace "program the Newton-Raphson method in `maple` by iterating" with "program the Newton-Raphson method in Python by iterating"; (3) in Discrete Cubic Map (f), replace "Take $r=1$ and set `Digits:=40`. Generate two series" with "Take $r=1$. Generate two series" — nothing else changes. Copy the exercise figure: `cp maple/_static/exercises/ex0093r00.png python/_static/exercises/`.

- [ ] **B12** — Add `disc1d` to `python/index.md`'s Text toctree (after `phenomenon`); update the landing sentence "The first chapter and the cookbook are available; further chapters follow." to "The first two chapters and the cookbook are available; further chapters follow."

- [ ] **Step: build and verify**

Run: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -M html python build/python`
Expected: exit 0; the only acceptable warning is the pre-existing cookbook.pdf button link. Check `build/python/html/disc1d.html`: all 23 figures render, 3 iframes present, code links on every script-generated figure, exercises included; `grep -i maple` on the built page → 0. Run the sanity diff (`git diff --no-index maple/disc1d.md python/disc1d.md`) and map every hunk to an enumerated edit (F1–F15, B1–B10); report the mapping.

- [ ] **Step: commit**

```bash
git add python/
git commit -m "Python edition: disc1d chapter complete with exercises and interactive figures"
```

---

### Task 8: Manifest, verification, publish

**Files:**
- Modify: `creators/porting_manifest.csv`

- [ ] **Step 1:** For every disc1d figure row in `creators/porting_manifest.csv` (figure files starting `disc1d_`), fill the `python_source` column with the generating script path (`creators/python/disc1d/fig_….py` per the script header comments) and `python_status` with `ported`. Preserve the file's formatting.

- [ ] **Step 2:** Full verification: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -q` → 20 passed; HTML build exit 0 (warnings as in Task 7); `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -b latex python build/python/latex` → exit 0.

- [ ] **Step 3:** Commit and push; watch CI to completion:

```bash
git add creators/porting_manifest.csv
git commit -m "Creators: track disc1d figures in the porting manifest"
git push
RUN_ID=$(gh run list --workflow pages.yml --branch main --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status --interval 30
```

Expected: build and deploy both succeed; the chapter is live at `https://mvreeuwijk.github.io/chaosbook/python/disc1d.html`.

---

## Self-review notes

- **Spec coverage** (pilot spec, disc1d scope): conversion model with verbatim prose + enumerated edits (Tasks 6–7); creators as published code with exhaustive per-figure code links (implementation note honored — every one of the 23 script-generated figures gets a link in F3–F15/B1–B7); all three disc1d interactive companions (explorer Task 2, deep zoom Task 4, Λ-link Task 5) embedded via `{raw} html` (Tasks 6–7); package additions generic-first with qualitative tests incl. Λ = ln 2 for logistic r=4 (Task 1; the spec's `tent(x, r)` sketch corrected to the book's parameterless tent, and `shift` likewise, per the APIs-mirror-the-book constraint); exercises ported with Python wording (B11); manifest (Task 8); CI untouched, push publishes.
- **Floating-point handling** is explicit and didactic (Global Constraints; fig_shift_tent; edit B4; regenerated round-off table B2–B3 with the data-dependent sentence update flagged as an instruction, not a placeholder).
- **Type consistency:** `discard=` keyword defined in Task 1 and used in Tasks 4–5 and edit F14; `lyapunov_sweep` signature matches between Task 1 and Task 5; `compose/periodic_points/sigma` are deliberately re-declared locally in each creators script (self-contained published scripts, per spec).
- **Numeric expectations** (tfp3 values, stability ±0.875/2.744, superstable r list, Feigenbaum table) are the chapter's own quoted values; implementers verify their code reproduces them and report discrepancies rather than editing the quoted text.
