"""Bouncing ball in a parabolic bowl, "Discrete mappings of higher order".

Dimensionless bowl y = x^2/2; the map (X, U, V) -> (X', U', V') is the one in
the chapter. Produces (in python/_static/disc2d/):
  disc2d_bowl_chaos.png     first 10 bounces, X0=-1.2, U0=2.2, V0=1.2
  disc2d_bowl_periodic.png  the two periodic solutions
  disc2d_bowl_energies.png  Ep, Ek and Et against recreated time, 20 bounces
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)


def bounce(s):
    """One bounce of the dimensionless map; s = (X, U, V)."""
    x, u, v = s
    x1 = (2 * u * v + x * (1 - u**2)) / (1 + u**2)
    v1 = v - (x1 - x) / u
    u1 = ((1 - x1**2) * u + 2 * x1 * v1) / (1 + x1**2)
    vn = (2 * x1 * u - (1 - x1**2) * v1) / (1 + x1**2)
    return np.array([x1, u1, vn])


def yb(x):
    return x**2 / 2


def flight(x, x0, u0, v0):
    """Free-flight parabola between two bounces, y as a function of x."""
    return yb(x0) + v0 * (x - x0) / u0 - 0.5 * (x - x0) ** 2 / u0**2


def trajectory(ax, S, nseg):
    for n in range(nseg):
        x = np.linspace(S[n, 0], S[n + 1, 0], 200)
        ax.plot(x, flight(x, *S[n]), color="0.75", lw=2.5)


xb = np.linspace(-2.5, 2.5, 300)

# -- chaotic trajectory --------------------------------------------------------
S = cb.orbit(bounce, x0=(-1.2, 2.2, 1.2), n=20)
fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.plot(xb, yb(xb), "k", lw=2.5)
trajectory(ax, S, 10)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(0, 4.3)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
fig.tight_layout()
fig.savefig(OUT / "disc2d_bowl_chaos.png", dpi=150)
plt.close(fig)

# -- two periodic solutions ----------------------------------------------------
fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.plot(xb, yb(xb), "k", lw=2.5)
Sa = cb.orbit(bounce, x0=(-0.5, 0.5, 23 / 8), n=3)
Sb = cb.orbit(bounce, x0=(-2.2, 2.2, 1.0), n=3)
trajectory(ax, Sa, 3)
trajectory(ax, Sb, 3)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(0, 4.5)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
fig.tight_layout()
fig.savefig(OUT / "disc2d_bowl_periodic.png", dpi=150)
plt.close(fig)

# -- energies against recreated time -------------------------------------------
N = 20
T = np.zeros(N + 1)
for n in range(N):
    T[n + 1] = T[n] + (S[n + 1, 0] - S[n, 0]) / S[n, 1]
fig, ax = plt.subplots(figsize=(6.5, 2.6))
for n in range(N):
    x = np.linspace(S[n, 0], S[n + 1, 0], 200)
    X0, U0, V0 = S[n]
    t = T[n] + (x - X0) / U0
    Ek = U0**2 / 2 + (V0 - (x - X0) / U0) ** 2 / 2
    Ep = flight(x, X0, U0, V0)
    for e in (Ek, Ep, Ek + Ep):
        ax.plot(t, e, color="0.75", lw=2)
Ep_n = yb(S[:N, 0])
Ek_n = (S[:N, 1] ** 2 + S[:N, 2] ** 2) / 2
ax.plot(T[:N], Ep_n, "ko", markersize=6, label=r"$E_\mathrm{p}$")
ax.plot(T[:N], Ek_n, "kD", markersize=5, label=r"$E_\mathrm{k}$")
ax.plot(T[:N], Ep_n + Ek_n, "ks", markersize=5, label=r"$E_\mathrm{t}$")
ax.set_xlim(-0.8, T[N] + 0.2)
ax.set_ylim(0, 4.5)
ax.set_xlabel("$t$")
ax.set_ylabel("$E(t)$")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3,
          columnspacing=1.5, handletextpad=0.3)
fig.tight_layout()
fig.savefig(OUT / "disc2d_bowl_energies.png", dpi=150)
plt.close(fig)
print("Et range over bounces:", (Ep_n + Ek_n).min(), (Ep_n + Ek_n).max())
print("fig_bowl: assets written to", OUT)
