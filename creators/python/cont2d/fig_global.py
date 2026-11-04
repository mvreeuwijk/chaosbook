"""Blue-sky (global) bifurcation of a limit cycle.

The figures follow the book's polar form  r' = -mu r - r^3 + r^5,  theta' = -1
(the Cartesian system of the chapter with time reversed; see the note in the
chapter), with the radial equation as used for Fig. (c) and the
fixed-point diagram of Fig. (d).

Produces (in python/_static/cont2d/):
  cont2d_global_phase1.png / cont2d_global_phase2.png  mu = -0.26 / -0.24, from (0.15, 0)
  cont2d_global_r.png      dr/dt versus r for mu = -0.3, -0.2, -0.1
  cont2d_global_fixed.png  radii of the fixed points versus mu; black stable, grey unstable
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)


def bluesky(t, s, mu=-0.24):
    """Cartesian form of the model, with the sign of time as drawn in the figures."""
    x, y = s
    q = mu + x * x + y * y - (x * x + y * y) ** 2
    return [-(-y + x * q), -(x + y * q)]


def escaped(t, s, mu):
    return np.hypot(s[0], s[1]) - 3.0


escaped.terminal = True

for k, mu in [(1, -0.26), (2, -0.24)]:
    t = np.linspace(0, 200, 20000)
    sol = solve_ivp(bluesky, [0, 200], [0.15, 0], t_eval=t, args=(mu,),
                    events=escaped, rtol=1e-10, atol=1e-12)
    plt.figure(figsize=(4.2, 4.2))
    ax = plt.gca()
    cb.phase_portrait(bluesky, (-1.25, 1.25), (-1.25, 1.25), ax=ax, n=20,
                      style="quiver", mu=mu)
    ax.plot(sol.y[0], sol.y[1], "k-", lw=2)
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_global_phase{k}.png", dpi=150)
    plt.close()
    rr = np.hypot(sol.y[0], sol.y[1])
    print(f"mu = {mu}: run ended at t = {sol.t[-1]:.1f}, r = {rr[-1]:.4f}"
          f" ({'escaped' if sol.status == 1 else 'trapped'})")

r = np.linspace(0, 1, 400)
plt.figure(figsize=(4.2, 3.2))
for mu, ls in [(-0.3, "-"), (-0.2, "--"), (-0.1, "-.")]:
    plt.plot(r, -mu * r - r**3 + r**5, "k" + ls, lw=2, label=rf"$\mu={mu}$")
plt.axhline(0, color="k", lw=0.8)
plt.xlim(0, 1)
plt.xlabel("$r$")
plt.ylabel(r"$\mathrm{d}r/\mathrm{d}t$")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig(OUT / "cont2d_global_r.png", dpi=150)
plt.close()

# fixed points of  F(r, mu) = mu r + r^3 - r^5  (the figure's stability colouring
# is that of this sign convention: stable where dF/dr < 0)
mus = np.linspace(-0.4, 0.2, 2001)
plt.figure(figsize=(4.2, 3.2))


def seg(mu_, r_, stable):
    plt.plot(mu_, r_, "-", color="k" if stable else "0.7", lw=3,
             solid_capstyle="butt")


# origin: stable for mu < 0
seg(mus[mus < 0], 0 * mus[mus < 0], True)
seg(mus[mus >= 0], 0 * mus[mus >= 0], False)
# non-trivial branches r^2 = (1 +- sqrt(1 + 4 mu))/2 for mu >= -1/4
mb = mus[mus >= -0.25]
mb_up = mb[mb <= 0]
seg(mb_up, np.sqrt((1 + np.sqrt(1 + 4 * mb_up)) / 2), True)
seg(mb_up, np.sqrt((1 - np.sqrt(1 + 4 * mb_up)) / 2), False)
plt.xlim(-0.4, 0.2)
plt.ylim(0, 1.02)
plt.xlabel(r"$\mu$")
plt.ylabel(r"$r^*$")
plt.tight_layout()
plt.savefig(OUT / "cont2d_global_fixed.png", dpi=150)
plt.close()

mu_c = -0.25
print("saddle-node at mu =", mu_c, " with r* =", np.sqrt(0.5))
print("fig_global: written to", OUT)
