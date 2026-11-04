"""Duffing-map figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_Duffing_series_phase.png  2x2: series and phase plot for a = 2.52
                                   (top) and a = 2.77 (bottom), b = 0.1,
                                   x0 = y0 = 1
  disc2d_Duffing_bifurx.png        bifurcation diagram in a, b = 0.1
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)

b, N = 0.1, 5000

# -- time series and phase plots: one figure, rows a = 2.52 and 2.77 ---------
fig, axs = plt.subplots(2, 2, figsize=(bf.FULL_W, 4.4),
                        gridspec_kw=dict(width_ratios=[3, 2]))
for k, (a, lim) in enumerate([(2.52, (0.5, 1.5)), (2.77, (-1.8, 1.8))]):
    X = cb.orbit(cb.duffing_map, x0=(1.0, 1.0), n=N, a=a, b=b)
    ax = axs[k, 0]
    ax.plot(np.arange(N + 1), X[:, 0], "k.", markersize=1.5)
    ax.set_xlim(0, N)
    ax.set_ylim(*lim)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$x_n$")
    ax = axs[k, 1]
    ax.plot(X[:, 0], X[:, 1], "k.", markersize=1.5)
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$y_n$")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc2d_Duffing_series_phase.png")

# -- bifurcation diagrams: 400 iterations from (0.1, 0.1), keep the last half --
Nb, Na, amin, amax = 400, 400, 0.0, 2.75
A, BX, BY = [], [], []
for i in range(1, Na + 1):
    a = amin + (amax - amin) * i / Na
    X = cb.orbit(cb.duffing_map, x0=(0.1, 0.1), n=Nb, a=a, b=b)[Nb // 2:]
    A.extend([a] * len(X))
    BX.extend(X[:, 0])
    BY.extend(X[:, 1])

fig, ax = plt.subplots(figsize=(3.8, 2.4))
ax.plot(A, BX, "k.", markersize=1)
ax.set_xlim(0, amax)
ax.set_xlabel("$a$")
ax.set_ylabel("$x(a)$")
bf.save(fig, OUT / "disc2d_Duffing_bifurx.png")

print("fig_duffing: assets written to", OUT)
