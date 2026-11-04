"""Exercise figures that are sketches or plots, redrawn in matplotlib.

Produces (in python/_static/exercises/):
  NuclearReactorCooling.png  natural-convection reactor loop (cont2d exercise)
  ex0082r00_1.png            U-tube with bubbles (disc2d exercise 'Kicked U-tube')
  ex0093r00.png              Newton-Raphson iteration (disc1d exercise)
  ex0036r03_fig1.png         earth-moon-satellite collage (phenomenon
                             exercise): the photographs are taken from the
                             Maple edition and the labels of the lost pstex
                             text layer are drawn on top

Left as they are (not redrawn):
  ex0082r00_2.png            raster basin-of-attraction map taken from the
                             literature; it cannot be regenerated from the
                             information in the exercise
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, save)

OUT = bf.out("exercises")

# Each sketch below was drawn at a larger size and is now drawn at the size it
# is printed; S scales line widths, markers and arrows to match, text is set
# to the style's 8-9 pt.
S = 1.0


def arrow(ax, p, q, ms=18, lw=1.5, color="k", style="-|>"):
    ax.annotate("", xy=q, xytext=p, zorder=6, arrowprops=dict(
        arrowstyle=style, color=color, lw=lw * S, mutation_scale=ms * S,
        shrinkA=0, shrinkB=0))


def blank(figsize, xlim, ylim):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    return fig, ax


S = 0.77
# --- natural-convection reactor cooling -------------------------------------
fig, ax = blank((2.8, 3.27), (-0.1, 11.7), (-0.1, 13.7))
k = dict(color="k", lw=1, solid_capstyle="butt")
ax.add_patch(Rectangle((0.03, 4.19), 3.3, 5.76, fc="w", ec="k", lw=1))   # riser
ax.add_patch(Rectangle((0.03, 1.70), 3.3, 2.49, fc="w", ec="k", lw=1))   # core
ax.add_patch(Rectangle((8.31, 1.70), 3.29, 8.25, fc="w", ec="k", lw=1))  # downcomer
for x0, x1 in ((0.62, 0.74), (2.05, 2.17), (2.75, 2.87)):                  # rods
    ax.add_patch(Rectangle((x0, 1.70), x1 - x0, 2.49, fc="w", ec="k", lw=0.77))
ax.plot([1.45, 1.45], [1.70, 4.19], **k)
# double-walled pipes (outer and inner wall)
top_o = [(1.33, 9.95), (1.33, 11.60), (10.18, 11.60), (10.18, 9.95)]
top_i = [(1.69, 9.95), (1.69, 11.14), (9.84, 11.14), (9.84, 9.95)]
bot_o = [(1.33, 1.70), (1.33, 0.03), (10.18, 0.03), (10.18, 1.70)]
bot_i = [(1.69, 1.70), (1.69, 0.52), (9.84, 0.52), (9.84, 1.70)]
for pts in (top_o, top_i, bot_o, bot_i):
    ax.plot(*np.array(pts).T, **k)
# cooler: coil strips across the top pipe, coolant tube through it
ax.add_patch(Rectangle((5.40, 12.09), 0.22, 1.53, fc="w", ec="k", lw=1, zorder=3))
ax.add_patch(Rectangle((4.05, 8.92), 0.23, 1.55, fc="w", ec="k", lw=1, zorder=3))
for d in range(4):
    x = 0.35 * d
    ax.add_patch(Polygon([(4.05 + x, 10.55), (4.28 + x, 10.55), (4.58 + x, 12.07),
                          (4.35 + x, 12.07)], fc="w", ec="k", lw=1, zorder=4))
# flow arrows and labels
arrow(ax, (5.7, 11.37), (8.75, 11.37), ms=26)
arrow(ax, (6.65, 0.27), (3.6, 0.27), ms=26)
# bubbles in the riser
rng = np.random.default_rng(2)
for x, y, r in ((0.5, 9.2, 0.18), (1.4, 8.9, 0.14), (2.5, 9.3, 0.12), (0.8, 8.1, 0.14),
                (2.9, 8.1, 0.08), (0.7, 7.5, 0.07), (1.8, 7.5, 0.12),
                (2.6, 7.2, 0.2), (1.9, 8.4, 0.09)):
    ax.add_patch(Circle((x, y), r, fc="w", ec="k", lw=0.69))
txt = dict(ha="center", va="center", fontsize=9)
ax.text(1.0, 5.9, "Riser", rotation=90, **txt)
ax.text(1.0, 2.9, "Core", rotation=90, **txt)
ax.text(9.7, 6.4, "Downcomer", rotation=-90, **txt)
ax.text(2.1, 5.2, "$T$", **txt)
ax.text(7.1, 10.55, "$Q$", **txt)
ax.text(4.35, 3.75, "$P$", **txt)
ax.text(4.0, 12.55, "Cooler", **txt)
# heating power P entering the core
ax.add_patch(Polygon([(3.35, 2.75), (4.28, 2.4), (4.28, 3.1)], fc="w", ec="k",
                     lw=1, zorder=4))
ax.plot(*np.array([(4.28, 2.75), (4.78, 2.75), (5.23, 3.72), (5.70, 2.27),
                   (6.40, 3.72), (6.88, 2.77)]).T, **k)
bf.save(fig, OUT / "NuclearReactorCooling.png")


S = 0.62
# --- U-tube with bubbles ------------------------------------------------------
fig, ax = blank((1.3, 1.86), (-0.75, 3.75), (-0.55, 4.6))
cx, rad, wall = 1.5, 1.2, 0.17        # tube centre-line radius, wall gap
th = np.linspace(np.pi, 2 * np.pi, 100)
yb, ytop = 1.4, 4.1                    # bottom centre of the bend, top of legs
xl, xr = cx - rad, cx + rad
for d in (-wall, wall):
    r_ = rad + d
    arc = np.array([(cx + r_ * np.cos(a), yb + rad + r_ * np.sin(a)) for a in th])
    left = np.array([(cx - r_, ytop), (cx - r_, yb + rad)])
    right = np.array([(cx + r_, yb + rad), (cx + r_, ytop)])
    ax.plot(*np.vstack([left, arc, right]).T, "k-", lw=0.81)
ax.text(xl, ytop + 0.28, "1", ha="center", va="center", fontsize=8)
ax.text(xr, ytop + 0.28, "2", ha="center", va="center", fontsize=8)
yeq = 3.15
ax.plot([-0.4, 3.45], [yeq, yeq], "k:", lw=0.81)
ax.plot([xl - wall - 0.18, xl - wall], [yeq + 0.28] * 2, "k-", lw=0.62)   # level 1
ax.plot([xr + wall, xr + wall + 0.18], [yeq - 0.22] * 2, "k-", lw=0.62)   # level 2
ax.annotate("", xy=(xl - wall - 0.09, yeq + 0.27), xytext=(xl - wall - 0.09, yeq),
            arrowprops=dict(arrowstyle="<->", lw=0.56, color="k", shrinkA=0,
                            shrinkB=0, mutation_scale=4.34))
ax.annotate("", xy=(xr + wall + 0.09, yeq - 0.21), xytext=(xr + wall + 0.09, yeq),
            arrowprops=dict(arrowstyle="<->", lw=0.56, color="k", shrinkA=0,
                            shrinkB=0, mutation_scale=4.34))
ax.text(xl - wall - 0.35, yeq + 0.45, r"$\delta_1$", ha="center", va="center",
        fontsize=8)
ax.text(xr + wall + 0.45, yeq - 0.55, r"$\delta_2$", ha="center", va="center",
        fontsize=8)
for x, y in ((xl, 3.0), (xl, 1.95), (xr, 2.55), (cx - 0.2, yb)):
    ax.plot(x, y, "o", ms=2.48, color="0.6", zorder=5)
ax.annotate("", xy=(cx + 0.65, yb), xytext=(cx, yb),
            arrowprops=dict(arrowstyle="-|>", lw=0.56, color="k", shrinkA=0,
                            shrinkB=0, mutation_scale=4.34))
arrow(ax, (cx, 0.15), (cx, 0.95), ms=16, lw=2.0)
ax.text(cx, -0.25, "bubble in", ha="center", va="center", fontsize=8)
bf.save(fig, OUT / "ex0082r00_1.png")


S = 0.76
# --- Newton-Raphson ----------------------------------------------------------
XR, XM, A, B = 1.75, 3.5, 0.449, 0.0273      # root, inflection, slopes


def g(x):
    return A * (x - XR) + B * ((x - XM) ** 3 + (XM - XR) ** 3)


def dg(x):
    return A + 3 * B * (x - XM) ** 2


x0 = 5.5
x1 = x0 - g(x0) / dg(x0)
x2 = x1 - g(x1) / dg(x1)
fig, ax = blank((3.8, 2.32), (-0.35, 7.5), (-0.55, 4.5))
xx = np.linspace(0.65, 6.4, 300)
ax.plot(xx, g(xx), "k-", lw=1.67)
ax.plot([-0.2, 7.1], [0, 0], "k-", lw=0.91)
arrow(ax, (6.9, 0), (7.15, 0), ms=18, lw=1.2)
ax.plot([1.0, 1.0], [-0.35, 4.3], "k-", lw=0.91)
arrow(ax, (1.0, 4.1), (1.0, 4.35), ms=18, lw=1.2)
ax.text(7.35, -0.3, "$x$", ha="center", va="center", fontsize=9)
ax.text(0.55, 4.3, "$g(x)$", ha="center", va="center", fontsize=9)
for a, b in ((x0, x1), (x1, x2)):          # tangent lines
    xs = np.array([b - 0.5, a + 0.7])
    ax.plot(xs, g(a) + dg(a) * (xs - a), "k-", lw=0.76)
for xi, name in ((x0, "x_0"), (x1, "x_1")):
    ax.plot([xi, xi], [0, g(xi)], "k--", lw=0.76)
    ax.plot(xi, g(xi), "ko", ms=6.08, zorder=5)
    ax.plot(xi, 0, "ko", ms=6.08, zorder=5)
ax.plot(x2, 0, "ko", ms=6.08, zorder=5)
ax.text(x0 - 0.6, g(x0) + 0.28, "$g(x_0)$", ha="center", va="center", fontsize=9)
ax.text(x1 - 0.2, g(x1) + 0.4, "$g(x_1)$", ha="center", va="center", fontsize=9)
ax.text(x0, -0.38, "$x_0$", ha="center", va="center", fontsize=9)
ax.text(x1, -0.38, "$x_1$", ha="center", va="center", fontsize=9)
ax.text(x2 - 0.05, 0.32, "$x_2$", ha="center", va="center", fontsize=9)
bf.save(fig, OUT / "ex0093r00.png")

# --- earth, moon and satellite: label the photograph collage ----------------
SRC = Path(__file__).resolve().parents[3] / "maple" / "_static" / "exercises"
img = plt.imread(SRC / "ex0036r03_fig1.png")
h, w = img.shape[:2]
fig = plt.figure(figsize=(bf.MEDIUM[0], bf.MEDIUM[0] * h / w))
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img)
ax.axis("off")
lab = dict(ha="center", va="center", fontsize=8)
ax.text(120, 360, "earth, $m_1$", **lab)
ax.text(1135, 625, "moon, $m_2$", **lab)
ax.text(735, 105, "satellite", **lab)
ax.text(805, 493, "$x$", **lab)
ax.text(413, 140, "$y$", **lab)
ax.text(395, 520, "$O$", **lab)
ax.text(780, 375, r"$\mathbf{x}_2$", **lab)
ax.text(330, 625, r"$\mathbf{x}_1$", **lab)
ax.text(620, 745, "$R$", **lab)
bf.save(fig, OUT / "ex0036r03_fig1.png")

print("fig_exercises: written to", OUT)
