"""Worked example of a Poincare section: the limit cycle r' = a r (1 - r^2).

Produces (in python/_static/cont3d/):
  cont3d_poincare_example.png  (a) phase portrait, section x > 0, y = 0,
                               crossings; (b) the Poincare map r_{n+1} = P(r_n);
                               (c) iterates r_n of the map
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
OUT.mkdir(parents=True, exist_ok=True)

a = 0.2
P = lambda r: (1 - (r**2 - 1) / r**2 * np.exp(-4 * a * np.pi)) ** -0.5

# iterates of the analytic map from r_1 = 0.01 (the book's choice)
rn = [0.01]
for _ in range(9):
    rn.append(P(rn[-1]))
rn = np.array(rn)
print("r_n:", np.round(rn, 4))
print("P'(1) = %.4f (= exp(-4 a pi) = %.4f)"
      % ((P(1 + 1e-6) - P(1 - 1e-6)) / 2e-6, np.exp(-4 * a * np.pi)))

# (a) phase portrait: normalised direction field, trajectory, section, crossings
f = lambda t, s: cb.circle_limit_cycle(t, s, a=a)
from scipy.integrate import solve_ivp
sol = solve_ivp(f, [0, 50], [0.01, 0.0], t_eval=np.linspace(0, 50, 4000),
                rtol=1e-10, atol=1e-12)
tc, Xc = cb.poincare_section(cb.circle_limit_cycle, [0.01, 0.0], 50,
                             (1, 0.0), direction=1, a=a)
g = np.linspace(-1.2, 1.2, 15)
Xg, Yg = np.meshgrid(g, g)
U, V = cb.circle_limit_cycle(0, [Xg, Yg], a=a)
L = np.hypot(U, V)
L[L == 0] = 1.0
fig, (ax, axm, axs) = plt.subplots(1, 3, figsize=(bf.FULL_W, 2.1),
                                   gridspec_kw=dict(width_ratios=[1, 1, 1.4]))
ax.quiver(Xg, Yg, U / L, V / L, angles="xy", scale=22, width=0.004, color="0.3")
ax.plot(*sol.y, "b", lw=1.2)
ax.plot([0, 1.5], [0, 0], "r", lw=2.5)
ax.plot(Xc[:, 0], Xc[:, 1], "bo", ms=5)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
print("crossings from events: ", np.round(Xc[:10, 0], 4))

# (b) the map
r = np.linspace(1e-3, 2, 400)
axm.plot(r, P(r), "k", lw=2)
axm.plot([0, 2], [0, 2], "k--", lw=1)
axm.set_xlim(0, 2); axm.set_ylim(0, 2); axm.set_aspect("equal")
axm.set_xlabel("$r_n$"); axm.set_ylabel("$r_{n+1}$")

# (c) iterates
axs.plot(np.arange(1, 11), rn, "kD", mfc="none", ms=6)
axs.set_xlabel("$n$"); axs.set_ylabel("$r_n$")
bf.panel_labels([ax, axm, axs])
bf.save(fig, OUT / "cont3d_poincare_example.png")
