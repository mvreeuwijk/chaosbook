# Phenomenon Chapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert chapter 1 ("A start at the end" — Lorenz + three-body) to the Python edition per `docs/superpowers/specs/2026-08-11-pilot-chapters-design.md`: package addition (`threebody`), published creators scripts regenerating every figure, the converted chapter with interactive plotly companions, and ported exercises.

**Architecture:** `flows.threebody` (inertial frame, circular primaries) + `flows.corotating` join the package. `creators/python/phenomenon/` holds two readable figure scripts that emit static PNG twins (matplotlib, Maple basenames, committed to `python/_static/phenomenon/`) and three interactive plotly HTML assets (self-hosted plotly.min.js). `python/phenomenon.md` copies the Maple prose verbatim with Python code admonitions, `{raw} html` iframes for the interactive companions (raw-html emits nothing in LaTeX, so the PDF pipeline is untouched), and "code behind this figure" links.

**Tech Stack:** numpy, scipy (solve_ivp), matplotlib, plotly (creators only), Sphinx/MyST.

## Global Constraints

- **Nothing under `python/` may mention Maple** (words, files, links).
- **Prose and mathematics copied verbatim** from `maple/phenomenon.md` except the enumerated edits in Task 4 (code blocks, Maple-workflow sentences, dangling cross-references). Do not rephrase anything else.
- **Figure basenames identical to the Maple edition** (`phenomenon_lorenz_xt_series.png`, …) under `python/_static/phenomenon/`.
- **Static twins must visually match the Maple originals** (`maple/_static/phenomenon/*.png`): same system, parameters, ranges, and qualitative appearance (colors/fonts may differ). Verify by Reading both images side by side.
- Lorenz: `sigma=10, r=28, b=8/3`, ic `(2, 5, 5)`, `epsilon` 1e-3/1e-5, `t = 0..30` for time series. Three-body: `G=6.67e-11`, `R=3.84e8`, `m1=5.97e24`, `m2=m1/4`, `omega=sqrt(G*(m1+m2)/R**3)` (≈2.96e-6 rad/s), satellite starts `y=u=v=0` with `x0/R ∈ {0.3, 0.5, 0.56}`, integration time two months (`60*24*3600 s`).
- Creators scripts are **reader-facing**: package-based, short, header comment naming the figures produced, no plumbing.
- Interactive assets self-hosted: one `python/_static/plotly.min.js`; plotly HTML files reference it as `../../plotly.min.js`. No CDN.
- Numbered `{figure}`/`{subfigure}` directives stay static; interactive iframes and code links are additions only.
- Windows/Git Bash; tooling via `C:/Users/mvr/cbenv2/Scripts/{python,pip,jupyter,sphinx-build}`. No `rm -rf`.
- Commits end with a blank line then `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.

---

### Task 1: `flows.threebody` and `flows.corotating`

**Files:**
- Modify: `src/chaosbook/flows.py`, `src/chaosbook/__init__.py`
- Test: `tests/test_flows.py` (extend)

**Interfaces:**
- Produces: `chaosbook.threebody(t, state, G=6.67e-11, m1=5.97e24, m2=1.4925e24, R=3.84e8)` — state `(x, y, u, v)`, returns 4 derivatives, inertial frame, primaries on circular orbits at `omega = sqrt(G*(m1+m2)/R**3)`; `chaosbook.corotating(x, y, t, omega)` → rotated coordinate arrays. Tasks 2–3 and the chapter use these exact names.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_flows.py`)

```python
from chaosbook import corotating, threebody
from scipy.integrate import solve_ivp


def test_threebody_reduces_to_kepler_when_moon_is_massless():
    # With m2 = 0 the satellite follows a circular Kepler orbit around m1.
    G, m1 = 6.67e-11, 5.97e24
    r0 = 1.0e8
    vc = np.sqrt(G * m1 / r0)
    period = 2 * np.pi * r0 / vc
    sol = solve_ivp(threebody, [0, period], [r0, 0, 0, vc],
                    args=(G, m1, 0.0), rtol=1e-10, atol=1e-3,
                    t_eval=np.linspace(0, period, 200))
    radius = np.sqrt(sol.y[0] ** 2 + sol.y[1] ** 2)
    assert np.allclose(radius, r0, rtol=1e-3)


def test_corotating_makes_the_primaries_stationary():
    G, m1, R = 6.67e-11, 5.97e24, 3.84e8
    m2 = m1 / 4
    omega = np.sqrt(G * (m1 + m2) / R**3)
    t = np.linspace(0, 5e6, 100)
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    xr, yr = corotating(x1, y1, t, omega)
    assert np.allclose(xr, -m2 * R / (m1 + m2))
    assert np.allclose(yr, 0, atol=1e-6 * R)
```

