"""Standard-map figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_standardmap_series     2x3: quasi-periodic (top) and chaotic (bottom)
                                x_n series, return plot, separation of two
                                orbits, at K = 2
  disc2d_standardmap_phase      (a) islands in a sea of chaos, (b) on a torus
  disc2d_standardmap_saddlenode 3x3: a cloud near (0,0), n = -6..-3, 0, 3..6
  disc2d_standardmap_manifolds                     W^u and W^s together
  (disc2d_manifolds, the sketch, is drawn by fig_schematics.py)
  interactive/standardmap_slider.html              phase portrait with a K slider
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

import chaosbook as cb

HERE = Path(__file__).resolve()
import sys
sys.path.insert(0, str(HERE.parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)
ROOT = HERE.parents[3]
OUT = ROOT / "python" / "_static" / "disc2d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

K = 2.0


def save(name):
    bf.save(plt.gcf(), OUT / f"{name}.png")


def jac(x, K):
    c = K * np.cos(2 * np.pi * x[0])
    return np.array([[1 + c, 1.0], [c, 1.0]])


def run(x0, n=2000, ntrans=1000):
    """Orbit of the standard map after discarding a transient."""
    X = cb.orbit(cb.standard_map, x0, ntrans, K=K)
    return cb.orbit(cb.standard_map, X[-1], n, K=K)


# -- series, return plots and deviations: rows quasi/chaos, columns series,
#    return plot, deviations; letters run down the columns ------------------
eps = 1e-8
fig, axs = plt.subplots(2, 3, figsize=(bf.FULL_W, 4.2),
                        gridspec_kw=dict(width_ratios=[1.3, 1, 1.3]))
for row, (name, x0, nmax) in enumerate([("quasi", (0.4, 0.1), 750),
                                        ("chaos", (0.1, 0.1), 75)]):
    X = run(x0)
    X2 = cb.orbit(cb.standard_map, X[0] + [eps, 0.0], 2000, K=K)
    ax = axs[row, 0]
    ax.plot(np.arange(1000), X[:1000, 0], "k.", markersize=2)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1000])
    ax.set_yticks([0, 1])
    ax.set_xlabel("$n$")
    ax.set_ylabel("$x_n$")

    ax = axs[row, 1]
    ax.plot(X[:-1, 0], X[1:, 0], "k.", markersize=2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")

    d = np.log10(np.linalg.norm(X2 - X, axis=1) + 1e-300)
    ax = axs[row, 2]
    ax.plot(np.arange(len(d)), d, "k", lw=1.5)
    ax.set_xlim(0, nmax)
    ax.set_ylim(-8, 0)
    ax.set_xlabel("$n$")
    ax.set_ylabel(r"$\Delta$")
    ax.set_yticks([-8, -6, -4, -2, 0],
                  [rf"$10^{{{k}}}$" for k in [-8, -6, -4, -2, 0]])
bf.panel_labels(axs, order="col")
bf.save(fig, OUT / "disc2d_standardmap_series.png")

# Lyapunov exponents (QR spectrum) for the initial conditions of the text
print("Lyapunov spectra at K=2 (n=20000):")
for lab, x0 in [("quasi (0.4,0.1)", (0.4, 0.1)), ("chaos, alternative IC (0.05,0.4)", (0.05, 0.4)),
                ("text chaos (0.1,0.1)", (0.1, 0.1))]:
    print("  ", lab, np.round(cb.lyapunov_spectrum(cb.standard_map, jac, x0, n=20000,
                                                   nskip=1000, K=K), 3))

# -- phase space with several initial conditions ---------------------------------------
y0s = [0.02, 0.08, 0.16, 0.22, 0.24, 0.32, 0.52]
# the island around (1/2, 1/2) and (0, 1/2) is grey, as the text says
cols = ["cyan", "brown", "green", "red", "blue", "black", "#8c8c8c"]
runs = [run((0.5, y0), n=3000) for y0 in y0s]
fig = plt.figure(figsize=(bf.FULL_W, 3.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.3])
ax1 = fig.add_subplot(gs[0, 0])
for X, c in zip(runs, cols):
    ax1.plot(X[:, 0], X[:, 1], "+", color=c, markersize=2.5, mew=0.6)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_xticks([0, 1])
ax1.set_yticks([0, 1])
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")

# on a torus (R = 5, r = 2.5 as in the original figure)
Rt, rt = 5.0, 2.5


def torus(u, v):
    return ((Rt + rt * np.cos(2 * np.pi * v)) * np.cos(2 * np.pi * u),
            (Rt + rt * np.cos(2 * np.pi * v)) * np.sin(2 * np.pi * u),
            rt * np.sin(2 * np.pi * v))


ax = fig.add_subplot(gs[0, 1], projection="3d")
uu, vv = np.meshgrid(np.linspace(0, 1, 40), np.linspace(0, 1, 20))
ax.plot_wireframe(*torus(uu, vv), color="0.75", linewidth=0.3, rstride=1, cstride=1)
for X, c in zip(runs, cols):
    ax.scatter(*torus(X[:, 0], X[:, 1]), s=1.0, color=c, depthshade=False, linewidths=0)
ax.set_box_aspect((1, 1, 0.5), zoom=1.25)
ax.view_init(elev=38, azim=-75)
ax.set_axis_off()
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_zlim(-4, 4)
bf.panel_labels([ax1])
ax.text2D(0.0, 1.0, "(b)", transform=ax.transAxes, ha="right", va="bottom",
          fontsize=plt.rcParams["axes.labelsize"])
bf.save(fig, OUT / "disc2d_standardmap_phase.png")


# -- saddle node (0,0): a cloud, forward and backward -----------------------------------
def mod_c(x):
    """Centred mod 1, in [-1/2, 1/2)."""
    return x - np.floor(x + 0.5)


def smap(x, y):
    yn = y + K / (2 * np.pi) * np.sin(2 * np.pi * x)
    return mod_c(x + yn), mod_c(yn)


def smap_inv(x, y):
    xn = x - y
    return mod_c(xn), mod_c(y - K / (2 * np.pi) * np.sin(2 * np.pi * xn))


# check: forward then backward returns to the start
xx, yy = np.array(0.4), np.array(0.4)
for _ in range(10):
    xx, yy = smap(xx, yy)
for _ in range(10):
    xx, yy = smap_inv(xx, yy)
print("forward/backward round trip (should be 0.4, 0.4):", float(xx), float(yy))

Nx = Ny = 75
L = 0.01
gx, gy = np.meshgrid(np.linspace(-L / 2, L / 2, Nx), np.linspace(-L / 2, L / 2, Ny))
cloud = {0: (gx.ravel(), gy.ravel())}
for n in range(10):
    cloud[n + 1] = smap(*cloud[n])
    cloud[-(n + 1)] = smap_inv(*cloud[-n])


def frame(ax):
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xticks([-0.5, 0.5], ["$-1/2$", "$1/2$"])
    ax.set_yticks([-0.5, 0.5], ["$-1/2$", "$1/2$"])
    ax.set_aspect("equal")


# 3 x 3 grid, shared axes, letters (a)-(i) row by row
fig, axs = plt.subplots(3, 3, figsize=(5.8, bf.MAX_H), sharex=True, sharey=True)
for ax, n in zip(axs.ravel(), [-6, -5, -4, -3, 0, 3, 4, 5, 6]):
    ax.plot(*cloud[n], "k.", markersize=1.6, markeredgewidth=0)
    frame(ax)
for ax in axs[-1]:
    ax.set_xlabel("$x$")
for ax in axs[:, 0]:
    ax.set_ylabel("$y$")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc2d_standardmap_saddlenode.png")

fig, ax = plt.subplots(figsize=bf.SQUARE)
ax.plot(*cloud[-6], ls="none", marker="D", color="0.55", markersize=1.5,
        markeredgewidth=0)
ax.plot(*cloud[6], ls="none", marker="o", color="k", markersize=1.5,
        markeredgewidth=0)
frame(ax)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
save("disc2d_standardmap_manifolds")

# eigenvalues and eigenvectors of J* at (0,0) for K = 2
Jstar = jac(np.array([0.0, 0.0]), K)
sig, vec = np.linalg.eig(Jstar)
sig, vec = sig.real, vec.real
order = np.argsort(-sig)
print("J* at (0,0), K=2:\n", Jstar)
for i in order:
    v = vec[:, i] * np.sign(vec[1, i])
    print(f"  sigma={sig[i]:.4f}  eigenvector={np.round(v, 4)}")
print("  det J =", np.linalg.det(Jstar), "; angle of e1 to horizontal =",
      np.degrees(np.arctan2(vec[1, order[0]], vec[0, order[0]])))
print("  closed form 1+K/2 +- sqrt(K(K+4))/2 =",
      1 + K / 2 + np.sqrt(K * (K + 4)) / 2, 1 + K / 2 - np.sqrt(K * (K + 4)) / 2)

# -- interactive: phase portrait with a K slider ---------------------------------------
rng = np.random.default_rng(3)
nic, nit = 45, 180
ic = rng.uniform(0, 1, size=(2, nic))
ic[:, :8] = np.array([[0.5] * 8, np.linspace(0.02, 0.5, 8)])   # a few islands
Ks = np.round(np.arange(0, 2.51, 0.25), 2)
fig = go.Figure()
for i, Kv in enumerate(Ks):
    X = cb.orbit(cb.standard_map, ic, nit, K=Kv)          # (nit+1, 2, nic)
    xs = np.round(X[:, 0, :], 4)
    ys = np.round(X[:, 1, :], 4)
    colors = np.tile(np.arange(nic), (nit + 1, 1))
    fig.add_trace(go.Scattergl(
        x=xs.ravel(), y=ys.ravel(), mode="markers", visible=(i == 0),
        marker=dict(size=2, color=colors.ravel(), colorscale="Turbo"),
        hoverinfo="skip"))
steps = [dict(method="update", label=f"{Kv:g}",
              args=[{"visible": [j == i for j in range(len(Ks))]}])
         for i, Kv in enumerate(Ks)]
fig.update_layout(
    sliders=[dict(active=0, steps=steps, currentvalue=dict(prefix="K = "),
                  pad=dict(t=30))],
    xaxis=dict(title="x", range=[0, 1], constrain="domain"),
    yaxis=dict(title="y", range=[0, 1], scaleanchor="x"),
    showlegend=False, margin=dict(l=50, r=10, t=10, b=40), height=620)
fig.write_html(OUT / "interactive" / "standardmap_slider.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)
print("fig_standardmap: assets written to", OUT)
