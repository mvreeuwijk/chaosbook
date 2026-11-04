"""Lyapunov figures for the Lorenz system (r = 28, sigma = 10, b = 8/3).

Produces (in python/_static/cont3d/):
  cont3d_lorenz_lyapunov.png         separation of two trajectories, log scale
  cont3d_LorenzLyapEffective.png     effective exponent Lambda_e(t)
  cont3d_LorenzLyapComprehensive.png eigenvalues of J_S with Lambda_e (top)
                                     and their cumulative averages (bottom)
  cont3d_LorenzLyapCumulative.png    cumulative averages on their own
  cont3d_lorenzlyapattractor.png     Lambda_e on the attractor
Prints the numbers quoted in the chapter.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "cont3d"
OUT.mkdir(parents=True, exist_ok=True)


def run(ic, tend, dt):
    t = np.arange(0, tend + dt / 2, dt)
    return solve_ivp(cb.lorenz, [0, tend], ic, t_eval=t, rtol=1e-12, atol=1e-14,
                     method="DOP853")


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


# -- initial condition on the attractor: integrate to t = 25 ------------------
x0 = solve_ivp(cb.lorenz, [0, 25], [2, 5, 5], rtol=1e-12, atol=1e-14,
               method="DOP853").y[:, -1]

# -- growth of a perturbation, eps = 1e-7, t in [0, 20] -----------------------
eps = 1e-7
s1, s2 = run(x0, 20, 0.01), run(x0 + [eps, 0, 0], 20, 0.01)
delta = np.linalg.norm(s2.y - s1.y, axis=0)
plt.figure(figsize=(5.0, 3.5))
plt.semilogy(s1.t, delta, "k", lw=1.5, label=r"$\delta$")
plt.semilogy(s1.t, eps * np.exp(0.9 * s1.t), "k--", lw=1,
             label=r"$10^{-7}\,e^{0.9\,t}$")
plt.xlim(0, 20)
plt.xlabel("$t$"); plt.ylabel(r"$\delta$")
plt.legend()
save("cont3d_lorenz_lyapunov")
m = (s1.t > 1) & (delta < 1e-1)
slope = np.polyfit(s1.t[m], np.log(delta[m]), 1)[0]
print("fit of ln(delta) against t (delta < 0.1): slope = %.3f" % slope)
# when does the separation reach the size of the attractor? (saturation)
t_sat = s1.t[np.argmax(delta > 10)]
print("delta first exceeds 10 at t = %.2f; delta(t=15) = %.2f; "
      "mean delta over t in [18, 20] = %.2f"
      % (t_sat, delta[s1.t >= 15][0], delta[s1.t >= 18].mean()))

# -- effective exponent: N = 6000, dt = 0.005, eps = 1e-12 --------------------
eps = 1e-12
dt = 0.005
x10 = solve_ivp(cb.lorenz, [0, 10], [2, 5, 5], rtol=1e-12, atol=1e-14,
                method="DOP853").y[:, -1]          # transient t = 10
a, bb = run(x10, 30 - dt, dt), run(x10 + [eps, 0, 0], 30 - dt, dt)
le, local_rates = cb.effective_lyapunov(cb.lorenz, a.t, a.y.T, bb.y.T)
ev = local_rates                       # instantaneous stretching rates of J_S
good = np.linalg.norm(bb.y - a.y, axis=0) < 1.0     # perturbation still small
print("Lambda_e time average (delta < 1): %.3f; between %.3f and %.3f"
      % (le[good].mean(), ev[good, 0].mean(), ev[good, -1].mean()))
print("J_S eigenvalue sum (= -(sigma+1+b) = %.4f): %.4f"
      % (-(10 + 1 + 8 / 3), ev.sum(axis=1).mean()))

plt.figure(figsize=(5.0, 3.5))
plt.plot(a.t[good], le[good], "k", lw=1)
plt.axhline(0, color="k", lw=0.5)
plt.xlabel("$t$"); plt.ylabel(r"$\Lambda_e$")
save("cont3d_LorenzLyapEffective")

# -- eigenvalues of J_S with Lambda_e, and cumulative averages ----------------
tmax = 11.0
sel = good & (a.t <= tmax)
cum = lambda y: np.cumsum(y) / np.arange(1, len(y) + 1)
curves = [(ev[:, 2], "r", r"$\Lambda_3$"), (ev[:, 1], "g", r"$\Lambda_2$"),
          (ev[:, 0], "b", r"$\Lambda_1$"), (le, "k", r"$\Lambda_e$")]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.0, 5.0), sharex=True)
for y, col, lab in curves:
    ax1.plot(a.t[sel], y[sel], col, lw=1.2, label=lab)
    ax2.plot(a.t[sel], cum(y[good])[sel[good]], col, lw=1.2)
ax1.axhline(0, color="k", lw=0.4); ax2.axhline(0, color="k", lw=0.4)
ax1.set_ylabel(r"$\Lambda$"); ax2.set_ylabel(r"$\langle\Lambda\rangle_t$")
ax2.set_xlabel("$t$"); ax2.set_xlim(0, tmax)
ax1.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.18))
save("cont3d_LorenzLyapComprehensive")

plt.figure(figsize=(5.0, 3.5))
for y, col, lab in curves:
    plt.plot(a.t[sel], cum(y[good])[sel[good]], col, lw=1.2, label=lab)
plt.axhline(0, color="k", lw=0.4)
plt.xlabel("$t$"); plt.ylabel(r"$\langle\Lambda\rangle_t$"); plt.xlim(0, tmax)
plt.legend(ncol=2)
save("cont3d_LorenzLyapCumulative")
print("cumulative averages at t = 11: " +
      ", ".join("%s %.2f" % (lab.strip(r"$\\"), cum(y[good])[sel[good]][-1])
                for y, _, lab in curves))

# -- Lambda_e on the attractor (long run, renormalised in segments) -----------
pts = []
x = x0
for seg in range(8):                      # 8 segments of t = 20
    sa = run(x, 20, 0.01)
    sb = run(x + [1e-9, 0, 0], 20, 0.01)
    l, _ = cb.effective_lyapunov(cb.lorenz, sa.t, sa.y.T, sb.y.T)
    keep = np.linalg.norm(sb.y - sa.y, axis=0) < 1e-3
    pts.append(np.column_stack([sa.y.T[keep], l[keep]]))
    x = sa.y[:, -1]
P = np.vstack(pts)
fig = plt.figure(figsize=(4.2, 4.2))
ax = fig.add_subplot(projection="3d")
mid = np.abs(P[:, 3]) <= 6
ax.scatter(*P[mid, :3].T, marker="+", s=4, color="0.7", linewidths=0.5)
hi, lo = P[:, 3] > 6, P[:, 3] < -6
ax.scatter(*P[lo, :3].T, marker="+", s=12, color="k", linewidths=0.7)
ax.scatter(*P[hi, :3].T, marker="o", s=12, facecolors="none",
           edgecolors="k", linewidths=0.7)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.view_init(elev=12, azim=-70)
save("cont3d_lorenzlyapattractor")
print("Lambda_e on the attractor: mean %.3f, fractions > 6: %.3f, < -6: %.3f"
      % (P[:, 3].mean(), hi.mean(), lo.mean()))
print("largest Lyapunov exponent (renormalisation, t = 200): %.3f"
      % cb.lyapunov_exponent(cb.lorenz, x0, 200, dt=0.05))
