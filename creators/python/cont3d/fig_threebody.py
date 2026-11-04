"""Restricted three-body problem in the co-rotating frame, mu = 0.2.

Produces (in python/_static/cont3d/):
  cont4d_3body_V.png         (a) isolines of V, Lagrange points L1-L5,
                             (b) cross-section V(x, y=0)
  cont4d_3body_trajectories.png  (a-d) four trajectories over the Hill region
                             V > V_L1, (e) (x_n, u_n) section at y = 0 (v > 0)
Prints the Lagrange points and the energies of the four orbits.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy.integrate import solve_ivp

import chaosbook as cb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
OUT.mkdir(parents=True, exist_ok=True)

mu = 0.2
V = lambda x, y: cb.threebody_potential(x, y, mu)
H = lambda s: 0.5 * (s[2] ** 2 + s[3] ** 2) + V(s[0], s[1])
xl = cb.lagrange_points(mu)                       # book numbering: L1, L2, L3
Vl = [V(x, 0) for x in xl]
print("x_L1, x_L2, x_L3 = %.4f %.4f %.4f" % xl)
print("V_L1, V_L2, V_L3 = %.4f %.4f %.4f" % tuple(Vl))
V_L1 = Vl[0]
L45 = ((1 - 2 * mu) / 2, np.sqrt(3) / 2)
print("V at L4/L5 = %.4f" % V(L45[0], L45[1]))


# -- potential: isolines of exp(V) and the Lagrange points ---------------------
x, y = np.meshgrid(np.linspace(-1.5, 1.5, 600), np.linspace(-1.5, 1.5, 600))
E = np.exp(V(x, y))
fig, (ax, axc) = plt.subplots(1, 2, figsize=(bf.FULL_W, 3.0),
                             gridspec_kw=dict(width_ratios=[1, 1.15]))
ax.contour(x, y, E, levels=np.linspace(0.03, 0.3, 14), colors="k", linewidths=1)
ax.plot([-1.5, 1.5], [0, 0], "k--", lw=0.8)
ax.plot(list(xl) + [L45[0]] * 2, [0, 0, 0, L45[1], -L45[1]], "rD", ms=6)
ax.plot([1 - mu], [0], "ko", ms=5)
ax.plot([-mu], [0], "ko", ms=9)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")

# -- cross-section at y = 0 -----------------------------------------------------
xs = np.linspace(-1.5, 1.5, 3001)
with np.errstate(divide="ignore"):
    Vx = V(xs, 0.0)
for lo, hi in [(-1.5, -mu - 0.02), (-mu + 0.02, 1 - mu - 0.02), (1 - mu + 0.02, 1.5)]:
    m = (xs > lo) & (xs < hi)
    axc.plot(xs[m], Vx[m], "k", lw=2)
axc.plot(xl, Vl, "rD", ms=6)
for k, (xx, vv) in enumerate(zip(xl, Vl), start=1):
    axc.text(xx, vv + 0.3, f"$L_{k}$", ha="center")
axc.set_xlim(-1.5, 1.5); axc.set_ylim(-5, 0)
axc.set_xlabel("$x$"); axc.set_ylabel("$V(x, y=0)$")
bf.panel_labels([ax, axc])
bf.save(fig, OUT / "cont4d_3body_V.png")

# -- four trajectories ----------------------------------------------------------
ics = [[0.1, 0, 0, 1], [0.5, 0, 0, 1], [0.9, 0, 0, 1], [0.45, 0.1, 0.1, -0.1]]
cols = ["tab:blue", "tab:red", "tab:green", "k"]
N, dt = 30000, 0.01
tev = np.arange(N) * dt
sols = []
for ic in ics:
    s = solve_ivp(lambda t, q: cb.rotating_threebody(t, q, mu=mu), [0, tev[-1]],
                  ic, t_eval=tev, rtol=1e-10, atol=1e-12, method="DOP853")
    sols.append(s)
    print("ic %s: H0 = %.4f (V_L1 = %.4f, %s), relative drift of H %.1e"
          % (ic, H(ic), V_L1, "below" if H(ic) < V_L1 else "above",
             abs(H(s.y[:, -1]) - H(ic)) / abs(H(ic))))

gx, gy = np.meshgrid(np.linspace(-1.1, 1.1, 500), np.linspace(-1.1, 1.1, 500))
fig = plt.figure(figsize=(bf.FULL_W, 4.2))
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1.2])
axes = []
for k, (s, col) in enumerate(zip(sols, cols), start=1):
    ax = fig.add_subplot(gs[0, k - 1])
    ax.contourf(gx, gy, V(gx, gy), levels=[V_L1, 1e3], colors=["0.75"])
    ax.plot(s.y[0], s.y[1], color=col, lw=0.5)
    ax.add_patch(Circle((-mu, 0), 0.06, fc="0.75", ec="k", lw=1.5))
    ax.add_patch(Circle((1 - mu, 0), 0.03, fc="0.75", ec="k", lw=1.5))
    ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal")
    ax.set_xlabel("$x/R$"); ax.set_ylabel("$y/R$")
    axes.append(ax)

# -- Poincare section y = 0, v > 0 (crossings y: - -> +), x_n and u_n ----------
ax = fig.add_subplot(gs[1, :])
axes.append(ax)
xg = np.linspace(-1.5, 1.5, 600)
ug = np.linspace(-3, 3, 400)
XG, UG = np.meshgrid(xg, ug)
with np.errstate(divide="ignore"):
    Hs = UG**2 / 2 + V(XG, 0.0)
ax.contourf(XG, UG, Hs, levels=[V_L1, 1e3], colors=["0.75"])
# the three regular orbits are run long enough to draw closed loops; the
# chaotic one (black) is cut at t = 300 to keep the picture readable
for ic, col, TMAX in zip(ics, cols, [1500.0] * 3 + [300.0]):
    tp, Xp = cb.poincare_section(cb.rotating_threebody, ic, TMAX, (1, 0.0),
                                 direction=+1, discard=75.0, rtol=1e-10,
                                 atol=1e-12, mu=mu)
    ax.plot(Xp[:, 0], Xp[:, 2], "D", color=col, ms=2.5,
            mfc="none" if col == "k" else col)
    print("section ic %s: %d crossings" % (ic, len(tp)))
ax.set_xlim(-1, 1); ax.set_ylim(-3, 3)
ax.set_xlabel("$x$"); ax.set_ylabel("$u$")
bf.panel_labels(axes)
bf.save(fig, OUT / "cont4d_3body_trajectories.png")