(`numpy` is already imported as `np` at the top of the file.)

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/test_flows.py -v`
Expected: FAIL — `ImportError: cannot import name 'threebody'`.

- [ ] **Step 2: Implement** (append to `src/chaosbook/flows.py`; add `import numpy as np` at the top of the module)

```python
def threebody(t, state, G=6.67e-11, m1=5.97e24, m2=1.4925e24, R=3.84e8):
    """The restricted three-body problem in the inertial frame.

    A massless satellite at (x, y) with velocity (u, v) moves in the
    gravitational field of two primaries (masses m1 and m2, separation R)
    that circle their common centre of mass at the Kepler frequency
    omega = sqrt(G (m1 + m2) / R^3). state = (x, y, u, v).
    """
    omega = np.sqrt(G * (m1 + m2) / R**3)
    x, y, u, v = state
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    x2 = m1 * R / (m1 + m2) * np.cos(omega * t)
    y2 = m1 * R / (m1 + m2) * np.sin(omega * t)
    d1 = np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    d2 = np.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
    return [u,
            v,
            G * m1 * (x1 - x) / d1**3 + G * m2 * (x2 - x) / d2**3,
            G * m1 * (y1 - y) / d1**3 + G * m2 * (y2 - y) / d2**3]


def corotating(x, y, t, omega):
    """Rotate inertial-frame coordinates into the frame co-rotating at omega."""
    c, s = np.cos(omega * t), np.sin(omega * t)
    return c * x + s * y, -s * x + c * y
```

Extend `src/chaosbook/__init__.py`: import line becomes `from .flows import lorenz, threebody, corotating` and add `"threebody", "corotating"` to `__all__`.

- [ ] **Step 3: Run the full suite**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -v`
Expected: 15 passed.

- [ ] **Step 4: Commit**

```bash
git add src/chaosbook/ tests/test_flows.py
git commit -m "chaosbook: restricted three-body flow and co-rotating transform"
```

---

### Task 2: Lorenz figures (static twins + interactive assets)

**Files:**
- Create: `creators/python/phenomenon/fig_lorenz.py`
- Create (generated, committed): `python/_static/phenomenon/phenomenon_lorenz_xt_series.png`, `phenomenon_lorenz_xt_two_series_em3.png`, `phenomenon_lorenz_xt_two_series_em5.png`, `phenomenon_lorenz_phasespace_close.png`, `phenomenon_lorenz_phasespace_far.png`, `python/_static/phenomenon/interactive/lorenz3d.html`, `python/_static/phenomenon/interactive/lorenz_sensitivity.html`
- Create: `python/_static/plotly.min.js` (copied from the plotly package)
- Modify: `requirements.txt` (append `plotly`)

**Interfaces:**
- Consumes: `cb.lorenz` from the package.
- Produces: the seven asset files above; Task 4's chapter references them by these exact paths.

- [ ] **Step 1: Install plotly and stage the shared bundle**

Append `plotly` to `requirements.txt`. Run:

```bash
"C:/Users/mvr/cbenv2/Scripts/pip" install plotly
"C:/Users/mvr/cbenv2/Scripts/python" -c "import plotly, shutil, pathlib; pathlib.Path('python/_static').mkdir(exist_ok=True); shutil.copy(pathlib.Path(plotly.__path__[0])/'package_data'/'plotly.min.js', 'python/_static/plotly.min.js'); print('copied')"
```

Expected: `copied`; `python/_static/plotly.min.js` exists (~4 MB).

- [ ] **Step 2: Write `creators/python/phenomenon/fig_lorenz.py`**

