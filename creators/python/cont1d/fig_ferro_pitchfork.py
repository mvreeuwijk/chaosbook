"""Ferromagnet without external field: dx/dt = -x + tanh(x/T).

Produces (in python/_static/cont1d/):
  cont1d_ferro_pitchfork.png            (a)-(c) f(x) at T = 0.5, 1, 1.5; (d) branches
                                        x*(T), all black; (e) same, unstable gray
  cont1d_ferro_pitch_evolution.png      x(t) from 21 initial conditions, T = 0.5, 1.5
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb
from _common import (bf, cross_axes, dferro, ferro, mark_fixed_points,
                     plot_branches, save)

# -- (a)-(c) f(x) at three temperatures, (d)-(e) bifurcation diagrams ----------
fig = plt.figure(figsize=(bf.FULL_W, 4.4))
gs = fig.add_gridspec(2, 6, height_ratios=[1, 1])
axs = [fig.add_subplot(gs[0, 2 * k:2 * k + 2]) for k in range(3)]
axs += [fig.add_subplot(gs[1, 0:3]), fig.add_subplot(gs[1, 3:6])]

for ax, T in zip(axs[:3], (0.5, 1.0, 1.5)):
    x = np.linspace(-1.1, 1.1, 400)
    ax.plot(x, ferro(x, T=T), "k", lw=2)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.3, 0.3)
    cross_axes(ax, "$x$", "$f(x)$", ticked=True)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
    # at T = 1 the origin has f'(0) = 0 but is stable through the cubic term
    mark_fixed_points(ax, ferro, -1, 1, dfdx=dferro, marginal="stable", size=6, T=T)
    ax.set_title(f"$T={T:g}$")

segs = cb.fixed_point_branches(ferro, "T", 0.01, 1.75, -1.1, 1.1,
                               shape=(900, 900), dfdx=dferro)
for ax, colour in zip(axs[3:], (False, True)):
    if colour:
        plot_branches(ax, segs, lw=3)
    else:
        for p, x, _ in segs:
            ax.plot(p, x, "k", lw=3)
    ax.set_xlim(0, 1.75)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("$T$")
    ax.set_ylabel("$x_{*}(T)$")
    ax.set_xticks([0, 0.5, 1, 1.5])
bf.panel_labels(axs)
save(fig, "cont1d_ferro_pitchfork")

# -- time evolution from 21 initial conditions -----------------------------------
fig, axs = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.6), sharey=True)
t = np.linspace(0, 25, 500)
for ax, T in zip(axs, (0.5, 1.5)):
    for x0 in np.linspace(-1, 1, 21):
        sol = solve_ivp(lambda t, y: ferro(y, T=T), [0, 25], [x0],
                        t_eval=t, rtol=1e-9, atol=1e-12)
        ax.plot(t, sol.y[0], "k", lw=0.8)
    ax.set_xlim(0, 25)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("$t$")
    ax.set_title(f"$T={T:g}$")
axs[0].set_ylabel("$x(t)$")
bf.panel_labels(axs)
save(fig, "cont1d_ferro_pitch_evolution")

print("fig_ferro_pitchfork: written")
