"""Series, cobweb and return-plot figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_series_r{1_5,3_2,3_5,3_9}.png
  disc1d_logist_cobweb_r{2_7,3_2,3_9}.png
  disc1d_logist_return_r{1_5,3_2,3_5,3_9}.png
  disc1d_unknownmapping_{series,return}_{henon,noise,sin3map}.png
  interactive/logistic_explorer.html
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def tag(r):
    return str(r).replace(".", "_")


# -- logistic time series ----------------------------------------------------
for r in [1.5, 3.2, 3.5, 3.9]:
    X = cb.orbit(cb.logistic, x0=0.1, n=30, r=r)
    plt.figure(figsize=(4.2, 3))
    plt.plot(range(len(X)), X, "o", markersize=4)
    plt.xlabel("n")
    plt.ylabel("xn")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_series_r{tag(r)}.png", dpi=150)
    plt.close()

# -- cobwebs -----------------------------------------------------------------
for r in [2.7, 3.2, 3.9]:
    fig, ax = plt.subplots(figsize=(4, 4))
    cb.cobweb(cb.logistic, x0=0.1, n=30, ax=ax, r=r)
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_cobweb_r{tag(r)}.png", dpi=150)
    plt.close()

# -- return plots (gray map line + points, transient dropped) ---------------
for r in [1.5, 3.2, 3.5, 3.9]:
    X = cb.orbit(cb.logistic, x0=0.1, n=200, r=r)
    xs = np.linspace(0, 1, 200)
    plt.figure(figsize=(4.2, 3.6))
    plt.plot(xs, cb.logistic(xs, r), color="gray")
    plt.plot(X[50:-1], X[51:], "ko", markersize=4)
    plt.xlabel("x[n]")
    plt.ylabel("x[n+1]")
    plt.axis([0, 1, 0, 1])
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_logist_return_r{tag(r)}.png", dpi=150)
    plt.close()

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

for name, data in [("henon", hx), ("noise", noise), ("sin3map", s3)]:
    plt.figure(figsize=(4.6, 2.6))
    plt.plot(range(len(data)), data, "k", linewidth=0.7)
    plt.xlabel("n")
    plt.ylabel("x[n]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_unknownmapping_series_{name}.png", dpi=150)
    plt.close()

    plt.figure(figsize=(3.4, 3.4))
    plt.plot(data[:-1], data[1:], "ko", markersize=3)
    plt.xlabel("x[n]")
    plt.ylabel("x[n+1]")
    plt.tight_layout()
    plt.savefig(OUT / f"disc1d_unknownmapping_return_{name}.png", dpi=150)
    plt.close()

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
                    subplot_titles=("series x[n]", "cobweb", "return plot"))
for tr, (row, col) in zip(frames[0].data,
                          [(1, 1), (1, 2), (1, 2), (1, 2), (1, 3)]):
    fig.add_trace(tr, row=row, col=col)
# route every frame's traces to the same subplots as the initial data
for fr in frames:
    fr.traces = [0, 1, 2, 3, 4]
fig.frames = frames
fig.update_layout(
    showlegend=False, margin=dict(l=40, r=10, t=40, b=40),
    sliders=[dict(
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
fig.write_html(OUT / "interactive" / "logistic_explorer.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_series_cobweb_return: assets written to", OUT)
