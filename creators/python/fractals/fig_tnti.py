"""Self-similar model of the turbulent/non-turbulent interface.

Produces (in python/_static/fractals/):
  fractals_tnti.png   (a) generator, (b) interfaces for r = 0.3 and 0.2,
                      (c) the exponent beta(r) = log m / log(2/m), m = sqrt(1+4 r^2)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "fractals"
OUT.mkdir(parents=True, exist_ok=True)

GRAY, RED = "#888888", "#b22222"


def beta(r):
    m = np.sqrt(1 + 4 * r**2)
    return np.log(m) / np.log(2 / m)


def interface(r, n):
    """n generations: each segment becomes two meeting at a vertex displaced
    r*length off the midpoint, the side alternating along the curve."""
    pts = [0j, 1 + 0j]
    for _ in range(n):
        new, side = [], 1
        for p, q in zip(pts[:-1], pts[1:]):
            apex = (p + q) / 2 + side * 1j * r * (q - p)
            new += [p, apex]
            side = -side
        pts = new + [pts[-1]]
    return np.array(pts)


fig = plt.figure(figsize=(9.0, 3.2))
gs = fig.add_gridspec(2, 3, width_ratios=[1.1, 1.1, 1.1], wspace=0.25)

ax = fig.add_subplot(gs[:, 0])
r0 = 0.3
ax.plot([0, 1], [0, 0], "--", color=GRAY, lw=1.2)
ax.plot([0, 0.5, 1], [0, r0, 0], "k", lw=2)
ax.plot([0, 0.5, 1], [0, r0, 0], "ko", ms=4)
ax.plot([0.5, 0.5], [0, r0], color=RED, lw=1.5)
ax.text(0.53, r0 / 2, r"$r\,l_n$", color=RED, va="center")
ax.text(0.5, -0.07, "$l_n$", color=GRAY, ha="center", va="top")
ax.text(0.2, 0.2, "$l_{n+1}$", rotation=31, ha="center")
ax.set_title("(a) generator")
ax.set_aspect("equal")
ax.set_ylim(-0.25, 0.5)
ax.axis("off")

for row, r in enumerate([0.3, 0.2]):
    ax = fig.add_subplot(gs[row, 1])
    z = interface(r, 5)
    ax.plot(z.real, z.imag, "k", lw=1)
    ax.set_aspect("equal")
    ax.set_ylim(-0.3, 0.3)
    ax.axis("off")
    ax.set_title(rf"$r={r}$,  $\beta\approx{beta(r):.2f}$", fontsize=11, y=-0.05)
    if row == 0:
        ax.text(0.5, 0.42, "(b) sample interfaces", ha="center", fontsize=13)
        ax.set_ylim(-0.3, 0.38)

ax = fig.add_subplot(gs[:, 2])
rr = np.linspace(0.005, 0.5, 300)
ax.plot(rr, beta(rr), "k", lw=2)
ax.axhline(1 / 3, color=GRAY, ls=":", lw=1.3)
r13 = rr[np.argmin(abs(beta(rr) - 1 / 3))]
ax.plot([r13], [1 / 3], "o", color=RED)
ax.text(0.02, 0.35, r"$\beta=1/3$", color=GRAY)
ax.set_xlim(0, 0.5)
ax.set_ylim(0, 1.02)
ax.set_xlabel("$r$")
ax.set_ylabel(r"$\beta$")
ax.set_title(r"(c) $\beta=\log m/\log(2/m)$")

fig.savefig(OUT / "fractals_tnti.png", dpi=150, bbox_inches="tight")
print("wrote fractals_tnti.png; r for beta=1/3:", round(r13, 3))
