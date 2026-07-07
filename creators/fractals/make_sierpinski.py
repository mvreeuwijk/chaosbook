"""Regenerate maple/_static/fractals/fractals_sierpinski.png as the Sierpinski
gasket (the book standardised on the gasket, D = log3/log2, to match the 2006
lecture and the cookbook's chaos-game example).

Run:  python creators/fractals/make_sierpinski.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 11,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                   "maple", "_static", "fractals"))
FILL = "#222222"
V0 = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])


def draw(ax, v, depth):
    if depth == 0:
        ax.fill(v[:, 0], v[:, 1], color=FILL, lw=0)
    else:
        m01 = (v[0] + v[1]) / 2
        m12 = (v[1] + v[2]) / 2
        m20 = (v[2] + v[0]) / 2
        draw(ax, np.array([v[0], m01, m20]), depth - 1)
        draw(ax, np.array([m01, v[1], m12]), depth - 1)
        draw(ax, np.array([m20, m12, v[2]]), depth - 1)


fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.6))
for ax, n in zip(axes, [0, 1, 2, 3]):
    draw(ax, V0, n)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(fr"$n = {n}$", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fractals_sierpinski.png"))
plt.close(fig)
print("wrote fractals_sierpinski.png (Sierpinski gasket)")