```python
"""Figures for the Lorenz section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_lorenz_xt_series.png          time series x(t)
  phenomenon_lorenz_xt_two_series_em3.png  sensitivity, epsilon = 1e-3
  phenomenon_lorenz_xt_two_series_em5.png  sensitivity, epsilon = 1e-5
  phenomenon_lorenz_phasespace_close.png   the butterfly attractor
  phenomenon_lorenz_phasespace_far.png     convergence onto the attractor
  interactive/lorenz3d.html                rotatable 3D attractor
  interactive/lorenz_sensitivity.html      divergence animation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "phenomenon"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def run(ic, tend, n=6000):
    return solve_ivp(cb.lorenz, [0, tend], ic,
                     t_eval=np.linspace(0, tend, n), rtol=1e-9)


# -- time series ------------------------------------------------------------
sol1 = run([2, 5, 5], 30)
plt.figure(figsize=(8, 3))
plt.plot(sol1.t, sol1.y[0], "b", linewidth=1)
plt.xlabel("t")
plt.ylabel("x")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_xt_series.png", dpi=150)
plt.close()

# -- sensitive dependence, epsilon = 1e-3 and 1e-5 --------------------------
for eps, name in [(1e-3, "em3"), (1e-5, "em5")]:
    sol2 = run([2 + eps, 5, 5], 30)
    plt.figure(figsize=(5, 3.2))
    plt.plot(sol1.t, sol1.y[0], "b", linewidth=1)
    plt.plot(sol2.t, sol2.y[0], "r", linewidth=1)
    plt.xlabel("t")
    plt.ylabel("x")
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_lorenz_xt_two_series_{name}.png", dpi=150)
    plt.close()

# -- phase space: the butterfly, and convergence onto it --------------------
solb = run([2, 5, 5], 40, n=12000)
ax = plt.figure(figsize=(5, 4)).add_subplot(projection="3d")
ax.plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_phasespace_close.png", dpi=150)
plt.close()

solf = run([100, 5, 5], 40, n=12000)
ax = plt.figure(figsize=(5, 4)).add_subplot(projection="3d")
ax.plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
ax.plot(solf.y[0], solf.y[1], solf.y[2], "r", linewidth=0.6)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_phasespace_far.png", dpi=150)
plt.close()

# -- interactive: rotatable attractor ---------------------------------------
fig = go.Figure(go.Scatter3d(
    x=solb.y[0], y=solb.y[1], z=solb.y[2], mode="lines",
    line=dict(width=2, color=solb.t, colorscale="Viridis"),
))
fig.update_layout(
    scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
    margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
)
fig.write_html(OUT / "interactive" / "lorenz3d.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

# -- interactive: divergence animation --------------------------------------
sol2 = run([2 + 1e-3, 5, 5], 30)
steps = np.linspace(2, len(sol1.t) - 1, 60).astype(int)
frames = [go.Frame(data=[
    go.Scatter(x=sol1.t[:k], y=sol1.y[0][:k], mode="lines",
               line=dict(color="blue")),
    go.Scatter(x=sol2.t[:k], y=sol2.y[0][:k], mode="lines",
               line=dict(color="red")),
]) for k in steps]
fig = go.Figure(data=frames[0].data, frames=frames)
fig.update_layout(
    xaxis=dict(range=[0, 30], title="t"),
    yaxis=dict(range=[-25, 25], title="x"),
    showlegend=False, margin=dict(l=40, r=10, t=10, b=40),
    updatemenus=[dict(type="buttons", x=1, y=1.15, xanchor="right",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=50,
                                                                redraw=False),
                                                     fromcurrent=True)])])],
)
fig.write_html(OUT / "interactive" / "lorenz_sensitivity.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_lorenz: all assets written to", OUT)
```

- [ ] **Step 3: Run it and verify against the Maple originals**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" creators/python/phenomenon/fig_lorenz.py`
Expected: exit 0, all 7 files exist. Then Read each generated PNG next to its Maple original (`maple/_static/phenomenon/<same name>.png`) and confirm the qualitative match (same trajectories/ranges; em3 diverges earlier than em5; far-IC trajectory converges onto the butterfly). Open the two HTML files' text to confirm they reference `../../plotly.min.js` and contain no CDN URL.

- [ ] **Step 4: Commit**

```bash
git add creators/python/phenomenon/fig_lorenz.py python/_static/phenomenon/ python/_static/plotly.min.js requirements.txt
git commit -m "Creators: Lorenz figures for the phenomenon chapter (static + interactive)"
```

---

### Task 3: Three-body figures (static twins + interactive asset)

**Files:**
- Create: `creators/python/phenomenon/fig_3body.py`
- Create (generated, committed): `python/_static/phenomenon/phenomenon_3body_example{1a,1b,2a,2b,3a,3b}.png`, `phenomenon_3body_example_sensitivity.png`, `python/_static/phenomenon/interactive/threebody.html`

**Interfaces:**
- Consumes: `cb.threebody`, `cb.corotating` from Task 1.
- Produces: the eight asset files above, referenced by Task 4's chapter.

- [ ] **Step 1: Write `creators/python/phenomenon/fig_3body.py`**

