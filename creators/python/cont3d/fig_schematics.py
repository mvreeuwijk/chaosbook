"""Schematics of "Chaos in continuous systems", redrawn in matplotlib.

Produces (in python/_static/cont3d/):
  cont3d_poincaresection.png   a trajectory crossing a surface of section S
  cont3d_doublewell.png        the forced double-well beam
  cont3d_lyap_formal.png       perturbation and Jacobian eigenvectors along x(t)
  cont3d_rosslertopology.png   band structure of the Rossler attractor
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
OUT.mkdir(parents=True, exist_ok=True)

ARROW = dict(arrowstyle="-|>", mutation_scale=12, color="k", lw=1.2)


def arrow(ax, p, q, **kw):
    ax.add_patch(FancyArrowPatch(p, q, **{**ARROW, **kw}))


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# -- Poincare section -----------------------------------------------------------
from scipy.interpolate import splev, splprep


def spline(pts, n=300, per=False):
    pts = np.asarray(pts, float)
    tck, _ = splprep(pts.T, s=0, per=per)
    return splev(np.linspace(0, 1, n), tck)


fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.add_patch(Polygon([[0.0, 0.3], [2.7, 0.3], [2.7, 3.1], [0.0, 3.1]],
                     closed=True, fc="0.93", ec="k", lw=1.2))
xk, xk1, xs = (2.2, 2.0), (1.6, 2.35), (0.95, 2.7)
inner = spline([xk, (2.05, 1.2), (2.6, 0.55), (3.2, 1.0), (3.35, 1.9), (3.3, 2.7)])
ax.plot(*inner, "k", lw=1.2)
outer = spline([(3.3, 2.7), (4.3, 2.2), (4.3, 1.1), (3.2, 0.1), (1.9, -0.1),
                (0.9, 0.7), (0.7, 1.7), xs])
ax.plot(*outer, "k", lw=1.2)
ax.plot(*spline([xs, (1.4, 3.05), (2.4, 3.2), (3.3, 2.7)], 100), "k--", lw=1)
ax.plot(*spline([xk1, (2.1, 2.65), (2.8, 2.7), (3.3, 2.7)], 100), "k--", lw=1)
arrow(ax, (3.35, 1.7), (3.35, 2.0))
for (pt, lab, dx, dy) in [(xs, r"$\mathbf{x}^*$", -0.45, 0.05),
                          (xk1, r"$\mathbf{x}_{k+1}$", -0.55, -0.3),
                          (xk, r"$\mathbf{x}_k$", 0.12, -0.12)]:
    ax.plot(*pt, "ko", ms=4)
    ax.text(pt[0] + dx, pt[1] + dy, lab)
ax.plot(0.62, 0.55, "ko", ms=4)
ax.text(-0.45, 1.7, r"$S$", fontsize=14)
ax.set_xlim(-0.7, 4.6); ax.set_ylim(-0.3, 3.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "cont3d_poincaresection")

# -- forced double-well beam ----------------------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 2.7))
frame = dict(fc="0.9", ec="k", lw=1.2)
# rigid frame: left wall, top bar, base bar
ax.add_patch(Rectangle((2.2, 0.0), 6.8, 0.4, **frame))             # base
ax.add_patch(Rectangle((2.2, 0.0), 0.4, 6.0, **frame))             # left wall
ax.add_patch(Rectangle((2.2, 5.6), 7.8, 0.4, **frame))             # top bar
ax.add_patch(Rectangle((-1.2, 2.6), 3.4, 0.4, **frame))            # drive rod
arrow(ax, (-1.2, 3.6), (2.1, 3.6), arrowstyle="<|-|>")
ax.text(-1.2, 4.1, "periodic\nforcing", va="bottom")
xb = 6.0
ax.plot([xb, xb], [0.4, 5.6], "k--", lw=1)
s = np.linspace(0, 1, 100)
ax.plot(xb + 1.4 * s**2.2, 5.6 - 4.4 * s, "k", lw=2)
ax.text(xb + 1.0, 3.0, "beam")
for xm in (4.0, 7.6):
    ax.add_patch(Rectangle((xm - 0.45, 0.4), 0.9, 0.5, fc="0.5", ec="k", lw=1))
ax.text(3.1, 1.2, "magnet")
arrow(ax, (xb, 0.95), (xb + 1.35, 0.95))
ax.text(xb + 0.55, 1.1, r"$x$")
ax.text(9.1, 0.0, "rigid frame", va="center")
ax.set_xlim(-1.4, 12.2); ax.set_ylim(-0.3, 6.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "cont3d_doublewell")

# -- perturbation along a trajectory (Lyapunov, formal) --------------------------
fig, ax = plt.subplots(figsize=(5.0, 2.2))
u = np.linspace(0, 1, 300)
X = 0.3 + 9.2 * u
Y = 1.4 - 1.5 * np.sin(np.pi * u) + 0.9 * u
ax.plot(X, Y, "k", lw=1.5)
arrow(ax, (X[-30], Y[-30]), (X[-1] + 0.4, Y[-1] + 0.15))
ax.text(X[-1] + 0.5, Y[-1] + 0.1, r"$\vec{x}(t)$")
for u0, lab, ang in [(0.28, 0, 0), (0.80, 1, 0)]:
    i = int(u0 * 299)
    p = np.array([X[i], Y[i]])
    sl = np.arctan2(Y[i + 1] - Y[i - 1], X[i + 1] - X[i - 1])
    def rot(v, a):
        c, s_ = np.cos(a), np.sin(a)
        return np.array([c * v[0] - s_ * v[1], s_ * v[0] + c * v[1]])
    if lab == 0:
        e1, e2, eps = rot([0.5, -0.9], 0.0), rot([0.9, 0.7], 0.0), rot([-1.4, -0.3], 0.0)
    else:
        e1, e2, eps = rot([1.0, -0.2], 0.0), rot([0.3, 0.9], 0.0), rot([0.3, -0.9], 0.0)
    arrow(ax, p, p + e1, lw=0.8)
    arrow(ax, p, p + e2, lw=0.8)
    arrow(ax, p, p + eps, lw=2.0, mutation_scale=14)
    t_ = r"t_%d" % lab
    ax.text(*(p + e1 + [0.0, -0.35]) if lab == 0 else p + e1 + [0.1, -0.1],
            r"$\vec{e}_1(t_0)$", ha="center" if lab == 0 else "left")
    ax.text(*(p + e2 + [0.05, 0.1]), r"$\vec{e}_2(%s)$" % t_,
            ha="center", va="bottom")
    ax.text(*(p + eps + ([-0.55, -0.4] if lab == 0 else [0.25, -0.4])),
            r"$\vec{\varepsilon}(%s)$" % t_, ha="center")
ax.set_xlim(-1.5, 11.5); ax.set_ylim(-1.5, 3.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "cont3d_lyap_formal")

# -- Rossler band topology -------------------------------------------------------
fig, ax = plt.subplots(figsize=(4.2, 3.8))
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), 0.55 * np.sin(th), "k", lw=1.2)                  # central hole
for w in (1.55, 1.85):                                               # "normal band"
    ax.plot(w * np.cos(th), 0.65 * w * np.sin(th) - 0.3, "k--", lw=1.0)
th2 = np.linspace(np.pi * 0.62, -np.pi * 1.1, 300)                   # "Mobius band"
for off in (0.0, 0.13):
    R = 2.55 + off
    ax.plot(R * np.cos(th2),
            1.4 * np.sin(th2) - 0.9 + 1.9 * np.maximum(np.cos(th2 - 0.4), 0) ** 3,
            "k", lw=1.2)
arrow(ax, (1.9, -1.7), (2.35, -1.0))
ax.text(0.0, 0.0, r'"normal band"', ha="center", va="center", fontsize=10)
ax.text(0.6, -2.55, '"M\u00f6bius band"', ha="center")
ax.set_xlim(-3.2, 3.4); ax.set_ylim(-3.0, 2.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "cont3d_rosslertopology")
print("fig_schematics: done")
