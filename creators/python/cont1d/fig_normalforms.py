"""Normal forms of the 1-D bifurcations: pitchfork, subcritical pitchfork,
saddle-node and transcritical.

Produces (in python/_static/cont1d/):
  cont1d_bifur_pitchfork{1,2,3}.png, cont1d_bifur_pitchfork.png
  cont1d_bifur_pitchfork_sub{1,2,3}.png, cont1d_bifur_pitchfork_sub.png
  cont1d_bifur_saddle{1,2,3}.png, cont1d_bifur_saddle.png
  cont1d_bifur_transcrit{1,2,3}.png, cont1d_bifur_transcrit.png
Panels 1-3 are f(x) for r<0, r=0, r>0 with the fixed points marked
(filled = stable, open = unstable, half = marginal); the last figure is the
bifurcation diagram x*(r), black = stable, gray = unstable.
"""

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb
from _common import (PANEL, SQUARE, cross_axes, mark_fixed_points,
                     plot_branches, save)

R = 1.25  # |r| used in the panels (as in the original figures)

SYSTEMS = {
    # name: (f, df/dx, xmax, ylim, rs shown as (r<0, r=0, r>0), diagram (rlim, xlim))
    "pitchfork": dict(
        f=lambda x, r: r * x - x**3, df=lambda x, r: r - 3 * x**2,
        xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), rs=(-R, 0, R),
        diag=((-1, 1), (-1.1, 1.1))),
    "pitchfork_sub": dict(
        f=lambda x, r: r * x + x**3, df=lambda x, r: r + 3 * x**2,
        xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), rs=(-R, 0, R),
        diag=((-1, 1), (-1.1, 1.1))),
    "saddle": dict(
        f=lambda x, r: r - x**2, df=lambda x, r: -2 * x,
        xlim=(-1.4, 1.4), ylim=(-2, 1), rs=(-0.5, 0, 0.5),
        diag=((-1, 1), (-1, 1))),
    "transcrit": dict(
        f=lambda x, r: r * x - x**2, df=lambda x, r: r - 2 * x,
        xlim=(-2.8, 2.8), ylim=(-3.64, 1.96), rs=(-R, 0, R),
        diag=((-1, 1), (-1, 1))),
}
TITLES = ("$r<0$", "$r=0$", "$r>0$")

for name, s in SYSTEMS.items():
    f, df = s["f"], s["df"]
    for k, (r, title) in enumerate(zip(s["rs"], TITLES), start=1):
        fig, ax = plt.subplots(figsize=SQUARE)
        x = np.linspace(*s["xlim"], 400)
        ax.plot(x, f(x, r), "k", lw=2.5)
        ax.set_xlim(*s["xlim"])
        ax.set_ylim(*s["ylim"])
        cross_axes(ax, "$x$", "$f(x)$")
        mark_fixed_points(ax, f, *s["xlim"], dfdx=df, r=r)
        ax.set_title(title)
        fig.tight_layout()
        save(fig, f"cont1d_bifur_{name}{k}")

    # bifurcation diagram: zero level set of f(x, r), coloured by sign of f'
    (r0, r1), (x0, x1) = s["diag"]
    segs = cb.fixed_point_branches(f, "r", r0, r1, x0, x1, shape=(800, 800), dfdx=df)
    fig, ax = plt.subplots(figsize=PANEL)
    plot_branches(ax, segs)
    ax.set_xlim(r0, r1)
    ax.set_ylim(x0, x1)
    cross_axes(ax, "$r$", "$x_*(r)$", zero=True)
    fig.tight_layout()
    save(fig, f"cont1d_bifur_{name}")

print("fig_normalforms: written")
