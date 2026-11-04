"""Shared plotting helpers for the cont1d figure scripts."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

PANEL = (4.2, 3.2)      # panel in a 2-column subfigure
SQUARE = (4.2, 4.2)     # square panel (phase-plot style)
SINGLE = (5.0, 3.5)     # single full-width figure
GRAY = "0.7"            # unstable branches


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=150)
    plt.close(fig)


def cross_axes(ax, xlabel, ylabel, zero=False, ticked=False):
    """Axes crossing at the origin (the book's graph-of-f(x) look), with
    the axis labels at the ends of the axes and no tick labels.

    With ticked=True the plot is boxed instead: the tick labels sit on the
    frame, away from the curve and the fixed-point markers, and the zero
    axes are drawn as thin lines through the origin."""
    if ticked:
        ax.axhline(0, color="k", lw=0.8, zorder=1)
        ax.axvline(0, color="k", lw=0.8, zorder=1)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    if not ticked:
        ax.set_xticks([])
        ax.set_yticks([])
    ax.annotate(xlabel, (1, 0), xycoords=("axes fraction", "data"),
                xytext=(0, -22 if ticked else -5), textcoords="offset points",
                ha="right", va="top")
    ax.annotate(ylabel, (0, 1), xycoords=("data", "axes fraction"),
                xytext=(6 if ticked else -5, -2), textcoords="offset points",
                ha="left" if ticked else "right", va="top")
    if zero:
        ax.annotate("0", (0, 0), xytext=(-4, -4), textcoords="offset points",
                    ha="right", va="top", fontsize=11)


def mark_fixed_points(ax, f, xlo, xhi, dfdx=None, size=8, marginal="half",
                      **params):
    """Plot the fixed points of f on the x-axis: filled = stable, open =
    unstable, half-filled = marginal (sigma = 0; marginal="stable" fills it)."""
    xs = cb.fixed_points(f, xlo, xhi, **params)
    sig = cb.stability(f, xs, dfdx=dfdx, **params)
    for x, kind in zip(xs, cb.classify(sig, tol=1e-6)):
        if kind == "marginal" and marginal == "stable":
            kind = "stable"
        if kind == "stable":
            ax.plot(x, 0, "o", ms=size, mfc="k", mec="k", clip_on=False, zorder=5)
        elif kind == "unstable":
            ax.plot(x, 0, "o", ms=size, mfc="w", mec="k", clip_on=False, zorder=5)
        else:
            ax.plot(x, 0, "o", ms=size, mfc="k", mec="k", mfcalt="w",
                    fillstyle="right", clip_on=False, zorder=5)
    return xs, sig


def plot_branches(ax, segs, lw=4):
    """Draw cb.fixed_point_branches output: stable black, unstable gray."""
    for p, x, stable in segs:
        # both above the axis spines (zorder 2.5), so the gray branch on
        # the r-axis stays visible
        ax.plot(p, x, color="k" if stable else GRAY, lw=lw,
                solid_capstyle="butt", zorder=4 if stable else 3)


def ferro(x, T=0.5, m=0.0):
    """Mean-field ferromagnet: dx/dt = -x + tanh((x + m)/T)."""
    return -x + np.tanh((x + m) / T)


def dferro(x, T=0.5, m=0.0):
    return -1 + (1 - np.tanh((x + m) / T) ** 2) / T
