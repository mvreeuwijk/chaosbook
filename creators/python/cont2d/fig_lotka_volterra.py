"""Lotka-Volterra figures for "Two-dimensional continuous systems".

Produces (in python/_static/cont2d/):
  cont2d_LV_time.png   time series of x(t) and y(t) for alpha = 3/4, x(0) = y(0) = 1/4
  cont2d_LV_phase.png  phase portrait with the closed orbit of the same run
  cont2d_LV_E.png      isocontours of the constant of motion H
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

alpha = 3 / 4
x0 = [0.25, 0.25]

sol = solve_ivp(cb.lotka_volterra, [0, 20], x0, args=(alpha,), rtol=1e-10,
                atol=1e-12, dense_output=True)
t = np.linspace(0, 20, 1000)
x, y = sol.sol(t)

# time series
plt.figure(figsize=(5.0, 3.5))
plt.plot(t, x, "b-", label="$x$")
plt.plot(t, y, "r--", label="$y$")
plt.xlabel("$t$")
plt.ylabel(r"$x(t),\ y(t)$")
plt.xlim(0, 20)
plt.ylim(0, 3.7)
plt.legend(ncol=2, loc="upper center")
plt.tight_layout()
plt.savefig(OUT / "cont2d_LV_time.png", dpi=150)
plt.close()

# phase portrait: direction field + the orbit
plt.figure(figsize=(4.2, 4.2))
ax = plt.gca()
cb.phase_portrait(cb.lotka_volterra, (0, 4.1), (0, 4.1), ax=ax, n=21,
                  style="quiver", alpha=alpha)
ax.plot(x, y, "r-", lw=2)
plt.tight_layout()
plt.savefig(OUT / "cont2d_LV_phase.png", dpi=150)
plt.close()

# isocontours of H
plt.figure(figsize=(4.2, 4.2))
g = np.linspace(0.02, 3, 400)
X, Y = np.meshgrid(g, g)
H = cb.lotka_volterra_invariant(X, Y, alpha)
plt.contour(X, Y, H, levels=[10, 14, 20, 30, 50], colors="k", linewidths=1.5)
plt.xlim(0, 3.05)
plt.ylim(0, 3.05)
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.tight_layout()
plt.savefig(OUT / "cont2d_LV_E.png", dpi=150)
plt.close()

print("LV period-ish: x max =", x.max(), " y max =", y.max(),
      " H(0.25,0.25) =", cb.lotka_volterra_invariant(0.25, 0.25, alpha))
