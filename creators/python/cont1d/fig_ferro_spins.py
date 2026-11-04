"""Monte-Carlo simulation of N = 20x20 mean-field spins (J_ij = 1, m = 0).

Produces (in python/_static/cont1d/):
  cont1d_ferro_spin_evolution.png   4x6 grid of snapshots at n = 0, 1000, ..., 5000
                                    (rows: T = 0.5 runs a, b; T = 1.5 runs a, b)
  cont1d_ferro_spin_mean_state.png  mean state x(t), t = n/N: (a) T = 0.5, (b) T = 1.5
Run 'a' starts from all spins +1, run 'b' from all spins -1, after flipping a
fraction F of them (F = 0.3 at T = 0.5, F = 0.1 at T = 1.5).
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import bf, save

K = 20
N = K * K
ITER = 10000
M = 0.0   # external field


def simulate(T, s0, F, seed):
    """Single-spin-flip dynamics; returns snapshots and the mean state x[n]."""
    rng = np.random.default_rng(seed)
    s = np.full(N, s0)
    s[rng.random(N) < F] *= -1
    snaps, x = [], np.empty(ITER + 1)
    for n in range(ITER + 1):
        i = rng.integers(N)
        h = s.sum() / N + M                       # local field of spin i
        p = 0.5 * (1 + np.tanh(s[i] * h / T))     # probability to stay
        if rng.random() > p:
            s[i] = -s[i]
        if n % 1000 == 0 and len(snaps) < 6:
            snaps.append(s.reshape(K, K).copy())
        x[n] = s.sum() / N
    return snaps, x


fig_s, axs_s = plt.subplots(4, 6, figsize=(bf.FULL_W, 4.3))
fig_m, axs_m = plt.subplots(1, 2, figsize=(bf.FULL_W, 2.6), sharey=True)
row = 0
for ax_m, (T, F) in zip(axs_m, ((0.5, 0.3), (1.5, 0.1))):
    for run, s0, seed in (("a", +1, 11), ("b", -1, 12)):
        snaps, x = simulate(T, s0, F, seed)
        print(f"T={T}: run {run}: x(0) = {x[0]:+.3f}, x(t=25) = {x[-1]:+.3f}, "
              f"mean over t in [15,25] = {x[6000:].mean():+.3f}")
        for ax, snap in zip(axs_s[row], snaps):
            ax.pcolormesh(snap[::-1], cmap="gray", vmin=-1, vmax=1,
                          edgecolors="k", linewidth=0.3)
            ax.set_aspect("equal")
            ax.axis("off")
        row += 1
        ax_m.plot(np.arange(0, ITER + 1, 10) / N, x[::10], "k", lw=1.0)
    ax_m.axhline(0, color="k", lw=0.8)
    ax_m.set_xlim(0, ITER / N)
    ax_m.set_ylim(-1, 1)
    ax_m.set_xlabel("$t$")
    ax_m.set_title(f"$T={T:g}$")
axs_m[0].set_ylabel("$x(t)$")
bf.panel_labels(axs_m)
save(fig_m, "cont1d_ferro_spin_mean_state")
fig_s.get_layout_engine().set(w_pad=0.01, h_pad=0.01, wspace=0.01, hspace=0.01)
save(fig_s, "cont1d_ferro_spin_evolution")

print("fig_ferro_spins: written")