```python
"""Figures for the three-body section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_3body_example{1a,1b,2a,2b,3a,3b}.png   trajectories for
      x0/R = 0.3, 0.5, 0.56 in the inertial (a) and co-rotating (b) frames
  phenomenon_3body_example_sensitivity.png          two nearby trajectories
  interactive/threebody.html                        chaotic orbit animation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "phenomenon"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

G, m1, R = 6.67e-11, 5.97e24, 3.84e8
m2 = m1 / 4
omega = np.sqrt(G * (m1 + m2) / R**3)
TWO_MONTHS = 60 * 24 * 3600


def run(x0, tend=TWO_MONTHS, n=8000):
    return solve_ivp(cb.threebody, [0, tend], [x0, 0, 0, 0],
                     t_eval=np.linspace(0, tend, n), rtol=1e-10, atol=1.0)


def primaries(t):
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    x2 = m1 * R / (m1 + m2) * np.cos(omega * t)
    y2 = m1 * R / (m1 + m2) * np.sin(omega * t)
    return x1, y1, x2, y2


def draw(ax, xs, ys, xe, ye, xm, ym):
    ax.plot(xe, ye, "k", linewidth=2.5)          # earth: thick black
    ax.plot(xm, ym, color="gray", linewidth=1.5)  # moon: gray
    ax.plot(xs, ys, "k", linewidth=0.6)           # satellite: thin black
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")


for i, x0_over_R in enumerate([0.3, 0.5, 0.56], start=1):
    sol = run(x0_over_R * R)
    x1, y1, x2, y2 = primaries(sol.t)
    # (a) inertial frame
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw(ax, sol.y[0], sol.y[1], x1, y1, x2, y2)
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_3body_example{i}a.png", dpi=150)
    plt.close()
    # (b) co-rotating frame
    xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
    x1r, y1r = cb.corotating(x1, y1, sol.t, omega)
    x2r, y2r = cb.corotating(x2, y2, sol.t, omega)
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw(ax, xs, ys, x1r, y1r, x2r, y2r)
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_3body_example{i}b.png", dpi=150)
    plt.close()

# -- sensitivity: relative difference 1e-4 in x(0), two panels ---------------
sola = run(0.5 * R)
solb = run(0.5 * R * (1 + 1e-4))
x1, y1, x2, y2 = primaries(sola.t)
fig, axes = plt.subplots(2, 1, figsize=(4.8, 8.6))
for ax, rotate in zip(axes, [False, True]):
    for sol, color in [(sola, "b"), (solb, "r")]:
        xs, ys = sol.y[0], sol.y[1]
        if rotate:
            xs, ys = cb.corotating(xs, ys, sol.t, omega)
        ax.plot(xs, ys, color, linewidth=0.6)
        ax.plot(xs[0], ys[0], color + "d")   # diamond: initial location
        ax.plot(xs[-1], ys[-1], color + "o")  # circle: end position
    xe, ye = (cb.corotating(x1, y1, sola.t, omega) if rotate else (x1, y1))
    xm, ym = (cb.corotating(x2, y2, sola.t, omega) if rotate else (x2, y2))
    ax.plot(xe, ye, "k", linewidth=2.5)
    ax.plot(xm, ym, color="gray", linewidth=1.5)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_3body_example_sensitivity.png", dpi=150)
plt.close()

# -- interactive: chaotic orbit in the co-rotating frame ---------------------
sol = run(0.5 * R)
xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
xe = -m2 * R / (m1 + m2)
xm = m1 * R / (m1 + m2)
steps = np.linspace(2, len(sol.t) - 1, 80).astype(int)
frames = [go.Frame(data=[
    go.Scatter(x=xs[:k], y=ys[:k], mode="lines",
               line=dict(color="black", width=1)),
    go.Scatter(x=[xs[k]], y=[ys[k]], mode="markers",
               marker=dict(color="red", size=8)),
]) for k in steps]
fig = go.Figure(data=frames[0].data, frames=frames)
fig.add_trace(go.Scatter(x=[xe], y=[xm * 0], mode="markers+text",
                         marker=dict(color="blue", size=14), text=["earth"],
                         textposition="bottom center"))
fig.add_trace(go.Scatter(x=[xm], y=[0], mode="markers+text",
                         marker=dict(color="gray", size=9), text=["moon"],
                         textposition="bottom center"))
fig.update_layout(
    xaxis=dict(title="x [m]", scaleanchor="y"),
    yaxis=dict(title="y [m]"),
    showlegend=False, margin=dict(l=40, r=10, t=10, b=40),
    updatemenus=[dict(type="buttons", x=1, y=1.15, xanchor="right",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=40,
                                                                redraw=False),
                                                     fromcurrent=True)])])],
)
fig.write_html(OUT / "interactive" / "threebody.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_3body: all assets written to", OUT)
```

- [ ] **Step 2: Run it and verify against the Maple originals**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" creators/python/phenomenon/fig_3body.py`
Expected: exit 0, 8 files. Read each PNG next to `maple/_static/phenomenon/<same name>.png` and confirm: example1 orbits the earth, example2 wanders chaotically around both, example3 orbits the moon; co-rotating panels show the primaries stationary; sensitivity shows blue/red trajectories separating with diamond/circle markers. If a trajectory looks qualitatively wrong (e.g. escapes), first check tolerances (`rtol=1e-10`) before touching parameters — the parameters are fixed by the Global Constraints.

