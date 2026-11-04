"""Shift-map and tent-map figures for "Chaos in Iterative Maps".

The shift and tent maps discard one binary digit per iteration, so
double-precision orbits collapse to exactly 0 after ~52 steps — itself a
neat illustration of the chapter's round-off story. To draw 400
meaningful steps we iterate in extended precision with mpmath.

Produces (in python/_static/disc1d/):
  disc1d_shiftmap_series_return.png, disc1d_tentmap_series_return.png
  (1x2: series (a) and return plot (b))
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpmath import mp, mpf

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

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
    fig, (axs, axr) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.4),
                                   width_ratios=[3, 2])
    axs.plot(range(N + 1), Y, "o", markersize=2)
    axs.set_xlabel("$n$")
    axs.set_ylabel(f"${label}_n$")
    axr.plot(Y[:-1], Y[1:], "o", markersize=2)
    axr.set_xlabel(f"${label}_n$")
    axr.set_ylabel(f"${label}_{{n+1}}$")
    axr.set_aspect("equal")
    bf.panel_labels([axs, axr])
    bf.save(fig, OUT / f"disc1d_{name}_series_return.png")

print("fig_shift_tent: assets written to", OUT)
