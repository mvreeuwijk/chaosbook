"""Box-counting, binomial multifractal and generalized dimensions.

Produces (in python/_static/fractals/):
  fractals_boxcount_fit.png   log N(eps) against log eps for a Sierpinski
                              gasket of 200 000 chaos-game points
  fractals_binomial.png       binomial measure, p1 = 0.7, k = 9
  fractals_Dq.png             D_q: closed form against box counting
  interactive/binomial_slider.html   measure and D_q under a p1 slider
  interactive/sierpinski_zoom.html   Sierpinski gasket, pan/zoom to depth 8
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "fractals"
(OUT / "interactive").mkdir(parents=True, exist_ok=True)
GRAY, RED = "#888888", "#b22222"


def binomial_measure(p1, k):
    """Mass of the 2**k sub-intervals after k binomial splittings."""
    m = np.array([1.0])
    for _ in range(k):
        m = np.ravel(np.column_stack([p1 * m, (1 - p1) * m]))
    return m


def dq_exact(q, p1):
    q = np.asarray(q, float)
    return -np.log(p1**q + (1 - p1) ** q) / ((q - 1) * np.log(2))


# -- box counting with under-sampling ---------------------------------------
X, Y = cb.chaos_game(n=200000, seed=1)
ps = np.arange(1, 12)
eps = 1.0 / 2.0**ps
counts = np.array([len(np.unique(np.floor(np.column_stack([X, Y]) / e).astype(int), axis=0))
                   for e in eps])
good = counts < len(X) / 4
slope, icpt = np.polyfit(np.log(eps[good][3:]), np.log(counts[good][3:]), 1)

fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.plot(np.log(eps[~good]), np.log(counts[~good]), "o", color=GRAY)
ax.plot(np.log(eps[good]), np.log(counts[good]), "o", mfc="none", mec="k",
        label="box counts")
xx = np.array([np.log(eps[good][3]), np.log(eps[good][-1])])
ax.plot(xx, slope * xx + icpt, color=RED, lw=2,
        label=rf"fit, slope $=-D_0={slope:.2f}$")
ax.axhline(np.log(len(X)), color=GRAY, ls=":", lw=1)
ax.text(np.log(eps[-1]), np.log(len(X)) + 0.3, r"$\log N_{\rm pts}$", color=GRAY, fontsize=10)
ax.annotate("under-sampled\n(flattening)", (np.log(eps[-2]), np.log(counts[-2])),
            xytext=(np.log(eps[-4]) + 0.3, 9.8), color=GRAY, fontsize=11,
            arrowprops=dict(arrowstyle="->", color=GRAY))
ax.set_xlabel(r"$\log\varepsilon$")
ax.set_ylabel(r"$\log N(\varepsilon)$")
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(OUT / "fractals_boxcount_fit.png", dpi=150)
plt.close(fig)
print("boxcount fit slope", slope, "N counts", counts)

# -- binomial measure -------------------------------------------------------
k, p1 = 9, 0.7
m = binomial_measure(p1, k)
x = (np.arange(2**k) + 0.5) / 2**k
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.vlines(x, 0, m, color="k", lw=1)
ax.set_xlim(0, 1)
ax.set_ylim(0, m.max() * 1.05)
ax.set_xlabel("position")
ax.set_ylabel(r"measure $p_i$")
ax.set_title(rf"$p_1={p1},\ p_2={1 - p1:.1f},\ k={k}$", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "fractals_binomial.png", dpi=150)
plt.close(fig)

# -- D_q: closed form against box counting ------------------------------------
qs = np.array([q for q in range(-10, 11) if q != 1])
Dnum = cb.generalized_dimensions(x, qs=qs, pmin=2, pmax=k, weights=m,
                                 origin=0.0, size=1.0)
qq = np.linspace(-10, 10, 400)
qq = qq[np.abs(qq - 1) > 1e-3]
fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.plot(qq, dq_exact(qq, p1), "k", lw=2, label="analytical")
ax.plot(qs, Dnum, "o", mfc="white", mec=RED, mew=1.5, ls="none", label="box counting")
ax.set_xlim(-10, 10)
ax.set_xlabel("$q$")
ax.set_ylabel("$D_q$")
ax.set_title(rf"$p_1={p1},\ p_2={1 - p1:.1f}$", fontsize=11)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "fractals_Dq.png", dpi=150)
plt.close(fig)
print("max |Dq numerical - analytical|", np.abs(Dnum - dq_exact(qs, p1)).max())

# -- interactive: binomial slider --------------------------------------------
p1s = np.round(np.arange(0.5, 0.96, 0.05), 2)
fig = make_subplots(rows=1, cols=2, subplot_titles=("measure $p_i$ ($k=9$)", "$D_q$"))
qd = np.linspace(-10, 10, 201)
qd = qd[np.abs(qd - 1) > 1e-3]
for j, p in enumerate(p1s):
    vis = j == 0
    mm = binomial_measure(p, k)
    xs = np.repeat(x, 3)
    ys = np.column_stack([np.zeros_like(mm), mm, np.full_like(mm, np.nan)]).ravel()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="black", width=1),
                             visible=vis, showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=qd, y=dq_exact(qd, p), mode="lines",
                             line=dict(color="black", width=2),
                             visible=vis, showlegend=False), row=1, col=2)
steps = [dict(method="update", label=f"{p:.2f}",
              args=[{"visible": [i // 2 == j for i in range(2 * len(p1s))]}])
         for j, p in enumerate(p1s)]
fig.update_layout(sliders=[dict(active=0, steps=steps, currentvalue=dict(prefix="p1 = "),
                                pad=dict(t=30))],
                  height=420, margin=dict(l=50, r=20, t=40, b=20), template="plotly_white")
fig.update_xaxes(title_text="position", range=[0, 1], row=1, col=1)
fig.update_yaxes(range=[0, 0.1], row=1, col=1)
fig.update_xaxes(title_text="q", row=1, col=2)
fig.update_yaxes(range=[0, 1.7], row=1, col=2)
fig.write_html(OUT / "interactive" / "binomial_slider.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)

# -- interactive: Sierpinski zoom ----------------------------------------------
def tri(v, depth, out):
    if depth == 0:
        out.append(v)
        return
    m01, m12, m20 = (v[0] + v[1]) / 2, (v[1] + v[2]) / 2, (v[2] + v[0]) / 2
    tri(np.array([v[0], m01, m20]), depth - 1, out)
    tri(np.array([m01, v[1], m12]), depth - 1, out)
    tri(np.array([m20, m12, v[2]]), depth - 1, out)


tris = []
tri(np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]]), 8, tris)
T = np.array(tris)  # (3**9, 3, 2)
xs = np.column_stack([T[:, :, 0], T[:, 0, 0], np.full(len(T), np.nan)]).ravel().round(6)
ys = np.column_stack([T[:, :, 1], T[:, 0, 1], np.full(len(T), np.nan)]).ravel().round(6)
fig = go.Figure(go.Scatter(x=xs, y=ys, fill="toself", mode="lines",
                           line=dict(width=0), fillcolor="#222222", hoverinfo="skip"))
fig.update_layout(height=460, margin=dict(l=10, r=10, t=10, b=10), template="plotly_white",
                  xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"))
fig.write_html(OUT / "interactive" / "sierpinski_zoom.html",
               include_plotlyjs="../../plotly.min.js", full_html=True,
               config=dict(scrollZoom=True))
print("wrote figures and interactive companions")
