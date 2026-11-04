"""Conservative and gradient systems for "Two-dimensional continuous systems".

Produces (in python/_static/cont2d/):
  cont2d_conservative_E.png   contours of H = x^4/4 - x^2/2 + y^2/2 (double well),
                              open circles at the fixed points (-1,0), (0,0), (1,0)
  cont2d_gradient.png         2x2 figure: (a) surface S = x^2 + 2 y^2 (local minimum),
                              (b) its isolines (black) and the field -grad S (red),
                              (c) surface S = x^2 - 2 y^2 (saddle), (d) its isolines
                              and field
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

# --- double well: contours of the Hamiltonian -------------------------------
g = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(g, g)
H = X**4 / 4 - X**2 / 2 + Y**2 / 2
levels = [-0.15, 0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]
plt.figure(figsize=bf.SQUARE)
plt.contour(X, Y, H, levels=levels, colors="k", linewidths=1.0,
            linestyles="solid")
plt.plot([-1, 0, 1], [0, 0, 0], "o", mfc="w", mec="k", ms=6, mew=1.0)
plt.gca().set_aspect("equal")
plt.xlabel("$x$")
plt.ylabel("$y$")
bf.save(plt.gcf(), OUT / "cont2d_conservative_E.png")

# --- gradient systems: V = a x^2 + b y^2 -------------------------------------
fig = plt.figure(figsize=(bf.FULL_W, 5.4))
gs_ = fig.add_gridspec(2, 2)
axs = np.empty((2, 2), dtype=object)
for row, (a, b) in enumerate([(1, 2), (1, -2)]):
    V = lambda x, y: a * x**2 + b * y**2

    ax = axs[row, 0] = fig.add_subplot(gs_[row, 0], projection="3d")
    gs = np.linspace(-2, 2, 40)
    XS, YS = np.meshgrid(gs, gs)
    ax.plot_surface(XS, YS, V(XS, YS), cmap="viridis", edgecolor="k",
                    linewidth=0.2, alpha=0.9)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$S$")
    ax.view_init(elev=28, azim=-55)

    ax = axs[row, 1] = fig.add_subplot(gs_[row, 1])
    ax.contour(X, Y, V(X, Y), levels=12, colors="k", linewidths=0.8,
               linestyles="solid")
    gq = np.linspace(-2, 2, 15)
    XQ, YQ = np.meshgrid(gq, gq)
    ax.quiver(XQ, YQ, -2 * a * XQ, -2 * b * YQ, color="r", angles="xy",
              scale_units="xy", scale=26, width=0.006)
    ax.set_aspect("equal")
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.1)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
bf.panel_labels(axs)
bf.save(fig, OUT / "cont2d_gradient.png")

print("fig_conservative_gradient: written to", OUT)
