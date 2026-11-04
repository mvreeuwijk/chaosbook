"""Hysteresis and hard bifurcations of the ferromagnet with m as parameter.

Produces (in python/_static/cont1d/):
  cont1d_ferro_field_hysteresis_T_{1_5,1_25,1_0,0_75,0_5}.png  branches x*(m)
  cont1d_ferro_field_hysdata_T_{...}.png     forward/backward sweeps of m
  cont1d_ferro_field_hysteresis_zoom.png     both combined at T = 0.5, with arrows
  cont1d_ferro_field_hysteresis_3d.png       the folded fixed-point surface
Branches: black = stable, gray = unstable.  Sweeps: integrate dx/dt to t = 100
at each of 201 values of m, starting from the previous end state.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import chaosbook as cb
from _common import GRAY, PANEL, SQUARE, dferro, ferro, plot_branches, save

TS = [(1.5, "1_5"), (1.25, "1_25"), (1.0, "1_0"), (0.75, "0_75"), (0.5, "0_5")]
MS = np.linspace(-1, 1, 201)


def branches(T):
    return cb.fixed_point_branches(ferro, "m", -1, 1, -1.4, 1.4,
                                   shape=(900, 900), dfdx=dferro, T=T)


def sweeps(T):
    up = cb.continuation_sweep(ferro, "m", MS, -1.0, tinf=100, T=T)
    down = cb.continuation_sweep(ferro, "m", MS[::-1], up[-1], tinf=100, T=T)
    return up, down


def decorate(ax, T):
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.4, 1.4)
    ax.set_xlabel("$m$")
    ax.set_ylabel("$x_{*}(m)$")
    ax.set_title(f"$T={T:g}$")


for T, tag in TS:
    fig, ax = plt.subplots(figsize=PANEL)
    plot_branches(ax, branches(T), lw=4)
    decorate(ax, T)
    fig.tight_layout()
    save(fig, f"cont1d_ferro_field_hysteresis_T_{tag}")

    up, down = sweeps(T)
    fig, ax = plt.subplots(figsize=PANEL)
    ax.plot(MS, up, "k", lw=3)
    ax.plot(MS[::-1], down, "k", lw=3)
    decorate(ax, T)
    fig.tight_layout()
    save(fig, f"cont1d_ferro_field_hysdata_T_{tag}")
    if T == 0.5:
        up5, down5 = up, down
        jump_up = MS[np.argmax(np.diff(up5)) + 1]
        jump_dn = MS[::-1][np.argmin(np.diff(down5)) + 1]
        print(f"T=0.5 sweeps: forward jump at m = {jump_up:+.3f}, "
              f"backward jump at m = {jump_dn:+.3f}")

# -- zoom: sweeps + branches + arrows at T = 0.5 -----------------------------------
T = 0.5
f_xm = lambda v: [ferro(v[0], T=T, m=v[1]), dferro(v[0], T=T, m=v[1])]
xc1, hc1 = fsolve(f_xm, [-1, 0.25])
xc2, hc2 = fsolve(f_xm, [1, -0.25])
print(f"T=0.5 folds: (m, x) = ({hc1:+.4f}, {xc1:+.4f}) and ({hc2:+.4f}, {xc2:+.4f})")

fig, ax = plt.subplots(figsize=SQUARE)
plot_branches(ax, branches(T), lw=2.5)
ax.plot(MS, up5, "k", lw=1.6, zorder=4)
ax.plot(MS[::-1], down5, "k", lw=1.6, zorder=4)
dx, dy = 0.1, 0.15
arrows = [(0.53, 1, dx, 0), (0.47, 1, -dx, 0), (0.93, 1, dx, 0), (0.87, 1, -dx, 0),
          (-0.53, -1, -dx, 0), (-0.47, -1, dx, 0), (-0.93, -1, -dx, 0), (-0.87, -1, dx, 0),
          (0.05, 0.97, -dx, -0.01), (-0.05, -0.97, dx, 0.01),
          (hc1, xc1 + 0.4, 0, dy), (hc1, -xc1 - 0.1, 0, dy),
          (hc2, xc2 - 0.4, 0, -dy), (hc2, -xc2 + 0.1, 0, -dy)]
for x0, y0, ddx, ddy in arrows:
    ax.annotate("", (x0 + ddx, y0 + ddy), (x0, y0), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color="k", mutation_scale=14,
                                shrinkA=0, shrinkB=0))
decorate(ax, T)
fig.tight_layout()
save(fig, "cont1d_ferro_field_hysteresis_zoom")

# -- 3-D view of the folded surface f(x, T, m) = 0 ---------------------------------
# solve f = 0 for m: m = T artanh(x) - x, so the surface is a graph over (x, T)
from scipy.optimize import brentq

Ts = np.linspace(0.5, 1.5, 90)
# x = tanh(u) gives m = T u - tanh(u); |m| = 1.1 is reached at x = +-tanh(u_lim)
u_lim = np.array([brentq(lambda u: T * u - np.tanh(u) - 1.1, 1.0, 10) for T in Ts])
s = np.linspace(-1, 1, 160)
X = np.tanh(u_lim[:, None] * s[None, :])
TT = Ts[:, None] * np.ones_like(X)
Mm = TT * np.arctanh(X) - X
fig = plt.figure(figsize=SQUARE)
ax = fig.add_subplot(projection="3d")
ax.plot_surface(TT, Mm, X, color="0.8", rcount=90, ccount=160, linewidth=0,
                antialiased=False, shade=True)
ax.set_xlim(0.5, 1.5)
ax.set_ylim(-1.1, 1.1)
ax.set_zlim(-1.2, 1.2)
ax.view_init(elev=24, azim=-55)
ax.set_box_aspect((1.1, 1.3, 1.1))
ax.set_axis_off()
ax.text(1.55, 1.2, 0, "$m$", fontsize=14)
ax.text(1.0, -1.45, -1.2, "$T$", fontsize=14)
ax.text(0.5, 1.0, 1.25, "$x$", fontsize=14)
fig.subplots_adjust(0, 0, 1, 1)
save(fig, "cont1d_ferro_field_hysteresis_3d")

print("fig_hysteresis: written")
