"""Conservative and gradient systems for "Two-dimensional continuous systems".

Produces (in python/_static/cont2d/):
  cont2d_conservative_E.png   contours of H = x^4/4 - x^2/2 + y^2/2 (double well),
                              open circles at the fixed points (-1,0), (0,0), (1,0)
  cont2d_gradient_ell1.png    surface S = x^2 + 2 y^2 (local minimum)
  cont2d_gradient_ell2.png    isolines of S (black) and the field -grad S (red)
  cont2d_gradient_hyp1.png    surface S = x^2 - 2 y^2 (saddle)
  cont2d_gradient_hyp2.png    isolines of S (black) and the field -grad S (red)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

# --- double well: contours of the Hamiltonian -------------------------------
g = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(g, g)
H = X**4 / 4 - X**2 / 2 + Y**2 / 2
levels = [-0.15, 0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]
plt.figure(figsize=(4.2, 4.2))
plt.contour(X, Y, H, levels=levels, colors="k", linewidths=1.5,
            linestyles="solid")
plt.plot([-1, 0, 1], [0, 0, 0], "o", mfc="w", mec="k", ms=8, mew=1.5)
plt.gca().set_aspect("equal")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.tight_layout()
plt.savefig(OUT / "cont2d_conservative_E.png", dpi=150)
plt.close()

# --- gradient systems: V = a x^2 + b y^2 -------------------------------------
for tag, (a, b) in [("ell", (1, 2)), ("hyp", (1, -2))]:
    V = lambda x, y: a * x**2 + b * y**2

    fig = plt.figure(figsize=(4.2, 4.2))
    ax = fig.add_subplot(projection="3d")
    gs = np.linspace(-2, 2, 40)
    XS, YS = np.meshgrid(gs, gs)
    ax.plot_surface(XS, YS, V(XS, YS), cmap="viridis", edgecolor="k",
                    linewidth=0.2, alpha=0.9)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$S$")
    ax.view_init(elev=28, azim=-55)
    fig.subplots_adjust(left=0.0, right=0.95, bottom=0.0, top=1.0)
    fig.savefig(OUT / f"cont2d_gradient_{tag}1.png", dpi=150)
    plt.close(fig)

    plt.figure(figsize=(4.2, 4.2))
    plt.contour(X, Y, V(X, Y), levels=12, colors="k", linewidths=1.0,
                linestyles="solid")
    gq = np.linspace(-2, 2, 15)
    XQ, YQ = np.meshgrid(gq, gq)
    plt.quiver(XQ, YQ, -2 * a * XQ, -2 * b * YQ, color="r", angles="xy",
               scale_units="xy", scale=26, width=0.006)
    plt.gca().set_aspect("equal")
    plt.xlim(-2.1, 2.1)
    plt.ylim(-2.1, 2.1)
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_gradient_{tag}2.png", dpi=150)
    plt.close()

print("fig_conservative_gradient: written to", OUT)
