"""Figures for the Lorenz section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_lorenz_xt_series.png          time series x(t)
  phenomenon_lorenz_xt_two_series.png      sensitivity, (a) epsilon = 1e-3,
                                           (b) epsilon = 1e-5
  phenomenon_lorenz_phasespace.png         (a) the butterfly attractor,
                                           (b) convergence onto it
  interactive/lorenz3d.html                rotatable 3D attractor
  interactive/lorenz_sensitivity.html      divergence animation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, panel labels, save)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "phenomenon"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def run(ic, tend, n=6000):
    return solve_ivp(cb.lorenz, [0, tend], ic,
                     t_eval=np.linspace(0, tend, n), rtol=1e-9)


# -- time series ------------------------------------------------------------
sol1 = run([2, 5, 5], 30)
fig, ax = plt.subplots(figsize=(bf.FULL_W, 2.4))
ax.plot(sol1.t, sol1.y[0], "b")
ax.set_xlabel("$t$")
ax.set_ylabel("$x$")
bf.save(fig, OUT / "phenomenon_lorenz_xt_series.png")

# -- sensitive dependence, epsilon = 1e-3 (a) and 1e-5 (b), one figure ------
fig, axs = plt.subplots(2, 1, figsize=(bf.FULL_W, 3.2), sharex=True)
for ax, eps in zip(axs, [1e-3, 1e-5]):
    sol2 = run([2 + eps, 5, 5], 30)
    ax.plot(sol1.t, sol1.y[0], "b")
    ax.plot(sol2.t, sol2.y[0], "r")
    ax.set_ylabel("$x$")
axs[-1].set_xlabel("$t$")
bf.panel_labels(axs, ha="left", pad=(0.0, 0.03))
bf.save(fig, OUT / "phenomenon_lorenz_xt_two_series.png")

# -- phase space: the butterfly (a), and convergence onto it (b) -------------
solb = run([2, 5, 5], 40, n=12000)
solf = run([100, 5, 5], 40, n=12000)
fig = plt.figure(figsize=(bf.FULL_W, 3.0))
axs = [fig.add_subplot(1, 2, k + 1, projection="3d") for k in range(2)]
axs[0].plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
axs[1].plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
axs[1].plot(solf.y[0], solf.y[1], solf.y[2], "r", linewidth=0.6)
for ax in axs:
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_box_aspect(None, zoom=0.78)   # keep the axis labels inside
for ax, lab in zip(axs, "ab"):      # 3-D axes: text2D, not text
    ax.text2D(0.02, 0.92, f"({lab})", transform=ax.transAxes,
              fontsize=plt.rcParams["axes.labelsize"])
bf.save(fig, OUT / "phenomenon_lorenz_phasespace.png")

# -- interactive: rotatable attractor ---------------------------------------
fig = go.Figure(go.Scatter3d(
    x=solb.y[0], y=solb.y[1], z=solb.y[2], mode="lines",
    line=dict(width=2, color=solb.t, colorscale="Viridis"),
))
fig.update_layout(
    scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
    margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
)
fig.write_html(OUT / "interactive" / "lorenz3d.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

# -- interactive: divergence animation --------------------------------------
sol2 = run([2 + 1e-3, 5, 5], 30)
steps = np.linspace(2, len(sol1.t) - 1, 60).astype(int)
frames = [go.Frame(data=[
    go.Scatter(x=sol1.t[:k], y=sol1.y[0][:k], mode="lines",
               line=dict(color="blue")),
    go.Scatter(x=sol2.t[:k], y=sol2.y[0][:k], mode="lines",
               line=dict(color="red")),
]) for k in steps]
fig = go.Figure(data=frames[0].data, frames=frames)
fig.update_layout(
    xaxis=dict(range=[0, 30], title="t"),
    yaxis=dict(range=[-25, 25], title="x"),
    showlegend=False, margin=dict(l=40, r=10, t=10, b=40),
    updatemenus=[dict(type="buttons", x=1, y=1.15, xanchor="right",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=50,
                                                                redraw=False),
                                                     fromcurrent=True)])])],
)
fig.write_html(OUT / "interactive" / "lorenz_sensitivity.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_lorenz: all assets written to", OUT)
