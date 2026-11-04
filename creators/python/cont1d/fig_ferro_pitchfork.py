"""Ferromagnet without external field: dx/dt = -x + tanh(x/T).

Produces (in python/_static/cont1d/):
  cont1d_ferro_pitchfork{1,2,3}.png     f(x) at T = 0.5, 1, 1.5
  cont1d_ferro_pitchfork.png            fixed-point branches x*(T) (all black)
  cont1d_ferro_pitchfork_stability.png  same, unstable branch gray
  cont1d_ferro_pitch_evolution{1,2}.png x(t) from 21 initial conditions, T = 0.5, 1.5
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb
from _common import (GRAY, PANEL, SQUARE, cross_axes, dferro, ferro,
                     mark_fixed_points, plot_branches, save)

# -- f(x) at three temperatures ----------------------------------------------
for k, T in enumerate((0.5, 1.0, 1.5), start=1):
    fig, ax = plt.subplots(figsize=SQUARE)
    x = np.linspace(-1.1, 1.1, 400)
    ax.plot(x, ferro(x, T=T), "k", lw=2.5)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.3, 0.3)
    cross_axes(ax, "$x$", "$f(x)$", ticked=True)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3])
    # at T = 1 the origin has f'(0) = 0 but is stable through the cubic term
    mark_fixed_points(ax, ferro, -1, 1, dfdx=dferro, marginal="stable", T=T)
    ax.set_title(f"$T={T:g}$")
    fig.tight_layout()
    save(fig, f"cont1d_ferro_pitchfork{k}")

# -- bifurcation diagrams ------------------------------------------------------
segs = cb.fixed_point_branches(ferro, "T", 0.01, 1.75, -1.1, 1.1,
                               shape=(900, 900), dfdx=dferro)
for name, colour in (("cont1d_ferro_pitchfork", False),
                     ("cont1d_ferro_pitchfork_stability", True)):
    fig, ax = plt.subplots(figsize=PANEL)
    if colour:
        plot_branches(ax, segs)
    else:
        for p, x, _ in segs:
            ax.plot(p, x, "k", lw=3)
    ax.set_xlim(0, 1.75)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("$T$")
    ax.set_ylabel("$x_{*}(T)$")
    ax.set_xticks([0, 0.5, 1, 1.5])
    fig.tight_layout()
    save(fig, name)

# -- time evolution from 21 initial conditions -----------------------------------
for k, T in enumerate((0.5, 1.5), start=1):
    fig, ax = plt.subplots(figsize=SQUARE)
    t = np.linspace(0, 25, 500)
    for x0 in np.linspace(-1, 1, 21):
        sol = solve_ivp(lambda t, y: ferro(y, T=T), [0, 25], [x0],
                        t_eval=t, rtol=1e-9, atol=1e-12)
        ax.plot(t, sol.y[0], "k", lw=1.2)
    ax.set_xlim(0, 25)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(f"$T={T:g}$")
    fig.tight_layout()
    save(fig, f"cont1d_ferro_pitch_evolution{k}")

print("fig_ferro_pitchfork: written")
