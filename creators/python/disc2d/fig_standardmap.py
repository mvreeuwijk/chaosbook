"""Standard-map figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_standardmap_quasi / _chaos                x_n series at K = 2
  disc2d_standardmap_quasi_return / _chaos_return  return plots
  disc2d_standardmap_quasi_deviations / _chaos_deviations  separation of two orbits
  disc2d_standardmap_phase                         islands in a sea of chaos
  disc2d_standardmap_phasetorus                    the same on a torus
  disc2d_standardmap_saddlenode_n=<n>.png          a cloud near (0,0), forward/backward
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
plt.style.use(HERE.parents[1] / "book.mplstyle")
ROOT = HERE.parents[3]
OUT = ROOT / "python" / "_static" / "disc2d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

K = 2.0


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


def jac(x, K):
    c = K * np.cos(2 * np.pi * x[0])
    return np.array([[1 + c, 1.0], [c, 1.0]])


def run(x0, n=2000, ntrans=1000):
    """Orbit of the standard map after discarding a transient."""
    X = cb.orbit(cb.standard_map, x0, ntrans, K=K)
    return cb.orbit(cb.standard_map, X[-1], n, K=K)


# -- series, return plots and deviations -----------------------------------------------
eps = 1e-8
for name, x0, nmax in [("quasi", (0.4, 0.1), 750), ("chaos", (0.1, 0.1), 75)]:
    X = run(x0)
    X2 = cb.orbit(cb.standard_map, X[0] + [eps, 0.0], 2000, K=K)
    plt.figure(figsize=(4.2, 3.2))
    plt.plot(np.arange(1000), X[:1000, 0], "k.", markersize=2)
    plt.xlim(0, 1000)
    plt.ylim(0, 1)
    plt.xticks([0, 1000])
    plt.yticks([0, 1])
    plt.xlabel("$n$")
    plt.ylabel("$x_n$")
    save(f"disc2d_standardmap_{name}")

    plt.figure(figsize=(4.2, 4.2))
    plt.plot(X[:-1, 0], X[1:, 0], "k.", markersize=2)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks([0, 1])
    plt.yticks([0, 1])
    plt.xlabel("$x_n$")
    plt.ylabel("$x_{n+1}$")
    save(f"disc2d_standardmap_{name}_return")

    d = np.log10(np.linalg.norm(X2 - X, axis=1) + 1e-300)
    plt.figure(figsize=(4.2, 3.2))
    plt.plot(np.arange(len(d)), d, "k", lw=1.5)
    plt.xlim(0, nmax)
    plt.ylim(-8, 0)
    plt.xlabel("$n$")
    plt.ylabel(r"$\Delta$")
    plt.yticks([-8, -6, -4, -2, 0],
               [rf"$10^{{{k}}}$" for k in [-8, -6, -4, -2, 0]])
    save(f"disc2d_standardmap_{name}_deviations")

# Lyapunov exponents (QR spectrum) for the initial conditions of the text/Maple
print("Lyapunov spectra at K=2 (n=20000):")
for lab, x0 in [("quasi (0.4,0.1)", (0.4, 0.1)), ("Maple chaos (0.05,0.4)", (0.05, 0.4)),
                ("text chaos (0.1,0.1)", (0.1, 0.1))]:
    print("  ", lab, np.round(cb.lyapunov_spectrum(cb.standard_map, jac, x0, n=20000,
                                                   nskip=1000, K=K), 3))

# -- phase space with several initial conditions ---------------------------------------
y0s = [0.02, 0.08, 0.16, 0.22, 0.24, 0.32, 0.52]
cols = ["cyan", "brown", "green", "red", "blue", "black", "violet"]
runs = [run((0.5, y0), n=3000) for y0 in y0s]
plt.figure(figsize=(4.2, 4.2))
for X, c in zip(runs, cols):
    plt.plot(X[:, 0], X[:, 1], "+", color=c, markersize=2.5, mew=0.6)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xticks([0, 1])
plt.yticks([0, 1])
plt.xlabel("$x$")
plt.ylabel("$y$")
save("disc2d_standardmap_phase")

# on a torus (R = 5, r = 2.5 as in the Maple worksheet)
Rt, rt = 5.0, 2.5


def torus(u, v):
    return ((Rt + rt * np.cos(2 * np.pi * v)) * np.cos(2 * np.pi * u),
            (Rt + rt * np.cos(2 * np.pi * v)) * np.sin(2 * np.pi * u),
            rt * np.sin(2 * np.pi * v))


fig = plt.figure(figsize=(4.2, 3.2))
ax = fig.add_subplot(projection="3d")
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
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.savefig(OUT / "disc2d_standardmap_phasetorus.png", dpi=150)
plt.close()


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


def frame(ax, size=4.2):
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xticks([-0.5, 0.5], ["$-1/2$", "$1/2$"])
    ax.set_yticks([-0.5, 0.5], ["$-1/2$", "$1/2$"])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect("equal")


for n in [-6, -5, -4, -3, 0, 3, 4, 5, 6]:
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.plot(*cloud[n], "k.", markersize=1.6, markeredgewidth=0)
    frame(ax)
    save(f"disc2d_standardmap_saddlenode_n={n}")

fig, ax = plt.subplots(figsize=(4.2, 4.2))
ax.plot(*cloud[-6], ls="none", marker="D", color="0.55", markersize=1.5,
        markeredgewidth=0)
ax.plot(*cloud[6], ls="none", marker="o", color="k", markersize=1.5,
        markeredgewidth=0)
frame(ax)
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
