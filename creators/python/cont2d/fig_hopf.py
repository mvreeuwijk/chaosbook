"""Hopf bifurcation:  x' = -y - x(-mu + r^2),  y' = x - y(-mu + r^2).

Produces (in python/_static/cont2d/):
  cont2d_Hopf_time1.png / cont2d_Hopf_time2.png    x(t) at mu = -0.1 / +0.1
  cont2d_Hopf_phase1.png / cont2d_Hopf_phase2.png  phase portraits, same runs
  cont2d_Hopf_ev1.png / cont2d_Hopf_ev2.png        Re and Im of the eigenvalues
                                                   of J(0,0) versus mu
All runs start at (0.15, 0) and last to t = 100.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

for k, mu in [(1, -0.1), (2, 0.1)]:
    f = lambda t, s: cb.hopf(t, s, mu=mu)
    t = np.linspace(0, 100, 4000)
    sol = solve_ivp(f, [0, 100], [0.15, 0], t_eval=t, rtol=1e-10, atol=1e-12)

    plt.figure(figsize=(4.2, 3.2))
    plt.plot(t, sol.y[0], "k-", lw=1.5)
    plt.axhline(0, color="k", lw=0.8)
    plt.xlim(0, 100)
    plt.ylim(-0.3, 0.3)
    plt.xlabel("$t$")
    plt.ylabel("$x$")
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_Hopf_time{k}.png", dpi=150)
    plt.close()

    plt.figure(figsize=(4.2, 4.2))
    ax = plt.gca()
    cb.phase_portrait(cb.hopf, (-0.5, 0.5), (-0.5, 0.5), ax=ax, n=20,
                      style="quiver", mu=mu)
    ax.plot(sol.y[0], sol.y[1], "k-", lw=2)
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_Hopf_phase{k}.png", dpi=150)
    plt.close()
    print(f"mu = {mu}: final radius {np.hypot(sol.y[0,-1], sol.y[1,-1]):.4f}"
          f"  (sqrt(mu) = {np.sqrt(mu) if mu > 0 else float('nan'):.4f})")

mus = np.linspace(-1, 1, 400)
ev = np.array([np.linalg.eigvals(cb.jacobian(cb.hopf, [0, 0], mu=m)) for m in mus])
ev = np.array([e[np.argsort(-e.imag)] for e in ev])  # sigma_1 has Im > 0
for name, vals, lab, lim in [("ev1", ev.real, r"$\mathrm{Re}(\sigma)$", None),
                             ("ev2", ev.imag, r"$\mathrm{Im}(\sigma)$", (-1.2, 1.2))]:
    plt.figure(figsize=(4.2, 3.2))
    plt.plot(mus, vals[:, 0], "k-", lw=2, label=r"$\sigma_1$")
    plt.plot(mus, vals[:, 1], "k--", lw=2, label=r"$\sigma_2$")
    plt.axhline(0, color="k", lw=0.8)
    plt.axvline(0, color="k", lw=0.8)
    plt.xlim(-1, 1)
    if lim:
        plt.ylim(*lim)
    plt.xlabel(r"$\mu$")
    plt.ylabel(lab)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_Hopf_{name}.png", dpi=150)
    plt.close()

print("fig_hopf: written to", OUT)
