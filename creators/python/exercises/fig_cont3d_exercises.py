"""Exercise figures of "Chaos in continuous systems", redrawn in matplotlib.

Produces (in python/_static/exercises/):
  ex0089r01_1.png   sketch of a neuron: dendrites, cell body, axon with
                    Schwann cells and nodes of Ranvier, axon terminals
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, save)

OUT = bf.out("exercises")

BODY, AXON, TERM = "#c9c4e6", "#f5d98a", "#d9a7a0"


def branch(ax, p, ang, length, depth, color, lw):
    """Recursive, deterministic tree of tapering branches."""
    q = (p[0] + length * np.cos(ang), p[1] + length * np.sin(ang))
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, solid_capstyle="round")
    if depth:
        branch(ax, q, ang + 0.5, 0.65 * length, depth - 1, color, 0.7 * lw)
        branch(ax, q, ang - 0.45, 0.7 * length, depth - 1, color, 0.7 * lw)


fig, ax = plt.subplots(figsize=(3.8, 1.9))
# dendrites (left) from the cell body
body = (1.6, 1.4)
for ang, ln in [(2.5, 0.6), (1.9, 0.75), (1.35, 0.65), (3.3, 0.6), (3.9, 0.65),
                (4.5, 0.6), (5.1, 0.55)]:
    branch(ax, body, ang, ln, 2, BODY, 2.3)
ax.add_patch(Ellipse(body, 1.0, 0.8, fc=BODY, ec="k", lw=0.8, zorder=3))
ax.add_patch(Ellipse((1.5, 1.35), 0.35, 0.28, fc="#8fc79a", ec="k", lw=0.6, zorder=4))
# axon: chain of Schwann cells following a shallow arc
cells = [(2.75, 1.1, -20), (3.65, 0.75, -12), (4.6, 0.7, 5), (5.5, 0.95, 32), (6.1, 1.6, 62)]
for x, y, a_ in cells:
    ax.add_patch(Ellipse((x, y), 1.05, 0.42, angle=a_, fc=AXON, ec="k", lw=0.8, zorder=3))
    ax.plot(x, y, "o", ms=2.5, color="#d98a70", zorder=4)
# axon terminals (right)
end = (6.3, 1.95)
for ang in (0.3, 0.8, 1.3, -0.3):
    branch(ax, end, ang, 0.45, 2, TERM, 1.7)
# labels
kw = dict(fontsize=7, ha="center", va="center")
arrow = dict(arrowstyle="-|>", color="k", lw=0.7, mutation_scale=7)
for txt, xy, xt in [("Dendrite", (1.2, 2.2), (0.8, 3.0)),
                    ("Cell body", (1.85, 1.65), (2.7, 2.7)),
                    ("Nucleus", (1.45, 1.25), (0.3, -0.1)),
                    ("Axon", (2.3, 0.95), (3.0, 0.0)),
                    ("Node of Ranvier", (5.9, 1.3), (4.2, 2.2)),
                    ("Schwann cell", (5.6, 0.85), (6.9, 0.1)),
                    ("Myelin sheath", (4.6, 0.45), (4.7, -0.5)),
                    ("Axon terminal", (7.0, 2.35), (7.4, 3.2))]:
    ax.annotate(txt, xy=xy, xytext=xt, arrowprops=arrow, **kw)
ax.set_xlim(-0.2, 8.4); ax.set_ylim(-0.8, 3.5); ax.set_aspect("equal"); ax.axis("off")
bf.save(fig, OUT / "ex0089r01_1.png")
print("fig_cont3d_exercises: done")
