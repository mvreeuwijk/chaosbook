"""Energy-balance climate model:  beta dT/dt = (1 - a) S/4 - eps sigma T^4.

Produces (in python/_static/cont1d/):
  cont1d_climate_single_fp.png     T*(eps) for constant albedo a = 0.3
  cont1d_climate_multiple_fp.png   T*(eps) with a(T) = 0.4 - 0.3 tanh((T - Tm)/DT),
                                   stable branches black, unstable gray, with
                                   arrows for the jumps at the two folds
Also prints the numbers quoted in the text: T* at eps = 0.61, f'(T*), and the
critical emissivities (folds) of the multiple-equilibrium model.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import chaosbook as cb
from _common import PANEL, plot_branches, save

sigma, S, Tm, DT = 5.67e-8, 1370.0, 273.0, 20.0
beta = 4e7            # h * rho * c_v = 10 * 1000 * 4000 (text and table)


def f_const(T, eps=0.61, a=0.3):
    return ((1 - a) * S / 4 - eps * sigma * T**4) / beta


def albedo(T):
    return 0.4 - 0.3 * np.tanh((T - Tm) / DT)


def f_alb(T, eps=0.61):
    return ((1 - albedo(T)) * S / 4 - eps * sigma * T**4) / beta


# -- numbers from the text ----------------------------------------------------------
Teq = cb.fixed_points(f_const, 100, 350, eps=0.61)[0]
print(f"constant albedo, eps = 0.61:  T* = {Teq:.2f} K,  f'(T*) = "
      f"{cb.stability(f_const, Teq, eps=0.61):.3e} 1/s  (beta = {beta:g})")
print(f"   analytic -4 eps sigma T*^3/beta = {-4 * 0.61 * sigma * Teq**3 / beta:.3e}")
for T0, e0 in ((280, 0.6), (250, 0.4)):
    Tc, ec = fsolve(lambda v: [f_alb(v[0], eps=v[1]),
                               cb.stability(f_alb, v[0], eps=v[1])], [T0, e0])
    print(f"fold of the multiple-equilibrium model: eps = {ec:.4f}, T = {Tc:.2f} K")
    if T0 == 280:
        eps_hi, T_hi = ec, Tc
    else:
        eps_lo, T_lo = ec, Tc

# -- figures ------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=PANEL)
segs = cb.fixed_point_branches(f_const, "eps", 0.3, 1.0, 200, 350, shape=(800, 800))
plot_branches(ax, segs, lw=2.5)
ax.set_xlim(0.3, 1.0)
ax.set_ylim(200, 350)
ax.set_xlabel(r"$\epsilon$")
ax.set_ylabel("$T_*$")
fig.tight_layout()
save(fig, "cont1d_climate_single_fp")

fig, ax = plt.subplots(figsize=PANEL)
segs = cb.fixed_point_branches(f_alb, "eps", 0.3, 1.0, 200, 350, shape=(1000, 1000))
plot_branches(ax, segs, lw=2.5)
for e, y0, y1 in ((eps_hi, T_hi - 7, 230), (eps_lo, T_lo + 7, 310)):
    ax.annotate("", (e, y1), (e, y0), arrowprops=dict(
        arrowstyle="-|>", color="k", lw=1, mutation_scale=12, shrinkA=0, shrinkB=0))
ax.set_xlim(0.3, 1.0)
ax.set_ylim(200, 350)
ax.set_xlabel(r"$\epsilon$")
ax.set_ylabel("$T_*$")
fig.tight_layout()
save(fig, "cont1d_climate_multiple_fp")

print("fig_climate: written")
