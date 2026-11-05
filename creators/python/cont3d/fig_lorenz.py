"""Lorenz figures of "Chaos in continuous systems" (time series, attractor,
maxima and the Lorenz map, Poincare section; the bifurcation diagram is in
fig_bifurcation.py).

Produces (in python/_static/cont3d/):
  cont3d_lorenz_time.png         time series x(t), r = 28
  cont3d_lorenz_attractors.png   (a) single trajectory, (b) four far-away
                                 starts converging onto it
  cont3d_lorenz_attractoryz.png  projection on the y-z plane
  cont3d_lorenz_zmax_map.png     (a) maxima z_n of z(t), (b) the Lorenz map
  cont3d_lorenz_poincare.png     Poincare section y = 0
  interactive/lorenz_poincare.html  rotatable attractor with the section
"""

from pathlib import Path

import sys

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

sigma, r, b = 10.0, 28.0, 8.0 / 3.0


def run(ic, tend, dt, t0=0.0):
    t = np.arange(t0, tend + dt / 2, dt)
    return solve_ivp(cb.lorenz, [0, tend], ic, t_eval=t, rtol=1e-10, atol=1e-12)


def save(name):
    bf.save(plt.gcf(), OUT / f"{name}.png")


# -- time series (full width) -------------------------------------------------
sol = run([2, 5, 5], 30, 0.01)
plt.figure(figsize=(bf.FULL_W, 2.2))
plt.plot(sol.t, sol.y[0], "k", lw=1)
plt.axhline(0, color="k", lw=0.5)
plt.xlabel("$t$")
plt.ylabel("$x$")
plt.xlim(0, 30)
save("cont3d_lorenz_time")

# -- attractor (a) and attraction from four far starts (b), one 1x2 figure ----
# explicit axes: constrained layout leaves wide empty bands around 3-D axes
fig = plt.figure(figsize=(bf.FULL_W, 2.7), layout="none")
ax_a = fig.add_axes([0.0, 0.0, 0.5, 1.0], projection="3d")
ax_b = fig.add_axes([0.5, 0.0, 0.5, 1.0], projection="3d")
sol = run([2, 5, 5], 60, 0.005)
m = sol.t >= 10
ax_a.plot(*sol.y[:, m], "k", lw=0.4)
ax_a.view_init(elev=22, azim=-67)
for dx, dz, col in [(-50, -100, "tab:blue"), (-50, 100, "tab:orange"),
                    (50, -100, "tab:red"), (50, 100, "k")]:
    s_ = run([2 + dx, 5, 5 + dz], 20, 0.004)
    ax_b.plot(*s_.y, color=col, lw=0.6)
ax_b.view_init(elev=11, azim=-108)
ax_b.set_xticks([-50, 0, 50]); ax_b.set_yticks([-100, 0, 100])  # uncrowded
for ax in (ax_a, ax_b):
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.set_box_aspect(None, zoom=0.88)
bf.panel_labels([ax_a, ax_b], loc=(0.04, 0.9), pad=(0, 0))
save("cont3d_lorenz_attractors")

# -- long run for projection, maxima and sections (N = 20000, dt = 0.01) ------
N, dt = 20000, 0.01
sol = run([2, 5, 5], (N - 1) * dt, dt)
t, x, y, z = sol.t, *sol.y

k = slice(14 * N // 32, 16 * N // 32 + 1)
plt.figure(figsize=bf.MEDIUM)
plt.plot(y[k], z[k], "k", lw=0.8)
plt.xlabel("$y$"); plt.ylabel("$z$")
save("cont3d_lorenz_attractoryz")

tm, zm = cb.maxima(t, z)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.5),
                               gridspec_kw=dict(width_ratios=[3, 2]))
ax1.plot(tm, zm, "kD", mfc="none", ms=3)
ax1.set_xlim(0, 200); ax1.set_ylim(25, 50)
ax1.set_xlabel("$t$"); ax1.set_ylabel("$z_n$")
ax2.plot(zm[9:-1], zm[10:], "kD", mfc="none", ms=3)
ax2.plot([25, 50], [25, 50], "k", lw=1)
ax2.set_xlim(25, 50); ax2.set_ylim(25, 50)
ax2.set_aspect("equal")
ax2.set_xlabel("$z_n$"); ax2.set_ylabel("$z_{n+1}$")
bf.panel_labels([ax1, ax2])
save("cont3d_lorenz_zmax_map")
print("Lorenz map: %d maxima, z in [%.2f, %.2f]" % (len(zm), zm.min(), zm.max()))

# -- Poincare section y = 0 (both directions), transient N/4 dropped ----------
tp, Xp = cb.poincare_section(cb.lorenz, [2, 5, 5], (N - 1) * dt, (1, 0.0),
                             discard=t[N // 4])
plt.figure(figsize=bf.SQUARE)
plt.plot(Xp[:, 0], Xp[:, 2], "kD", mfc="none", ms=3.5)
plt.xlabel("$x$"); plt.ylabel("$z$")
save("cont3d_lorenz_poincare")
print("Lorenz section y=0: %d crossings" % len(tp))

# -- interactive: attractor with the y = 0 section highlighted ----------------
s = run([2, 5, 5], 60, 0.01)
m = s.t >= 5
tp, Xp = cb.poincare_section(cb.lorenz, [2, 5, 5], 60, (1, 0.0), discard=5)
gx, gz = np.meshgrid([-22, 22], [0, 50])
fig = go.Figure([
    go.Scatter3d(x=s.y[0][m].round(3), y=s.y[1][m].round(3), z=s.y[2][m].round(3),
                 mode="lines", line=dict(width=2, color="royalblue"),
                 name="trajectory", hoverinfo="skip"),
    go.Scatter3d(x=Xp[:, 0].round(3), y=Xp[:, 1].round(3), z=Xp[:, 2].round(3),
                 mode="markers", marker=dict(size=4, color="crimson"),
                 name="y = 0 crossings"),
    go.Surface(x=gx, y=np.zeros_like(gx), z=gz, showscale=False, opacity=0.2,
               colorscale=[[0, "gray"], [1, "gray"]], hoverinfo="skip",
               name="section y = 0"),
])
fig.update_layout(scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
                  margin=dict(l=0, r=0, t=0, b=0),
                  legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)"))
fig.write_html(OUT / "interactive" / "lorenz_poincare.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)
print("fig_lorenz: done")
