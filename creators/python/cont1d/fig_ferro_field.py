"""Ferromagnet with an external field m: dx/dt = -x + tanh((x+m)/T).

Produces (in python/_static/cont1d/):
  cont1d_ferro_field_bifurcation{1,2,3}.png   f(x) at T = 0.5, Tc, 1.5 for m = 0.1
  cont1d_ferro_field_bifurcation_large_m.png  branches x*(T), m = 0.1
  cont1d_ferro_field_bifurcation_small_m.png  branches x*(T), m = 0.005
Also prints the critical point (xc, Tc) of the saddle-node for m = 0.1.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import chaosbook as cb
from _common import (PANEL, SQUARE, cross_axes, dferro, ferro,
                     mark_fixed_points, plot_branches, save)

m = 0.1
# critical point of the saddle-node: f = 0 and f' = 0 simultaneously
xc, Tc = fsolve(lambda v: [ferro(v[0], T=v[1], m=m), dferro(v[0], T=v[1], m=m)],
                [-0.5, 0.7])
print(f"critical point for m = {m}:  Tc = {Tc:.4f},  xc = {xc:.4f}")

for k, T in enumerate((0.5, Tc, 1.5), start=1):
    fig, ax = plt.subplots(figsize=SQUARE)
    x = np.linspace(-1, 1, 400)
    ax.plot(x, ferro(x, T=T, m=m), "k", lw=2.5)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.5, 0.5)
    cross_axes(ax, "$x$", "$f(x)$", ticked=True)
    ax.set_xticks([-1, -0.5, 0.5, 1])
    ax.set_yticks([-0.4, -0.2, 0.2, 0.4])
    if k == 2:      # at Tc the fixed points collide; draw the double root by hand
        mark_fixed_points(ax, ferro, 0.0, 1, dfdx=dferro, T=T, m=m)
        ax.plot(xc, 0, "o", ms=8, mfc="k", mec="k", mfcalt="w", fillstyle="right",
                zorder=5)
    else:
        mark_fixed_points(ax, ferro, -1, 1, dfdx=dferro, T=T, m=m)
    ax.set_title("$T=0.729$" if k == 2 else f"$T={T:g}$")
    fig.tight_layout()
    save(fig, f"cont1d_ferro_field_bifurcation{k}")

for name, mm in (("large_m", 0.1), ("small_m", 0.005)):
    segs = cb.fixed_point_branches(ferro, "T", 0.01, 1.75, -1.1, 1.1,
                                   shape=(900, 900), dfdx=dferro, m=mm)
    fig, ax = plt.subplots(figsize=PANEL)
    plot_branches(ax, segs)
    ax.set_xlim(0, 1.75)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("$T$")
    ax.set_ylabel("$x_*(T)$")
    ax.set_xticks([0, 0.5, 1, 1.5])
    ax.set_title(f"$m={mm:g}$")
    fig.tight_layout()
    save(fig, f"cont1d_ferro_field_bifurcation_{name}")

print("fig_ferro_field: written")
