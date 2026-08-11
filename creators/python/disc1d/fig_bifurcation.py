"""Bifurcation-diagram figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_bifur_theo.png            analytical branches (period 1,2,4)
  disc1d_logist_stability_p3both.png      period-3 stable/unstable branches
  disc1d_bifurcation_implicit_sin.png     implicit x = f^(4)(x), sine map
  disc1d_logist_series_bifurcation.png    numerical bifurcation diagram
  disc1d_logist_series_bifurcation_zoom_doubling.png
  disc1d_logist_series_bifurcation_zoom_p3.png
  interactive/bifurcation_zoom.html       high-resolution pan/zoom diagram
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import brentq

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def compose(f, m, x, r):
    for _ in range(m):
        x = f(x, r)
    return x


def periodic_points(m, r, exclude=()):
    xs = np.linspace(0, 1, 4001)
    h = compose(cb.logistic, m, xs, r) - xs
    roots = []
    for i in range(len(xs) - 1):
        if h[i] == 0 or h[i] * h[i + 1] < 0:
            root = brentq(lambda x: compose(cb.logistic, m, x, r) - x,
                          xs[i], xs[i + 1])
            if all(abs(root - e) > 1e-6 for e in exclude + tuple(roots)):
                roots.append(root)
    return roots


def sigma_at(p, r, m=3):
    """Stability of the m-cycle through p: product of f' along its own orbit."""
    sig, x = 1.0, p
    for _ in range(m):
        sig *= r * (1 - 2 * x)
        x = cb.logistic(x, r)
    return sig


# -- analytical branches: periods 1, 2 and 4 ---------------------------------
plt.figure(figsize=(4.2, 3.2))
rs = np.linspace(0.5, 3.6, 500)
plt.plot(rs, np.where(rs < 1, 0, np.nan), "k")            # x*=0 stable
plt.plot(rs, np.where(rs >= 1, 0, np.nan), "gray")         # x*=0 unstable
x1 = 1 - 1 / rs
plt.plot(rs, np.where((rs > 1) & (rs < 3), x1, np.nan), "k")
plt.plot(rs, np.where(rs >= 3, x1, np.nan), color="gray")
r2 = np.linspace(3.0, 3.6, 400)
disc = np.sqrt(r2**2 - 2 * r2 - 3)
for sign in [+1, -1]:
    branch = (r2 + 1 + sign * disc) / (2 * r2)
    stable = r2 < 1 + np.sqrt(6)
    plt.plot(r2[stable], branch[stable], "k")
    plt.plot(r2[~stable], branch[~stable], color="gray")
for r in np.linspace(1 + np.sqrt(6) + 1e-4, 3.56, 120):   # period-4, numeric
    pts = periodic_points(4, r, exclude=tuple(
        [0, 1 - 1 / r] + periodic_points(2, r, exclude=(0, 1 - 1 / r))))
    for p in pts:
        plt.plot(r, p, "k.", markersize=2)
plt.xlabel("$r$")
plt.ylabel("$x^*(r)$")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_bifur_theo.png", dpi=150)
plt.close()

# -- period-3 stable and unstable branches -----------------------------------
plt.figure(figsize=(4.2, 3.2))
for r in np.linspace(3.8284, 3.856, 140):
    pts = periodic_points(3, r, exclude=(0, 1 - 1 / r))
    if len(pts) >= 6:
        for p in pts:
            color = "k" if abs(sigma_at(p, r)) < 1 else "gray"
            plt.plot(r, p, ".", color=color, markersize=2)
plt.xlabel("$r$")
plt.ylabel("$x^*(r)$")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_stability_p3both.png", dpi=150)
plt.close()

# -- implicit plot x = f^(4)(x) for the sine map -----------------------------
R, Xg = np.meshgrid(np.linspace(0.0, 1, 400), np.linspace(0, 1, 400))
plt.figure(figsize=(5.0, 3.5))
plt.contour(R, Xg, compose(cb.sine, 4, Xg, R) - Xg, levels=[0],
            colors="black", linewidths=1.5)
plt.axis([0, 1, -0.1, 1])
plt.xlabel("$r$")
plt.ylabel("$x(r)$")
plt.tight_layout()
plt.savefig(OUT / "disc1d_bifurcation_implicit_sin.png", dpi=150)
plt.close()

# -- numerical bifurcation diagram --------------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.5))
cb.bifurcation_diagram(cb.logistic, 3.3, 4.0, nr=500, n=1000,
                       x0=0.57, discard=0.8, ax=ax)
ax.set_xlim(3.3, 4.0)
ax.set_ylim(0, 1)
ax.set_xlabel("$r$")
ax.set_ylabel("$x(r)$")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_series_bifurcation.png", dpi=150)
plt.close()

# -- zooms on the bifurcation diagram -----------------------------------------
for rmin, rmax, name in [
    (2.8, 3.6, "disc1d_logist_series_bifurcation_zoom_doubling"),
    (3.82, 3.86, "disc1d_logist_series_bifurcation_zoom_p3"),
]:
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    cb.bifurcation_diagram(cb.logistic, rmin, rmax, nr=500, n=1000,
                           x0=0.57, discard=0.8, ax=ax)
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0, 1)
    ax.set_xlabel("$r$")
    ax.set_ylabel("$x(r)$")
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()

# -- interactive: high-resolution pan/zoom bifurcation diagram ---------------
rs, xs = [], []
for r in np.linspace(2.5, 4.0, 2001):
    X = cb.orbit(cb.logistic, x0=0.57, n=1000, r=r)
    rs.extend([r] * 150)
    xs.extend(X[-150:])
fig = go.Figure(go.Scattergl(x=rs, y=xs, mode="markers",
                             marker=dict(size=1, color="darkblue")))
fig.update_layout(
    xaxis_title="r", yaxis_title="x(r)",
    margin=dict(l=40, r=10, t=10, b=40),
    dragmode="zoom",
)
fig.write_html(OUT / "interactive" / "bifurcation_zoom.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_bifurcation: assets written to", OUT)
