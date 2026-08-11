"""Figures for the Lorenz section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_lorenz_xt_series.png          time series x(t)
  phenomenon_lorenz_xt_two_series_em3.png  sensitivity, epsilon = 1e-3
  phenomenon_lorenz_xt_two_series_em5.png  sensitivity, epsilon = 1e-5
  phenomenon_lorenz_phasespace_close.png   the butterfly attractor
  phenomenon_lorenz_phasespace_far.png     convergence onto the attractor
  interactive/lorenz3d.html                rotatable 3D attractor
  interactive/lorenz_sensitivity.html      divergence animation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "phenomenon"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def run(ic, tend, n=6000):
    return solve_ivp(cb.lorenz, [0, tend], ic,
                     t_eval=np.linspace(0, tend, n), rtol=1e-9)


# -- time series ------------------------------------------------------------
sol1 = run([2, 5, 5], 30)
plt.figure(figsize=(8, 3))
plt.plot(sol1.t, sol1.y[0], "b", linewidth=1)
plt.xlabel("t")
plt.ylabel("x")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_xt_series.png", dpi=150)
plt.close()

# -- sensitive dependence, epsilon = 1e-3 and 1e-5 --------------------------
for eps, name in [(1e-3, "em3"), (1e-5, "em5")]:
    sol2 = run([2 + eps, 5, 5], 30)
    plt.figure(figsize=(5, 3.2))
    plt.plot(sol1.t, sol1.y[0], "b", linewidth=1)
    plt.plot(sol2.t, sol2.y[0], "r", linewidth=1)
    plt.xlabel("t")
    plt.ylabel("x")
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_lorenz_xt_two_series_{name}.png", dpi=150)
    plt.close()

# -- phase space: the butterfly, and convergence onto it --------------------
solb = run([2, 5, 5], 40, n=12000)
ax = plt.figure(figsize=(5, 4)).add_subplot(projection="3d")
ax.plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_phasespace_close.png", dpi=150)
plt.close()

solf = run([100, 5, 5], 40, n=12000)
ax = plt.figure(figsize=(5, 4)).add_subplot(projection="3d")
ax.plot(solb.y[0], solb.y[1], solb.y[2], "b", linewidth=0.4)
ax.plot(solf.y[0], solf.y[1], solf.y[2], "r", linewidth=0.6)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_lorenz_phasespace_far.png", dpi=150)
plt.close()

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
