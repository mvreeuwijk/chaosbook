"""Circle-map figures for "Discrete mappings of higher order".

Produces (in python/_static/disc2d/):
  disc2d_circle                    sketch of a flow on a circle
  disc2d_lincircle_cobweb          period-3 cobweb of x + Omega mod 1
  disc2d_lincircle_quasi           (a) quasi-periodic series, Omega = golden
                                   ratio, (b) its cobweb
  disc2d_circlemap_series          phase locking, Omega near 1/2 (K = 1)
  disc2d_circlemap_return_p2       second iterate f(f(x)) for three Omega
  disc2d_circlemap_winding         Devil's staircase W(Omega) at K = 1
  disc2d_circlemap_bifurcation     bifurcation diagram and Lyapunov exponent
  disc2d_circlemap_lyapunov        Lyapunov exponent in the Omega-K plane
  interactive/devils_staircase.html  deep-zoom Devil's staircase
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import fsolve

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)
OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def save(name):
    bf.save(plt.gcf(), OUT / f"{name}.png")


def mod1(x):
    return x - np.floor(x)


def lin(x, Omega):
    return mod1(x + Omega)


def circ(x, Omega, K=1.0):
    return mod1(cb.circle_map(x, Omega, K))


def jumpless(x, y):
    """Insert NaN where y jumps (the mod 1 discontinuities), for line plots."""
    y = y.copy()
    y[1:][np.abs(np.diff(y)) > 0.5] = np.nan
    return x, y


def cobweb_black(f, x0, n, ax, lw_map=2.0, **params):
    X = cb.orbit(f, x0, n, **params)
    xs = np.linspace(0, 1, 4001)
    ax.plot(*jumpless(xs, f(xs, **params)), "k", lw=lw_map)
    ax.plot(xs, xs, "k--", lw=1)
    px, py = [], []
    for k in range(1, n):
        px += [X[k], X[k]]
        py += [X[k], X[k + 1]]
    ax.plot(px, py, "k", lw=0.8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")
    return X


# -- sketch of a circle ------------------------------------------------------
fig, ax = plt.subplots(figsize=(2.5, 2.5))
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), "k", lw=1.5)
for ang, lab, ha, va in [(0, "$0$", "left", "center"),
                         (np.pi / 2, r"$\pi/2$", "center", "bottom"),
                         (np.pi, r"$\pi$", "right", "center"),
                         (3 * np.pi / 2, r"$3\pi/2$", "center", "top")]:
    c, s = np.cos(ang), np.sin(ang)
    ax.plot([c, 1.1 * c], [s, 1.1 * s], "k", lw=1.5)
    ax.text(1.15 * c, 1.15 * s, lab, ha=ha, va=va)
th = 0.8
ax.plot([0, np.cos(th)], [0, np.sin(th)], "k", lw=0.8)
ax.plot([0, 1], [0, 0], "k", lw=0.8)
ax.plot(np.cos(th), np.sin(th), "ko", markersize=8)
ax.set_aspect("equal")
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.45, 1.45)
ax.axis("off")
save("disc2d_circle")

# -- linear map on the circle: period 3 --------------------------------------
fig, ax = plt.subplots(figsize=bf.SQUARE)
X = cobweb_black(lin, 0.2, 40, ax, Omega=1 / 3)
# the original figure labels x_1, x_2, x_0 (= x_3) on the axes
ax.set_xticks([X[1], X[2], X[3]], ["$x_1$", "$x_2$", "$x_0$"])
ax.set_yticks([X[1], X[2], X[3]], ["$x_1$", "$x_2$", "$x_0$"])
for a, b in [(1, 2), (2, 3), (3, 4)]:
    ax.plot([0, X[a]], [X[b], X[b]], "k:", lw=0.8)
    ax.plot([X[b], X[b]], [0, X[b + 1]], "k:", lw=0.8)
save("disc2d_lincircle_cobweb")
print("period-3 orbit (Omega=1/3, x0=0.2):", np.round(X[:5], 4))

# -- quasi-periodic ------------------------------------------------------------
Om = (1 + np.sqrt(5)) / 2
X = cb.orbit(lin, 0.2, 150, Omega=Om)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.5),
                             gridspec_kw=dict(width_ratios=[3, 2]))
a1.plot(np.arange(1, 101), X[1:101], "ko", markersize=3, mfc="none")
a1.set_xlim(0, 100)
a1.set_ylim(0, 1)
a1.set_xlabel("$n$")
a1.set_ylabel("$x_n$")
cobweb_black(lin, 0.2, 150, a2, lw_map=1.5, Omega=Om)
a2.set_xticks([0, 1])
a2.set_yticks([0, 1])
bf.panel_labels([a1, a2])
save("disc2d_lincircle_quasi")

# -- phase locking: series -----------------------------------------------------
Oms = [0.46, 0.464, 0.5, 0.536, 0.54]
plt.figure(figsize=(3.8, 3.4))
for i, Om in enumerate(Oms):
    off = 1.5 * (len(Oms) - 1 - i)
    X = cb.orbit(circ, 0.1, 2000, Omega=Om)          # discard transient
    X = cb.orbit(circ, X[-1], 100, Omega=Om)
    plt.plot(range(101), X + off, "k-o", markersize=3, mfc="none", lw=1)
    plt.text(50, off + X.max() + 0.12, rf"$\Omega={Om:.3f}$", ha="center")
plt.xlim(0, 100)
plt.ylim(-0.1, 8)
plt.yticks([0])
plt.xlabel("$n$")
plt.ylabel("$x_n$")
save("disc2d_circlemap_series")

# -- second iterate ---------------------------------------------------------------
xs = np.linspace(0, 1, 4001)
plt.figure(figsize=bf.SQUARE)
plt.plot(xs, xs, "k", lw=1)
for Om, ls, lw in [(0.464, "--", 1.2), (0.5, "-", 2.2), (0.536, "-.", 1.5)]:
    y = circ(circ(xs, Om), Om)
    plt.plot(*jumpless(xs, y), "k", ls=ls, lw=lw)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel("$x$")
plt.ylabel("$f(f(x))$")
save("disc2d_circlemap_return_p2")


# -- period-2 stability limits: f2'(x) = 1 and f2(x) = x simultaneously ----------
def df(x, Om):
    return 1 + np.cos(2 * np.pi * x)


def system(v):
    x, Om = v
    f1 = cb.circle_map(x, Om)
    f2 = cb.circle_map(f1, Om)
    return [df(x, Om) * df(f1, Om) - 1, mod1(f2) - x]


sols = []
for x0 in np.linspace(0.02, 0.98, 25):
    for O0 in np.linspace(0.05, 0.95, 25):
        s, info, ier, _ = fsolve(system, [x0, O0], full_output=True)
        if (ier == 1 and 0 <= s[0] <= 1 and 0 <= s[1] <= 1
                and np.max(np.abs(system(s))) < 1e-9
                and not any(np.allclose(s, t, atol=1e-5) for t in sols)):
            sols.append(s)
print("f2'=1 and f2=x solutions (x, Omega):")
for s in sorted(sols, key=lambda s: s[1]):
    print(f"  x={s[0]:.5f}  Omega={s[1]:.5f}")


# -- Devil's staircase (vectorised over Omega) -------------------------------------
def winding(Oms, N, x0=0.1, K=1.0):
    x = np.full_like(Oms, x0)
    for _ in range(N):
        x = cb.circle_map(x, Oms, K)
    return (x - x0) / N


# the package routine agrees with the vectorised one
chk = [cb.winding_number(cb.circle_map, 0.1, 200, Omega=o) for o in (0.3, 0.5)]
assert np.allclose(chk, winding(np.array([0.3, 0.5]), 200))

Os = np.linspace(0, 1, 501)
W = winding(Os, 200)
fig, ax = plt.subplots(figsize=bf.SQUARE)
ax.plot([0, 1], [0, 1], "k", lw=1)
ax.plot(Os, W, "kD", markersize=2, mfc="none")
for (xx, yy, s) in [(0.1, 0.02, "0/1"), (0.23, 1 / 4, "1/4"), (0.30, 1 / 3, "1/3"),
                    (0.42, 1 / 2, "1/2"), (0.60, 2 / 3, "2/3"),
                    (0.67, 3 / 4, "3/4"), (0.88, 1.01, "1/1")]:
    ax.text(xx, yy + 0.015, s, ha="center", va="bottom", fontsize=8)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.06)
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xlabel(r"$\Omega$")
ax.set_ylabel("$W$")
save("disc2d_circlemap_winding")
print("W plateaus (N=200): W(0.5), W(1/3), W(2/3), W(1/4), W(3/4) =",
      np.round(winding(np.array([0.5, 1 / 3, 2 / 3, 0.25, 0.75]), 200), 4))

# -- bifurcation diagram and Lyapunov exponent ----------------------------------------
N, M = 200, 500
Os = np.linspace(0, 1, M + 1)
x = np.full_like(Os, 0.1)
pts_O, pts_x, lam = [], [], np.zeros_like(Os)
for k in range(1, N + 1):
    x = cb.circle_map(x, Os)
    if k > N // 4:
        with np.errstate(divide="ignore"):
            lam += np.log(np.abs(df(x, Os)))
    if k >= 3 * N // 4:
        pts_O.append(Os)
        pts_x.append(mod1(x))
lam /= 0.75 * N
fig, (a1, a2) = plt.subplots(2, 1, figsize=(3.8, 3.4), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.3, 1]))
a1.plot(np.concatenate(pts_O), np.concatenate(pts_x), "k.", markersize=1.5)
a1.set_ylabel("$x$")
a1.set_ylim(0, 1)
a2.plot(Os, lam, "k", lw=1.2)
a2.axhline(0, color="gray", lw=0.8)
a2.set_ylim(-4, 0.5)
a2.set_ylabel(r"$\Lambda$")
a2.set_xlabel(r"$\Omega$")
a2.set_xlim(0, 1)
save("disc2d_circlemap_bifurcation")
print("circle map K=1: max Lambda over Omega grid = %.3f" % np.max(lam))

# -- Lyapunov exponent in the Omega-K plane --------------------------------------------
nO, nK = 700, 700
Og, Kg = np.meshgrid(np.linspace(0, 1, nO), np.linspace(0, 10, nK))
x = np.full_like(Og, 0.1)
for _ in range(100):
    x = cb.circle_map(x, Og, Kg)
acc = np.zeros_like(Og)
for _ in range(300):
    x = cb.circle_map(x, Og, Kg)
    acc += np.log(np.maximum(np.abs(1 + Kg * np.cos(2 * np.pi * x)), 1e-12))
Lam = acc / 300
plt.figure(figsize=bf.SQUARE)
plt.imshow(Lam, origin="lower", extent=[0, 1, 0, 10], aspect="auto",
           cmap="bwr", vmin=-1, vmax=1, interpolation="nearest")
plt.xlabel(r"$\Omega$")
plt.ylabel("$K$")
save("disc2d_circlemap_lyapunov")

# -- interactive: Devil's staircase on a fine grid ---------------------------------------
Of = np.linspace(0, 1, 8001)
Wf = winding(Of, 2000)
fig = go.Figure()
fig.add_trace(go.Scattergl(x=[0, 1], y=[0, 1], mode="lines",
                           line=dict(color="gray", width=1), name="W = Ω"))
fig.add_trace(go.Scattergl(x=Of, y=Wf, mode="markers",
                           marker=dict(size=2, color="darkblue"),
                           name="W(Ω), K = 1"))
fig.update_layout(xaxis_title="Ω", yaxis_title="W", showlegend=False,
                  margin=dict(l=50, r=10, t=10, b=40), dragmode="zoom")
fig.write_html(OUT / "interactive" / "devils_staircase.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)
print("fig_circlemap: assets written to", OUT)
