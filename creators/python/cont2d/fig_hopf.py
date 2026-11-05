"""Hopf bifurcation:  x' = -y - x(-mu + r^2),  y' = x - y(-mu + r^2).

Produces (in python/_static/cont2d/):
  cont2d_Hopf.png  3x2 figure: (a, b) x(t) at mu = -0.1 / +0.1, (c, d) phase
                   portraits of the same runs, (e, f) Re and Im of the
                   eigenvalues of J(0,0) versus mu
All runs start at (0.15, 0) and last to t = 100.
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

fig, axs = plt.subplots(3, 2, figsize=(bf.FULL_W, 5.4),
                        height_ratios=[0.8, 1.5, 0.9])

for k, mu in [(0, -0.1), (1, 0.1)]:
    f = lambda t, s: cb.hopf(t, s, mu=mu)
    t = np.linspace(0, 100, 4000)
    sol = solve_ivp(f, [0, 100], [0.15, 0], t_eval=t, rtol=1e-10, atol=1e-12)

    ax = axs[0, k]
    ax.plot(t, sol.y[0], "k-", lw=1.0)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.3, 0.3)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$x$")

    ax = axs[1, k]
    cb.phase_portrait(cb.hopf, (-0.5, 0.5), (-0.5, 0.5), ax=ax, n=20,
                      style="quiver", mu=mu)
    ax.plot(sol.y[0], sol.y[1], "k-", lw=1.5)
    ax.set_aspect("equal")
    print(f"mu = {mu}: final radius {np.hypot(sol.y[0,-1], sol.y[1,-1]):.4f}"
          f"  (sqrt(mu) = {np.sqrt(mu) if mu > 0 else float('nan'):.4f})")

mus = np.linspace(-1, 1, 400)
ev = np.array([np.linalg.eigvals(cb.jacobian(cb.hopf, [0, 0], mu=m)) for m in mus])
ev = np.array([e[np.argsort(-e.imag)] for e in ev])  # sigma_1 has Im > 0
# legend positions keep the entries off the curves (Im sigma_2 = -1 runs along
# the bottom of the ev2 panel)
for k, (vals, lab, lim, leg) in enumerate([
        (ev.real, r"$\mathrm{Re}(\sigma)$", None, dict(loc="lower right")),
        (ev.imag, r"$\mathrm{Im}(\sigma)$", (-1.5, 1.5),
         dict(loc="center right", bbox_to_anchor=(1.0, 0.33)))]):
    ax = axs[2, k]
    ax.plot(mus, vals[:, 0], "k-", lw=1.5, label=r"$\sigma_1$")
    ax.plot(mus, vals[:, 1], "k--", lw=1.5, label=r"$\sigma_2$")
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlim(-1, 1)
    if lim:
        ax.set_ylim(*lim)
    ax.set_xlabel(r"$\mu$")
    ax.set_ylabel(lab)
    ax.legend(**leg)
bf.panel_labels(axs)
bf.save(fig, OUT / "cont2d_Hopf.png")

print("fig_hopf: written to", OUT)