- [ ] **Step 3: Commit**

```bash
git add creators/python/phenomenon/fig_3body.py python/_static/phenomenon/
git commit -m "Creators: three-body figures for the phenomenon chapter (static + interactive)"
```

---

### Task 4: The converted chapter and exercises

**Files:**
- Create: `python/phenomenon.md`
- Create: `python/_includes/phenomenon_exercises.md`
- Create: `creators/python/phenomenon/ex_datasets.py` (+ generated `python/_static/exercises/set1.txt`, `set2.txt`, `set3.txt`)
- Copy: `maple/_static/phenomenon/3body.png` → `python/_static/phenomenon/3body.png`; `maple/_static/exercises/ex0036r03_fig1.png`, `dataset1.txt`, `dataset2.txt` → `python/_static/exercises/`
- Modify: `python/index.md`

**Interfaces:**
- Consumes: every asset from Tasks 2–3 (exact paths), `cb.lorenz`/`cb.threebody` naming.
- Produces: the chapter page pattern (code links, iframes) that the disc1d plan will replicate.

- [ ] **Step 1: Write `python/phenomenon.md`**

Copy `maple/phenomenon.md` and apply EXACTLY these edits — everything else stays byte-identical:

1. Replace line 17 (the "we start `maple` and load…" sentence) with:

```markdown
With a modern PC we can today easily retrace Lorenz' footsteps and experience ourselves the remarkably rich behaviour of his simple system as well as the sensitive dependence on initial conditions. To this end, we implement the system {eq}`eq:phenomenon_lorenz` in a few lines of Python using the `chaosbook` package — `cb.lorenz` is exactly the right-hand side above, and the {ref}`cookbook <app:cookbook>` shows the same computation written out in plain code:
```

2. Replace the first Maple admonition (lines 19–43) with:

````markdown
````{admonition} Python
:class: python

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import chaosbook as cb

# set the integration range and initial conditions
tstart, tend = 0, 30
ic1 = [2, 5, 5]
# solve the system (cb.lorenz has sigma=10, r=28, b=8/3 built in)
sol1 = solve_ivp(cb.lorenz, [tstart, tend], ic1,
                 t_eval=np.linspace(tstart, tend, 3000), rtol=1e-9)
# and plot the timeseries
plt.plot(sol1.t, sol1.y[0])
plt.xlabel("t")
plt.ylabel("x")
```
````
````

3. Line 45: "Running the entire worksheet produces" → "Running the script produces".

4. In the paragraph before the second code block, replace "removing the `#` symbols at the end of the worksheet activates the commands below, which produce plots like" with "adding the lines below produces plots like".

5. Replace the second Maple admonition (lines 56–69) with:

````markdown
````{admonition} Python
:class: python

```{code-block} python
epsilon = 1e-3
ic2 = [2 + epsilon, 5, 5]
sol2 = solve_ivp(cb.lorenz, [tstart, tend], ic2,
                 t_eval=np.linspace(tstart, tend, 3000), rtol=1e-9)
# plot 2 timeseries in one plot
plt.plot(sol1.t, sol1.y[0], "b")
plt.plot(sol2.t, sol2.y[0], "r")
plt.xlabel("t")
plt.ylabel("x")
```
````
````

6. Directly after the `fig:phenomenon_lorenz_xt_two_series` subfigure block, insert:

````markdown
```{raw} html
<p><em>Watch the divergence unfold — press play:</em></p>
<iframe src="_static/phenomenon/interactive/lorenz_sensitivity.html" width="100%" height="420" style="border:none;"></iframe>
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/phenomenon/fig_lorenz.py)*
:::
````

7. In the paragraph after that figure, replace "Increasing the working precision — for instance with `> Digits := 20;`, which instructs `maple` to use $20$ digits instead of the default $10$ — restores the divergence." with "Tightening the integration tolerances — for instance `solve_ivp(..., rtol=1e-12, atol=1e-12)`, which makes the solver track the true trajectory more closely — restores the divergence."

8. Replace the phase-space sentence ("Apart from analysing the time-series, much can be learned by studying the system in the 3d-*phase-space*. In `maple` this requires only a minor change of the plot command: `odeplot(...)` which gives a plot like {numref}`fig:phenomenon_lorenz_phasespace`.") with:

````markdown
Apart from analysing the time-series, much can be learned by studying the system in the 3d-*phase-space*. This requires only a minor change of the plotting commands, which gives a plot like {numref}`fig:phenomenon_lorenz_phasespace`:

````{admonition} Python
:class: python

```{code-block} python
ax = plt.figure().add_subplot(projection="3d")
ax.plot(sol1.y[0], sol1.y[1], sol1.y[2], linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
```
````
````

9. Directly after the `fig:phenomenon_lorenz_phasespace` subfigure block, insert:

````markdown
```{raw} html
<p><em>The attractor itself — drag to rotate, scroll to zoom:</em></p>
<iframe src="_static/phenomenon/interactive/lorenz3d.html" width="100%" height="520" style="border:none;"></iframe>
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/phenomenon/fig_lorenz.py)*
:::
````

