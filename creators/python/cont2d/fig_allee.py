"""Predator-prey with an Allee effect (exercise on the Lotka-Volterra variant).

  x' = x^2/(x + beta) - x y,    y' = x y - alpha y^2,    beta = 3/16

Produces (in python/_static/cont2d/):
  cont2d_LV_Allee_stab_Re.png / cont2d_LV_Allee_stab_Im.png
      real and imaginary parts of the eigenvalues of the non-zero fixed point
      (alpha - beta, (alpha - beta)/alpha) as functions of alpha
  cont2d_LV_Allee_extinct1.png / cont2d_LV_Allee_extinct2.png
      phase portraits at alpha = 0.5 for x(0) = 0.1 and y(0) = 0.06 / 0.05:
      the first run spirals to the coexistence point, the second goes extinct
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

beta = 3 / 16

# eigenvalues of J at the non-zero fixed point (analytic fixed point,
# numerical Jacobian from chaosbook)
alphas = np.linspace(0.12, 0.5, 600)
ev = np.array([np.linalg.eigvals(
    cb.jacobian(cb.lotka_volterra_allee, [a - beta, (a - beta) / a],
                alpha=a, beta=beta)) for a in alphas])
# order the pair by (real, imag) so the branches are continuous
s1 = np.where(ev[:, 0].imag >= ev[:, 1].imag, ev[:, 0], ev[:, 1])
s2 = np.where(ev[:, 0].imag >= ev[:, 1].imag, ev[:, 1], ev[:, 0])
# real branches: sigma_1 is the larger real part where the pair is real
real = np.abs(s1.imag) < 1e-9
hi = np.maximum(ev[:, 0].real, ev[:, 1].real)
lo = np.minimum(ev[:, 0].real, ev[:, 1].real)
# the two real branches swap labels where the fixed point crosses x = 0
# (alpha = beta), as in the analytic eigenvalue formulae
swap = alphas < beta
r1 = np.where(real, np.where(swap, lo, hi), s1.real)
r2 = np.where(real, np.where(swap, hi, lo), s2.real)

for name, a_, b_, ylab, ylim in [
    ("Re", r1, r2, r"$\mathrm{Re}(\sigma)$", (-0.85, 0.1)),
    ("Im", s1.imag, s2.imag, r"$\mathrm{Im}(\sigma)$", None),
]:
    plt.figure(figsize=(5.0, 3.5))
    plt.plot(alphas, a_, "k-", lw=2, label=r"$\sigma_1$")
    plt.plot(alphas, b_, "k--", lw=2, label=r"$\sigma_2$")
    plt.axhline(0, color="k", lw=0.8)
    plt.xlabel(r"$\alpha$")
    plt.ylabel(ylab)
    plt.xlim(alphas[0], alphas[-1])
    if ylim:
        plt.ylim(*ylim)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_LV_Allee_stab_{name}.png", dpi=150)
    plt.close()

# phase portraits (1000 time units, as in the original)
alpha = 0.5
for k, (y0, lim) in enumerate([(0.06, 2.05), (0.05, 2.05)], start=1):
    f = lambda t, s: cb.lotka_volterra_allee(t, s, alpha=alpha, beta=beta)
    sol = solve_ivp(f, [0, 1000], [0.1, y0], rtol=1e-9, atol=1e-12,
                    t_eval=np.linspace(0, 1000, 40000))
    plt.figure(figsize=(4.2, 4.2))
    ax = plt.gca()
    cb.phase_portrait(cb.lotka_volterra_allee, (0, lim), (0, lim), ax=ax,
                      n=21, style="quiver", alpha=alpha, beta=beta)
    ax.plot(sol.y[0], sol.y[1], "r-", lw=1.5)
    plt.tight_layout()
    plt.savefig(OUT / f"cont2d_LV_Allee_extinct{k}.png", dpi=150)
    plt.close()
    print(f"extinct{k}: y(0)={y0}  final state ({sol.y[0,-1]:.4f}, {sol.y[1,-1]:.4f})")

print("Hopf-like sign changes of Re(sigma) in alpha:",
      alphas[np.where(np.diff(np.sign(r1)))[0]])
print("onset of complex eigenvalues at alpha =", alphas[np.argmax(~real)])
