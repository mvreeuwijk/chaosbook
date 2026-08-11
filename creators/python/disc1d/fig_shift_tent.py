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
