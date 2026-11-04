"""Schematics and the Poincare section for the fractals chapter and exercises.

Produces:
  python/_static/fractals/fractals_cloudscaling.png   schematic cloud scaling A ~ L^(7/3)
                                                      (seeded synthetic scatter, not data)
  python/_static/exercises/FractalCurve.png           recursive fractal-curve sketch
  python/_static/exercises/ex0121r00_fig1.png         forced double-well beam sketch
  python/_static/exercises/ex0121r00_fig2.png         its Poincare section (A=0.3, N=10000)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.integrate import solve_ivp

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

ROOT = Path(__file__).resolve().parents[3] / "python" / "_static"
(ROOT / "fractals").mkdir(parents=True, exist_ok=True)
(ROOT / "exercises").mkdir(parents=True, exist_ok=True)
GRAY, RED = "#888888", "#b22222"

# -- cloud scaling (schematic) -------------------------------------------------
rng = np.random.default_rng(3)
L = 10 ** rng.uniform(np.log10(45), 3, 250)
A = 0.008 * (L / 45) ** (7 / 3) * 10 ** rng.normal(0, 0.1, L.size)
Ls = np.array([45, 1000.0])
fig, ax = plt.subplots(figsize=(4.2, 3.3))
ax.loglog(L, A, ".", color="k", alpha=0.45, ms=4)
ax.loglog(Ls, 0.008 * (Ls / 45) ** (7 / 3), color=RED, lw=2,
          label=r"$A\sim L^{D_s},\ D_s\simeq 7/3$")
ax.loglog(Ls, 0.008 * (Ls / 45) ** 2, "--", color=GRAY, lw=1.5,
          label=r"smooth objects, $D_s=2$")
ax.set_xlabel(r"linear size $L=V^{1/3}$ [m]")
ax.set_ylabel(r"surface area $A$ [km$^2$]")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=10)
fig.tight_layout()
fig.savefig(ROOT / "fractals" / "fractals_cloudscaling.png", dpi=150)
plt.close(fig)

# -- fractal curve sketch ---------------------------------------------------------
phi = np.pi / 7
c = np.cos(phi)
a = (2 * c - np.sqrt(4 * c**2 - 3)) / 3  # equal segments: 3a^2 - 4a cos(phi) + 1 = 0
gen = np.array([0, a * np.exp(1j * phi), 1 - a * np.exp(1j * phi), 1])


def refine(pts):
    out = []
    for p, q in zip(pts[:-1], pts[1:]):
        out += list(p + (q - p) * gen[:-1])
    return np.array(out + [pts[-1]])


fig, axes = plt.subplots(2, 2, figsize=(8.0, 3.6))
(a0, a1), (a2, a3) = axes
a0.plot([0, 1], [0, 0], "k", lw=1.5)
a0.text(0.5, 0.04, r"$1\,$m", ha="center")
a1.plot(gen.real, gen.imag, "k", lw=1.5)
a1.plot([0, 1], [0, 0], "k:", lw=1)
a1.text(0.2, 0.2, r"$a$", ha="center")
a1.text(0.5, 0.03, r"$a$", ha="left")
a1.text(0.8, -0.2, r"$a$", ha="center")
a1.text(0.1, 0.02, r"$\phi$", ha="left")
a1.text(0.84, -0.02, r"$\phi$", ha="left", va="top")
p1 = gen.copy()
p2 = refine(p1)
a2.plot(p2.real, p2.imag, "k", lw=1.5)
a2.plot(p1.real, p1.imag, "k:", lw=1)
p = np.array([0, 1 + 0j])
for _ in range(4):
    p = refine(p)
a3.plot(p.real, p.imag, "k", lw=1)
for ax in axes.ravel():
    ax.set_aspect("equal")
    ax.axis("off")
fig.tight_layout()
fig.savefig(ROOT / "exercises" / "FractalCurve.png", dpi=150)
plt.close(fig)

# -- double-well beam sketch ------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.0, 2.8))
lw = 1.5
ax.add_patch(Rectangle((0.6, 0.0), 6.2, 0.3, fc="none", ec="k", lw=lw))      # base
ax.add_patch(Rectangle((0.6, 0.0), 0.3, 4.8, fc="none", ec="k", lw=lw))      # left wall
ax.add_patch(Rectangle((0.6, 4.5), 6.6, 0.3, fc="none", ec="k", lw=lw))      # top
ax.add_patch(Rectangle((-0.8, 1.8), 1.7, 0.3, fc="none", ec="k", lw=lw))     # driving arm
ax.add_patch(Rectangle((2.2, 0.3), 0.55, 0.3, fc="#bbbbbb", ec="k", lw=lw, hatch="////"))
ax.add_patch(Rectangle((5.0, 0.3), 0.55, 0.3, fc="#bbbbbb", ec="k", lw=lw, hatch="////"))
ax.plot([4.0, 4.0], [0.3, 4.5], "k--", lw=1)
s = np.linspace(0, 1, 100)
ax.plot(4.0 + 1.1 * s**2.2, 4.5 - 3.9 * s, "k", lw=2)
ax.annotate("", xy=(5.05, 0.8), xytext=(4.0, 0.8), arrowprops=dict(arrowstyle="-|>", color="k"))
ax.text(4.5, 0.9, r"$x$", ha="center", va="bottom")
ax.text(4.9, 2.5, "beam")
ax.text(2.4, 0.75, "magnet", ha="center")
ax.text(7.3, 0.05, "rigid frame", va="bottom")
ax.text(-2.4, 3.0, "periodic\nforcing", ha="left")
ax.annotate("", xy=(-0.9, 2.4), xytext=(0.5, 2.4),
            arrowprops=dict(arrowstyle="<|-|>", color="k"))
ax.set_xlim(-2.5, 8.8)
ax.set_ylim(-0.1, 5.0)
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(ROOT / "exercises" / "ex0121r00_fig1.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# -- Poincare section of the forced double well -----------------------------------
A_, f_, om, N = 0.3, 0.15, 1.0, 10000


def rhs(t, s):
    x, y, z = s
    return [y, -f_ * y + x - x**3 + A_ * np.cos(z), om]


tt = 2 * np.pi / om * np.arange(1, N + 1)
sol = solve_ivp(rhs, (0, tt[-1]), [0, 0, 0], t_eval=tt, rtol=1e-8, atol=1e-10)
x, y = sol.y[0][N // 2:], sol.y[1][N // 2:]
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.plot(x, y, "k.", ms=2)
ax.set_xlim(-2, 2)
ax.set_ylim(-1.0, 1.4)   # the section reaches y > 1
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
fig.tight_layout()
fig.savefig(ROOT / "exercises" / "ex0121r00_fig2.png", dpi=150)
plt.close(fig)
print("wrote cloudscaling, FractalCurve, ex0121r00_fig1, ex0121r00_fig2")
