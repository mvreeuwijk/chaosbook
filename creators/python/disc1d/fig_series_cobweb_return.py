"""Series, cobweb and return-plot figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_series.png                2x2 series, r = 1.5, 3.2, 3.5, 3.9
  disc1d_logist_cobwebs.png               cobwebs, r = 2.7, 3.2, 3.9 (a)-(c)
  disc1d_logist_return.png                1x4 return plots
  disc1d_unknownmappings.png              2x3: series over return plots
  interactive/logistic_explorer.html
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def tag(r):
    return str(r).replace(".", "_")


# -- logistic time series: one 2x2 figure, (a) r = 1.5 ... (d) r = 3.9 -------
fig, axs = plt.subplots(2, 2, figsize=(bf.FULL_W, 4.0))
for ax, r in zip(axs.ravel(), [1.5, 3.2, 3.5, 3.9]):
    X = cb.orbit(cb.logistic, x0=0.1, n=30, r=r)
    ax.plot(range(len(X)), X, "o", markersize=4)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$x_n$")
    ax.set_ylim(0, 1)
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_logist_series.png")

# -- cobwebs: one figure, (a) r = 2.7, (b) r = 3.2, (c) r = 3.9 -------------
fig, axs = plt.subplots(1, 3, figsize=(bf.FULL_W, 2.25))
for ax, r in zip(axs, [2.7, 3.2, 3.9]):
    cb.cobweb(cb.logistic, x0=0.1, n=30, ax=ax, r=r)
    ax.set_aspect("equal")
    if r == 2.7:
        # the construction lines of the text: from every point on the diagonal
        # straight down to the x-axis, where the next iterate x_k is read off
        X = cb.orbit(cb.logistic, x0=0.1, n=30, r=r)
        for xk in X[1:6]:
            ax.plot([xk, xk], [0, xk], ":", color="0.4", lw=0.8)
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_logist_cobwebs.png")

# -- return plots (gray map line + points, transient dropped): 1x4 ---------
fig, axs = plt.subplots(1, 4, figsize=(bf.FULL_W, 1.8))
for ax, r in zip(axs, [1.5, 3.2, 3.5, 3.9]):
    X = cb.orbit(cb.logistic, x0=0.1, n=200, r=r)
    xs = np.linspace(0, 1, 200)
    ax.plot(xs, cb.logistic(xs, r), color="gray")
    ax.plot(X[50:-1], X[51:], "ko", markersize=3)
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")
    ax.axis([0, 1, 0, 1])
    ax.set_aspect("equal")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_logist_return.png")

# -- three unknown data sets: henon, noise, sin3 -----------------------------
rng = np.random.default_rng(seed=1)
N = 200

hx, hy = np.zeros(N + 1), np.zeros(N + 1)
hx[0], hy[0] = 0.1, 0.1
for n in range(N):
    hx[n + 1] = 1 - 1.4 * hx[n] ** 2 + hy[n]
    hy[n + 1] = 0.3 * hx[n]

noise = rng.uniform(-1, 1, N + 1)

s3 = np.zeros(N + 1)
s3[0] = 0.3
for n in range(N):
    s3[n + 1] = -4 * s3[n] ** 3 + 3 * s3[n]

# one 2x3 figure: top row the three series, bottom row the return plots,
# one column per data set
fig, axs = plt.subplots(2, 3, figsize=(bf.FULL_W, 4.0))
for j, data in enumerate([hx, noise, s3]):
    axs[0, j].plot(range(len(data)), data, "k", linewidth=0.7)
    axs[0, j].set_xlabel("$n$")
    axs[0, j].set_ylabel("$x_n$")
    axs[1, j].plot(data[:-1], data[1:], "ko", markersize=2)
    axs[1, j].set_xlabel("$x_n$")
    axs[1, j].set_ylabel("$x_{n+1}$")
bf.panel_labels(axs)
bf.save(fig, OUT / "disc1d_unknownmappings.png")

# -- interactive: logistic explorer (series + cobweb + return, r slider) -----
rgrid = np.round(np.arange(0.5, 4.0001, 0.1), 2)
frames = []
for r in rgrid:
    X = cb.orbit(cb.logistic, x0=0.1, n=100, r=r)
    xs = np.linspace(0, 1, 100)
    px, py = [X[0]], [0.0]
    for k in range(40):
        px += [X[k], X[k]]
        py += [X[k], X[k + 1]]
    frames.append(go.Frame(name=f"{r}", data=[
        go.Scatter(x=list(range(41)), y=X[:41], mode="lines+markers",
                   marker=dict(size=4), line=dict(color="steelblue")),
        go.Scatter(x=xs, y=cb.logistic(xs, r), mode="lines",
                   line=dict(color="black")),
        go.Scatter(x=xs, y=xs, mode="lines", line=dict(color="royalblue")),
        go.Scatter(x=px, y=py, mode="lines",
                   line=dict(color="crimson", width=1)),
        go.Scatter(x=X[50:-1], y=X[51:], mode="markers",
                   marker=dict(color="crimson", size=4)),
    ]))
fig = make_subplots(rows=1, cols=3,
                    subplot_titles=("series xₙ", "cobweb", "return plot"))
for tr, (row, col) in zip(frames[0].data,
                          [(1, 1), (1, 2), (1, 2), (1, 2), (1, 3)]):
    fig.add_trace(tr, row=row, col=col)
# route every frame's traces to the same subplots as the initial data
for fr in frames:
    fr.traces = [0, 1, 2, 3, 4]
fig.frames = frames
fig.update_layout(
    showlegend=False, margin=dict(l=50, r=10, t=40, b=40),
    sliders=[dict(
        pad=dict(t=60), font=dict(color="#333333"),
        currentvalue=dict(prefix="r = "),
        steps=[dict(label=f"{r}", method="animate",
                    args=[[f"{r}"], dict(mode="immediate",
                                         frame=dict(duration=0, redraw=False))])
               for r in rgrid],
    )],
)
fig.update_yaxes(range=[0, 1])
fig.update_xaxes(range=[0, 1], row=1, col=2)
fig.update_xaxes(range=[0, 1], row=1, col=3)
fig.update_xaxes(title_text="n", row=1, col=1)
fig.update_yaxes(title_text="xₙ", row=1, col=1)
fig.update_xaxes(title_text="xₙ", row=1, col=2)
fig.update_yaxes(title_text="xₙ₊₁", row=1, col=2)
fig.update_xaxes(title_text="xₙ", row=1, col=3)
fig.update_yaxes(title_text="xₙ₊₁", row=1, col=3)
fig.write_html(OUT / "interactive" / "logistic_explorer.html",
               include_plotlyjs="../../plotly.min.js", full_html=True,
               auto_play=False)

print("fig_series_cobweb_return: assets written to", OUT)