10. Replace "See the file `LorenzSensitiveDependence.mws` for a worked-out maple-sheet. The Lorenz system will be studied in more detail in chapter {numref}`chap:cont3d`." with "The scripts behind these figures are linked beneath each of them. The Lorenz system will be studied in more detail later in the book."

11. Replace "…calculate numerically some possible trajectories with the aid of `maple` ." with "…calculate numerically some possible trajectories."

12. Replace "This reduction, from Newton's law {eq}`eq:phenomenon_3body_full` to the compact system below, is carried out step by step in Appendix {numref}`app:twobody`." with "This reduction, from Newton's law {eq}`eq:phenomenon_3body_full` to the compact system below, is carried out step by step in the book's two-body appendix."

13. Directly after the `fig:phenomenon_3body_some_examples` subfigure block, insert:

````markdown
```{raw} html
<p><em>The chaotic orbit in the co-rotating frame — press play:</em></p>
<iframe src="_static/phenomenon/interactive/threebody.html" width="100%" height="480" style="border:none;"></iframe>
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/phenomenon/fig_3body.py)*
:::
````

14. Replace "With use of `maple` we can however integrate the system numerically" with "We can however integrate the system numerically".

15. Replace "In the exercise  you can manipulate a `maple` -worksheet that contains an implementation of the three-body problem {eq}`…`." with "In the exercise you can experiment with an implementation of the three-body problem {eq}`eq:phenomenon_3body_simple1_m3_full__phenomenon`."

16. Directly after the `fig:phenomenon_3body_example_sensitivity` figure block, insert the same code-link pattern:

````markdown
:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/phenomenon/fig_3body.py)*
:::
````

17. The final `{include} _includes/phenomenon_exercises.md` stays.

- [ ] **Step 2: Write `python/_includes/phenomenon_exercises.md`**

```markdown
## Exercises

### Sensitive dependence on initial conditions in the Lorenz System

Study the Lorenz system

```{math}
:label: eq0035:lorenzx
\begin{aligned}
\dot{x} &= \sigma(y-x)\\
\dot{y} &= rx - y -xz\\
\dot{z} &= xy-bz
\end{aligned}
```

with the parameters given $r=28,b=8/3,\sigma=10$. Start from the script shown in this chapter (or build it yourself from the {ref}`cookbook <app:cookbook>` recipes).

a) Run the script once and have a look at the time series of $x(t)$.

b) Plot the time series of $y(t)$ instead of $x(t)$ (you only need to change `sol1.y[0]` to `sol1.y[1]`). Study also $z(t)$.

c) Change the time range by modifying `tstart` and `tend`.

d) Add the second initial condition from the chapter so that you can study simultaneously the system's behaviour for two different initial conditions. The difference between the initial values of $x$ is `epsilon`. Reduce the value of `epsilon` and observe the effect.

e) Reduce `epsilon` until the solutions are no longer different. Increase `tend` to make sure. Can you understand this seemingly critical value of `epsilon`?

f) Make a plot of the 3d-*phase-space* by plotting $(x(t),y(t),z(t))$ instead of $(t,x(t))$, as shown in the chapter.

g) If everything went well you saw a so-called "strange attractor". Why it is called *strange* will be dealt with later, but to see that the object is really attracting, change the initial condition $x(0) = 2$ to $x(0) = 100$ and look at the trajectories in phase-space. Study other initial conditions and verify that the trajectories converge upon the *attractor*.

### Classification of timeseries

**Downloads:** {download}`set1.txt <_static/exercises/set1.txt>`, {download}`set2.txt <_static/exercises/set2.txt>`, {download}`set3.txt <_static/exercises/set3.txt>`

Load the three data sets with `np.loadtxt` and study them. Find out which one is a: pure random noise, b: a one dimensional mapping, c: a higher order mapping. Explain your answer. (Hint: a return plot — $x_{n+1}$ against $x_n$ — reveals more than the time series.)

### Three body problem

Consider a satellite in space under influence of the gravitational pull of the earth and the moon.

