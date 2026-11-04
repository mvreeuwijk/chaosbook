"""Schematics of "Continuous systems of higher order", redrawn in matplotlib.

Produces (in python/_static/cont2d/):
  cont2d_phasespace.png        a trajectory x(t) in the (x, y) phase plane
  cont2d_phase_r1..r3.png      linear 2-D systems with real eigenvalues:
                               stable node, saddle, unstable node
  cont2d_phase_i1..i3.png      complex eigenvalues: stable spiral, centre,
                               unstable spiral
  cont2d_classification.png    classification in the (T, D) plane
  cont2d_zoo.png               a nonlinear phase plane with several fixed
                               points and a limit cycle
The trajectories of the linear cases are computed from x(t) = exp(A t) x0 for
the matrices listed in PORTRAITS; in the zoo the same curves are drawn in
rotated / sheared eigen-coordinates.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "C0"

# --- linear systems: matrices, seeds on the boundary of the unit box -------
EDGE = [(sx * a, sy * 1.0) for a in (0.4, 0.9) for sx in (-1, 1) for sy in (-1, 1)]
SPIRAL_SEEDS = [(1.0, 0.5), (-1.0, -0.5)]
PORTRAITS = {
    # name: (A, seeds, filled centre?, tmax, flow sign along the two eigen-axes)
    "r1": (np.diag([-1.0, -3.0]), EDGE, True, 14, (-1, -1)),
    "r2": (np.diag([1.0, -1.0]),
           [(sx * a, sy) for a in (0.12, 0.45) for sx in (-1, 1) for sy in (-1, 1)],
           False, 14, (1, -1)),
    "r3": (np.diag([1.0, 3.0]), EDGE, False, 14, (1, 1)),
    "i1": (np.array([[-0.35, -1.0], [1.0, -0.35]]), SPIRAL_SEEDS, True, 20, None),
    "i2": (np.array([[0.0, -2.0], [0.5, 0.0]]), [(0.45, 0.0), (0.9, 0.0)],
           True, np.pi + 0.02, None),
    "i3": (np.array([[0.35, -1.0], [1.0, 0.35]]), [(0.1, 0.0), (-0.1, 0.0)],
           False, 20, None),
}


def trajectory(A, seed, tmax, L=1.0, eps=0.04):
    """Piece of exp(At) seed inside the box |.|<=L, away from the origin."""
    w, V = np.linalg.eig(A)
    c = np.linalg.solve(V, np.asarray(seed, float).astype(complex))
    t = np.linspace(-tmax, tmax, 6001)
    X = (V @ (np.exp(np.outer(w, t)) * c[:, None])).real
    ok = (np.abs(X).max(axis=0) <= L + 1e-9) & (np.hypot(*X) > eps)
    i0 = np.argmin(np.abs(t))
    lo = i0
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    hi = i0
    while hi < len(t) - 1 and ok[hi + 1]:
        hi += 1
    return X[:, lo:hi + 1]


def arrow(ax, p, q, color, ms, lw=0.0):
    ax.annotate("", xy=q, xytext=p, zorder=4, arrowprops=dict(
        arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms,
        shrinkA=0, shrinkB=0))


def head(ax, p, d, color, ms):
    """Arrowhead at p pointing along direction d."""
    d = np.asarray(d, float)
    arrow(ax, p, np.asarray(p) + d / np.hypot(*d) * 1e-3, color, ms)


def flow_arrow(ax, P, frac, color, ms):
    """Arrowhead at fraction `frac` of the arclength of path P (2 x n)."""
    s = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=1)))]
    i = min(np.searchsorted(s, frac * s[-1]), P.shape[1] - 2)
    head(ax, P[:, i], P[:, i + 1] - P[:, i], color, ms)


def portrait(ax, name, c=(0, 0), s=1.0, M=np.eye(2), ms=14, lw=1.5,
             axes_lw=1.6, dot=9):
    """Draw one linear portrait in the plot region c + s*M@[-1,1]^2."""
    A, seeds, filled, tmax, signs = PORTRAITS[name]
    c = np.asarray(c, float)[:, None]

    def T(p):
        p = np.asarray(p, float)
        return (c + s * (M @ p.reshape(2, -1))).reshape(p.shape)

    for sd in seeds:
        Q = T(trajectory(A, sd, tmax))
        ax.plot(*Q, color=BLUE, lw=lw, zorder=2)
        flow_arrow(ax, Q, 0.55 if signs is None else 0.5 if name == "r2" else 0.45,
                   BLUE, ms * 1.4)
    # eigen-axes (the coordinate axes of the local portrait)
    for e in (np.array([1.0, 0]), np.array([0, 1.0])):
        a, b = T(-1.1 * e), T(1.1 * e)
        ax.plot(*np.c_[a, b], color="k", lw=axes_lw, zorder=1,
                solid_capstyle="butt")
        head(ax, T(1.05 * e), T(1.1 * e) - T(1.05 * e), "k", ms * 1.1)
    if signs is not None:                       # flow along the eigen-axes
        for k, sg in enumerate(signs):
            e = np.eye(2)[k]
            for sd in (-1, 1):
                p = 0.62 * sd * e
                head(ax, T(p), T(p + sg * sd * 0.01 * e) - T(p), BLUE, ms * 1.5)
    ax.plot(*c[:, 0], "o", ms=dot, mfc="k" if filled else "w", mec="k",
            mew=1.8, zorder=5)


# --- single-panel linear portraits ----------------------------------------
for name in PORTRAITS:
    fig = plt.figure(figsize=(2.5, 2.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-1.3, 1.4)
    ax.set_ylim(-1.28, 1.3)
    ax.axis("off")
    portrait(ax, name, ms=10, dot=7, lw=1.0, axes_lw=1.0)
    ax.text(0.08, 1.14, "$y$", ha="left", va="center")
    ax.text(1.2, -0.13, "$x$", ha="center", va="center")
    bf.save(fig, OUT / f"cont2d_phase_{name}.png")


# --- phase space with one trajectory --------------------------------------
fig = plt.figure(figsize=(3.8, 2.05))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-1.45, 2.8)
ax.set_ylim(-1.05, 1.35)
ax.set_aspect("equal")
px = np.array([[750, 290], [785, 460], [700, 560], [610, 585], [470, 560],
               [300, 500], [190, 430], [125, 310], [125, 230], [160, 160]], float)
q = np.c_[(px[:, 0] - 470) / 400, (460 - px[:, 1]) / 400]
u = np.r_[0, np.cumsum(np.hypot(*np.diff(q, axis=0).T))]
cs = CubicSpline(u, q)
uu = np.linspace(0, u[-1], 200)
ax.plot(*cs(uu).T, "k-", lw=1.7)
head(ax, cs(uu[-6]), cs(uu[-1]) - cs(uu[-6]), "k", 24)
ax.plot(*q[0], "o", ms=10, mfc="C0", mec="k", mew=0.8)
for a, b in (((-0.85, 0), (1.2, 0)), ((0, -0.9), (0, 1.05))):
    ax.plot(*np.c_[a, b], "k-", lw=0.9)
    head(ax, np.array(b) - 0.001 * (np.array(b) - a) / np.hypot(*(np.array(b) - a)),
         np.array(b) - a, "k", 14)
ax.text(1.28, -0.2, "$x$", ha="center")
ax.text(0.1, 1.05, "$y$", ha="center")
ax.text(-1.4, 1.05, r"$\dot{\mathbf{x}}=\mathbf{f}(\mathbf{x})$", 
        ha="left", va="center")
ax.text(2.8, 0.85, r"$\mathbf{x}=\binom{x}{y}$",
        ha="right", va="center")
ax.annotate("", xy=(q[0, 0] + 0.12, q[0, 1] + 0.1), xytext=(1.85, 0.8), zorder=6,
            arrowprops=dict(arrowstyle="->", color="k", lw=0.8, shrinkA=0,
                            shrinkB=0, mutation_scale=11))
bf.save(fig, OUT / "cont2d_phasespace.png")


# --- classification in the (T, D) plane ------------------------------------
fig = plt.figure(figsize=(bf.FULL_W, 3.9))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-5.0, 5.6)
ax.set_ylim(-3.0, 3.5)
ax.set_aspect("equal")
Tt = np.linspace(-3.7, 3.7, 300)
ax.plot(Tt, Tt ** 2 / 4, "k--", lw=1.6)
ax.plot([-4.6, 4.6], [0, 0], "k-", lw=1.4)
head(ax, (4.59, 0), (1, 0), "k", 16)
ax.plot([0, 0], [0, 3.4], "k-", lw=1.4)
head(ax, (0, 3.39), (0, 1), "k", 16)
ax.text(4.55, -0.28, "$T$", ha="center", va="top")
ax.text(0.14, 3.3, "$D$", ha="left", va="center")
ax.text(3.95, 3.2, r"$D=T^2/4$", ha="left", va="center")
small = dict(s=0.78, ms=8, lw=1.0, axes_lw=1.0, dot=6)
portrait(ax, "r1", c=(-3.3, 0.92), **small)
portrait(ax, "r3", c=(3.3, 0.92), **small)
portrait(ax, "i1", c=(-1.4, 2.35), **small)
portrait(ax, "i3", c=(1.4, 2.35), **small)
portrait(ax, "r2", c=(0, -1.75), **small)
for txt, pos in (("Stable\nnode", (-3.95, 2.3)), ("Unstable\nnode", (3.95, 2.3)),
                 ("Stable\nspiral", (-1.0, 1.0)), ("Unstable\nspiral", (1.0, 1.0)),
                 ("Saddle", (1.5, -1.5))):
    ax.text(*pos, txt, ha="center", va="center", linespacing=1.0)
bf.save(fig, OUT / "cont2d_classification.png")


# --- zoo: a nonlinear phase plane -----------------------------------------
def rot(deg):
    a = np.radians(deg)
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


fig = plt.figure(figsize=(bf.MEDIUM[0], 3.42))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-5.4, 5.4)
ax.set_ylim(-4.85, 4.85)
ax.set_aspect("equal")
ax.plot([-5.2, 5.2], [0, 0], "k-", lw=1.1)
head(ax, (5.19, 0), (1, 0), "k", 14)
ax.plot([0, 0], [-4.6, 4.6], "k-", lw=1.1)
head(ax, (0, 4.59), (0, 1), "k", 14)
ax.text(5.25, -0.3, "$x$", ha="center", va="top")
ax.text(0.15, 4.6, "$y$", ha="left", va="center")
big = dict(ms=8, lw=0.9, axes_lw=1.0, dot=6)
portrait(ax, "r3", c=(0, 0), s=1.6, **big)
portrait(ax, "i1", c=(-3.1, 2.7), s=1.3, M=rot(15), **big)
portrait(ax, "r2", c=(3.3, 2.7), s=1.3, M=rot(-20), **big)
# stable node with non-orthogonal eigenvectors (columns of M)
M = np.array([[np.cos(np.radians(35)), -np.cos(np.radians(55))],
              [np.sin(np.radians(35)), np.sin(np.radians(55))]])
portrait(ax, "r1", c=(3.3, -2.7), s=1.35, M=M, **big)
# limit cycle: r' = r(1 - r^2), theta' = 2.0
c0, R = np.array([-3.1, -2.7]), 0.95
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(c0[0] + R * np.cos(th), c0[1] + R * np.sin(th), color=BLUE, lw=2.4)
for r0, tm, th0 in ((0.15, 5.2, 0.8), (1.45, 4.0, 0.6)):
    t = np.linspace(0, tm, 400)
    r = 1 / np.sqrt(1 + (r0 ** -2 - 1) * np.exp(-2 * t))
    P = c0[:, None] + R * np.array([r * np.cos(th0 + 2.0 * t),
                                    r * np.sin(th0 + 2.0 * t)])
    ax.plot(*P, color=BLUE, lw=0.9)
    flow_arrow(ax, P, 0.6, BLUE, 8)
for ang in (110, 330):
    a = np.radians(ang)
    head(ax, c0 + R * np.array([np.cos(a), np.sin(a)]),
         [-np.sin(a), np.cos(a)], BLUE, 15)
bf.save(fig, OUT / "cont2d_zoo.png")
print("fig_schematics: written to", OUT)
