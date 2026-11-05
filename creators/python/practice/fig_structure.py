"""Finding simplicity in complexity, "Chaos in practice".

Produces (in python/_static/practice/):
  practice_weathermodel.png   schematic: a weather model is a dynamical system
  practice_manifold.png       schematic: collapse onto an attracting manifold
  practice_pod.png            POD of a Lorenz-driven synthetic field
  practice_koopman.png        schematic: the Koopman viewpoint
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, save)

OUT = bf.out("practice")

C_TRUTH, C_FREE, C_ANA, C_FAINT = "#111111", "#c0392b", "#1f6aa5", "#b8b8b8"


def lorenz_run(T, dt, x0=(1.0, 1.0, 1.0), t_transient=50.0):
    """A Lorenz trajectory (3, n) sampled every dt, after a transient."""
    xa = solve_ivp(cb.lorenz, [0, t_transient], x0, rtol=1e-10, atol=1e-12).y[:, -1]
    return solve_ivp(cb.lorenz, [0, T], xa, t_eval=np.arange(0, T, dt),
                     rtol=1e-9, atol=1e-11).y


def arrow(ax, p0, p1, color=C_TRUTH, lw=1.3):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, zorder=1))


# -- the weather model as a dynamical system (schematic) ---------------------
fig, ax = plt.subplots(figsize=(bf.FULL_W, 3.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis("off")
for i in range(4):                                  # fields on a grid
    for j in range(3):
        ax.add_patch(plt.Rectangle((0.3 + i * 0.42, 1.2 + j * 0.42), 0.42, 0.42,
                                   fc="#dfeaf5", ec="#8fb2d6", lw=0.6))
ax.text(1.14, 3.2, "discretised\nfields on a grid", ha="center", fontsize=8)
x0c = 3.6                                           # the stacked state vector
for j in range(9):
    ax.add_patch(plt.Rectangle((x0c, 0.6 + j * 0.28), 0.5, 0.28,
                               fc="#eef3f8", ec=C_ANA, lw=0.7))
ax.text(x0c + 0.25, 3.35, r"$\mathbf{x}$", ha="center", fontsize=10)
ax.text(x0c + 0.25, 0.15, r"$\dim \sim 10^{9}$", ha="center", fontsize=8)
ax.text(6.2, 2.05, r"$\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$",
        ha="center", fontsize=11)
th = np.linspace(0, 2 * np.pi, 300)                 # flow on an attractor
ax.plot(8.4 + 0.7 * np.cos(th) + 0.25 * np.cos(2 * th), 2.0 + 0.6 * np.sin(th),
        color=C_TRUTH, lw=1.1)
ax.text(8.5, 0.7, "flow on an\nattractor", ha="center", fontsize=8)
back = lorenz_run(40, 0.01)                         # Lorenz: the same object
axins = fig.add_axes([0.64, 0.58, 0.18, 0.34])
axins.plot(back[0], back[2], color=C_FREE, lw=0.3)
axins.axis("off")
axins.set_title(r"Lorenz: $\dim = 3$", fontsize=8)
arrow(ax, (1.95, 1.9), (3.5, 1.9))
arrow(ax, (4.2, 1.9), (5.4, 1.9))
arrow(ax, (7.0, 1.9), (7.6, 1.9))
bf.save(fig, OUT / "practice_weathermodel.png")

# -- trajectories collapsing onto an attracting manifold (schematic) ---------
fig = plt.figure(figsize=bf.SQUARE)
ax = fig.add_subplot(111, projection="3d")
u = v = np.linspace(-1, 1, 40)
U, V = np.meshgrid(u, v)
ax.plot_surface(U, V, 0.5 * (U ** 2 - V ** 2), alpha=0.35, color=C_ANA,
                edgecolor="none")
rng = np.random.default_rng(3)
for _ in range(6):
    p = rng.uniform(-1, 1, 3)
    pts = [p]
    for _ in range(40):
        target_w = 0.5 * (p[0] ** 2 - p[1] ** 2)
        p = p + 0.15 * np.array([rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3),
                                 target_w - p[2]])
        p[2] += 0.02 * rng.standard_normal()
        pts.append(p.copy())
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=C_TRUTH, lw=0.8)
    ax.scatter(*pts[0], color=C_FREE, s=12)
ax.text2D(0.5, 0.94, "high-dimensional state space", transform=ax.transAxes,
          ha="center", fontsize=8)
ax.text2D(0.99, 0.02, "low-dimensional\nattracting manifold",
          transform=ax.transAxes, ha="right", fontsize=8, color=C_ANA)
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.grid(False)
ax.view_init(elev=22, azim=-60)
bf.save(fig, OUT / "practice_manifold.png")

# -- POD of a field whose amplitudes are a Lorenz trajectory -----------------
Nx, Nt = 200, 800
xg = np.linspace(0, 2 * np.pi, Nx)
phi1 = np.sin(xg)                                   # three fixed spatial patterns
phi2 = np.sin(2 * xg) * np.exp(-((xg - np.pi) ** 2) / 4)
phi3 = np.cos(3 * xg)
traj = lorenz_run(Nt * 0.01, 0.01).T                # (Nt, 3)
a = (traj - traj.mean(0)) / traj.std(0)             # normalised amplitudes
rng = np.random.default_rng(11)
field = (np.outer(a[:, 0], phi1) + np.outer(a[:, 1], phi2)
         + 0.6 * np.outer(a[:, 2], phi3)) + 0.15 * rng.standard_normal((Nt, Nx))
Xm = field.T - field.T.mean(axis=1, keepdims=True)  # snapshots as columns
U_, S, Vt = np.linalg.svd(Xm, full_matrices=False)
energy = S ** 2 / np.sum(S ** 2)
snap = 300
recon = {k: (U_[:, :k] * S[:k]) @ Vt[:k, snap] for k in (1, 2, 3)}
print("POD: energy of first 3 modes =", np.round(energy[:3], 3),
      "cumulative", round(energy[:3].sum(), 4))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.6))
idx = np.arange(1, 11)
ax1.bar(idx, energy[:10], color=C_ANA, width=0.6)
ax1.set_xlabel("mode number")
ax1.set_ylabel("relative energy")
ax1.set_xticks(idx)
ax1.set_title("POD spectrum")
ax1b = ax1.twinx()
ax1b.plot(idx, np.cumsum(energy)[:10], "o-", color=C_FREE, ms=4, lw=1.0)
ax1b.set_ylabel("cumulative", color=C_FREE)
ax1b.tick_params(axis="y", colors=C_FREE)
ax1b.set_ylim(0, 1.02)
ax2.plot(xg, Xm[:, snap], color=C_FAINT, lw=2.4, label="full field")
for k, style in zip((1, 2, 3), ["--", "-.", "-"]):
    ax2.plot(xg, recon[k], style, lw=1.2, label=f"{k} mode" + ("s" if k > 1 else ""))
ax2.set_xlabel("$x$")
ax2.set_ylabel("$u(x)$")
ax2.set_title("reconstruction of one snapshot")
ax2.set_ylim(-1.25, 1.8)
ax2.legend(loc="upper right", ncol=2)
ax2.set_xlim(0, 2 * np.pi)
bf.save(fig, OUT / "practice_pod.png")

# -- the Koopman viewpoint (schematic) ---------------------------------------
fig, ax = plt.subplots(figsize=(bf.MEDIUM[0], 2.2))
ax.set_xlim(0, 10)
ax.set_ylim(-0.7, 5)
ax.axis("off")
th = np.linspace(0, 1.6 * np.pi, 200)
ax.plot(2.2 + 1.6 * np.cos(th) + 0.3 * np.cos(2.3 * th), 0.9 + 0.7 * np.sin(th),
        color=C_TRUTH, lw=1.4)
ax.text(2.2, -0.55, r"state space $\mathbf{x}$", ha="center", fontsize=8)
ax.text(2.2, 2.0, "nonlinear\nflow", ha="center", fontsize=8, color=C_TRUTH)
ax.plot([6.0, 9.4], [3.7, 4.2], color=C_ANA, lw=1.4)
xs = np.array([6.0, 7.1, 8.2, 9.4])
ax.scatter(xs, np.interp(xs, [6.0, 9.4], [3.7, 4.2]), color=C_ANA, s=16, zorder=3)
ax.text(7.7, 4.55, r"observables $g(\mathbf{x})$", ha="center", fontsize=8)
ax.text(7.7, 3.1, r"linear: $g_{k+1} = \mathcal{K}\, g_k$", ha="center",
        fontsize=8, color=C_ANA)
arrow(ax, (4.3, 1.7), (5.8, 3.7), color=C_FREE, lw=1.4)
ax.text(4.5, 2.9, "lift", fontsize=8, color=C_FREE, rotation=32)
bf.save(fig, OUT / "practice_koopman.png")
print("fig_structure: assets written to", OUT)