```{figure} _static/exercises/ex0036r03_fig1.png
:name: fig:ex0036r03:ex0036r03_fig1
```

```{list-table}
:header-rows: 0
:class: noheader

* - gravitational constant
  - $G$
  - $6.67 \times 10^{-11}\ Nm^2 kg^{-1}$
* - distance between earth and moon
  - $R$
  - $3.84 \times 10^{8}\ m$
* - mass of earth
  - $m_1$
  - $5.97 \times 10^{24}\ kg$
* - mass of moon
  - $m_2$
  - $7.36 \times 10^{22}\ kg$
```

For simplicity, the orbits of earth and moon are assumed to be circular. Defining the position of the earth and moon as $\mathbf{x}_1$ and $\mathbf{x}_ 2$, respectively, and their mean distance as $R$, the motion is parametrized as

$$
\begin{gathered}
\mathbf{x}_1 =
 -r_1 \left[
 \begin{array}{c}
 \cos \omega t \\
 \sin \omega t
 \end{array} \right],\ \
 \mathbf{x}_2 =
 r_2 \left[
 \begin{array}{c}
 \cos \omega t \\
 \sin \omega t
 \end{array} \right], \\
 r_1 = R \frac{m_2}{m_1+m_2}, \ \ \
 r_2 = R \frac{m_1}{m_1+m_2}, \ \ \
 \omega = \sqrt{\frac{G(m_1+m_2)}{R^3} },
\end{gathered}
$$

where $r_1$ and  $r_2$ are the radii of earth and moon, and $\omega$ denotes the angular frequency. Using the law of gravitation $F=G\frac{m m'}{r^2}$, the motion of the satellite is governed by

$$
\mathbf{\ddot{x}} = G m_1 \frac{\mathbf{x}_1 - \mathbf{x}} {\left|\mathbf{x}_1 - \mathbf{x}\right|^3} + G m_2 \frac{\mathbf{x}_2 - \mathbf{x}} {\left|\mathbf{x}_2 - \mathbf{x}\right|^3}.
$$

Remarkably, this relatively simple system has very complex and rich behavior. `cb.threebody` implements this system (see the code linked beneath {numref}`fig:phenomenon_3body_some_examples`), and to magnify the chaotic behavior, we have increased the mass of the moon to $25 \%$ of the earth's mass.

a) Vary the satellite's initial position $x_0$ in the range $[-5\cdot10^8,5\cdot10^8]$ and determine for which interval the system behaves chaotic. Study also the system in a co-rotating reference frame (`cb.corotating`).

b) Check the sensitive dependence on initial conditions. Take $x_0=2 \times 10^8$ m and set the perturbation $\epsilon=1$ m. How many days does it take before there is a visual difference between the satellite's original and perturbed trajectory?

c) In reality the mass of the moon is a factor $81$ lower than the earth's. If you change this (`m2=7.36e22`), are there still chaotic trajectories? You may need to increase the initial velocity a bit.

### Attractor reconstruction

**Downloads:** {download}`dataset1.txt <_static/exercises/dataset1.txt>`, {download}`dataset2.txt <_static/exercises/dataset2.txt>`

a) Study the data set `dataset1.txt`, which consists of a one-dimensional time series $xx[1]\ldots xx[N]$, "measured" with a constant sampling rate (i.e. with a constant time interval). Try to reconstruct the attractor by making a three-dimensional plot of the points $(xx[j], xx[j+\Delta j], xx[j + 2\Delta j])$, for all possible $j$ (a 3d line plot, as used for the phase space in this chapter, works well). Change $\Delta j$ to get the best result.

b) Do the same for `dataset2.txt`, which has some additional noise superimposed.
```

Note the deliberate correction: the angular-frequency formula reads $\omega = \sqrt{G(m_1+m_2)/R^3}$ (the source had a stray factor 2 that contradicts both the chapter's $\omega = 2.96\cdot 10^{-6}$ and Kepler's law — do not copy it).

- [ ] **Step 3: Write `creators/python/phenomenon/ex_datasets.py`, run it, copy the static assets**

```python
"""Data sets for the "Classification of timeseries" exercise.

set1.txt  uniform random noise
set2.txt  a one-dimensional mapping (logistic, r = 3.9)
set3.txt  a higher-order mapping (Henon x-coordinate)
"""

from pathlib import Path

import numpy as np

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "exercises"
OUT.mkdir(parents=True, exist_ok=True)

N = 1000
rng = np.random.default_rng(seed=1)

np.savetxt(OUT / "set1.txt", rng.uniform(0, 1, N))

np.savetxt(OUT / "set2.txt", cb.orbit(cb.logistic, 0.4, N - 1, r=3.9))

