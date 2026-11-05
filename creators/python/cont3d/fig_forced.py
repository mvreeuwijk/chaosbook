"""Forced double-well oscillator: phase portrait and stroboscopic section.

x' = y,  y' = x - x^3 - f y + A cos z,  z' = omega, with
omega = 1, f = 0.15, A = 0.3 and x(0) = y(0) = z(0) = 0.

Produces (in python/_static/cont3d/):
  cont3d_doublewell_results.png  (a) (x, y) trajectory for 800 < t < 1000 over
                                 contours of H and the three fixed points;
                                 (b) stroboscopic section, phase 0
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
OUT.mkdir(parents=True, exist_ok=True)

f, A, omega = 0.15, 0.3, 1.0
params = dict(f=f, A=A, omega=omega)

# (a) trajectory over contours of the energy H = x^4/4 - x^2/2 + y^2/2
t = np.linspace(800, 1000, 10000)
sol = solve_ivp(lambda t_, s: cb.forced_double_well(t_, s, **params), [0, 1000],
                [0, 0, 0], t_eval=t, rtol=1e-10, atol=1e-12, method="DOP853")
X, Y = np.meshgrid(np.linspace(-2, 2, 70), np.linspace(-2, 2, 70))
H = X**4 / 4 - X**2 / 2 + Y**2 / 2
fig, (ax, axp) = plt.subplots(1, 2, figsize=(bf.BOX_W, 2.8))
ax.contour(X, Y, H, levels=np.arange(-0.2, 3.1, 0.4), colors="k", linewidths=1.2,
           linestyles="solid")
ax.plot(sol.y[0], sol.y[1], "r", lw=0.7)
ax.plot([-1, 0, 1], [0, 0, 0], "o", mfc="none", mec="k", ms=9)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")

# (b) stroboscopic section: N = 5000 periods, second half plotted
N = 5000
P = cb.stroboscopic_section(cb.forced_double_well, [0, 0, 0], 2 * np.pi / omega,
                            N, phase=0.0, discard=N // 2, **params)
axp.plot(P[:, 0], P[:, 1], "k.", ms=2)
axp.set_xlim(-2, 2); axp.set_ylim(-1.0, 1.4)   # the section reaches y = 1.13
axp.set_xlabel("$x$"); axp.set_ylabel("$y$")
bf.panel_labels([ax, axp])
bf.save(fig, OUT / "cont3d_doublewell_results.png")
print("stroboscopic section: %d points, x in [%.2f, %.2f], y in [%.2f, %.2f]"
      % (len(P), P[:, 0].min(), P[:, 0].max(), P[:, 1].min(), P[:, 1].max()))
