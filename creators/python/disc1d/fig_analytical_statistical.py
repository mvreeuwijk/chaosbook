"""Closed-form-solution and pdf figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_analytical.png  x_n = sin^2(2^n theta) vs the iterated map
  disc1d_tanh_analytical.png    x_n = tanh(2^n theta) vs the iterated map
  disc1d_logist_pdf.png         histogram vs 1/(pi sqrt(x(1-x)))
  disc1d_sin3map_pdf.png        histogram vs 1/(pi sqrt(1-x^2))
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

# -- analytical solution of the r=4 logistic map -----------------------------
x0 = 0.36
theta = np.arcsin(np.sqrt(x0))
t = np.linspace(0, 7, 400)
plt.figure(figsize=(6.4, 3))
plt.plot(t, np.sin(2**t * theta) ** 2, "gray", linewidth=1)
X = cb.orbit(cb.logistic, x0=x0, n=7, r=4)
plt.plot(range(8), X, "ko", markersize=6)
plt.xlabel("n")
plt.ylabel("x[n]")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_analytical.png", dpi=150)
plt.close()

# -- analytical solution of the tanh map -------------------------------------
x0 = 0.05
theta = np.arctanh(x0)
t = np.linspace(0, 14, 400)
plt.figure(figsize=(6.4, 3))
plt.plot(t, np.tanh(2**t * theta), "gray", linewidth=1)
X = np.zeros(15)
X[0] = x0
for n in range(14):
    X[n + 1] = 2 * X[n] / (1 + X[n] ** 2)
plt.plot(range(15), X, "ko", markersize=6)
plt.xlabel("n")
plt.ylabel("x[n]")
plt.tight_layout()
plt.savefig(OUT / "disc1d_tanh_analytical.png", dpi=150)
plt.close()

# -- pdfs --------------------------------------------------------------------
X = cb.orbit(cb.logistic, x0=0.1, n=8192, r=4)
plt.figure(figsize=(4.8, 3.4))
plt.hist(X, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(0.005, 0.995, 300)
plt.plot(xs, 1 / (np.pi * np.sqrt(xs * (1 - xs))), "k", linewidth=2.5)
plt.axis([0, 1, 0, 2])
plt.xlabel("x")
plt.ylabel("p(x)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_pdf.png", dpi=150)
plt.close()

S = np.zeros(8193)
S[0] = 0.3
for n in range(8192):
    S[n + 1] = -4 * S[n] ** 3 + 3 * S[n]
plt.figure(figsize=(4.8, 3.4))
plt.hist(S, bins=32, density=True, color="lightgray", edgecolor="gray")
xs = np.linspace(-0.995, 0.995, 300)
plt.plot(xs, 1 / (np.pi * np.sqrt(1 - xs**2)), "k", linewidth=2.5)
plt.axis([-1, 1, 0, 2])
plt.xlabel("x")
plt.ylabel("p(x)")
plt.tight_layout()
plt.savefig(OUT / "disc1d_sin3map_pdf.png", dpi=150)
plt.close()

print("fig_analytical_statistical: assets written to", OUT)
