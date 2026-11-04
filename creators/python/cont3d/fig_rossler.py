"""Rossler figures: period-doubling route, return map, bifurcation diagram.

System: x' = -y - z, y' = x + a y, z' = b + z (x - c), a = 0.432, b = 2.

Produces (in python/_static/cont3d/):
  cont3d_rosslerperiod{1..4}a.png  attractor for c = 3, 3.4, 3.55, 4
  cont3d_rosslerperiod{1..4}b.png  the sequence of x-maxima x_n
  cont3d_rosslerattractor.png      the chaotic attractor, c = 4
  cont3d_rosslerreturn.png         return map x_{n+1} vs x_n at c = 4
  cont3d_rosslerbifurcation.png    maxima of x against c in [3, 4]
  interactive/rossler3d.html       rotatable attractor at c = 4
  interactive/rossler_slider.html  c-slider linked to the bifurcation diagram
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

a, b = 0.432, 2.0
IC = [1, 0, 0]


def run(c, tend, dt=0.02):
    t = np.arange(0, tend + dt / 2, dt)
    return solve_ivp(lambda t_, s: cb.rossler(t_, s, a=a, b=b, c=c), [0, tend],
                     IC, t_eval=t, rtol=1e-10, atol=1e-12, method="DOP853")


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


def attractor3d(x, y, z, name, azim, elev=30, lw=0.5):
    fig = plt.figure(figsize=(4.2, 4.2))
    ax = fig.add_subplot(projection="3d")
    ax.plot(x, y, z, "b", lw=lw)
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6); ax.set_zlim(0, 10)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
    ax.view_init(elev=elev, azim=azim)
    plt.savefig(OUT / f"{name}.png", dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close()


# -- the four panels of the route to chaos (book windows: t = 100/200/200/750) --
cases = [(1, 3.0, 100), (2, 3.4, 200), (3, 3.55, 200), (4, 4.0, 750)]
for k, c, tend in cases:
    s = run(c, tend)
    h = len(s.t) // 2
    x, y, z = s.y[:, h:]
    attractor3d(x, y, z, f"cont3d_rosslerperiod{k}a", azim=-72 - 90 + 20)
    _, xm = cb.maxima(s.t[h:], x)
    plt.figure(figsize=(4.2, 3.2))
    plt.plot(np.arange(1, len(xm) + 1), xm, "kD", mfc="none", ms=4)
    plt.xlim(1, len(xm)); plt.ylim(0, 8)
    plt.xlabel("$n$"); plt.ylabel("$x_n$")
    save(f"cont3d_rosslerperiod{k}b")
    print("c = %.2f: %d maxima in the second half, distinct values %s"
          % (c, len(xm), np.unique(np.round(xm, 2))[:6] if k < 4 else "(chaos)"))

# -- the attractor itself (c = 4; viewing angle as in the original figure) ---------------
s = run(4.0, 750)
h = len(s.t) // 2
attractor3d(*s.y[:, h:], "cont3d_rosslerattractor", azim=-169 + 90 - 40 + 20, elev=30)

# -- return map x_{n+1} vs x_n at c = 4 (long run for a clean curve) ----------
s = run(4.0, 3000, dt=0.02)
_, xm = cb.maxima(s.t[len(s.t) // 10:], s.y[0][len(s.t) // 10:])
plt.figure(figsize=(4.2, 4.2))
plt.plot(xm[:-1], xm[1:], "kD", mfc="none", ms=2.5)
plt.xlim(0, 6); plt.ylim(0, 6); plt.gca().set_aspect("equal")
plt.xlabel("$x_n$"); plt.ylabel("$x_{n+1}$")
save("cont3d_rosslerreturn")
print("return map: %d points, x_n in [%.2f, %.2f], map peak %.2f"
      % (len(xm) - 1, xm.min(), xm.max(), xm[1:].max()))


# -- bifurcation diagram: batch RK4 over all c --------------------------------
def rossler_batch(X, c):
    x, y, z = X
    return np.array([-y - z, x + a * y, b + z * (x - c)])


def rk4(X, c, h):
    k1 = rossler_batch(X, c)
    k2 = rossler_batch(X + h / 2 * k1, c)
    k3 = rossler_batch(X + h / 2 * k2, c)
    k4 = rossler_batch(X + h * k3, c)
    return X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def bifurcation(cs, h=0.02, ttrans=300.0, trec=400.0):
    X = np.tile(np.array(IC, float).reshape(3, 1), (1, len(cs)))
    for _ in range(int(ttrans / h)):
        X = rk4(X, cs, h)
    xs = np.empty((int(trec / h), len(cs)))
    for i in range(xs.shape[0]):
        X = rk4(X, cs, h)
        xs[i] = X[0]
    pc, px = [], []
    for j, c in enumerate(cs):
        _, m = cb.maxima(np.arange(xs.shape[0]) * h, xs[:, j])
        pc += [c] * len(m)
        px += list(m)
    return np.array(pc), np.array(px)


cs = np.linspace(3.0, 4.0, 700)
pc, px = bifurcation(cs)
plt.figure(figsize=(4.2, 3.2))
plt.plot(pc, px, "k.", ms=1.2)
plt.xlim(3, 4); plt.ylim(0, 6)
plt.xlabel("$c$"); plt.ylabel("$x$")
save("cont3d_rosslerbifurcation")

# -- interactive 1: rotatable attractor at c = 4 --------------------------------
s = run(4.0, 400, dt=0.02)
m = s.t >= 50
fig = go.Figure(go.Scatter3d(
    x=s.y[0][m].round(3), y=s.y[1][m].round(3), z=s.y[2][m].round(3),
    mode="lines", line=dict(width=2, color=s.t[m], colorscale="Viridis")))
fig.update_layout(scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                             aspectmode="data"),
                  margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
fig.write_html(OUT / "interactive" / "rossler3d.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

# -- interactive 2: c-slider (x-y projection + maxima against c) ----------------
frames_c = np.round(np.arange(3.0, 4.0001, 0.02), 2)
sel = (px < 6.5)
rng = np.random.default_rng(0)
keep = rng.random(len(px)) < 0.35               # thin the static background
traj = {}
for c in frames_c:
    s = run(c, 230, dt=0.1)
    mm = s.t >= 100
    traj[c] = (s.y[0][mm].round(3), s.y[1][mm].round(3))
c0 = frames_c[-1]
fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55],
                    subplot_titles=("orbit projected on the (x, y) plane",
                                    "maxima of x against c"))
fig.add_trace(go.Scatter(x=traj[c0][0], y=traj[c0][1], mode="lines",
                         line=dict(color="royalblue", width=1)), row=1, col=1)
fig.add_trace(go.Scattergl(x=pc[keep].round(4), y=px[keep].round(3),
                           mode="markers", marker=dict(size=1.5, color="black"),
                           hoverinfo="skip"), row=1, col=2)
fig.add_trace(go.Scatter(x=[c0, c0], y=[0, 6], mode="lines",
                         line=dict(color="crimson", width=2)), row=1, col=2)
frames = [go.Frame(name=str(c), traces=[0, 2],
                   data=[go.Scatter(x=traj[c][0], y=traj[c][1]),
                         go.Scatter(x=[c, c], y=[0, 6])]) for c in frames_c]
fig.frames = frames
fig.update_xaxes(range=[-7, 7], title_text="x", row=1, col=1)
fig.update_yaxes(range=[-7, 7], title_text="y", row=1, col=1,
                 scaleanchor="x", scaleratio=1)
fig.update_xaxes(range=[3, 4], title_text="c", row=1, col=2)
fig.update_yaxes(range=[0, 6], title_text="x maxima", row=1, col=2)
fig.update_layout(
    showlegend=False, margin=dict(l=40, r=10, t=40, b=60),
    sliders=[dict(active=len(frames) - 1, x=0.05, len=0.9,
                  currentvalue=dict(prefix="c = "),
                  steps=[dict(method="animate", label=str(c),
                              args=[[str(c)], dict(mode="immediate",
                                                   frame=dict(duration=0, redraw=True),
                                                   transition=dict(duration=0))])
                         for c in frames_c])])
fig.write_html(OUT / "interactive" / "rossler_slider.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)
print("fig_rossler: done")
