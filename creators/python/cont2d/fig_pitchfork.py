"""Pitchfork bifurcation in two dimensions:  x' = (mu - 2) x + y + sin x,  y' = x - y.

Produces (in python/_static/cont2d/):
  cont2d_pitchfork.png  2x2 figure: (a) phase portrait at mu = -0.1 (one stable
                        node), (b) phase portrait at mu = +0.1 (saddle + two
                        nodes), (c) fixed points x* versus mu, (d) eigenvalues
                        of J(0,0) versus mu (both real)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)


def pitchfork(t, s, mu=0.0):
    x, y = s
    return [(mu - 2) * x + y + np.sin(x), x - y]


ics = [(-2, 0), (2, 0), (-2, 2), (2, -2)]
colors = ["r", "b", "g", "c"]

fig, axs = plt.subplots(2, 2, figsize=(bf.FULL_W, 4.8))

for k, mu in [(0, -0.1), (1, 0.1)]:
    ax = axs[0, k]
    cb.phase_portrait(pitchfork, (-2, 2), (-2, 2), ax=ax, n=21, style="quiver",
                      trajectories=ics, tmax=100, colors=colors, lw=1.5, mu=mu)
    if mu > 0:
        # non-trivial fixed points (x*, x*) with (mu - 1) x + sin x = 0
        xs = brentq(lambda x: (mu - 1) * x + np.sin(x), 0.3, 2.0)
        ax.plot([0], [0], "o", mfc="w", mec="k", ms=7, mew=1.0)
        ax.plot([xs, -xs], [xs, -xs], "ko", ms=7)
        print(f"mu = {mu}: nontrivial fixed points at +-({xs:.10f}, {xs:.10f})")
    else:
        ax.plot([0], [0], "ko", ms=7)
    ax.set_aspect("equal")

# fixed points: (mu - 1) x* + sin x* = 0  <=>  mu = 1 - sin(x*)/x*
x = np.linspace(-10, 10, 2001)
x = x[x != 0]
ax = axs[1, 0]
ax.plot(1 - np.sin(x) / x, x, "k-", lw=1.5)
ax.axhline(0, color="k", lw=1.5)
ax.set_xlim(-1, 2)
ax.set_ylim(-10, 10)
ax.set_xlabel(r"$\mu$")
ax.set_ylabel(r"$x^*$")

# eigenvalues of the Jacobian at the origin
mus = np.linspace(-1, 2, 400)
ev = np.array([np.sort(np.linalg.eigvals(cb.jacobian(pitchfork, [0, 0], mu=m)).real)[::-1]
               for m in mus])
ax = axs[1, 1]
ax.plot(mus, ev[:, 0], "k-", lw=1.5, label=r"$\sigma_1$")
ax.plot(mus, ev[:, 1], "k--", lw=1.5, label=r"$\sigma_2$")
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel(r"$\mu$")
ax.set_ylabel(r"$\mathrm{Re}(\sigma)$")
ax.set_xlim(-1, 2)
ax.legend(loc="center right")
bf.panel_labels(axs)
bf.save(fig, OUT / "cont2d_pitchfork.png")

# analytic check: sigma = -1 + mu/2 +- sqrt(4 + mu^2)/2
m = 0.7
print("sigma(mu=0.7): numerical", np.sort(np.linalg.eigvals(cb.jacobian(pitchfork, [0, 0], mu=m)).real),
      " formula", np.sort([-1 + m / 2 - np.sqrt(4 + m**2) / 2, -1 + m / 2 + np.sqrt(4 + m**2) / 2]))
print("fig_pitchfork: written to", OUT)
