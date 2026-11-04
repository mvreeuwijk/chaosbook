"""Closed-form-solution and pdf figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_analytical.png  x_n = sin^2(2^n theta) vs the iterated map
  disc1d_tanh_analytical.png    x_n = tanh(2^n theta) vs the iterated map
  disc1d_pdfs.png               1x2: histogram vs 1/(pi sqrt(x(1-x))) and
                                1/(pi sqrt(1-x^2))
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- analytical solution of the r=4 logistic map -----------------------------
x0 = 0.36
theta = np.arcsin(np.sqrt(x0))
t = np.linspace(0, 7, 400)
fig, ax = plt.subplots(figsize=(bf.FULL_W, 2.2))
ax.plot(t, np.sin(2**t * theta) ** 2, "gray", linewidth=1)
X = cb.orbit(cb.logistic, x0=x0, n=7, r=4)
ax.plot(range(8), X, "ko", markersize=4)
ax.set_xlabel("$n$")
ax.set_ylabel("$x_n$")
bf.save(fig, OUT / "disc1d_logist_analytical.png")

# -- analytical solution of the tanh map -------------------------------------
x0 = 0.05
theta = np.arctanh(x0)
t = np.linspace(0, 14, 400)
fig, ax = plt.subplots(figsize=(bf.FULL_W, 2.2))
ax.plot(t, np.tanh(2**t * theta), "gray", linewidth=1)
X = np.zeros(15)
X[0] = x0
for n in range(14):
    X[n + 1] = 2 * X[n] / (1 + X[n] ** 2)
ax.plot(range(15), X, "ko", markersize=4)
ax.set_xlabel("$n$")
ax.set_ylabel("$x_n$")
bf.save(fig, OUT / "disc1d_tanh_analytical.png")

# -- pdfs: 1x2 ---------------------------------------------------------------
fig, (axa, axb) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.4))
X = cb.orbit(cb.logistic, x0=0.1, n=8192, r=4)
axa.hist(X, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(0.005, 0.995, 300)
axa.plot(xs, 1 / (np.pi * np.sqrt(xs * (1 - xs))), "k", linewidth=1.5)
axa.axis([0, 1, 0, 2])
axa.set_xlabel("$x$")
axa.set_ylabel("$p(x)$")

S = np.zeros(8193)
S[0] = 0.3
for n in range(8192):
    S[n + 1] = -4 * S[n] ** 3 + 3 * S[n]
axb.hist(S, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(-0.995, 0.995, 300)
axb.plot(xs, 1 / (np.pi * np.sqrt(1 - xs**2)), "k", linewidth=1.5)
axb.axis([-1, 1, 0, 2])
axb.set_xlabel("$x$")
axb.set_ylabel("$p(x)$")
bf.panel_labels([axa, axb])
bf.save(fig, OUT / "disc1d_pdfs.png")

print("fig_analytical_statistical: assets written to", OUT)
