"""Blue-sky (global) bifurcation of a limit cycle.

The figures follow the book's polar form  r' = -mu r - r^3 + r^5,  theta' = 1,
i.e. the Cartesian system as printed in the chapter,
    x' = -y - x (mu + r^2 - r^4),   y' = x - y (mu + r^2 - r^4),
with the radial equation as used for Fig. (c) and the fixed-point diagram of
Fig. (d).

Produces (in python/_static/cont2d/):
  cont2d_global.png  2x2 figure: (a, b) phase portraits at mu = -0.26 / -0.24,
                     from (0.15, 0); (c) dr/dt versus r for mu = -0.3, -0.2, -0.1;
                     (d) radii of the fixed points versus mu; black stable,
                     grey unstable
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)


def bluesky(t, s, mu=-0.24):
    """Cartesian form of the model as printed in the chapter: r' = -mu r - r^3 + r^5, theta' = 1."""
    x, y = s
    q = mu + x * x + y * y - (x * x + y * y) ** 2
    return [-y - x * q, x - y * q]


def escaped(t, s, mu):
    return np.hypot(s[0], s[1]) - 3.0


escaped.terminal = True

fig, axs = plt.subplots(2, 2, figsize=(bf.FULL_W, 4.8))

for k, mu in [(0, -0.26), (1, -0.24)]:
    t = np.linspace(0, 200, 20000)
    sol = solve_ivp(bluesky, [0, 200], [0.15, 0], t_eval=t, args=(mu,),
                    events=escaped, rtol=1e-10, atol=1e-12)
    ax = axs[0, k]
    cb.phase_portrait(bluesky, (-1.25, 1.25), (-1.25, 1.25), ax=ax, n=20,
                      style="quiver", mu=mu)
    ax.plot(sol.y[0], sol.y[1], "k-", lw=1.5)
    ax.set_aspect("equal")
    rr = np.hypot(sol.y[0], sol.y[1])
    print(f"mu = {mu}: run ended at t = {sol.t[-1]:.1f}, r = {rr[-1]:.4f}"
          f" ({'escaped' if sol.status == 1 else 'trapped'})")

r = np.linspace(0, 1, 400)
ax = axs[1, 0]
for mu, ls in [(-0.3, "-"), (-0.2, "--"), (-0.1, "-.")]:
    ax.plot(r, -mu * r - r**3 + r**5, "k" + ls, lw=1.5, label=rf"$\mu={mu}$")
ax.axhline(0, color="k", lw=0.8)
ax.set_xlim(0, 1)
ax.set_xlabel("$r$")
ax.set_ylabel(r"$\mathrm{d}r/\mathrm{d}t$")
ax.legend(loc="upper left")

# fixed points of the radial equation of panels (a)-(c),  dr/dt = g(r, mu) =
# -mu r - r^3 + r^5. Stable where dg/dr < 0: the origin for mu > 0, the inner
# branch (the stable limit cycle born in the saddle-node at mu = -1/4); the
# outer branch is unstable.
mus = np.linspace(-0.4, 0.2, 2001)
ax = axs[1, 1]


def seg(mu_, r_, stable):
    ax.plot(mu_, r_, "-", color="k" if stable else "0.7", lw=2.2,
             solid_capstyle="butt")


# origin: dg/dr = -mu, unstable for mu < 0, stable for mu > 0
seg(mus[mus < 0], 0 * mus[mus < 0], False)
seg(mus[mus >= 0], 0 * mus[mus >= 0], True)
# non-trivial branches r^2 = (1 +- sqrt(1 + 4 mu))/2 for mu >= -1/4;
# dg/dr = 2 r^2 (2 r^2 - 1): the inner (minus) branch is stable
mb = mus[mus >= -0.25]
mb_up = mb[mb <= 0]
seg(mb_up, np.sqrt((1 + np.sqrt(1 + 4 * mb_up)) / 2), False)
seg(mb_up, np.sqrt((1 - np.sqrt(1 + 4 * mb_up)) / 2), True)
ax.set_xlim(-0.4, 0.2)
ax.set_ylim(0, 1.02)
ax.set_xlabel(r"$\mu$")
ax.set_ylabel(r"$r^*$")
bf.panel_labels(axs)
bf.save(fig, OUT / "cont2d_global.png")

mu_c = -0.25
print("saddle-node at mu =", mu_c, " with r* =", np.sqrt(0.5))
print("fig_global: written to", OUT)
