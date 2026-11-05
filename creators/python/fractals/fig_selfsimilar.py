"""Self-similar constructions for "Fractal geometries".

Produces (in python/_static/fractals/):
  fractals_koch.png        von Koch curve, generations 0-3
  fractals_cantor.png      middle-third Cantor set, generations 0-5
  fractals_sierpinski.png  Sierpinski gasket, generations 0-3
  fractals_kochisland.png  Koch island, generations 0-2
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = bf.out("fractals")


def koch_step(pts, turn):
    """Replace every segment by four; the bump is the first third rotated by turn."""
    new = []
    for p, q in zip(pts[:-1], pts[1:]):
        d = (q - p) / 3
        new += [p, p + d, p + d + d * np.exp(1j * turn), p + 2 * d]
    return new + [pts[-1]]


# -- von Koch curve ----------------------------------------------------------
fig, axes = plt.subplots(4, 1, figsize=(3.0, 4.2))
pts = [0j, 1 + 0j]
for n, ax in enumerate(axes):
    z = np.array(pts)
    ax.plot(z.real, z.imag, "k", lw=1.5)
    ax.set_aspect("equal")
    ax.set_xlim(-0.2, 1.02)
    ax.set_ylim(-0.02, 0.34)
    ax.axis("off")
    ax.text(-0.03, 0.0, f"$n={n}$", ha="right", va="center")
    pts = koch_step(pts, np.pi / 3)
bf.save(fig, OUT / "fractals_koch.png")

# -- Cantor set --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(bf.MEDIUM[0], 2.0))
segs = [(0.0, 1.0)]
for n in range(6):
    for a, b in segs:
        ax.fill_between([a, b], -n - 0.3, -n + 0.3, color="k", lw=0)
    ax.text(-0.03, -n, f"$n={n}$", ha="right", va="center")
    segs = [s for a, b in segs
            for s in ((a, a + (b - a) / 3), (b - (b - a) / 3, b))]
ax.set_xlim(-0.25, 1.01)
ax.axis("off")
bf.save(fig, OUT / "fractals_cantor.png")

# -- Sierpinski gasket (ported from creators/fractals/make_sierpinski.py) ----
V0 = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])


def draw(ax, v, depth):
    if depth == 0:
        ax.fill(v[:, 0], v[:, 1], color="#222222", lw=0)
    else:
        m01, m12, m20 = (v[0] + v[1]) / 2, (v[1] + v[2]) / 2, (v[2] + v[0]) / 2
        draw(ax, np.array([v[0], m01, m20]), depth - 1)
        draw(ax, np.array([m01, v[1], m12]), depth - 1)
        draw(ax, np.array([m20, m12, v[2]]), depth - 1)


fig, axes = plt.subplots(1, 4, figsize=(bf.FULL_W, 1.6))
for n, ax in enumerate(axes):
    draw(ax, V0, n)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"$n={n}$")
bf.save(fig, OUT / "fractals_sierpinski.png")

# -- Koch island -------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(bf.FULL_W, 2.1))
for n, ax in enumerate(axes):
    corners = [0j, 1 + 0j, 0.5 + 1j * np.sqrt(3) / 2, 0j]
    for _ in range(n):  # outward bumps: rotate by -pi/3 on this orientation
        corners = koch_step(corners, -np.pi / 3)
    z = np.array(corners)
    ax.fill(z.real, z.imag, color="#d9d9d9", ec="k", lw=1.5)
    ax.set_aspect("equal")
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-0.45, 1.25)
    ax.axis("off")
    ax.set_title(f"$n={n}$")
bf.save(fig, OUT / "fractals_kochisland.png")
print("wrote koch, cantor, sierpinski, kochisland")
