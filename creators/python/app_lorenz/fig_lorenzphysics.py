"""Velocity and temperature field described by the Lorenz amplitudes x, y, z."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
plt.style.use(HERE.parent / "book.mplstyle")
OUT = HERE.parents[2] / "python" / "_static" / "app_lorenz"
OUT.mkdir(parents=True, exist_ok=True)

a = 1 / np.sqrt(2)
r = 28.0
X, Y, Z = 1.0, 20.0, 20.0  # representative amplitudes x(t), y(t), z(t)


def fields(x, z):
    u = -X * (1 + a**2) * np.pi / a * np.sin(np.pi * a * x) * np.cos(np.pi * z)
    w = X * np.pi * (1 + a**2) * np.cos(np.pi * a * x) * np.sin(np.pi * z)
    th = (Y * np.cos(np.pi * a * x) * np.sin(np.pi * z)
          - 0.5 * Z * np.sin(2 * np.pi * z)) / (r * np.pi) - (z - 0.5)
    return u, w, th


xg = np.linspace(-2.8, 2.8, 300)
zg = np.linspace(0, 1, 120)
XX, ZZ = np.meshgrid(xg, zg)
_, _, TH = fields(XX, ZZ)

xq = np.linspace(-2.6, 2.6, 15)
zq = np.linspace(0.07, 0.93, 8)
XQ, ZQ = np.meshgrid(xq, zq)
UQ, WQ, _ = fields(XQ, ZQ)

fig, ax = plt.subplots(figsize=(5.0, 2.8), layout="constrained")
cf = ax.contourf(XX, ZZ, TH, levels=10, cmap="Greys_r")
ax.contour(XX, ZZ, TH, levels=10, colors="k", linewidths=0.6)
ax.quiver(XQ, ZQ, UQ, WQ, color="w", edgecolor="k", linewidth=0.5,
          pivot="mid", scale=120, width=0.005)
ax.set_xlabel(r"$\xi$")
ax.set_ylabel(r"$\zeta$")
fig.colorbar(cf, ax=ax, label=r"$\Theta$", pad=0.02)
fig.savefig(OUT / "cont3d_lorenzphysics.png", dpi=150)
