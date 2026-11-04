"""Schematics of "Discrete mappings of higher order", redrawn in matplotlib.

Produces (in python/_static/disc2d/):
  disc2d_kickedrotor.png   sketch of the kicked rotor: mass m on an arm of
                           length r rotating in the horizontal (x, y) plane
  disc2d_manifolds.png     sketch of the stable and unstable manifolds of a
                           saddle with the iterates x_1, x_2, x_3, ..., x_n,
                           x_{n+1}
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)


def arrow(ax, p, q, ms=14, lw=1.6, style="-|>", rad=0.0, color="k", z=3):
    ax.annotate("", xy=q, xytext=p, zorder=z, arrowprops=dict(
        arrowstyle=style, color=color, lw=lw, mutation_scale=ms,
        shrinkA=0, shrinkB=0, connectionstyle=f"arc3,rad={rad}"))


# --- kicked rotor -----------------------------------------------------------
fig = plt.figure(figsize=(3.6, 2.97))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-1.45, 1.75)
ax.set_ylim(-1.2, 1.45)
ax.set_aspect("equal")
ex, ey, ez = np.array([-0.5, -0.5]), np.array([1.0, 0.0]), np.array([0.0, 1.0])
R, th = 1.0, np.radians(55)
proj = lambda a, b: R * (a * ex + b * ey)
phi = np.linspace(0, 2 * np.pi, 400)
ring = np.array([proj(np.cos(f), np.sin(f)) for f in phi])
ax.plot(*ring.T, "k--", lw=1.0)
for tip, lab, lp in (((0.0, 1.25), "$z$", (0.0, 1.38)),
                     ((1.25, 0.0), "$y$", (1.4, 0.0)),
                     ((-0.7, -0.7), "$x$", (-0.8, -0.9))):
    arrow(ax, (0, 0), tip, ms=14, lw=1.4)
    ax.text(*lp, lab, ha="center", va="center", fontsize=12)
m = proj(np.cos(th), np.sin(th))
ax.plot(*np.c_[(0, 0), m], "k-", lw=1.2)
ax.plot(*m, "ko", ms=13)
ax.text(m[0], m[1] - 0.25, "$m$", ha="center", va="center", fontsize=12)
ax.text(*(0.5 * m + np.array([-0.05, -0.2])), "$r$", ha="center", va="center",
        fontsize=11)
arc = np.array([proj(0.28 * np.cos(f), 0.28 * np.sin(f)) / 1.0
                for f in np.linspace(0, th, 40)]) / 1.0
ax.plot(*arc.T, "k-", lw=0.9)
ax.text(*(proj(0.45 * np.cos(th / 2), 0.45 * np.sin(th / 2)) + np.array([0, -0.1])),
        r"$\theta$", ha="center", va="center", fontsize=11)
bf.save(fig, OUT / "disc2d_kickedrotor.png")


# --- stable and unstable manifolds -----------------------------------------
def spline(pts):
    p = np.array(pts, float) / 100.0
    p[:, 1] = (738 - np.array(pts, float)[:, 1]) / 100.0
    u = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
    cs = CubicSpline(u, p)
    uu = np.linspace(0, u[-1], 400)
    return cs(uu)


Ws = spline([(237, 52), (380, 170), (500, 340), (600, 420), (700, 462), (767, 477),
             (850, 477), (1000, 455), (1133, 407), (1250, 418), (1315, 500),
             (1315, 620), (1298, 690)])
Wu = spline([(180, 607), (420, 607), (560, 560), (655, 418), (697, 348),
             (741, 240), (830, 125), (1020, 75), (1180, 65)])


def on(curve, px):
    q = np.array([px[0] / 100.0, (738 - px[1]) / 100.0])
    return curve[np.argmin(np.hypot(*(curve - q).T))]


fig = plt.figure(figsize=(bf.FULL_W, 2.83))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-0.2, 17.6)
ax.set_ylim(-0.1, 7.9)
ax.set_aspect("equal")
ax.plot(*Ws.T, "k-", lw=2.6)
ax.plot(*Wu.T, "k-", lw=2.6)
th_ = np.linspace(0, 2 * np.pi, 200)
cc, rr = np.array([6.55, 3.7]), 1.15
ax.plot(cc[0] + rr * np.cos(th_), cc[1] + rr * np.sin(th_), "k--", lw=0.9)
s1, s2, s3 = (on(Ws, (1310, 632)), on(Ws, (1133, 407)), on(Ws, (850, 477)))
s4, s5, s6 = (on(Ws, (767, 477)), on(Ws, (720, 465)), on(Ws, (683, 452)))
u1, u2, un, un1 = (on(Wu, (655, 418)), on(Wu, (697, 348)), on(Wu, (741, 240)),
                   on(Wu, (1027, 75)))
for p in (s1, s2, s3, s4, s5, s6, u1, u2, un, un1):
    ax.plot(*p, "ko", ms=7, zorder=5)
for p, q, rad in ((s1, s2, -0.25), (s2, s3, 0.2), (s3, s4, -0.5), (u1, u2, -0.5),
                  (u2, un, -0.5), (un, un1, 0.15)):
    d = q - p
    arrow(ax, p + 0.3 * d / np.hypot(*d), q - 0.34 * d / np.hypot(*d), ms=12,
          lw=1.0, rad=rad)
ax.text(s1[0] + 0.25, s1[1] - 0.05, r"$\mathbf{x}_1$", va="center", fontsize=10)
ax.text(s2[0] - 0.2, s2[1] + 0.35, r"$\mathbf{x}_2$", ha="center", fontsize=10)
ax.text(s3[0] - 0.2, s3[1] - 0.55, r"$\mathbf{x}_3$", ha="center", fontsize=10)
ax.text(un[0] + 0.3, un[1] - 0.2, r"$\mathbf{x}_n$", va="center", fontsize=10)
ax.text(un1[0] - 0.1, un1[1] + 0.4, r"$\mathbf{x}_{n+1}$", ha="center", fontsize=10)
ax.text(12.4, 7.1, "unstable manifold", va="center", fontsize=10)
ax.text(8.6, 0.45, "stable manifold", va="center", fontsize=10)
ax.text(0.0, 2.4, "linear\napproximation\nvalid", va="center", fontsize=10,
        linespacing=1.1)
arrow(ax, (3.0, 2.8), (5.35, 3.45), ms=12, lw=1.0)
bf.save(fig, OUT / "disc2d_manifolds.png")
print("fig_schematics: written to", OUT)
