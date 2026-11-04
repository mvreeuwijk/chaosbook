"""Data assimilation for the Lorenz system, "Chaos in practice".

Produces (in python/_static/practice/):
  practice_assimilation.png   twin experiment: truth, free forecast and the
                              extended Kalman filter, with their RMS errors
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

import chaosbook as cb

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bookfig as bf  # noqa: E402  (house style: sizes, save)

OUT = bf.out("practice")

C_TRUTH, C_FREE, C_ANA, C_OBS = "#111111", "#c0392b", "#1f6aa5", "#e08a1e"
sigma, r, b = 10.0, 28.0, 8.0 / 3.0


def jac(x):
    """Jacobian of the Lorenz equations (as for the Lyapunov exponents)."""
    return np.array([[-sigma, sigma, 0.0],
                     [r - x[2], -1.0, -x[0]],
                     [x[1], x[0], -b]])


def advance_with_transition(x, dt, n_path=10):
    """Integrate the state and d(Phi)/dt = J Phi over one window.

    Returns the end state, the end transition matrix and, for plotting, the
    state at n_path equally spaced times inside the window.
    """
    def rhs(t, s):
        Phi = s[3:].reshape(3, 3)
        return np.concatenate([cb.lorenz(t, s[:3]), (jac(s[:3]) @ Phi).ravel()])
    s0 = np.concatenate([x, np.eye(3).ravel()])
    sol = solve_ivp(rhs, [0, dt], s0, t_eval=np.linspace(0, dt, n_path + 1)[1:],
                    rtol=1e-9, atol=1e-11)
    s = sol.y[:, -1]
    return s[:3], s[3:].reshape(3, 3), sol.y[:3].T


dt_obs, T = 0.2, 12.0
nobs = int(T / dt_obs)
rng = np.random.default_rng(7)

# truth, started on the attractor
x0 = solve_ivp(cb.lorenz, [0, 50], [1, 1, 1], rtol=1e-10, atol=1e-12).y[:, -1]
tobs = dt_obs * np.arange(1, nobs + 1)
t = np.linspace(0, T, 1201)
truth = solve_ivp(cb.lorenz, [0, T], x0, t_eval=t, rtol=1e-9, atol=1e-11).y.T
truth_obs = solve_ivp(cb.lorenz, [0, T], x0, t_eval=tobs, rtol=1e-9, atol=1e-11).y.T

# noisy observations of the full state
H = np.eye(3)
R = 1.5 ** 2 * np.eye(3)
Q = 0.01 * np.eye(3)
y = truth_obs + 1.5 * rng.standard_normal((nobs, 3))

# both estimates start from the same wrong first guess
x_start = x0 + 8.0
free = solve_ivp(cb.lorenz, [0, T], x_start, t_eval=t, rtol=1e-9, atol=1e-11).y.T

# extended Kalman filter: forecast over one window, then update
xa, Pa = x_start.copy(), 4.0 * np.eye(3)
path, tpath = [xa.copy()], [0.0]          # analysis trajectory for plotting
for k in range(nobs):
    xf, Phi, seg = advance_with_transition(xa, dt_obs)
    Pf = 1.03 * Phi @ Pa @ Phi.T + Q                    # mild inflation
    S = H @ Pf @ H.T + R
    K = Pf @ H.T @ np.linalg.inv(S)                     # Kalman gain
    xa = xf + K @ (y[k] - H @ xf)                       # analysis
    Pa = (np.eye(3) - K @ H) @ Pf                       # reduced uncertainty
    path.extend(seg[:-1]); path.append(xa.copy())      # forecast, then the jump
    tpath.extend(dt_obs * k + np.linspace(0, dt_obs, 11)[1:-1]); tpath.append(tobs[k])
analysis, ta = np.array(path), np.array(tpath)

truth_a = np.array([np.interp(ta, t, truth[:, i]) for i in range(3)]).T
err_ana = np.sqrt(np.mean((analysis - truth_a) ** 2, axis=1))
err_free = np.sqrt(np.mean((free - truth) ** 2, axis=1))
print(f"RMS error: free forecast {err_free[-100:].mean():.2f} (last 1 time unit), "
      f"analysis {err_ana[-50:].mean():.2f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(bf.FULL_W, 4.0), sharex=True,
                               height_ratios=[2, 1])
ax1.plot(t, truth[:, 0], color=C_TRUTH, lw=1.4, label="truth", zorder=3)
ax1.plot(t, free[:, 0], color=C_FREE, lw=1.2, ls="--", label="free forecast", zorder=2)
ax1.plot(ta, analysis[:, 0], color=C_ANA, lw=1.2, label="analysis", zorder=4)
ax1.scatter(tobs, y[:, 0], s=12, color=C_OBS, zorder=5, edgecolors="none",
            label="observations")
ax1.set_ylabel("$x$")
ax1.set_ylim(-28, 34)
ax1.legend(ncol=2, loc="upper center")
ax2.semilogy(t, err_free, color=C_FREE, lw=1.2, ls="--", label="free forecast")
ax2.semilogy(ta, err_ana, color=C_ANA, lw=1.2, label="Kalman filter")
ax2.set_ylabel("RMS error")
ax2.set_xlabel("$t$")
ax2.set_xlim(0, T)
ax2.set_ylim(1e-2, 3e2)
ax2.legend(ncol=2, loc="upper center")
bf.save(fig, OUT / "practice_assimilation.png")
print("fig_assimilation: assets written to", OUT)
