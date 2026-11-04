"""Interactive companions for the continuous-systems chapter (plotly, precomputed frames).

Produces (in python/_static/cont1d/interactive/):
  normal_forms.html   r-slider for the pitchfork, subcritical pitchfork, saddle-node
                      and transcritical normal forms: f(x) with its fixed points
                      (filled = stable, open = unstable, dotted = marginal) above
                      the bifurcation diagram with a marker at the current r.
  ferro_temperature.html   T-slider for the ferromagnet, m = 0 and m = 0.1 side by side.
  hysteresis_sweep.html    slider along a forward-then-backward sweep of the field m
                           at T = 0.5 (hysteresis) and T = 1.5 (none).
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb
from _common import OUT, dferro, ferro

HTML = OUT / "interactive"
GRAY = "#b3b3b3"
BLACK = "#111111"
RED = "#c0392b"


def write(fig, name, height):
    fig.update_layout(height=height, margin=dict(l=55, r=10, t=40, b=40),
                      showlegend=False, template="simple_white")
    fig.write_html(HTML / name, include_plotlyjs="../../plotly.min.js", full_html=True)
    print(f"{name}: {(HTML / name).stat().st_size / 1e3:.0f} kB")


def add_slider(fig, names, labels, prefix):
    fig.update_layout(sliders=[dict(
        active=0, x=0.05, len=0.9, y=-0.02,
        currentvalue=dict(prefix=prefix, font=dict(size=14)),
        pad=dict(t=30, b=0),
        steps=[dict(method="animate", label=lab,
                    args=[[nm], dict(mode="immediate", frame=dict(duration=0, redraw=True),
                                     transition=dict(duration=0))])
               for nm, lab in zip(names, labels)])])


def fixed_point_sets(f, df, xlo, xhi, params):
    """Return (stable, unstable, marginal) x-arrays for the given parameters."""
    xs = cb.fixed_points(f, xlo, xhi, n=3001, **params)
    kinds = np.array(cb.classify(cb.stability(f, xs, dfdx=df, **params), tol=1e-6))
    return xs[kinds == "stable"], xs[kinds == "unstable"], xs[kinds == "marginal"]


def marker(symbol, size=13):
    return dict(symbol=symbol, size=size, color=BLACK, line=dict(color=BLACK, width=2))


def add_branches(fig, segs, row, col, width=4):
    for p, x, stable in segs:
        fig.add_trace(go.Scatter(x=p, y=x, mode="lines",
                                 line=dict(color=BLACK if stable else GRAY, width=width)),
                      row=row, col=col)


def rd(d):
    return {k: np.round(np.asarray(v, dtype=float), 4).tolist() for k, v in d.items()}


def zeros(a):
    return np.zeros(len(a))


# =========================================================================== 1
SYSTEMS = [
    ("pitchfork: x' = rx - x^3", lambda x, r: r * x - x**3,
     lambda x, r: r - 3 * x**2, (-2, 2)),
    ("subcritical: x' = rx + x^3", lambda x, r: r * x + x**3,
     lambda x, r: r + 3 * x**2, (-2, 2)),
    ("saddle-node: x' = r - x^2", lambda x, r: r - x**2,
     lambda x, r: -2 * x, (-3.5, 2)),
    ("transcritical: x' = rx - x^2", lambda x, r: r * x - x**2,
     lambda x, r: r - 2 * x, (-4, 2)),
]
XL = 1.5
rs = np.round(np.linspace(-1.5, 1.5, 61), 3)
xg = np.linspace(-XL, XL, 121)


def nf_column(c, r):
    _, f, df, _ = SYSTEMS[c]
    st, un, ma = fixed_point_sets(f, df, -XL, XL, dict(r=r))
    return [dict(x=xg, y=f(xg, r)),
            dict(x=st, y=zeros(st)), dict(x=un, y=zeros(un)), dict(x=ma, y=zeros(ma)),
            dict(x=[r, r], y=[-XL, XL])]


fig = make_subplots(rows=2, cols=4, subplot_titles=[s[0] for s in SYSTEMS] + [""] * 4,
                    vertical_spacing=0.14, horizontal_spacing=0.05)
for c, (_, f, df, _) in enumerate(SYSTEMS, start=1):
    add_branches(fig, cb.fixed_point_branches(f, "r", -XL, XL, -XL, XL,
                                              shape=(300, 300), dfdx=df), 2, c)
n_static = len(fig.data)
for c in range(4):
    d0 = nf_column(c, rs[0])
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=BLACK, width=3), **d0[0]),
                  row=1, col=c + 1)
    for d, sym in zip(d0[1:4], ("circle", "circle-open", "circle-open-dot")):
        fig.add_trace(go.Scatter(mode="markers", marker=marker(sym), **d),
                      row=1, col=c + 1)
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=RED, width=2, dash="dot"),
                             **d0[4]), row=2, col=c + 1)
    fig.update_xaxes(range=[-XL, XL], zeroline=True, row=1, col=c + 1, title_text="x")
    fig.update_yaxes(range=list(SYSTEMS[c][3]), zeroline=True, row=1, col=c + 1,
                     title_text="f(x)" if c == 0 else "")
    fig.update_xaxes(range=[-XL, XL], zeroline=True, row=2, col=c + 1, title_text="r")
    fig.update_yaxes(range=[-XL, XL], zeroline=True, row=2, col=c + 1,
                     title_text="x*(r)" if c == 0 else "")
frames = []
for r in rs:
    data, idx = [], []
    for c in range(4):
        for k, d in enumerate(nf_column(c, r)):
            data.append(go.Scatter(**rd(d)))
            idx.append(n_static + 5 * c + k)
    frames.append(go.Frame(data=data, traces=idx, name=f"{r:g}"))
fig.frames = frames
add_slider(fig, [fr.name for fr in frames], [fr.name for fr in frames], "r = ")
write(fig, "normal_forms.html", 560)

# =========================================================================== 2
Ts = np.round(np.linspace(0.2, 2.0, 55), 3)
FM = (0.0, 0.1)
xg = np.linspace(-1.2, 1.2, 121)


def ferro_col(m, T):
    st, un, ma = fixed_point_sets(ferro, dferro, -1.2, 1.2, dict(T=T, m=m))
    return [dict(x=xg, y=ferro(xg, T=T, m=m)),
            dict(x=st, y=zeros(st)), dict(x=un, y=zeros(un)), dict(x=ma, y=zeros(ma)),
            dict(x=[T, T], y=[-1.1, 1.1])]


fig = make_subplots(rows=2, cols=2, vertical_spacing=0.16, horizontal_spacing=0.09,
                    subplot_titles=[f"m = {m:g}" for m in FM] + [""] * 2)
for c, m in enumerate(FM, start=1):
    add_branches(fig, cb.fixed_point_branches(ferro, "T", 0.02, 2.0, -1.1, 1.1,
                                              shape=(350, 350), dfdx=dferro, m=m), 2, c)
n_static = len(fig.data)
for c, m in enumerate(FM, start=1):
    d0 = ferro_col(m, Ts[0])
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=BLACK, width=3), **d0[0]),
                  row=1, col=c)
    for d, sym in zip(d0[1:4], ("circle", "circle-open", "circle-open-dot")):
        fig.add_trace(go.Scatter(mode="markers", marker=marker(sym), **d), row=1, col=c)
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=RED, width=2, dash="dot"),
                             **d0[4]), row=2, col=c)
    fig.update_xaxes(range=[-1.2, 1.2], zeroline=True, row=1, col=c, title_text="x")
    fig.update_yaxes(range=[-0.6, 0.6], zeroline=True, row=1, col=c,
                     title_text="f(x)" if c == 1 else "")
    fig.update_xaxes(range=[0, 2], row=2, col=c, title_text="T")
    fig.update_yaxes(range=[-1.1, 1.1], zeroline=True, row=2, col=c,
                     title_text="x*(T)" if c == 1 else "")
frames = []
for T in Ts:
    data, idx = [], []
    for c, m in enumerate(FM):
        for k, d in enumerate(ferro_col(m, T)):
            data.append(go.Scatter(**rd(d)))
            idx.append(n_static + 5 * c + k)
    frames.append(go.Frame(data=data, traces=idx, name=f"{T:g}"))
fig.frames = frames
add_slider(fig, [fr.name for fr in frames], [fr.name for fr in frames], "T = ")
write(fig, "ferro_temperature.html", 620)

# =========================================================================== 3
MS = np.round(np.linspace(-1, 1, 61), 3)
path = np.r_[MS, MS[::-1]]
TH = (0.5, 1.5)
state = {}
for T in TH:
    up = cb.continuation_sweep(ferro, "m", MS, -1.0, tinf=100, T=T)
    down = cb.continuation_sweep(ferro, "m", MS[::-1], up[-1], tinf=100, T=T)
    state[T] = np.r_[up, down]
xg = np.linspace(-1.6, 1.6, 101)


def hyst_col(T, k):
    m, x = path[k], state[T][k]
    st, un, ma = fixed_point_sets(ferro, dferro, -1.6, 1.6, dict(T=T, m=m))
    allfp = np.r_[st, un, ma]
    return [dict(x=xg, y=ferro(xg, T=T, m=m)),
            dict(x=allfp, y=zeros(allfp)),
            dict(x=[x], y=[0]),
            dict(x=path[:k + 1], y=state[T][:k + 1]),
            dict(x=[m], y=[x])]


fig = make_subplots(rows=2, cols=2, vertical_spacing=0.16, horizontal_spacing=0.09,
                    subplot_titles=[f"T = {T:g}" for T in TH] + [""] * 2)
for c, T in enumerate(TH, start=1):
    for p, x, stable in cb.fixed_point_branches(ferro, "m", -1, 1, -1.4, 1.4,
                                                shape=(350, 350), dfdx=dferro, T=T):
        fig.add_trace(go.Scatter(x=p, y=x, mode="lines",
                                 line=dict(color="#d9d9d9" if stable else "#bdbdbd",
                                           width=8 if stable else 4)), row=2, col=c)
n_static = len(fig.data)
for c, T in enumerate(TH, start=1):
    d0 = hyst_col(T, 0)
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=BLACK, width=3), **d0[0]),
                  row=1, col=c)
    fig.add_trace(go.Scatter(mode="markers", marker=dict(
        symbol="circle-open", size=11, color="#777777", line=dict(width=2)), **d0[1]),
        row=1, col=c)
    fig.add_trace(go.Scatter(mode="markers", marker=dict(symbol="circle", size=15,
                                                         color=RED), **d0[2]),
                  row=1, col=c)
    fig.add_trace(go.Scatter(mode="lines", line=dict(color=BLACK, width=2.5), **d0[3]),
                  row=2, col=c)
    fig.add_trace(go.Scatter(mode="markers", marker=dict(symbol="circle", size=13,
                                                         color=RED), **d0[4]),
                  row=2, col=c)
    fig.update_xaxes(range=[-1.6, 1.6], zeroline=True, row=1, col=c, title_text="x")
    fig.update_yaxes(range=[-0.8, 0.8], zeroline=True, row=1, col=c,
                     title_text="f(x)" if c == 1 else "")
    fig.update_xaxes(range=[-1, 1], zeroline=True, row=2, col=c, title_text="m")
    fig.update_yaxes(range=[-1.4, 1.4], zeroline=True, row=2, col=c,
                     title_text="x*(m)" if c == 1 else "")
frames, labels = [], []
for k in range(len(path)):
    data, idx = [], []
    for c, T in enumerate(TH):
        for j, d in enumerate(hyst_col(T, k)):
            data.append(go.Scatter(**rd(d)))
            idx.append(n_static + 5 * c + j)
    frames.append(go.Frame(data=data, traces=idx, name=str(k)))
    labels.append(f"{path[k]:+.2f}{' up' if k < len(MS) else ' down'}")
fig.frames = frames
add_slider(fig, [fr.name for fr in frames], labels, "field m (sweep up, then down): ")
write(fig, "hysteresis_sweep.html", 620)
print("fig_interactive: written")
