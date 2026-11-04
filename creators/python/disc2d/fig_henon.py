"""Henon-map figures for "Discrete mappings of higher order".

a = 1.4, b = 0.3 throughout. Produces (in python/_static/disc2d/):
  disc2d_HenonAttractor.png     x0=(0.1, 0.3), 10000 steps, first 100 dropped
  disc2d_HenonLyap.png          Lyapunov exponents from blocks of N = 1, 10, 200
  disc2d_HenonFold0..5.png      10^4 random initial conditions in
                                [-1.23,1.23] x [-0.41,0.41], steps n = 0..5
  disc2d_HenonStretch{0,4,...,20}.png
                                10^4 initial conditions in a 0.02 x 0.02 box
                                near (1.02, 0.31), steps n = 0, 4, ..., 20
  interactive/henon_fold.html   play-button animation of the folding
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc2d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

a, b = 1.4, 0.3
rng = np.random.default_rng(2)


def henon_jac(x, a=a, b=b):
    return np.array([[-2 * a * x[0], 1.0], [b, 0.0]])


# -- the attractor -------------------------------------------------------------
X = cb.orbit(cb.henon, x0=(0.1, 0.3), n=10000, a=a, b=b)[100:]
plt.figure(figsize=(4.2, 4.2))
plt.plot(X[:, 0], X[:, 1], "k.", markersize=1)
plt.xlim(-1.5, 1.5)
plt.ylim(-0.4, 0.4)
plt.xlabel("$x_n$")
plt.ylabel("$y_n$")
plt.tight_layout()
plt.savefig(OUT / "disc2d_HenonAttractor.png", dpi=150)
plt.close()


# -- Lyapunov exponents from blocks of N iterations -----------------------------
def block_exponents(N, P, x0=(0.1, 0.3)):
    """Per block: eigenvalues of the product of N Jacobians, as in the chapter text.

    The larger eigenvalue is taken directly; the smaller one follows from
    det = (-b)^N, which avoids the cancellation a plain eigensolver would
    suffer (the chapter avoids this with 800-digit arithmetic).
    """
    x = np.array(x0, dtype=float)
    lam1, lam2 = np.zeros(P), np.zeros(P)
    for p in range(P):
        C = np.eye(2)
        for _ in range(N):
            C = henon_jac(x) @ C
            x = cb.henon(x, a=a, b=b)
        big = np.max(np.abs(np.linalg.eigvals(C)))
        lbig = np.log(big)
        lsmall = N * np.log(b) - lbig
        lam1[p], lam2[p] = lsmall / N, lbig / N
    return lam1, lam2


runs = [(1, 4000, "0.7", 1.0, "-"), (10, 400, "0.3", 2.0, "-"),
        (200, 20, "0.0", 2.0, "-o")]
plt.figure(figsize=(5.0, 3.5))
means = {}
for N, P, grey, lw, style in runs:
    l1, l2 = block_exponents(N, P)
    means[N] = (l1.mean(), l2.mean())
    t = (np.arange(1, P + 1) - 0.5) * N
    for lam in (l1, l2):
        plt.plot(t, lam, style, color=grey, lw=lw, markersize=5)
plt.xlim(0, 4000)
plt.ylim(-2.6, 1.6)
plt.xlabel("$n$")
plt.ylabel(r"$\Lambda$")
plt.tight_layout()
plt.savefig(OUT / "disc2d_HenonLyap.png", dpi=150)
plt.close()
for N, (m1, m2) in means.items():
    print(f"block average, N={N}: Lambda_1 = {m1:.6f}, Lambda_2 = {m2:.6f}")
spec = cb.lyapunov_spectrum(cb.henon, henon_jac, (0.1, 0.3), n=200000,
                            nskip=1000, a=a, b=b)
print("cb.lyapunov_spectrum (QR, n=2e5): Lambda_2, Lambda_1 =", spec,
      " sum =", spec.sum(), " ln b =", np.log(b))


# -- ensembles: evolve many initial conditions, dropping those that escape -----
def evolve(P0, nsteps, crit=2.0):
    """Array (nsteps+1, npts, 2); points with |x| > crit become NaN from then on."""
    S = np.full((nsteps + 1,) + P0.shape, np.nan)
    S[0] = P0
    for n in range(nsteps):
        x, y = S[n, :, 0], S[n, :, 1]
        with np.errstate(invalid="ignore", over="ignore"):
            nx, ny = y + 1 - a * x**2, b * x
        nx = np.where(np.abs(nx) > crit, np.nan, nx)
        S[n + 1] = np.stack([nx, ny], axis=1)
        S[n + 1, np.isnan(nx)] = np.nan
    return S


NPTS = 10000
fold0 = np.column_stack([rng.uniform(-1.23, 1.23, NPTS),
                         rng.uniform(-0.41, 0.41, NPTS)])
stretch0 = np.column_stack([rng.uniform(1.01, 1.03, NPTS),
                            rng.uniform(0.30, 0.32, NPTS)])
FOLD = evolve(fold0, 12)
STRETCH = evolve(stretch0, 20)


def snapshot(P, n, name):
    plt.figure(figsize=(4.2, 4.2))
    plt.plot(P[:, 0], P[:, 1], "k.", markersize=1)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-0.5, 0.5)
    plt.title(f"$n={n}$")
    plt.xlabel("$x_n$")
    plt.ylabel("$y_n$")
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=150)
    plt.close()


for n in range(6):
    snapshot(FOLD[n], n, f"disc2d_HenonFold{n}.png")
for n in range(0, 21, 4):
    snapshot(STRETCH[n], n, f"disc2d_HenonStretch{n}.png")
print("survivors of fold after 5 steps:", int(np.sum(~np.isnan(FOLD[5, :, 0]))),
      "of", NPTS)

# -- interactive companion: play-button animation of the folding ---------------
alive = ~np.isnan(FOLD[-1, :, 0])
idx = np.flatnonzero(alive)[:6000]
frames_data = [np.round(FOLD[n][idx], 4) for n in range(13)]


def trace(P):
    return go.Scattergl(x=P[:, 0], y=P[:, 1], mode="markers",
                        marker=dict(size=2, color="black"))


fig = go.Figure(
    data=[trace(frames_data[0])],
    frames=[go.Frame(data=[trace(P)], name=str(n),
                     layout=go.Layout(title_text=f"n = {n}"))
            for n, P in enumerate(frames_data)],
)
fig.update_layout(
    title_text="n = 0",
    xaxis=dict(range=[-1.5, 1.5], title="xₙ"),
    yaxis=dict(range=[-0.5, 0.5], title="yₙ", scaleanchor=None),
    margin=dict(l=50, r=10, t=40, b=90),
    updatemenus=[dict(
        type="buttons", direction="left", x=0.0, y=-0.15, showactive=False,
        buttons=[
            dict(label="Play", method="animate",
                 args=[None, dict(frame=dict(duration=700, redraw=True),
                                  fromcurrent=True, transition=dict(duration=0))]),
            dict(label="Pause", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode="immediate", transition=dict(duration=0))]),
        ])],
    sliders=[dict(
        active=0, x=0.25, len=0.75, y=-0.1, pad=dict(t=10),
        font=dict(color="#333333"),
        currentvalue=dict(prefix="n = "),
        steps=[dict(label=str(n), method="animate",
                    args=[[str(n)], dict(mode="immediate",
                                         frame=dict(duration=0, redraw=True),
                                         transition=dict(duration=0))])
               for n in range(13)])],
)
target = OUT / "interactive" / "henon_fold.html"
fig.write_html(target, include_plotlyjs="../../plotly.min.js", full_html=True,
               auto_play=False)
print("companion size: %.2f MB" % (target.stat().st_size / 1e6))
print("fig_henon: assets written to", OUT)
