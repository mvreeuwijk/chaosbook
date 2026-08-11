"""Figures for the three-body section of "A start at the end".

Produces (in python/_static/phenomenon/):
  phenomenon_3body_example{1a,1b,2a,2b,3a,3b}.png   trajectories for
      x0/R = 0.3, 0.5, 0.56 in the inertial (a) and co-rotating (b) frames
  phenomenon_3body_example_sensitivity.png          two nearby trajectories
  interactive/threebody.html                        chaotic orbit animation
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

import chaosbook as cb

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


def draw(ax, xs, ys, xe, ye, xm, ym):
    ax.plot(xe, ye, "k", linewidth=2.5)          # earth: thick black
    ax.plot(xm, ym, color="gray", linewidth=1.5)  # moon: gray
    ax.plot(xs, ys, "k", linewidth=0.6)           # satellite: thin black
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")


for i, x0_over_R in enumerate([0.3, 0.5, 0.56], start=1):
    sol = run(x0_over_R * R)
    x1, y1, x2, y2 = primaries(sol.t)
    # (a) inertial frame
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw(ax, sol.y[0], sol.y[1], x1, y1, x2, y2)
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_3body_example{i}a.png", dpi=150)
    plt.close()
    # (b) co-rotating frame
    xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
    x1r, y1r = cb.corotating(x1, y1, sol.t, omega)
    x2r, y2r = cb.corotating(x2, y2, sol.t, omega)
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    draw(ax, xs, ys, x1r, y1r, x2r, y2r)
    plt.tight_layout()
    plt.savefig(OUT / f"phenomenon_3body_example{i}b.png", dpi=150)
    plt.close()

# -- sensitivity: relative difference 1e-4 in x(0), two panels ---------------
sola = run(0.5 * R)
solb = run(0.5 * R * (1 + 1e-4))
x1, y1, x2, y2 = primaries(sola.t)
fig, axes = plt.subplots(2, 1, figsize=(4.8, 8.6))
for ax, rotate in zip(axes, [False, True]):
    for sol, color in [(sola, "b"), (solb, "r")]:
        xs, ys = sol.y[0], sol.y[1]
        if rotate:
            xs, ys = cb.corotating(xs, ys, sol.t, omega)
        ax.plot(xs, ys, color, linewidth=0.6)
        ax.plot(xs[0], ys[0], color + "d")   # diamond: initial location
        ax.plot(xs[-1], ys[-1], color + "o")  # circle: end position
    xe, ye = (cb.corotating(x1, y1, sola.t, omega) if rotate else (x1, y1))
    xm, ym = (cb.corotating(x2, y2, sola.t, omega) if rotate else (x2, y2))
    ax.plot(xe, ye, "k", linewidth=2.5)
    ax.plot(xm, ym, color="gray", linewidth=1.5)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(OUT / "phenomenon_3body_example_sensitivity.png", dpi=150)
plt.close()

# -- interactive: chaotic orbit in the co-rotating frame ---------------------
sol = run(0.5 * R)
xs, ys = cb.corotating(sol.y[0], sol.y[1], sol.t, omega)
xe = -m2 * R / (m1 + m2)
xm = m1 * R / (m1 + m2)
steps = np.linspace(2, len(sol.t) - 1, 80).astype(int)
frames = [go.Frame(data=[
    go.Scatter(x=xs[:k], y=ys[:k], mode="lines",
               line=dict(color="black", width=1)),
    go.Scatter(x=[xs[k]], y=[ys[k]], mode="markers",
               marker=dict(color="red", size=8)),
]) for k in steps]
fig = go.Figure(data=frames[0].data, frames=frames)
fig.add_trace(go.Scatter(x=[xe], y=[xm * 0], mode="markers+text",
                         marker=dict(color="blue", size=14), text=["earth"],
                         textposition="bottom center"))
fig.add_trace(go.Scatter(x=[xm], y=[0], mode="markers+text",
                         marker=dict(color="gray", size=9), text=["moon"],
                         textposition="bottom center"))
fig.update_layout(
    xaxis=dict(title="x [m]", scaleanchor="y"),
    yaxis=dict(title="y [m]"),
    showlegend=False, margin=dict(l=40, r=10, t=10, b=40),
    updatemenus=[dict(type="buttons", x=1, y=1.15, xanchor="right",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=40,
                                                                redraw=False),
                                                     fromcurrent=True)])])],
)
fig.write_html(OUT / "interactive" / "threebody.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_3body: all assets written to", OUT)
