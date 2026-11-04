"""Flows on the line: the graph of f(x), its fixed points and the evolution.

Produces (in python/_static/cont1d/):
  cont1d_simplecubic_graph.png        f(x) = x - x^3 with fixed points and flow arrows
  cont1d_simplecubic_evolution.png    x(t) from four initial conditions
  cont1d_generic_graphical_stable.png     f'(x*) < 0: all arrows point to x*
  cont1d_generic_graphical_unstable.png   f'(x*) > 0: all arrows point away
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb
from _common import PANEL, SQUARE, cross_axes, mark_fixed_points, save


def flow_arrows(ax, f, xs, dx):
    """Square marker on the graph, dashed drop line and an arrow on the axis."""
    for x0 in xs:
        y = f(x0)
        ax.plot([x0, x0], [0, y], "k--", lw=0.8)
        ax.plot(x0, y, "s", mfc="w", mec="k", ms=6, zorder=4, clip_on=False)
        ax.annotate("", (x0 + np.sign(y) * dx, 0), (x0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2,
                                    mutation_scale=14, shrinkA=0, shrinkB=0))


# -- x' = x - x^3 ------------------------------------------------------------
f = lambda x: x - x**3
fig, ax = plt.subplots(figsize=SQUARE)
x = np.linspace(-1.5, 1.5, 400)
ax.plot(x, f(x), "k", lw=1.5)
ax.set_xlim(-1.65, 1.65)
ax.set_ylim(-2.1, 2.1)
cross_axes(ax, "$x$", "$f(x)$", ticked=True)
ax.set_xticks([-1, -0.5, 0.5, 1])
ax.set_yticks([-1.5, -1, -0.5, 0.5, 1, 1.5])
flow_arrows(ax, f, [-1.5, -1.25, -0.75, -0.4, -0.1, 0.1, 0.4, 0.75, 1.25, 1.5], 0.12)
mark_fixed_points(ax, lambda x: f(x), -1.5, 1.5, dfdx=lambda x: 1 - 3 * x**2)
fig.tight_layout()
save(fig, "cont1d_simplecubic_graph")

fig, ax = plt.subplots(figsize=SQUARE)
for x0 in (-1.5, -0.1, 0.1, 1.5):
    sol = solve_ivp(lambda t, y: f(y), [0, 8], [x0], dense_output=True,
                    rtol=1e-9, atol=1e-12)
    t = np.linspace(0, 8, 400)
    ax.plot(t, sol.sol(t)[0], "k", lw=1.2)
ax.axhline(0, color="k", lw=0.6)
ax.set_xlabel("$t$")
ax.set_ylabel("$x(t)$")
ax.set_xlim(0, 8)
ax.set_ylim(-1.5, 1.5)
fig.tight_layout()
save(fig, "cont1d_simplecubic_evolution")

# -- generic stable / unstable fixed point -----------------------------------
for name, sgn in (("unstable", 1), ("stable", -1)):
    g = lambda x, sgn=sgn: sgn * (x**2 - 1)
    dg = lambda x, sgn=sgn: sgn * 2 * x
    fig, ax = plt.subplots(figsize=PANEL)
    x = np.linspace(0.4, 1.5, 200)
    ax.plot(x, g(x), "k", lw=2.5)
    ax.set_xlim(0, 1.6)
    ax.set_ylim(-1.1, 1.1)
    cross_axes(ax, "$x$", "$f(x)$")
    ax.set_yticks([0])
    flow_arrows(ax, g, [0.6, 0.8, 1.2, 1.4], 0.07)
    mark_fixed_points(ax, g, 0.4, 1.5, dfdx=dg)
    fig.tight_layout()
    save(fig, f"cont1d_generic_graphical_{name}")

print("fig_flow_basics: written")
