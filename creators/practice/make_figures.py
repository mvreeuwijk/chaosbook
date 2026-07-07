"""Figure generator for the chapter *Chaos in practice* (chap:practice).

Produces the figures used in maple/practice.md.  The *book* code fragments are
Maple; this script is only the figure-generation pipeline and may therefore be
Python (cf. the edition split described in ROADMAP.md).

All figures are written to maple/_static/practice/ as PNG.

Run:  python creators/practice/make_figures.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

# --------------------------------------------------------------------------
# House style: plain, serif, book-like.
# --------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 11,
    "axes.linewidth": 0.8,
    "axes.grid": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
})

# Consistent palette across the chapter.
C_TRUTH = "#111111"    # the truth trajectory
C_FREE  = "#c0392b"    # uncorrected ("free") forecast
C_ANA   = "#1f6aa5"    # analysis / assimilated estimate
C_OBS   = "#e08a1e"    # observations
C_FAINT = "#b8b8b8"    # attractor backdrop
C_ENS   = "#1f6aa5"    # ensemble members

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "maple", "_static", "practice")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

# --------------------------------------------------------------------------
# Lorenz-63 system, its Jacobian, and an RK4 integrator.
# --------------------------------------------------------------------------
SIGMA, RHO, BETA = 10.0, 28.0, 8.0 / 3.0


def lorenz(x):
    return np.array([
        SIGMA * (x[1] - x[0]),
        RHO * x[0] - x[1] - x[0] * x[2],
        x[0] * x[1] - BETA * x[2],
    ])


def jacobian(x):
    return np.array([
        [-SIGMA,        SIGMA,     0.0],
        [RHO - x[2],   -1.0,      -x[0]],
        [x[1],          x[0],     -BETA],
    ])


def rk4_step(x, dt, f=lorenz):
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def integrate(x0, dt, n):
    """Return array (n+1, dim) of the trajectory from x0."""
    xs = np.empty((n + 1, len(x0)))
    xs[0] = x0
    x = x0.copy()
    for i in range(n):
        x = rk4_step(x, dt)
        xs[i + 1] = x
    return xs


def on_attractor(seed=(1.0, 1.0, 1.0), t_transient=40.0, dt=0.01):
    """Integrate away the transient and return a point on the attractor."""
    x = np.array(seed, dtype=float)
    for _ in range(int(t_transient / dt)):
        x = rk4_step(x, dt)
    return x


def attractor_backdrop(dt=0.01, t=60.0):
    x0 = on_attractor()
    return integrate(x0, dt, int(t / dt))


# ==========================================================================
# Figure 1 -- ensemble forecast: a tight blob stretches and folds.
# ==========================================================================
def fig_ensemble():
    dt = 0.01
    x0 = on_attractor()
    M = 400
    rng = np.random.default_rng(1)
    blob = x0 + 0.5 * rng.standard_normal((M, 3))

    times = [0.0, 3.0, 8.0]
    steps = [int(t / dt) for t in times]
    nmax = max(steps)

    # advance the whole ensemble, storing snapshots at the requested times
    ens = blob.copy()
    snaps = {0: ens.copy()}
    for i in range(1, nmax + 1):
        for m in range(M):
            ens[m] = rk4_step(ens[m], dt)
        if i in steps:
            snaps[i] = ens.copy()

    back = attractor_backdrop()

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.2))
    for ax, t, s in zip(axes, times, steps):
        ax.plot(back[:, 0], back[:, 2], color=C_FAINT, lw=0.3, alpha=0.7, zorder=1)
        pts = snaps[s]
        ax.scatter(pts[:, 0], pts[:, 2], s=6, color=C_ENS, alpha=0.7,
                   edgecolors="none", zorder=3)
        ax.set_title(fr"$t = {t:.0f}$", fontsize=11)
        ax.set_xlabel(r"$x$")
        ax.set_xlim(-22, 22)
        ax.set_ylim(0, 52)
        ax.set_xticks([-20, 0, 20])
        ax.set_yticks([0, 25, 50])
    axes[0].set_ylabel(r"$z$")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_ensemble.png"))
    plt.close(fig)
    print("wrote practice_ensemble.png")


# ==========================================================================
# Figure 2 -- growth of ensemble spread and the predictability horizon.
# ==========================================================================
def fig_horizon():
    dt = 0.01
    T = 22.0
    n = int(T / dt)
    x0 = on_attractor()
    M = 600
    rng = np.random.default_rng(2)
    eps0 = 1e-3
    ens = x0 + eps0 * rng.standard_normal((M, 3))

    spread = np.empty(n + 1)
    t = np.linspace(0, T, n + 1)
    for i in range(n + 1):
        mean = ens.mean(axis=0)
        spread[i] = np.sqrt(np.mean(np.sum((ens - mean) ** 2, axis=1)))
        if i < n:
            for m in range(M):
                ens[m] = rk4_step(ens[m], dt)

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.semilogy(t, spread, color=C_ANA, lw=1.6, label="ensemble spread")

    # reference line of slope Lambda_e = 0.9 through the initial spread
    Le = 0.9
    tref = np.linspace(0, 14, 50)
    s0 = spread[0]
    ax.semilogy(tref, s0 * np.exp(Le * tref), "--", color=C_TRUTH, lw=1.1,
                label=r"$\propto e^{\Lambda_e t},\ \Lambda_e = 0.9$")

    # saturation level (size of the attractor)
    sat = spread[int(18 / dt):].mean()
    ax.axhline(sat, color=C_FREE, lw=1.0, ls=":", label="attractor size")

    # predictability horizon: spread reaches a fraction of saturation
    thr = 0.4 * sat
    ih = np.argmax(spread > thr)
    th = t[ih]
    ax.axvline(th, color=C_OBS, lw=1.0)
    ax.annotate("predictability\nhorizon", xy=(th, thr), xytext=(th + 1.0, 3e-2),
                color=C_OBS, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=C_OBS, lw=0.8))

    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"ensemble spread $\delta(t)$")
    ax.set_xlim(0, T)
    ax.set_ylim(5e-4, 5e1)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_horizon.png"))
    plt.close(fig)
    print("wrote practice_horizon.png")


# ==========================================================================
# Figure 3 -- data assimilation: the (extended) Kalman filter twin experiment.
# ==========================================================================
def aug_rhs(state, Q):
    """RHS for the joint (state, covariance) forecast used by the EKF."""
    x = state[:3]
    P = state[3:].reshape(3, 3)
    J = jacobian(x)
    dx = lorenz(x)
    dP = J @ P + P @ J.T + Q
    return np.concatenate([dx, dP.ravel()])


def aug_step(state, dt, Q):
    k1 = aug_rhs(state, Q)
    k2 = aug_rhs(state + 0.5 * dt * k1, Q)
    k3 = aug_rhs(state + 0.5 * dt * k2, Q)
    k4 = aug_rhs(state + dt * k3, Q)
    return state + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def fig_assimilation():
    dt = 0.01
    dt_obs = 0.20                 # assimilate every 20 steps
    every = int(dt_obs / dt)
    T = 12.0
    n = int(T / dt)
    rng = np.random.default_rng(7)

    # truth
    x0 = on_attractor()
    truth = integrate(x0, dt, n)
    t = np.linspace(0, T, n + 1)

    # noisy observations of the full state
    H = np.eye(3)
    sig_obs = 1.5
    R = sig_obs ** 2 * np.eye(3)
    obs_idx = np.arange(every, n + 1, every)
    obs = (H @ truth[obs_idx].T).T + sig_obs * rng.standard_normal((len(obs_idx), 3))

    # both estimates start from the same wrong initial condition
    x_start = x0 + np.array([8.0, 8.0, 8.0])

    # free forecast: integrate, never look at the data
    free = integrate(x_start, dt, n)

    # extended Kalman filter, with mild multiplicative covariance inflation
    Q = 1e-2 * np.eye(3)
    infl = 1.03
    P = 4.0 * np.eye(3)
    x = x_start.copy()
    ana = np.empty((n + 1, 3))
    ana[0] = x
    state = np.concatenate([x, P.ravel()])
    k = 0
    for i in range(1, n + 1):
        state = aug_step(state, dt, Q)
        if i in obs_idx:
            xf = state[:3]
            Pf = infl * state[3:].reshape(3, 3)
            S = H @ Pf @ H.T + R
            K = Pf @ H.T @ np.linalg.inv(S)
            xa = xf + K @ (obs[k] - H @ xf)
            Pa = (np.eye(3) - K @ H) @ Pf
            state = np.concatenate([xa, Pa.ravel()])
            k += 1
        ana[i] = state[:3]

    # RMS error over the full 3-vector
    err_free = np.sqrt(np.mean((free - truth) ** 2, axis=1))
    err_ana = np.sqrt(np.mean((ana - truth) ** 2, axis=1))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 5.2), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(t, truth[:, 0], color=C_TRUTH, lw=1.4, label="truth", zorder=3)
    ax1.plot(t, free[:, 0], color=C_FREE, lw=1.2, ls="--",
             label="free forecast", zorder=2)
    ax1.plot(t, ana[:, 0], color=C_ANA, lw=1.2, label="analysis (Kalman filter)",
             zorder=4)
    ax1.scatter(t[obs_idx], obs[:, 0], s=12, color=C_OBS, zorder=5,
                edgecolors="none", label="observations of $x$")
    ax1.set_ylabel(r"$x$")
    ax1.set_ylim(-28, 28)
    ax1.legend(frameon=False, fontsize=9, ncol=2, loc="upper center")

    ax2.semilogy(t, err_free, color=C_FREE, lw=1.2, ls="--", label="free forecast")
    ax2.semilogy(t, err_ana, color=C_ANA, lw=1.2, label="Kalman filter")
    ax2.set_ylabel("RMS error")
    ax2.set_xlabel(r"$t$")
    ax2.set_xlim(0, T)
    ax2.set_ylim(1e-1, 4e1)
    ax2.legend(frameon=False, fontsize=9, loc="upper right")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_assimilation.png"))
    plt.close(fig)
    print("wrote practice_assimilation.png")


# ==========================================================================
# Figure 4 -- POD: a high-dimensional field with low-dimensional structure.
# The spatial patterns are carried by a few modes whose amplitudes are the
# Lorenz variables themselves -- tying the reduction back to chapter cont3d.
# ==========================================================================
def fig_pod():
    # spatial grid
    Nx = 200
    xg = np.linspace(0, 2 * np.pi, Nx)

    # three fixed spatial structures (the "coherent structures")
    phi1 = np.sin(xg)
    phi2 = np.sin(2 * xg) * np.exp(-((xg - np.pi) ** 2) / 4)
    phi3 = np.cos(3 * xg)

    # time-dependent amplitudes = a Lorenz trajectory (normalised)
    dt = 0.01
    Nt = 800
    x0 = on_attractor()
    traj = integrate(x0, dt, Nt - 1)
    a = (traj - traj.mean(0)) / traj.std(0)

    rng = np.random.default_rng(11)
    field = (np.outer(a[:, 0], phi1)
             + np.outer(a[:, 1], phi2)
             + 0.6 * np.outer(a[:, 2], phi3))
    field += 0.15 * rng.standard_normal(field.shape)   # measurement noise

    # snapshot matrix: columns are snapshots in time
    Xm = field.T                      # (Nx, Nt)
    Xm = Xm - Xm.mean(axis=1, keepdims=True)
    U, S, Vt = np.linalg.svd(Xm, full_matrices=False)

    energy = S ** 2 / np.sum(S ** 2)

    # reconstruct one snapshot with r modes
    snap = 300
    recon = {}
    for r in (1, 2, 3):
        recon[r] = (U[:, :r] * S[:r]) @ Vt[:r, snap]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.6))

    idx = np.arange(1, 11)
    ax1.bar(idx, energy[:10], color=C_ANA, width=0.6)
    ax1.set_xlabel("mode number")
    ax1.set_ylabel("relative energy")
    ax1.set_xticks(idx)
    ax1.set_title("POD spectrum", fontsize=11)
    cum = np.cumsum(energy)
    ax1b = ax1.twinx()
    ax1b.plot(idx, cum[:10], "o-", color=C_FREE, ms=4, lw=1.0)
    ax1b.set_ylabel("cumulative", color=C_FREE)
    ax1b.tick_params(axis="y", colors=C_FREE)
    ax1b.set_ylim(0, 1.02)

    ax2.plot(xg, Xm[:, snap], color=C_FAINT, lw=2.4, label="full field")
    for r, style in zip((1, 2, 3), ["--", "-.", "-"]):
        ax2.plot(xg, recon[r], style, lw=1.2, label=f"{r} mode" + ("s" if r > 1 else ""))
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$u(x)$")
    ax2.set_title("reconstruction of one snapshot", fontsize=11)
    ax2.legend(frameon=False, fontsize=8, loc="upper right")
    ax2.set_xlim(0, 2 * np.pi)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_pod.png"))
    plt.close(fig)
    print("wrote practice_pod.png")


# ==========================================================================
# Schematic figures (drawn, not computed).
# ==========================================================================
def _box(ax, xy, w, h, text, fc="#eef3f8", ec=C_ANA, fs=10):
    b = FancyBboxPatch((xy[0], xy[1]), w, h,
                       boxstyle="round,pad=0.02,rounding_size=0.03",
                       fc=fc, ec=ec, lw=1.2, zorder=2)
    ax.add_patch(b)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
            fontsize=fs, zorder=3)


def _arrow(ax, p0, p1, color=C_TRUTH, lw=1.3, style="-|>"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=14,
                                 color=color, lw=lw, zorder=1))


def fig_weathermodel():
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    # (a) grid of fields
    for i in range(4):
        for j in range(3):
            ax.add_patch(plt.Rectangle((0.3 + i * 0.42, 1.2 + j * 0.42), 0.42, 0.42,
                                       fc="#dfeaf5", ec="#8fb2d6", lw=0.6))
    ax.text(1.14, 3.2, "discretised\nfields on a grid", ha="center", fontsize=9)

    # (b) stacked state vector
    x0 = 3.6
    for j in range(9):
        ax.add_patch(plt.Rectangle((x0, 0.6 + j * 0.28), 0.5, 0.28,
                                   fc="#eef3f8", ec=C_ANA, lw=0.7))
    ax.text(x0 + 0.25, 3.35, r"$\mathbf{x}$", ha="center", fontsize=13)
    ax.text(x0 + 0.25, 0.25, r"$\dim \sim 10^{9}$", ha="center", fontsize=9)

    # (c) abstract flow x-dot = f(x)
    ax.text(6.2, 2.05, r"$\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$",
            ha="center", fontsize=15)

    # (d) an attractor loop
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(8.4 + 0.7 * np.cos(th) + 0.25 * np.cos(2 * th),
            2.0 + 0.6 * np.sin(th), color=C_TRUTH, lw=1.1)
    ax.text(8.5, 0.7, "flow on an\nattractor", ha="center", fontsize=9)

    # Lorenz inset: same object, 3 dimensions
    back = attractor_backdrop(t=40)
    axins = fig.add_axes([0.66, 0.60, 0.16, 0.34])
    axins.plot(back[:, 0], back[:, 2], color=C_FREE, lw=0.3)
    axins.axis("off")
    axins.set_title(r"Lorenz: $\dim = 3$", fontsize=8)

    _arrow(ax, (1.95, 1.9), (3.5, 1.9))
    _arrow(ax, (4.2, 1.9), (5.4, 1.9))
    _arrow(ax, (7.0, 1.9), (7.6, 1.9))

    fig.savefig(os.path.join(OUT, "practice_weathermodel.png"))
    plt.close(fig)
    print("wrote practice_weathermodel.png")


def fig_manifold():
    fig = plt.figure(figsize=(6.0, 4.0))
    ax = fig.add_subplot(111, projection="3d")

    # a curved low-dimensional manifold
    u = np.linspace(-1, 1, 40)
    v = np.linspace(-1, 1, 40)
    U, V = np.meshgrid(u, v)
    W = 0.5 * (U ** 2 - V ** 2)
    ax.plot_surface(U, V, W, alpha=0.35, color=C_ANA, edgecolor="none")

    # trajectories in the ambient space collapsing onto it
    rng = np.random.default_rng(3)
    for _ in range(6):
        p = rng.uniform(-1, 1, 3)
        pts = [p]
        for _ in range(40):
            target_w = 0.5 * (p[0] ** 2 - p[1] ** 2)
            p = p + 0.15 * np.array([rng.uniform(-0.3, 0.3),
                                     rng.uniform(-0.3, 0.3),
                                     (target_w - p[2])])
            p[2] += 0.02 * rng.standard_normal()
            pts.append(p.copy())
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=C_TRUTH, lw=0.8)
        ax.scatter(pts[0, 0], pts[0, 1], pts[0, 2], color=C_FREE, s=12)

    ax.text2D(0.5, 0.92, "high-dimensional state space", transform=ax.transAxes,
              ha="center", fontsize=10)
    ax.text2D(0.72, 0.10, "low-dimensional\nattracting manifold",
              transform=ax.transAxes, ha="center", fontsize=9, color=C_ANA)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.grid(False)
    ax.view_init(elev=22, azim=-60)
    fig.savefig(os.path.join(OUT, "practice_manifold.png"))
    plt.close(fig)
    print("wrote practice_manifold.png")


def fig_koopman():
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # lower plane: nonlinear flow in state space
    th = np.linspace(0, 1.6 * np.pi, 200)
    ax.plot(1.2 + 1.6 * np.cos(th) + 0.3 * np.cos(2.3 * th),
            0.9 + 0.7 * np.sin(th), color=C_TRUTH, lw=1.4)
    ax.text(1.9, 0.1, "state space  " + r"$\mathbf{x}$", ha="center", fontsize=10)
    ax.text(1.9, 2.0, "nonlinear\nflow", ha="center", fontsize=9, color=C_TRUTH)

    # upper plane: linear evolution of observables
    ax.plot([6.0, 9.4], [3.7, 4.2], color=C_ANA, lw=1.4)
    ax.scatter([6.0, 7.1, 8.2, 9.4], np.interp([6.0, 7.1, 8.2, 9.4],
               [6.0, 9.4], [3.7, 4.2]), color=C_ANA, s=16, zorder=3)
    ax.text(7.7, 4.55, "observables  " + r"$g(\mathbf{x})$", ha="center", fontsize=10)
    ax.text(7.7, 3.15, r"linear:  $g_{k+1} = \mathcal{K}\, g_k$",
            ha="center", fontsize=9, color=C_ANA)

    _arrow(ax, (3.2, 1.4), (5.8, 3.7), color=C_FREE, lw=1.4)
    ax.text(4.2, 2.9, "lift", fontsize=9, color=C_FREE, rotation=32)

    fig.savefig(os.path.join(OUT, "practice_koopman.png"))
    plt.close(fig)
    print("wrote practice_koopman.png")


# ==========================================================================
# Harnessing chaos.
# ==========================================================================

# Figure -- chaotic mixing: an alternating shear (a "sine flow") stretches and
# folds two blobs of dye until they are interleaved into fine filaments.
def fig_mixing():
    A = 0.9

    def step(pts):
        x = (pts[:, 0] + A * np.sin(2 * np.pi * pts[:, 1])) % 1.0
        y = (pts[:, 1] + A * np.sin(2 * np.pi * x)) % 1.0
        return np.column_stack([x, y])

    rng = np.random.default_rng(5)
    n = 6000
    blob1 = np.column_stack([0.25 + 0.05 * rng.standard_normal(n),
                             0.5 + 0.05 * rng.standard_normal(n)])
    blob2 = np.column_stack([0.75 + 0.05 * rng.standard_normal(n),
                             0.5 + 0.05 * rng.standard_normal(n)])

    times = [0, 2, 5]
    a1, a2 = blob1.copy(), blob2.copy()
    snaps = {0: (a1.copy(), a2.copy())}
    for i in range(1, max(times) + 1):
        a1, a2 = step(a1), step(a2)
        if i in times:
            snaps[i] = (a1.copy(), a2.copy())

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.2))
    for ax, s in zip(axes, times):
        p1, p2 = snaps[s]
        ax.scatter(p1[:, 0], p1[:, 1], s=1.5, color=C_FREE, edgecolors="none")
        ax.scatter(p2[:, 0], p2[:, 1], s=1.5, color=C_ANA, edgecolors="none")
        ax.set_title(fr"$n = {s}$", fontsize=11)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
        ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_mixing.png"))
    plt.close(fig)
    print("wrote practice_mixing.png")


# Figure -- controlling chaos: OGY-style stabilisation of the unstable fixed
# point of the logistic map by tiny adjustments of the growth rate r.
def fig_control():
    r0 = 3.9
    xstar = 1.0 - 1.0 / r0            # the unstable fixed point (a period-1 orbit)
    drmax = 0.05                      # largest admissible parameter nudge
    N, Ncon = 240, 100
    x = 0.2
    xs = np.empty(N)
    dr = np.zeros(N)
    for n in range(N):
        xs[n] = x
        rr = r0
        if n >= Ncon:                 # switch the controller on
            denom = x * (1.0 - x)
            d = xstar / denom - r0 if denom > 1e-9 else 1e9
            if abs(d) <= drmax:       # only nudge when already near x*
                rr = r0 + d
                dr[n] = d
        x = rr * x * (1.0 - x)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 4.6), sharex=True,
                                   gridspec_kw={"height_ratios": [3, 1]})
    ax1.plot(xs, color=C_TRUTH, lw=0.8, marker="o", ms=2.2, markerfacecolor=C_TRUTH)
    ax1.axhline(xstar, color=C_ANA, ls="--", lw=1.1, label=r"target orbit $x^{*}$")
    ax1.axvline(Ncon, color=C_OBS, lw=1.0)
    ax1.text(Ncon + 4, 0.06, "control on", color=C_OBS, fontsize=9)
    ax1.set_ylabel(r"$x_n$")
    ax1.set_ylim(0, 1)
    ax1.legend(frameon=False, fontsize=9, loc="upper right")

    ax2.axhline(0, color="#999999", lw=0.6)
    ax2.plot(dr, color=C_FREE, lw=1.0)
    ax2.set_ylabel(r"$\delta r_n$")
    ax2.set_xlabel(r"$n$")
    ax2.set_xlim(0, N)
    ax2.set_ylim(-drmax, drmax)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_control.png"))
    plt.close(fig)
    print("wrote practice_control.png")


# Figure -- attractor reconstruction: rebuild the Lorenz attractor from a single
# recorded coordinate x(t) using delay coordinates (Takens' theorem).
def fig_reconstruction():
    dt = 0.01
    x0 = on_attractor()
    traj = integrate(x0, dt, 8000)
    xt = traj[:, 0]
    tau = 18                                    # delay in steps (~0.18 time units)
    M = len(xt) - 2 * tau
    emb = np.column_stack([xt[:M], xt[tau:M + tau], xt[2 * tau:M + 2 * tau]])

    fig = plt.figure(figsize=(9.0, 4.2))
    ax1 = fig.add_subplot(121, projection="3d")
    ax1.plot(traj[:, 0], traj[:, 1], traj[:, 2], color=C_TRUTH, lw=0.3)
    ax1.set_title(r"true attractor $(x,y,z)$", fontsize=11)
    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot(emb[:, 0], emb[:, 1], emb[:, 2], color=C_ANA, lw=0.3)
    ax2.set_title(r"reconstruction $(x_t,\,x_{t+\tau},\,x_{t+2\tau})$", fontsize=11)
    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.grid(False)
        ax.view_init(elev=22, azim=-125)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "practice_reconstruction.png"))
    plt.close(fig)
    print("wrote practice_reconstruction.png")


if __name__ == "__main__":
    fig_ensemble()
    fig_horizon()
    fig_assimilation()
    fig_pod()
    fig_weathermodel()
    fig_manifold()
    fig_koopman()
    fig_mixing()
    fig_control()
    fig_reconstruction()
    print("all figures written to", OUT)
