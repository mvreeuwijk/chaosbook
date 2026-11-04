"""Limit-cycle figures for "Two-dimensional continuous systems".

Produces (in python/_static/cont2d/):
  cont2d_Limit.png         1x2 figure: (a) x(t) for the system with limit cycle
                           r = 1, from (0.01, 0) (red) and (2, 0) (blue, dashed);
                           (b) the same two orbits in the phase plane
  cont2d_vdPol_phase.png   van der Pol oscillator, mu = 1, from (0.01, 0) and (3, -3)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)


def limit(t, s):
    """Limit-cycle system with r' = (1 - r^2)/4 and theta' = 1 exactly."""
    x, y = s
    k = (1 - x**2 - y**2) / (4 * np.hypot(x, y))
    return [-y + k * x, x + k * y]


def run(f, x0, tend, **kw):
    t = np.linspace(0, tend, 3000)
    return t, solve_ivp(f, [0, tend], x0, t_eval=t, rtol=1e-10, atol=1e-12, **kw).y


# -- limit cycle ---------------------------------------------------------------
t, a = run(limit, [0.01, 0], 30)
_, b = run(limit, [2, 0], 30)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.5),
                               width_ratios=[3, 2])
ax1.plot(t, a[0], "r-", label="1")
ax1.plot(t, b[0], "b--", label="2")
ax1.set_xlabel("$t$")
ax1.set_ylabel("$x(t)$")
ax1.set_xlim(0, 30)

cb.phase_portrait(limit, (-2.1, 2.1), (-2.1, 2.1), ax=ax2, n=16,
                  style="quiver")
ax2.plot(a[0], a[1], "r-", lw=1.5)
ax2.plot(b[0], b[1], "b--", lw=1.5)
ax2.set_aspect("equal")
bf.panel_labels([ax1, ax2])
bf.save(fig, OUT / "cont2d_Limit.png")

r_end = np.hypot(a[0, -1], a[1, -1]), np.hypot(b[0, -1], b[1, -1])
print("limit cycle: final radii from inside / outside =", r_end)

# -- van der Pol -----------------------------------------------------------------
plt.figure(figsize=bf.SQUARE)
ax = plt.gca()
cb.phase_portrait(cb.vanderpol, (-3, 3), (-3, 3), ax=ax, n=20, style="quiver",
                  mu=1.0)
for x0, st, col in [([0.01, 0], "-", "r"), ([3, -3], "--", "b")]:
    _, s = run(lambda t, q: cb.vanderpol(t, q, mu=1.0), x0, 20)
    ax.plot(s[0], s[1], col + st, lw=1.5)
bf.save(plt.gcf(), OUT / "cont2d_vdPol_phase.png")

print("fig_limit_cycles: written to", OUT)
