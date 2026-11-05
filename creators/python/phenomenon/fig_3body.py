"""Figures for the three-body section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_3body_examples.png   2 x 3: columns x0/R = 0.3, 0.5, 0.56; top
      row the inertial frame, bottom row the co-rotating frame
  phenomenon_3body_example_sensitivity.png   two nearby trajectories,
      (a) inertial, (b) co-rotating frame
  interactive/threebody.html                        chaotic orbit animation
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

G, m1, R = 6.67e-11, 5.97e24, 3.84e8
m2 = m1 / 4
omega = np.sqrt(G * (m1 + m2) / R**3)
TWO_MONTHS = 60 * 24 * 3600


def run(x0, tend=TWO_MONTHS, n=8000):
    return solve_ivp(cb.threebody, [0, tend], [x0, 0, 0, 0],
                     t_eval=np.linspace(0, tend, n), rtol=1e-10, atol=1.0)


def primaries(t):
    x1 = -m2 * R / (m1 + m2) * np.cos(omega * t)
    y1 = -m2 * R / (m1 + m2) * np.sin(omega * t)
    x2 = m1 * R / (m1 + m2) * np.cos(omega * t)
    y2 = m1 * R / (m1 + m2) * np.sin(omega * t)
    return x1, y1, x2, y2


def draw(ax, xs, ys, xe, ye, xm, ym, rotating=False):
    # plot in units of the earth-moon distance R, as the captions quote x(0)/R
    xs, ys, xe, ye, xm, ym = (np.asarray(a) / R for a in (xs, ys, xe, ye, xm, ym))
    if rotating:
        # the primaries are stationary in the co-rotating frame: draw points
        ax.plot(xe[0], ye[0], "ko", markersize=8)               # earth
        ax.plot(xm[0], ym[0], "o", color="gray", markersize=5)  # moon
    else:
        ax.plot(xe, ye, "k", linewidth=2.5)           # earth: thick black
        ax.plot(xm, ym, color="gray", linewidth=1.5)  # moon: gray
    ax.plot(xs, ys, "k", linewidth=0.6)               # satellite: thin black
    ax.set_xlabel("$x/R$")
    ax.set_ylabel("$y/R$")
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_box_aspect(1)   # square panels, so every row has equal heights


# 2 x 3 grid: columns = x(0)/R = 0.3, 0.5, 0.56; top row inertial frame,
# bottom row co-rotating frame. Caption letters run down the columns.
fig, axs = plt.subplots(2, 3, figsize=(bf.FULL_W, 4.3))
for i, x0_over_R in enumerate([0.3, 0.5, 0.56]):
    sol = run(x0_over_R * R)
    x1, y1, x2, y2 = primaries(sol.t)
    draw(axs[0, i], sol.y[0], sol.y[1], x1, y1, x2, y2)
    xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
    x1r, y1r = cb.corotating(x1, y1, sol.t, omega)
    x2r, y2r = cb.corotating(x2, y2, sol.t, omega)
    draw(axs[1, i], xs, ys, x1r, y1r, x2r, y2r, rotating=True)
bf.panel_labels(axs, order="col")
bf.save(fig, OUT / "phenomenon_3body_examples.png")

# -- sensitivity: relative difference 1e-4 in x(0), (a) inertial, (b) co-rotating
sola = run(0.5 * R)
solb = run(0.5 * R * (1 + 1e-4))
x1, y1, x2, y2 = primaries(sola.t)
fig, axes = plt.subplots(1, 2, figsize=(bf.FULL_W, 3.2))
for ax, rotate in zip(axes, [False, True]):
    for sol, color in [(sola, "b"), (solb, "r")]:
        xs, ys = sol.y[0], sol.y[1]
        if rotate:
            xs, ys = cb.corotating(xs, ys, sol.t, omega)
        xs, ys = xs / R, ys / R
        ax.plot(xs, ys, color, linewidth=0.6)
        ax.plot(xs[0], ys[0], color + "d")   # diamond: initial location
        ax.plot(xs[-1], ys[-1], color + "o")  # circle: end position
    xe, ye = (cb.corotating(x1, y1, sola.t, omega) if rotate else (x1, y1))
    xm, ym = (cb.corotating(x2, y2, sola.t, omega) if rotate else (x2, y2))
    xe, ye, xm, ym = xe / R, ye / R, xm / R, ym / R
    if rotate:
        ax.plot(xe[0], ye[0], "ko", markersize=8)
        ax.plot(xm[0], ym[0], "o", color="gray", markersize=5)
    else:
        ax.plot(xe, ye, "k", linewidth=2.5)
        ax.plot(xm, ym, color="gray", linewidth=1.5)
    ax.set_xlabel("$x/R$")
    ax.set_ylabel("$y/R$")
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_box_aspect(1)   # square panels, so every row has equal heights
bf.panel_labels(axes)
bf.save(fig, OUT / "phenomenon_3body_example_sensitivity.png")

# -- interactive: chaotic orbit in the co-rotating frame ---------------------
sol = run(0.5 * R)
xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
xs, ys = xs / R, ys / R
xe = -m2 / (m1 + m2)
xm = m1 / (m1 + m2)
steps = np.linspace(2, len(sol.t) - 1, 80).astype(int)
frames = [go.Frame(data=[
    go.Scatter(x=xs[:k], y=ys[:k], mode="lines",
               line=dict(color="black", width=1)),
    go.Scatter(x=[xs[k]], y=[ys[k]], mode="markers",
               marker=dict(color="red", size=8)),
]) for k in steps]
fig = go.Figure(data=frames[0].data, frames=frames)
fig.add_trace(go.Scatter(x=[xe], y=[0], mode="markers+text",
                         marker=dict(color="blue", size=14), text=["earth"],
                         textposition="bottom center"))
fig.add_trace(go.Scatter(x=[xm], y=[0], mode="markers+text",
                         marker=dict(color="gray", size=9), text=["moon"],
                         textposition="bottom center"))
fig.update_layout(
    xaxis=dict(title="x/R", scaleanchor="y"),
    yaxis=dict(title="y/R"),
    showlegend=False, margin=dict(l=40, r=10, t=10, b=40),
    updatemenus=[dict(type="buttons", x=1, y=1.15, xanchor="right",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=40,
                                                                redraw=False),
                                                     fromcurrent=True)])])],
)
fig.write_html(OUT / "interactive" / "threebody.html",
               include_plotlyjs="../../plotly.min.js", full_html=True,
               auto_play=False)

print("fig_3body: all assets written to", OUT)
