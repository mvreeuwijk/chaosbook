"""Schematic of the three-body problem, redrawn in matplotlib.

Produces (in python/_static/phenomenon/):
  3body.png   three bodies m_1, m_2, m_3 at positions x_1, x_2, x_3 (dashed
              arrows from the origin) and the vectors x_j - x_i between them
              (solid arrows) that enter the gravitational forces
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "phenomenon"
OUT.mkdir(parents=True, exist_ok=True)


def arrow(ax, p, q, ls="-", lw=1.0, ms=10, shrink=(0, 0)):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(
        arrowstyle="-|>", color="k", lw=lw, ls=ls, mutation_scale=ms,
        shrinkA=shrink[0], shrinkB=shrink[1]))


O = np.array([3.95, 1.41])
body = {1: np.array([3.95, 3.75]), 2: np.array([0.4, 1.4]),
        3: np.array([6.3, 0.25])}
fig = plt.figure(figsize=(3.8, 2.5))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(-0.35, 7.05)
ax.set_ylim(-0.1, 4.45)
ax.set_aspect("equal")

for i, p in body.items():
    arrow(ax, O, p, ls="--", lw=0.8, ms=8, shrink=(0, 6))
for i, j in ((1, 2), (2, 3), (3, 1)):
    arrow(ax, body[i], body[j], shrink=(6, 6))
for p in body.values():
    ax.plot(*p, "ko", ms=6, zorder=5)
ax.plot(*O, "k.", ms=4)

lab = dict(fontsize=10, ha="center", va="center")
ax.text(*(body[1] + [0.35, 0.18]), "$m_1$", **lab)
ax.text(*(body[2] + [0.0, 0.38]), "$m_2$", **lab)
ax.text(*(body[3] + [0.0, -0.3]), "$m_3$", **lab)
ax.text(O[0] - 0.32, O[1] + 0.2, "$O$", fontsize=10, ha="center", va="center")
ax.text(4.2, 2.65, r"$\mathbf{x}_1$", **lab)
ax.text(2.2, 1.68, r"$\mathbf{x}_2$", **lab)
ax.text(5.3, 1.12, r"$\mathbf{x}_3$", **lab)
ax.text(1.55, 3.0, r"$\mathbf{x}_2-\mathbf{x}_1$", fontsize=9, ha="center",
        va="center", rotation=34)
ax.text(3.5, 0.2, r"$\mathbf{x}_3-\mathbf{x}_2$", fontsize=9, ha="center",
        va="center", rotation=-11)
ax.text(5.55, 2.35, r"$\mathbf{x}_1-\mathbf{x}_3$", fontsize=9, ha="center",
        va="center", rotation=-58)
bf.save(fig, OUT / "3body.png")
print("fig_schematics: written to", OUT)