x, y = np.zeros(N), np.zeros(N)
x[0], y[0] = 0.1, 0.1
for n in range(N - 1):
    x[n + 1] = 1 - 1.4 * x[n] ** 2 + y[n]
    y[n + 1] = 0.3 * x[n]
np.savetxt(OUT / "set3.txt", x)

print("ex_datasets: written to", OUT)
```

Run it, then copy the language-neutral assets:

```bash
"C:/Users/mvr/cbenv2/Scripts/python" creators/python/phenomenon/ex_datasets.py
cp maple/_static/phenomenon/3body.png python/_static/phenomenon/3body.png
cp maple/_static/exercises/ex0036r03_fig1.png maple/_static/exercises/dataset1.txt maple/_static/exercises/dataset2.txt python/_static/exercises/
```

- [ ] **Step 4: Update `python/index.md`**

Insert a Text toctree BEFORE the Cookbook toctree, and update the landing sentence "The Python edition is under construction. The cookbook — … — is available now; the chapters will follow." to "The Python edition is under construction. The first chapter and the cookbook are available; further chapters follow."

```markdown
```{toctree}
:hidden:
:numbered:
:caption: Text

phenomenon
```
```

(Write the toctree with a normal three-backtick fence in the actual file.)

- [ ] **Step 5: Build and verify**

Run: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -M html python build/python`
Expected: exit 0. Acceptable warnings: the pre-existing cookbook.pdf button link only — in particular NO warnings about missing figures, undefined references (`chap:cont3d` and `app:twobody` must no longer be referenced), or the includes. Open `build/python/html/phenomenon.html` and confirm: chapter renders with all figures, three iframes present, code links present, exercises included; grep the built page for "maple" (case-insensitive) → 0 hits.

- [ ] **Step 6: Commit**

```bash
git add python/ creators/python/phenomenon/ex_datasets.py
git commit -m "Python edition: add chapter 1 (A start at the end) with interactive figures"
```

---

### Task 5: Manifest, verification, publish

**Files:**
- Modify: `creators/porting_manifest.csv`
- Modify: none else expected

- [ ] **Step 1: Extend the porting manifest**

Add two columns `python_source,python_status` to the header of `creators/porting_manifest.csv` (append `,,` to every non-phenomenon row). For the 13 phenomenon figure rows, set `python_source` to `creators/python/phenomenon/fig_lorenz.py` or `fig_3body.py` as appropriate and `python_status` to `ported`. The hand-drawn `3body` row gets `copied from maple/_static,copied`. Rows for figures the Python chapter does not use (`phenomenon_3body_example_sensitivity_corot` if present as a separate row) get `merged into phenomenon_3body_example_sensitivity,ported`.

- [ ] **Step 2: Full verification**

Run: `"C:/Users/mvr/cbenv2/Scripts/python" -m pytest tests/ -q` → 15 passed.
Run: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -M html python build/python` → exit 0, warnings as in Task 4.
Run the PDF check: `"C:/Users/mvr/cbenv2/Scripts/sphinx-build" -b latex python build/python/latex` → exit 0 (the raw-html blocks emit nothing into LaTeX; the cookbook PDF target is unaffected — `latexmk` run optional since the chapter is not part of `latex_documents`).

- [ ] **Step 3: Commit and push**

```bash
git add creators/porting_manifest.csv
git commit -m "Creators: track phenomenon figures in the porting manifest"
git push
```

Then watch the Pages workflow (`gh run watch`) — build and deploy must both succeed; afterwards the chapter is live at `https://mvreeuwijk.github.io/chaosbook/python/phenomenon.html`.

---

## Self-review notes

- **Spec coverage** (pilot spec §1–5 for phenomenon): conversion model incl. verbatim prose + enumerated edits (Task 4 Step 1), ported exercises with the ω-typo fix documented (Step 2), hand-drawn/static asset copies (Step 3), toctree (Step 4); creators as published code with header comments + code links (Tasks 2–4); interactive companions — all three phenomenon rows of the spec's table (Tasks 2–3), self-hosted plotly (Task 2 Step 1); package additions generic-first with qualitative tests (Task 1: Kepler-limit and stationary-primaries tests); manifest columns (Task 5); CI untouched; push publishes (user-approved workflow).
- **Placeholder scan:** every file's full content present; commands carry expected outcomes.
- **Consistency:** `threebody(t, state, G, m1, m2, R)` signature identical in Task 1 (definition), tests (`args=(G, m1, 0.0)`), Task 3 (default use), and the exercise text (`m2=7.36e22` keyword). Asset paths in Task 4's edits match Tasks 2–3's outputs exactly.
