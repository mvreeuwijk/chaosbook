"""Lorenz figures of "Chaos in continuous systems" (time series, attractor,
maxima and the Lorenz map, Poincare section, bifurcation diagram).

Produces (in python/_static/cont3d/):
  cont3d_lorenz_time.png         time series x(t), r = 28
  cont3d_lorenz_attractor.png    single trajectory in (x, y, z)
  cont3d_lorenz_attraction.png   four far-away starts converging onto it
  cont3d_lorenz_attractoryz.png  projection on the y-z plane
  cont3d_lorenz_zmax.png         successive maxima z_n of z(t)
  cont3d_lorenz_map.png          the Lorenz map z_{n+1} versus z_n
  cont3d_lorenz_poincare.png     Poincare section y = 0
  cont3d_lorenz_bifurcation.png  maxima of z against r
  interactive/lorenz_poincare.html  rotatable attractor with the section
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

sigma, r, b = 10.0, 28.0, 8.0 / 3.0


def run(ic, tend, dt, t0=0.0):
    t = np.arange(t0, tend + dt / 2, dt)
    return solve_ivp(cb.lorenz, [0, tend], ic, t_eval=t, rtol=1e-10, atol=1e-12)


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


# -- time series (full width) -------------------------------------------------
sol = run([2, 5, 5], 30, 0.01)
plt.figure(figsize=(5.0, 3.5))
plt.plot(sol.t, sol.y[0], "k", lw=1)
plt.axhline(0, color="k", lw=0.5)
plt.xlabel("$t$")
plt.ylabel("$x$")
plt.xlim(0, 30)
save("cont3d_lorenz_time")

# -- attractor: single trajectory, t in [10, 60] ------------------------------
sol = run([2, 5, 5], 60, 0.005)
m = sol.t >= 10
fig = plt.figure(figsize=(4.2, 4.2))
ax = fig.add_subplot(projection="3d")
ax.plot(*sol.y[:, m], "k", lw=0.4)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.view_init(elev=22, azim=-67)
save("cont3d_lorenz_attractor")

# -- attraction: four far starts, t in [0, 20] --------------------------------
fig = plt.figure(figsize=(4.2, 4.2))
ax = fig.add_subplot(projection="3d")
for dx, dz, col in [(-50, -100, "tab:blue"), (-50, 100, "tab:orange"),
                    (50, -100, "tab:red"), (50, 100, "k")]:
    s = run([2 + dx, 5, 5 + dz], 20, 0.004)
    ax.plot(*s.y, color=col, lw=0.6)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.view_init(elev=11, azim=-108)
save("cont3d_lorenz_attraction")

# -- long run for projection, maxima and sections (N = 20000, dt = 0.01) ------
N, dt = 20000, 0.01
sol = run([2, 5, 5], (N - 1) * dt, dt)
t, x, y, z = sol.t, *sol.y

k = slice(14 * N // 32, 16 * N // 32 + 1)
plt.figure(figsize=(5.0, 3.5))
plt.plot(y[k], z[k], "k", lw=0.8)
plt.xlabel("$y$"); plt.ylabel("$z$")
save("cont3d_lorenz_attractoryz")

tm, zm = cb.maxima(t, z)
plt.figure(figsize=(5.0, 3.5))
plt.plot(tm, zm, "kD", mfc="none", ms=3)
plt.xlim(0, 200); plt.ylim(25, 50)
plt.xlabel("$t$"); plt.ylabel("$z_n$")
save("cont3d_lorenz_zmax")

plt.figure(figsize=(4.2, 4.2))
plt.plot(zm[9:-1], zm[10:], "kD", mfc="none", ms=3)
plt.plot([25, 50], [25, 50], "k", lw=1)
plt.xlim(25, 50); plt.ylim(25, 50)
plt.gca().set_aspect("equal")
plt.xlabel("$z_n$"); plt.ylabel("$z_{n+1}$")
save("cont3d_lorenz_map")
print("Lorenz map: %d maxima, z in [%.2f, %.2f]" % (len(zm), zm.min(), zm.max()))

# -- Poincare section y = 0 (both directions), transient N/4 dropped ----------
tp, Xp = cb.poincare_section(cb.lorenz, [2, 5, 5], (N - 1) * dt, (1, 0.0),
                             discard=t[N // 4])
plt.figure(figsize=(4.2, 4.2))
plt.plot(Xp[:, 0], Xp[:, 2], "kD", mfc="none", ms=3.5)
plt.xlabel("$x$"); plt.ylabel("$z$")
save("cont3d_lorenz_poincare")
print("Lorenz section y=0: %d crossings" % len(tp))

# -- bifurcation diagram of z-maxima against r (batch RK4 over all r) ---------
def lorenz_batch(X, rr):
    x_, y_, z_ = X
    return np.array([sigma * (y_ - x_), rr * x_ - y_ - x_ * z_, x_ * y_ - b * z_])


def rk4(X, rr, h):
    k1 = lorenz_batch(X, rr)
    k2 = lorenz_batch(X + h / 2 * k1, rr)
    k3 = lorenz_batch(X + h / 2 * k2, rr)
    k4 = lorenz_batch(X + h * k3, rr)
    return X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


rs = np.linspace(0.05, 30, 600)
h = 0.01
# start close to the non-zero fixed point (it exists for r > 1); the origin
# otherwise. This avoids the long chaotic transients that exist below r_c.
fp = np.sqrt(b * np.maximum(rs - 1, 0))
X = np.array([fp + 0.1, fp + 0.1, np.maximum(rs - 1, 0) + 0.1])
for _ in range(int(500 / h)):
    X = rk4(X, rs, h)
Z = np.empty((int(100 / h), len(rs)))
for i in range(Z.shape[0]):
    X = rk4(X, rs, h)
    Z[i] = X[2]
pts_r, pts_z = [], []
for j, rr in enumerate(rs):
    col = Z[:, j]
    _, zmx = cb.maxima(np.arange(len(col)) * h, col)
    if len(zmx) < 3:                       # settled on a fixed point
        zmx = [col[-1]]
    pts_r += [rr] * len(zmx)
    pts_z += list(zmx)
plt.figure(figsize=(4.2, 3.2))
plt.plot(pts_r, pts_z, "k.", ms=1.2)
rc = sigma * (sigma + b + 3) / (sigma - b - 1)
plt.xlabel("$r$"); plt.ylabel("$z$")
plt.xlim(0, 30); plt.ylim(0, 52)
save("cont3d_lorenz_bifurcation")
print("Lorenz critical r_c = %.4f" % rc)

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
