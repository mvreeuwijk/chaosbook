"""Harnessing chaos, "Chaos in practice".

Produces (in python/_static/practice/):
  practice_mixing.png          chaotic advection: two dye blobs stretched and folded
  practice_control.png         OGY-style control of the logistic map
  practice_reconstruction.png  Lorenz attractor from the x-coordinate alone
  practice_reactor.png         the same idea on a noisy signal (illustrative)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

plt.style.use(Path(__file__).resolve().parents[1] / "book.mplstyle")
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "practice"
OUT.mkdir(parents=True, exist_ok=True)

C_TRUTH, C_FREE, C_ANA, C_OBS = "#111111", "#c0392b", "#1f6aa5", "#e08a1e"

# -- chaotic mixing: two shears, stretched and folded dye --------------------
A = 0.9


def mix_step(p):
    x = (p[:, 0] + A * np.sin(2 * np.pi * p[:, 1])) % 1.0
    y = (p[:, 1] + A * np.sin(2 * np.pi * x)) % 1.0
    return np.column_stack([x, y])


rng = np.random.default_rng(5)
n = 6000
blob1 = np.column_stack([0.25 + 0.05 * rng.standard_normal(n),
                         0.5 + 0.05 * rng.standard_normal(n)])
blob2 = np.column_stack([0.75 + 0.05 * rng.standard_normal(n),
                         0.5 + 0.05 * rng.standard_normal(n)])
times = [0, 2, 5]
snaps = {0: (blob1, blob2)}
for i in range(1, max(times) + 1):
    blob1, blob2 = mix_step(blob1), mix_step(blob2)
    snaps[i] = (blob1, blob2)

fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.4))
for ax, s in zip(axes, times):
    p1, p2 = snaps[s]
    ax.scatter(p1[:, 0], p1[:, 1], s=1.5, color=C_FREE, edgecolors="none")
    ax.scatter(p2[:, 0], p2[:, 1], s=1.5, color=C_ANA, edgecolors="none")
    ax.set_title(f"$n = {s}$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
axes[0].set_ylabel("$y$")
fig.tight_layout()
fig.savefig(OUT / "practice_mixing.png", dpi=150)
plt.close(fig)

# -- controlling chaos: OGY on the logistic map -------------------------------
r0 = 3.9
xstar = 1.0 - 1.0 / r0                 # the unstable fixed point
drmax = 0.05                           # largest admissible nudge
N, Ncon = 240, 100
x = 0.2
xs, dr = np.empty(N), np.zeros(N)
for k in range(N):
    xs[k] = x
    rr = r0
    if k >= Ncon:                      # switch the controller on
        d = xstar / (x * (1 - x)) - r0
        if abs(d) <= drmax:            # only nudge when already near x*
            rr, dr[k] = r0 + d, d
    x = cb.logistic(x, rr)
captured = Ncon + int(np.argmax(np.abs(xs[Ncon:] - xstar) < 1e-6))
print(f"control: captured onto x* = {xstar:.4f} at n = {captured}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.8, 4.4), sharex=True,
                               height_ratios=[3, 1])
ax1.plot(xs, color=C_TRUTH, lw=0.8, marker="o", ms=2.2)
ax1.axhline(xstar, color=C_ANA, ls="--", lw=1.1, label=r"target orbit $x^{*}$")
ax1.axvline(Ncon, color=C_OBS, lw=1.0)
ax1.text(Ncon + 4, 0.06, "control on", color=C_OBS, fontsize=11)
ax1.set_ylabel("$x_n$")
ax1.set_ylim(0, 1)
ax1.legend(loc="lower right")
ax2.axhline(0, color="#999999", lw=0.6)
ax2.plot(dr, color=C_FREE, lw=1.0)
ax2.set_ylabel(r"$\delta r_n$")
ax2.set_xlabel("$n$")
ax2.set_xlim(0, N)
ax2.set_ylim(-drmax, drmax)
fig.tight_layout()
fig.savefig(OUT / "practice_control.png", dpi=150)
plt.close(fig)

# -- attractor reconstruction from x(t) alone (Takens) -----------------------
xa = solve_ivp(cb.lorenz, [0, 50], [1, 1, 1], rtol=1e-10, atol=1e-12).y[:, -1]
sol = solve_ivp(cb.lorenz, [0, 80], xa, t_eval=np.arange(0, 80, 0.01),
                rtol=1e-9, atol=1e-11)
X = sol.y[0]
tau = 18                               # delay, in samples
M = len(X) - 2 * tau
emb = np.column_stack([X[:M], X[tau:M + tau], X[2 * tau:M + 2 * tau]])

fig = plt.figure(figsize=(9.0, 4.2))
ax1 = fig.add_subplot(121, projection="3d")
ax1.plot(*sol.y, color=C_TRUTH, lw=0.3)
ax1.set_title(r"true attractor $(x,y,z)$")
ax2 = fig.add_subplot(122, projection="3d")
ax2.plot(*emb.T, color=C_ANA, lw=0.3)
ax2.set_title(r"reconstruction $(x_t,\,x_{t+\tau},\,x_{t+2\tau})$")
for ax in (ax1, ax2):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.grid(False)
    ax.view_init(elev=22, azim=-125)
fig.tight_layout()
fig.savefig(OUT / "practice_reconstruction.png", dpi=150)
plt.close(fig)


# -- the Takens route in industry: a noisy Rossler signal (illustrative) -----
def rossler(t, s, a=0.2, b=0.2, c=5.7):
    x, y, z = s
    return [-y - z, x + a * y, b + z * (x - c)]


dt = 0.03
rs = solve_ivp(rossler, [0, 7000 * dt], [1, 1, 1],
               t_eval=np.arange(7000) * dt, rtol=1e-9, atol=1e-11)
xs_r = rs.y[0][1500:]                                   # discard transient
rng = np.random.default_rng(9)
p = xs_r + 0.20 * rng.standard_normal(len(xs_r))        # measurement noise
tau = 12
emb = np.column_stack([p[:-2 * tau], p[tau:-tau], p[2 * tau:]])

fig = plt.figure(figsize=(9.0, 3.6))
ax1 = fig.add_subplot(121)
ax1.plot(np.arange(700) * dt, p[:700], color=C_TRUTH, lw=0.7)
ax1.set_title(r"measured signal $p(t)$")
ax1.set_xlabel("time")
ax1.set_ylabel("$p$")
ax1.set_yticks([])
ax2 = fig.add_subplot(122, projection="3d")
ax2.plot(*emb.T, color=C_ANA, lw=0.3)
ax2.set_title("reconstructed attractor (fingerprint)")
ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_zticks([])
ax2.grid(False)
ax2.view_init(elev=26, azim=-60)
fig.tight_layout()
fig.savefig(OUT / "practice_reactor.png", dpi=150)
plt.close(fig)
print("fig_harness: assets written to", OUT)
