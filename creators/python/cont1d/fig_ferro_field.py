"""Ferromagnet with an external field m: dx/dt = -x + tanh((x+m)/T).

Produces (in python/_static/cont1d/):
  cont1d_ferro_field_bifurcation.png   (a)-(c) f(x) at T = 0.5, Tc, 1.5 for m = 0.1;
                                       (d) branches x*(T), m = 0.1; (e) m = 0.005
Also prints the critical point (xc, Tc) of the saddle-node for m = 0.1.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import chaosbook as cb
from _common import (bf, cross_axes, dferro, ferro, mark_fixed_points,
                     plot_branches, save)

m = 0.1
# critical point of the saddle-node: f = 0 and f' = 0 simultaneously
xc, Tc = fsolve(lambda v: [ferro(v[0], T=v[1], m=m), dferro(v[0], T=v[1], m=m)],
                [-0.5, 0.7])
print(f"critical point for m = {m}:  Tc = {Tc:.4f},  xc = {xc:.4f}")

fig = plt.figure(figsize=(bf.FULL_W, 4.4))
gs = fig.add_gridspec(2, 6, height_ratios=[1, 1])
axs = [fig.add_subplot(gs[0, 2 * k:2 * k + 2]) for k in range(3)]
axs += [fig.add_subplot(gs[1, 0:3]), fig.add_subplot(gs[1, 3:6])]

for k, (ax, T) in enumerate(zip(axs[:3], (0.5, Tc, 1.5)), start=1):
    x = np.linspace(-1.1, 1.1, 400)
    ax.plot(x, ferro(x, T=T, m=m), "k", lw=2)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.5, 0.5)
    cross_axes(ax, "$x$", "$f(x)$", ticked=True)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-0.4, -0.2, 0, 0.2, 0.4])
    if k == 2:      # at Tc the fixed points collide; draw the double root by hand
        mark_fixed_points(ax, ferro, 0.0, 1, dfdx=dferro, size=6, T=T, m=m)
        ax.plot(xc, 0, "o", ms=6, mfc="k", mec="k", mfcalt="w", fillstyle="right",
                zorder=5)
    else:
        mark_fixed_points(ax, ferro, -1, 1, dfdx=dferro, size=6, T=T, m=m)
    ax.set_title("$T=0.729$" if k == 2 else f"$T={T:g}$")

for ax, mm in zip(axs[3:], (0.1, 0.005)):
    segs = cb.fixed_point_branches(ferro, "T", 0.01, 1.75, -1.1, 1.1,
                                   shape=(900, 900), dfdx=dferro, m=mm)
    plot_branches(ax, segs, lw=3)
    ax.set_xlim(0, 1.75)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("$T$")
    ax.set_ylabel("$x_{*}(T)$")
    ax.set_xticks([0, 0.5, 1, 1.5])
    ax.set_title(f"$m={mm:g}$")
bf.panel_labels(axs)
save(fig, "cont1d_ferro_field_bifurcation")

print("fig_ferro_field: written")
