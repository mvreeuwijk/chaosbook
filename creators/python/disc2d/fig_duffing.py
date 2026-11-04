"""Duffing-map figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_Duffing_series1.png / _phase1.png   a = 2.52, b = 0.1, x0 = y0 = 1
  disc2d_Duffing_series2.png / _phase2.png   a = 2.77, b = 0.1, x0 = y0 = 1
  disc2d_Duffing_bifurx.png / _bifury.png    bifurcation diagrams in a, b = 0.1
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)

b, N = 0.1, 5000

# -- time series and phase plots ---------------------------------------------
for k, (a, lim) in enumerate([(2.52, (0.5, 1.5)), (2.77, (-1.8, 1.8))], start=1):
    X = cb.orbit(cb.duffing_map, x0=(1.0, 1.0), n=N, a=a, b=b)

    plt.figure(figsize=(4.2, 3.2))
    plt.plot(np.arange(N + 1), X[:, 0], "k.", markersize=1.5)
    plt.xlim(0, N)
    plt.ylim(*lim)
    plt.xlabel("$n$")
    plt.ylabel("$x_n$")
    plt.tight_layout()
    plt.savefig(OUT / f"disc2d_Duffing_series{k}.png", dpi=150)
    plt.close()

    plt.figure(figsize=(4.2, 4.2))
    plt.plot(X[:, 0], X[:, 1], "k.", markersize=1.5)
    plt.xlim(*lim)
    plt.ylim(*lim)
    plt.xlabel("$x_n$")
    plt.ylabel("$y_n$")
    plt.tight_layout()
    plt.savefig(OUT / f"disc2d_Duffing_phase{k}.png", dpi=150)
    plt.close()

# -- bifurcation diagrams: 400 iterations from (0.1, 0.1), keep the last half --
Nb, Na, amin, amax = 400, 400, 0.0, 2.75
A, BX, BY = [], [], []
for i in range(1, Na + 1):
    a = amin + (amax - amin) * i / Na
    X = cb.orbit(cb.duffing_map, x0=(0.1, 0.1), n=Nb, a=a, b=b)[Nb // 2:]
    A.extend([a] * len(X))
    BX.extend(X[:, 0])
    BY.extend(X[:, 1])

for data, ylab, name in [(BX, "$x(a)$", "bifurx"), (BY, "$y(a)$", "bifury")]:
    plt.figure(figsize=(5.0, 3.5))
    plt.plot(A, data, "k.", markersize=1)
    plt.xlim(0, amax)
    plt.xlabel("$a$")
    plt.ylabel(ylab)
    plt.tight_layout()
    plt.savefig(OUT / f"disc2d_Duffing_{name}.png", dpi=150)
    plt.close()

print("fig_duffing: assets written to", OUT)
