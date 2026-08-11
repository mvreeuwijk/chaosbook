"""Fixed-point and periodic-solution figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_attractor_r1_5.png        many x0 converge to x*=1/3
  disc1d_logist_attractor_local_r2_0.png  superstable convergence (sigma=0)
  disc1d_logist_attractor_local_r1_5.png  ordinary convergence
  disc1d_logist_p2graph.png               f, g=f(f(x)), y=x at r=3.2
  disc1d_logist_p3graph_r380.png          f, f^(3), y=x at r=3.80
  disc1d_logist_p3graph_r384.png          f, f^(3), y=x at r=3.84
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- global attraction: many initial conditions at r = 1.5 -------------------
plt.figure(figsize=(5.2, 3.4))
for x0 in [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    X = cb.orbit(cb.logistic, x0=x0, n=20, r=1.5)
    plt.plot(range(len(X)), X, "-o", markersize=3)
plt.axhline(1 / 3, color="gray", linewidth=0.8)
plt.xlabel("n")
plt.ylabel("xn")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_attractor_r1_5.png", dpi=150)
plt.close()

# -- local convergence: superstable (r=2) vs ordinary (r=1.5) ----------------
for r, xstar in [(2.0, 0.5), (1.5, 1 / 3)]:
    plt.figure(figsize=(4.2, 3.2))
    X = cb.orbit(cb.logistic, x0=xstar + 0.2, n=12, r=r)
    plt.plot(range(len(X)), X, "-o", markersize=4)
    plt.axhline(xstar, color="gray", linewidth=0.8)
    plt.xlabel("n")
    plt.ylabel("xn")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_attractor_local_r{str(r).replace('.', '_')}.png",
                dpi=150)
    plt.close()


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


def sigma(points, r):
    """Stability of a periodic orbit: product of f' along the orbit."""
    return np.prod([r * (1 - 2 * x) for x in points])


# -- f, g = f(f(x)), y = x at r = 3.2 with period-2 and fixed points ---------
r = 3.2
xs = np.linspace(0, 1, 400)
plt.figure(figsize=(4.4, 4.4))
plt.plot(xs, cb.logistic(xs, r), "k", label="f(x)")
plt.plot(xs, compose(cb.logistic, 2, xs, r), "k--", label="g(x)=f(f(x))")
plt.plot(xs, xs, color="gray", linewidth=0.8)
fixed = [0, 1 - 1 / r]
p2 = periodic_points(2, r, exclude=tuple(fixed))
plt.plot(p2, p2, "ko", markersize=7)
plt.plot(fixed, fixed, "o", color="gray", markersize=9)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_p2graph.png", dpi=150)
plt.close()

# -- f, f^(3), y = x at r = 3.80 and 3.84 ------------------------------------
for r, name in [(3.80, "r380"), (3.84, "r384")]:
    plt.figure(figsize=(4.4, 4.4))
    plt.plot(xs, cb.logistic(xs, r), "k")
    plt.plot(xs, compose(cb.logistic, 3, xs, r), "k--")
    plt.plot(xs, xs, color="gray", linewidth=0.8)
    fixed = [0, 1 - 1 / r]
    plt.plot(fixed, fixed, "o", color="gray", markersize=10)
    p3 = periodic_points(3, r, exclude=tuple(fixed))
    if p3:
        # split the six points into the stable and the unstable 3-cycle
        orbit_a = [p3[0]]
        for _ in range(2):
            orbit_a.append(cb.logistic(orbit_a[-1], r))
        orbit_b = [p for p in p3
                   if all(abs(p - q) > 1e-6 for q in orbit_a)]
        for orb in [orbit_a, orbit_b]:
            color = "k" if abs(sigma(orb, r)) < 1 else "gray"
            plt.plot(orb, orb, "o", color=color, markersize=5)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_p3graph_{name}.png", dpi=150)
    plt.close()

print("fig_fixedpoints: assets written to", OUT)
