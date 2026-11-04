"""Kicked-rotor figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_kickedrotor.png         hand-drawn sketch, copied from the Maple edition
                                 (no generating script exists)
  disc2d_kickedrotor_delta.png   kicking force F_t at t = 0, 10, ..., 50
  disc2d_kickedrotor_v.png       velocity v before (circle) and after (square) kicks
  disc2d_kickedrotor_theta.png   phase angle theta at kicks
K = 0.5, T = 10, tau = 5e8 (friction negligible), r = m = 1,
theta_0 = 0.4, v_0 = 0.05.
"""

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "python" / "_static" / "disc2d"
OUT.mkdir(parents=True, exist_ok=True)

shutil.copyfile(ROOT / "maple" / "_static" / "disc2d" / "disc2d_kickedrotor.png",
                OUT / "disc2d_kickedrotor.png")

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
SIZE = (4.2, 2.2)
TICKS = [0, 10, 20, 30, 40, 50]


def finish(name, xlabel, ylabel):
    plt.xlim(0, 50)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=150)
    plt.close()


# forcing: kick at each time iT with strength S(theta_i)
plt.figure(figsize=SIZE)
Fk = S(theta)
plt.vlines(tk, 0, Fk, color="k", lw=2)
plt.plot(tk, Fk, "kD", markerfacecolor="none", markersize=6)
plt.plot(tk, np.zeros_like(tk), "ko", markerfacecolor="none", markersize=5)
plt.axhline(0, color="k", lw=0.6)
plt.xticks(TICKS)
plt.yticks([0])
plt.ylim(-0.75, 0.75)
finish("disc2d_kickedrotor_delta.png", "$t$", "$F_t$")

# phase angle: linear between kicks
plt.figure(figsize=SIZE)
for i in range(N):
    plt.plot([i * T, (i + 1) * T], [theta[i], theta[i + 1]], "k", lw=2)
plt.plot(tk, theta, "ko", markerfacecolor="none", markersize=6)
plt.ylim(0, 2 * np.pi)
plt.yticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
plt.xticks(TICKS)
finish("disc2d_kickedrotor_theta.png", "$t$", r"$\theta$")

# velocity: constant between kicks, jumps at kicks
plt.figure(figsize=SIZE)
for i in range(N):
    plt.plot([i * T, (i + 1) * T], [v[i], v_minus[i + 1]], "k", lw=2)
plt.plot(tk[1:], v_minus[1:], "ko", markerfacecolor="none", markersize=6)
plt.plot(tk, v, "ks", markerfacecolor="none", markersize=6)
plt.axhline(0, color="k", lw=0.6)
plt.ylim(-1, 1)
plt.yticks([-1, 0, 1])
plt.xticks(TICKS)
finish("disc2d_kickedrotor_v.png", "$t$", "$v$")
print("theta:", theta)
print("v:", v)
print("fig_kickedrotor: assets written to", OUT)
