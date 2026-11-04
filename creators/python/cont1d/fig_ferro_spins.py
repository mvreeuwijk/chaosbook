"""Monte-Carlo simulation of N = 20x20 mean-field spins (J_ij = 1, m = 0).

Produces (in python/_static/cont1d/):
  cont1d_ferro_spin_T_{0_50,1_50}_{a,b}{0..5}.png  snapshots at n = 0, 1000, ..., 5000
  cont1d_ferro_spin_T_{0_50,1_50}.png              mean state x(t), t = n/N, both runs
Run 'a' starts from all spins +1, run 'b' from all spins -1, after flipping a
fraction F of them (F = 0.3 at T = 0.5, F = 0.1 at T = 1.5).
"""

import matplotlib.pyplot as plt
import numpy as np

from _common import SQUARE, save

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


for T, F, tag in ((0.5, 0.3, "0_50"), (1.5, 0.1, "1_50")):
    fig_m, ax_m = plt.subplots(figsize=SQUARE)
    for run, s0, seed in (("a", +1, 11), ("b", -1, 12)):
        snaps, x = simulate(T, s0, F, seed)
        print(f"T={T}: run {run}: x(0) = {x[0]:+.3f}, x(t=25) = {x[-1]:+.3f}, "
              f"mean over t in [15,25] = {x[6000:].mean():+.3f}")
        for k, snap in enumerate(snaps):
            fig, ax = plt.subplots(figsize=(3, 3))
            ax.pcolormesh(snap[::-1], cmap="gray", vmin=-1, vmax=1,
                          edgecolors="k", linewidth=0.5)
            ax.set_aspect("equal")
            ax.axis("off")
            fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
            save(fig, f"cont1d_ferro_spin_T_{tag}_{run}{k}")
        ax_m.plot(np.arange(0, ITER + 1, 10) / N, x[::10], "k", lw=2)
    ax_m.axhline(0, color="k", lw=0.8)
    ax_m.set_xlim(0, ITER / N)
    ax_m.set_ylim(-1, 1)
    ax_m.set_xlabel("$t$")
    ax_m.set_ylabel("$x(t)$")
    ax_m.set_title(f"$T={T:g}$")
    fig_m.tight_layout()
    save(fig_m, f"cont1d_ferro_spin_T_{tag}")

print("fig_ferro_spins: written")
