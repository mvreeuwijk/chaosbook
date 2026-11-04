"""Interactive companions for "Two-dimensional continuous systems".

Precomputed frames, one slider each (serverless), written to
python/_static/cont2d/interactive/:
  hopf_slider.html           Hopf normal form: phase plane and x(t) versus mu
  lotka_volterra_slider.html Lotka-Volterra: orbits, fixed point and time series versus alpha
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import solve_ivp

import chaosbook as cb

OUT = (Path(__file__).resolve().parents[3] / "python" / "_static" / "cont2d"
       / "interactive")
OUT.mkdir(parents=True, exist_ok=True)


def integrate(f, x0, tend, npts, **params):
    t = np.linspace(0, tend, npts)
    s = solve_ivp(lambda t, s: f(t, s, **params), [0, tend], x0, t_eval=t,
                  rtol=1e-9, atol=1e-12)
    return np.round(t, 3), np.round(s.y, 4)


def build(name, grid, make_frame, titles, layout_axes, prefix, fmt):
    frames = []
    for p in grid:
        data = make_frame(p)
        frames.append(go.Frame(name=fmt(p), data=data,
                               traces=list(range(len(data)))))
    fig = make_subplots(rows=1, cols=2, subplot_titles=titles)
    first = frames[0].data
    for k, tr in enumerate(first):
        fig.add_trace(tr, row=1, col=1 if tr.meta == "phase" else 2)
    fig.frames = frames
    fig.update_layout(
        showlegend=False, margin=dict(l=45, r=10, t=40, b=40),
        sliders=[dict(
            currentvalue=dict(prefix=prefix),
            steps=[dict(label=fmt(p), method="animate",
                        args=[[fmt(p)], dict(mode="immediate",
                                             frame=dict(duration=0, redraw=False))])
                   for p in grid])])
    layout_axes(fig)
    fig.write_html(OUT / name, include_plotlyjs="../../plotly.min.js",
                   full_html=True)
    print(name, (OUT / name).stat().st_size, "bytes")


# --- Hopf bifurcation ------------------------------------------------------------
mus = np.round(np.arange(-0.5, 0.5001, 0.025), 3)
th = np.linspace(0, 2 * np.pi, 200)


def hopf_frame(mu):
    out = []
    for x0, col in [([0.15, 0.0], "crimson"), ([0.6, 0.0], "steelblue")]:
        t, y = integrate(cb.hopf, x0, 80, 450, mu=mu)
        out.append(go.Scatter(x=y[0], y=y[1], mode="lines", meta="phase",
                              line=dict(color=col, width=1.5)))
    for x0, col in [([0.15, 0.0], "crimson"), ([0.6, 0.0], "steelblue")]:
        t, y = integrate(cb.hopf, x0, 80, 450, mu=mu)
        out.append(go.Scatter(x=t, y=y[0], mode="lines", meta="time",
                              line=dict(color=col, width=1.5)))
    r = np.sqrt(mu) if mu > 0 else 0.0
    out.append(go.Scatter(x=r * np.cos(th), y=r * np.sin(th), mode="lines",
                          meta="phase", line=dict(color="black", dash="dot", width=1)))
    out.append(go.Scatter(x=[0], y=[0], mode="markers", meta="phase",
                          marker=dict(color="black", size=7,
                                      symbol="circle" if mu < 0 else "circle-open")))
    out.append(go.Scatter(x=[0, 80], y=[0, 0], mode="lines", meta="time",
                          line=dict(color="gray", width=0.5)))
    out.append(go.Scatter(x=[0], y=[0], mode="markers", meta="time",
                          marker=dict(size=0.1)))
    return out


def hopf_axes(fig):
    fig.update_xaxes(range=[-0.8, 0.8], title_text="x", row=1, col=1)
    fig.update_yaxes(range=[-0.8, 0.8], title_text="y", scaleanchor="x",
                     row=1, col=1)
    fig.update_xaxes(range=[0, 80], title_text="t", row=1, col=2)
    fig.update_yaxes(range=[-0.8, 0.8], title_text="x(t)", row=1, col=2)


build("hopf_slider.html", mus, hopf_frame,
      ("phase plane: Re(sigma) = mu, Im(sigma) = +-1", "x(t)"),
      hopf_axes, "mu = ", lambda m: f"{m:g}")


# --- Lotka-Volterra ---------------------------------------------------------------
alphas = np.round(np.arange(0.3, 1.5001, 0.05), 2)
ICS = [([0.25, 0.25], "crimson"), ([1.0, 0.5], "steelblue")]


def lv_frame(a):
    out = []
    for x0, col in ICS:
        t, y = integrate(cb.lotka_volterra, x0, 40, 600, alpha=a)
        out.append(go.Scatter(x=y[0], y=y[1], mode="lines", meta="phase",
                              line=dict(color=col, width=1.5)))
    t, y = integrate(cb.lotka_volterra, ICS[0][0], 40, 600, alpha=a)
    out.append(go.Scatter(x=t, y=y[0], mode="lines", meta="time",
                          line=dict(color="blue", width=1.5)))
    out.append(go.Scatter(x=t, y=y[1], mode="lines", meta="time",
                          line=dict(color="red", dash="dash", width=1.5)))
    out.append(go.Scatter(x=[a], y=[1], mode="markers", meta="phase",
                          marker=dict(color="black", size=8)))
    out.append(go.Scatter(x=[0], y=[0], mode="markers", meta="phase",
                          marker=dict(color="black", size=8, symbol="circle-open")))
    out.append(go.Scatter(x=[0], y=[0], mode="markers", meta="time",
                          marker=dict(size=0.1)))
    return out


def lv_axes(fig):
    fig.update_xaxes(range=[0, 6], title_text="x (prey)", row=1, col=1)
    fig.update_yaxes(range=[0, 6], title_text="y (predator)", row=1, col=1)
    fig.update_xaxes(range=[0, 40], title_text="t", row=1, col=2)
    fig.update_yaxes(range=[0, 6], title_text="x(t), y(t)", row=1, col=2)


build("lotka_volterra_slider.html", alphas, lv_frame,
      ("phase plane (fixed point at (alpha, 1))", "x(t) blue, y(t) red"),
      lv_axes, "alpha = ", lambda a: f"{a:g}")
