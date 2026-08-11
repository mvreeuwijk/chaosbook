"""Lyapunov-exponent figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_logist_lyap_r39_lin.png     two series, eps=1e-9, linear scale
  disc1d_logist_lyap_r39_log.png     ln|y-x| with slope-0.6 guide line
  disc1d_logist_lyap_bifurcation.png bifurcation diagram + Lambda(r)
  interactive/lyapunov_link.html     linked bifurcation/Lambda slider view
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)


def dlogistic(x, r):
    return r * (1 - 2 * x)


# -- two series at r=3.9, eps = 1e-9 -----------------------------------------
N, eps = 60, 1e-9
X = cb.orbit(cb.logistic, x0=0.1, n=N, r=3.9)
Y = cb.orbit(cb.logistic, x0=0.1 + eps, n=N, r=3.9)
plt.figure(figsize=(6.4, 3.2))
plt.plot(range(N + 1), X, "-o", markersize=3, label="x")
plt.plot(range(N + 1), Y, "-s", markersize=3, label="y")
plt.xlabel("n")
plt.ylabel("x, y")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_r39_lin.png", dpi=150)
plt.close()

plt.figure(figsize=(5.4, 3.4))
plt.plot(range(N + 1), np.log(np.abs(Y - X)), "o", markersize=3)
n = np.arange(0, 36)
plt.plot(n, np.log(eps) + 0.6 * n, "k--")
plt.xlabel("n")
plt.ylabel("ln|y[n]-x[n]|")
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_r39_log.png", dpi=150)
plt.close()

# -- combined bifurcation + Lambda(r) ----------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6),
                               sharex=True, height_ratios=[2, 1])
cb.bifurcation_diagram(cb.logistic, 2.5, 4.0, nr=800, n=1000,
                       x0=0.57, discard=0.8, ax=ax1)
rs, lams = cb.lyapunov_sweep(cb.logistic, dlogistic, 2.5, 4.0, nr=800)
ax2.plot(rs, lams, "k", linewidth=0.7)
ax2.axhline(0, color="gray", linewidth=0.8)
ax2.set_xlabel("r")
ax2.set_ylabel("Lambda(r)")
ax2.set_ylim(-2.5, 1)
ax1.set_xlim(2.5, 4)
plt.tight_layout()
plt.savefig(OUT / "disc1d_logist_lyap_bifurcation.png", dpi=150)
plt.close()

# -- interactive: bifurcation + Lambda(r) with a linked r-cursor -------------
rs_b, xs_b = [], []
for r in np.linspace(2.5, 4.0, 1001):
    X = cb.orbit(cb.logistic, x0=0.57, n=1000, r=r)
    rs_b.extend([r] * 100)
    xs_b.extend(X[-100:])
rs_l, lams_l = cb.lyapunov_sweep(cb.logistic, dlogistic, 2.5, 4.0, nr=1000)

rcursor = np.round(np.arange(2.5, 4.0001, 0.05), 3)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.65, 0.35],
                    vertical_spacing=0.05)
fig.add_trace(go.Scattergl(x=rs_b, y=xs_b, mode="markers",
                           marker=dict(size=1, color="darkblue")), row=1, col=1)
fig.add_trace(go.Scatter(x=rs_l, y=np.clip(lams_l, -3, None), mode="lines",
                         line=dict(color="black", width=1)), row=2, col=1)
fig.add_trace(go.Scatter(x=[3.0, 3.0], y=[0, 1], mode="lines",
                         line=dict(color="crimson", width=1.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=[3.0, 3.0], y=[-3, 1], mode="lines",
                         line=dict(color="crimson", width=1.5)), row=2, col=1)
frames = []
for r in rcursor:
    lam = np.interp(r, rs_l, np.clip(lams_l, -3, None))
    frames.append(go.Frame(name=f"{r}", traces=[2, 3], data=[
        go.Scatter(x=[r, r], y=[0, 1]),
        go.Scatter(x=[r, r], y=[-3, 1]),
    ], layout=dict(title=f"r = {r:.2f},  Lambda = {lam:+.3f}")))
fig.frames = frames
fig.update_layout(
    showlegend=False, margin=dict(l=50, r=10, t=40, b=40),
    yaxis_title="x(r)", yaxis2_title="Lambda(r)", xaxis2_title="r",
    sliders=[dict(
        currentvalue=dict(prefix="r = "),
        steps=[dict(label=f"{r}", method="animate",
                    args=[[f"{r}"], dict(mode="immediate",
                                         frame=dict(duration=0, redraw=True))])
               for r in rcursor],
    )],
)
fig.write_html(OUT / "interactive" / "lyapunov_link.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

print("fig_lyapunov: assets written to", OUT)
