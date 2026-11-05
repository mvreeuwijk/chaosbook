"""Fixed-point and periodic-solution figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_attractor_r1_5.png        many x0 converge to x*=1/3
  disc1d_logist_attractor_local.png       1x2: superstable (r=2), ordinary (r=1.5)
  disc1d_logist_p2graph.png               f, g=f(f(x)), y=x at r=3.2
  disc1d_logist_p3graph.png               1x2: f, f^(3), y=x at r=3.80, 3.84
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- global attraction: many initial conditions at r = 1.5 -------------------
plt.figure(figsize=bf.MEDIUM)
for x0 in [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    X = cb.orbit(cb.logistic, x0=x0, n=20, r=1.5)
    plt.plot(range(len(X)), X, "-o", markersize=3)
plt.axhline(1 / 3, color="gray", linewidth=0.8)
plt.xlabel("$n$")
plt.ylabel("$x_n$")
bf.save(plt.gcf(), OUT / "disc1d_logist_attractor_r1_5.png")

# -- local convergence: superstable (r=2) vs ordinary (r=1.5), 1x2 ----------
fig, axs = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.3))
for ax, (r, xstar) in zip(axs, [(2.0, 0.5), (1.5, 1 / 3)]):
    X = cb.orbit(cb.logistic, x0=xstar + 0.2, n=12, r=r)
    ax.plot(range(len(X)), X, "-o", markersize=3)
    ax.axhline(xstar, color="gray", linewidth=0.8)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$x_n$")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_logist_attractor_local.png")


def compose(f, m, x, r):
    for _ in range(m):
        x = f(x, r)
    return x


def periodic_points(m, r, exclude=()):
    """Real solutions of x = f^(m)(x) on [0,1], minus the excluded points."""
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


# -- f, g = f(f(x)), y = x at r = 3.2 with period-2 and fixed points ---------
r = 3.2
xs = np.linspace(0, 1, 400)
fig, ax = plt.subplots(figsize=bf.SQUARE)
ax.plot(xs, cb.logistic(xs, r), "k", label="$f(x)$")
ax.plot(xs, compose(cb.logistic, 2, xs, r), "k--", label="$g(x)=f(f(x))$")
ax.plot(xs, xs, color="gray", linewidth=0.8)
fixed = [0, 1 - 1 / r]
p2 = periodic_points(2, r, exclude=tuple(fixed))
ax.plot(p2, p2, "ko", markersize=5)
ax.plot(fixed, fixed, "o", color="gray", markersize=6)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.legend()
bf.save(fig, OUT / "disc1d_logist_p2graph.png")

# -- f, f^(3), y = x at r = 3.80 and 3.84: 1x2 ------------------------------
fig, axs = plt.subplots(1, 2, figsize=(bf.FULL_W, 3.0))
for ax, r in zip(axs, [3.80, 3.84]):
    ax.plot(xs, cb.logistic(xs, r), "k")
    ax.plot(xs, compose(cb.logistic, 3, xs, r), "k--")
    ax.plot(xs, xs, color="gray", linewidth=0.8)
    fixed = [0, 1 - 1 / r]
    ax.plot(fixed, fixed, "o", color="gray", markersize=7)
    p3 = periodic_points(3, r, exclude=tuple(fixed))
    for p in p3:
        # classify each root by its own orbit's stability, not a shared one
        color = "k" if abs(sigma_at(p, r)) < 1 else "gray"
        ax.plot(p, p, "o", color=color, markersize=3.5)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_aspect("equal")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_logist_p3graph.png")

print("fig_fixedpoints: assets written to", OUT)
