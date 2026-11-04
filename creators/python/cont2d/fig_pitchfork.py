"""Pitchfork bifurcation in two dimensions:  x' = (mu - 2) x + y + sin x,  y' = x - y.

Produces (in python/_static/cont2d/):
  cont2d_pitchfork_phase1.png  phase portrait at mu = -0.1 (one stable node)
  cont2d_pitchfork_phase2.png  phase portrait at mu = +0.1 (saddle + two nodes)
  cont2d_pitchfork_fixed.png   fixed points x* versus mu
  cont2d_pitchfork_stab.png    eigenvalues of J(0,0) versus mu (both real)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)


def pitchfork(t, s, mu=0.0):
    x, y = s
    return [(mu - 2) * x + y + np.sin(x), x - y]


ics = [(-2, 0), (2, 0), (-2, 2), (2, -2)]
colors = ["r", "b", "g", "c"]

for k, mu in [(1, -0.1), (2, 0.1)]:
    plt.figure(figsize=(4.2, 4.2))
    ax = plt.gca()
    cb.phase_portrait(pitchfork, (-2, 2), (-2, 2), ax=ax, n=21, style="quiver",
                      trajectories=ics, tmax=100, colors=colors, lw=2.5, mu=mu)
    if mu > 0:
        # non-trivial fixed points (x*, x*) with (mu - 1) x + sin x = 0
        xs = brentq(lambda x: (mu - 1) * x + np.sin(x), 0.3, 2.0)
        ax.plot([0], [0], "o", mfc="w", mec="k", ms=10, mew=1.5)
        ax.plot([xs, -xs], [xs, -xs], "ko", ms=10)
        print(f"mu = {mu}: nontrivial fixed points at +-({xs:.10f}, {xs:.10f})")
    else:
        ax.plot([0], [0], "ko", ms=10)
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_pitchfork_phase{k}.png", dpi=150)
    plt.close()

# fixed points: (mu - 1) x* + sin x* = 0  <=>  mu = 1 - sin(x*)/x*
x = np.linspace(-10, 10, 2001)
x = x[x != 0]
plt.figure(figsize=(4.2, 3.2))
plt.plot(1 - np.sin(x) / x, x, "k-", lw=2)
plt.axhline(0, color="k", lw=2)
plt.xlim(-1, 2)
plt.ylim(-10, 10)
plt.xlabel(r"$\mu$")
plt.ylabel(r"$x^*$")
plt.tight_layout()
plt.savefig(OUT / "cont2d_pitchfork_fixed.png", dpi=150)
plt.close()

# eigenvalues of the Jacobian at the origin
mus = np.linspace(-1, 2, 400)
ev = np.array([np.sort(np.linalg.eigvals(cb.jacobian(pitchfork, [0, 0], mu=m)).real)[::-1]
               for m in mus])
plt.figure(figsize=(4.2, 3.2))
plt.plot(mus, ev[:, 0], "k-", lw=2, label=r"$\sigma_1$")
plt.plot(mus, ev[:, 1], "k--", lw=2, label=r"$\sigma_2$")
plt.axhline(0, color="k", lw=0.8)
plt.xlabel(r"$\mu$")
plt.ylabel(r"$\mathrm{Re}(\sigma)$")
plt.xlim(-1, 2)
plt.legend(loc="center right")
plt.tight_layout()
plt.savefig(OUT / "cont2d_pitchfork_stab.png", dpi=150)
plt.close()

# analytic check: sigma = -1 + mu/2 +- sqrt(4 + mu^2)/2
m = 0.7
print("sigma(mu=0.7): numerical", np.sort(np.linalg.eigvals(cb.jacobian(pitchfork, [0, 0], mu=m)).real),
      " formula", np.sort([-1 + m / 2 - np.sqrt(4 + m**2) / 2, -1 + m / 2 + np.sqrt(4 + m**2) / 2]))
print("fig_pitchfork: written to", OUT)
