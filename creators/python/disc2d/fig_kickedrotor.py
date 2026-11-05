"""Kicked-rotor figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  (disc2d_kickedrotor.png, the sketch, is drawn by fig_schematics.py)
  disc2d_kickedrotor_dynamics.png  1x3: (a) kicking force F_t at t = 0, 10, ..., 50;
                                   (b) velocity v before (circle) and after
                                   (square) kicks; (c) phase angle theta
K = 0.5, T = 10, tau = 5e8 (friction negligible), r = m = 1,
theta_0 = 0.4, v_0 = 0.05.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)


K, T, tau, r, m = 0.5, 10.0, 5e8, 1.0, 1.0
N = 5


def S(th):
    return K * np.sin(th)


def f_theta(th0, v0, t):
    return v0 * tau / r * (1 - np.exp(-t / tau)) + th0


def f_v(th0, v0, t):
    return v0 * np.exp(-t / tau)


theta, v, v_minus = [0.4], [0.05], [0.05]
for i in range(N):
    theta.append(f_theta(theta[i], v[i], T))
    v_minus.append(f_v(theta[i], v[i], T))
    v.append(v_minus[-1] + S(theta[i + 1]) / m)
theta, v, v_minus = map(np.array, (theta, v, v_minus))
tk = T * np.arange(N + 1)
TICKS = [0, 10, 20, 30, 40, 50]

fig, axs = plt.subplots(1, 3, figsize=(bf.FULL_W, 2.0))

# (a) forcing: kick at each time iT with strength S(theta_i)
ax = axs[0]
Fk = S(theta)
ax.vlines(tk, 0, Fk, color="k", lw=2)
ax.plot(tk, Fk, "kD", markerfacecolor="none", markersize=6)
ax.plot(tk, np.zeros_like(tk), "ko", markerfacecolor="none", markersize=5)
ax.axhline(0, color="k", lw=0.6)
ax.set_xticks(TICKS)
ax.set_yticks([0])
ax.set_ylim(-0.75, 0.75)
ax.set_ylabel("$F_t$")

# (b) velocity: constant between kicks, jumps at kicks
ax = axs[1]
for i in range(N):
    ax.plot([i * T, (i + 1) * T], [v[i], v_minus[i + 1]], "k", lw=2)
ax.plot(tk[1:], v_minus[1:], "ko", markerfacecolor="none", markersize=6)
ax.plot(tk, v, "ks", markerfacecolor="none", markersize=6)
ax.axhline(0, color="k", lw=0.6)
ax.set_ylim(-1, 1)
ax.set_yticks([-1, 0, 1])
ax.set_xticks(TICKS)
ax.set_ylabel("$v$")

# (c) phase angle: linear between kicks
ax = axs[2]
for i in range(N):
    ax.plot([i * T, (i + 1) * T], [theta[i], theta[i + 1]], "k", lw=2)
ax.plot(tk, theta, "ko", markerfacecolor="none", markersize=6)
ax.set_ylim(0, 2 * np.pi)
ax.set_yticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
ax.set_xticks(TICKS)
ax.set_ylabel(r"$\theta$")

for ax in axs:
    ax.set_xlim(0, 50)
    ax.set_xlabel("$t$")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc2d_kickedrotor_dynamics.png")
print("theta:", theta)
print("v:", v)
print("fig_kickedrotor: assets written to", OUT)
