"""Ensemble forecasting for the Lorenz system, "Chaos in practice".

Produces (in python/_static/practice/):
  practice_ensemble.png            blob of initial conditions at t = 0, 3, 8
  practice_horizon.png             growth and saturation of the ensemble spread
  interactive/ensemble_spread.html animated ensemble with its spread delta(t)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, save)

OUT = bf.out("practice")
(OUT / "interactive").mkdir(parents=True, exist_ok=True)

C_ANA, C_TRUTH, C_FREE, C_OBS, C_FAINT = "#1f6aa5", "#111111", "#c0392b", "#e08a1e", "#b8b8b8"


def on_attractor(seed=(1.0, 1.0, 1.0), t_transient=50.0):
    """A point on the Lorenz attractor: integrate away the transient."""
    sol = solve_ivp(cb.lorenz, [0, t_transient], seed, rtol=1e-10, atol=1e-12)
    return sol.y[:, -1]


def ensemble(x0, eps0, M, t_eval, seed):
    """Integrate M perturbed copies of x0 (all at once, as one big system).

    Returns an array of shape (len(t_eval), M, 3).
    """
    rng = np.random.default_rng(seed)
    ics = x0 + eps0 * rng.standard_normal((M, 3))          # (M, 3)
    f = lambda t, Y: np.ravel(cb.lorenz(t, Y.reshape(3, M)))  # stacked state
    sol = solve_ivp(f, [0, t_eval[-1]], ics.T.ravel(), t_eval=t_eval,
                    rtol=1e-9, atol=1e-11)
    return sol.y.reshape(3, M, -1).transpose(2, 1, 0)


def spread(cloud):
    """RMS distance of the members from the ensemble mean, per time."""
    d = cloud - cloud.mean(axis=1, keepdims=True)
    return np.sqrt((d ** 2).sum(axis=2).mean(axis=1))


x0 = on_attractor()
back = solve_ivp(cb.lorenz, [0, 60], x0, t_eval=np.arange(0, 60, 0.01),
                 rtol=1e-9, atol=1e-11).y

# -- ensemble snapshots at t = 0, 3, 8 --------------------------------------
times = [0.0, 3.0, 8.0]
cloud = ensemble(x0, 0.5, 400, np.array(times), seed=1)
fig, axes = plt.subplots(1, 3, figsize=(bf.FULL_W, 2.4))
for ax, t, pts in zip(axes, times, cloud):
    ax.plot(back[0], back[2], color=C_FAINT, lw=0.3, alpha=0.7, zorder=1)
    ax.scatter(pts[:, 0], pts[:, 2], s=6, color=C_ANA, alpha=0.7,
               edgecolors="none", zorder=3)
    ax.set_title(f"$t = {t:.0f}$")
    ax.set_xlabel("$x$")
    ax.set_xlim(-22, 22)
    ax.set_ylim(0, 52)
    ax.set_xticks([-20, 0, 20])
    ax.set_yticks([0, 25, 50])
axes[0].set_ylabel("$z$")
bf.save(fig, OUT / "practice_ensemble.png")

# -- spread delta(t) and the predictability horizon -------------------------
T = 22.0
t = np.linspace(0, T, 2201)
delta = spread(ensemble(x0, 1e-3, 600, t, seed=2))
Le = 0.9
sat = delta[t >= 18].mean()
# predictability horizon, as defined in the text: the time at which the
# exponential growth delta(0) exp(Le t) reaches the size of the attractor
th = np.log(sat / delta[0]) / Le

fig, ax = plt.subplots(figsize=bf.MEDIUM)
ax.semilogy(t, delta, color=C_ANA, lw=1.6, label="ensemble spread")
tref = np.linspace(0, 14, 50)
ax.semilogy(tref, delta[0] * np.exp(Le * tref), "--", color=C_TRUTH, lw=1.1,
            label=r"$\propto \mathrm{e}^{\Lambda_e t}$, $\Lambda_e = 0.9$")
ax.axhline(sat, color=C_FREE, lw=1.0, ls=":", label="attractor size")
ax.axvline(th, color=C_OBS, lw=1.0)
ax.annotate("predictability\nhorizon", xy=(th, 0.4 * sat), xytext=(th + 1.0, 3e-2),
            color=C_OBS, fontsize=8,
            arrowprops=dict(arrowstyle="->", color=C_OBS, lw=0.8))
ax.set_xlabel("$t$")
ax.set_ylabel(r"ensemble spread $\delta(t)$")
ax.set_xlim(0, T)
ax.set_ylim(5e-4, 5e1)
ax.legend(loc="lower right")
bf.save(fig, OUT / "practice_horizon.png")
print(f"horizon: delta(0) = {delta[0]:.2e}, spread saturates at {sat:.2f}; "
      f"t_h = ln(sat/delta0)/Le = {th:.2f}")
print(f"  (text numbers: ln(10/1e-3)/0.9 = {np.log(10 / 1e-3) / 0.9:.2f}; "
      f"spread reaches 40% of saturation at t = {t[np.argmax(delta > 0.4 * sat)]:.2f})")
for t1, t2 in [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]:
    i1, i2 = np.searchsorted(t, [t1, t2])
    print(f"  growth rate of the spread over t in [{t1}, {t2}]: "
          f"{np.log(delta[i2] / delta[i1]) / (t2 - t1):.2f}")

# -- interactive: ensemble animation with its spread ------------------------
tt = np.round(np.arange(0, 14.01, 0.25), 2)
cl = ensemble(x0, 1e-2, 300, tt, seed=3)
dl = spread(cl)
bk = back[:, ::3]

fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45],
                    subplot_titles=("ensemble in the (x, z) plane",
                                    "ensemble spread δ(t)"))
fig.add_trace(go.Scatter(x=bk[0], y=bk[2], mode="lines", hoverinfo="skip",
                         line=dict(color=C_FAINT, width=0.6)), row=1, col=1)
fig.add_trace(go.Scatter(x=cl[0, :, 0].round(3), y=cl[0, :, 2].round(3),
                         mode="markers", marker=dict(size=4, color=C_ANA)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[0], y=[dl[0]], mode="lines",
                         line=dict(color=C_ANA, width=2)), row=1, col=2)
fig.add_trace(go.Scatter(x=[0], y=[dl[0]], mode="markers",
                         marker=dict(size=9, color=C_FREE)), row=1, col=2)
fig.frames = [
    go.Frame(name=f"{t}", traces=[1, 2, 3], data=[
        go.Scatter(x=cl[i, :, 0].round(3), y=cl[i, :, 2].round(3)),
        go.Scatter(x=tt[: i + 1], y=dl[: i + 1]),
        go.Scatter(x=[tt[i]], y=[dl[i]]),
    ], layout=dict(title=f"t = {t:.2f},  δ = {dl[i]:.3g}"))
    for i, t in enumerate(tt)
]
fig.update_xaxes(title_text="x", range=[-22, 22], row=1, col=1)
fig.update_yaxes(title_text="z", range=[0, 52], row=1, col=1)
fig.update_xaxes(title_text="t", range=[0, 14], row=1, col=2)
fig.update_yaxes(title_text="δ(t)", type="log", range=[-2.5, 1.5], row=1, col=2)
fig.update_layout(
    showlegend=False, margin=dict(l=50, r=10, t=70, b=40), title="t = 0.00",
    updatemenus=[dict(type="buttons", x=0.0, y=-0.12, direction="left",
                      buttons=[dict(label="Play", method="animate",
                                    args=[None, dict(frame=dict(duration=120, redraw=True),
                                                     fromcurrent=True)]),
                               dict(label="Pause", method="animate",
                                    args=[[None], dict(mode="immediate",
                                                       frame=dict(duration=0))])])],
    sliders=[dict(currentvalue=dict(prefix="t = "), pad=dict(t=40),
                  steps=[dict(label=f"{t}", method="animate",
                              args=[[f"{t}"], dict(mode="immediate",
                                                   frame=dict(duration=0, redraw=True))])
                         for t in tt])],
)
fig.write_html(OUT / "interactive" / "ensemble_spread.html",
               include_plotlyjs="../../plotly.min.js", full_html=True)
print("fig_ensemble: assets written to", OUT)
