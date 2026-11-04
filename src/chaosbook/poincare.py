"""Tools for continuous flows: sections, maxima and Lyapunov exponents.

All functions accept any right-hand side ``f(t, x, **params)`` in the
``scipy.integrate.solve_ivp`` convention; nothing here assumes a particular
system. Extra keyword arguments are passed on to ``f`` as parameters. The
leading arguments are positional-only so that a parameter of the flow may be
called ``f`` (the damping coefficient of the forced double well is).

Calling convention of the package: maps and one-dimensional flows take
``f(x, **params)``; flows in two or more dimensions take
``f(t, x, **params)`` exactly as ``solve_ivp`` does, so any right-hand side
that works with ``solve_ivp`` works here.
"""

import numpy as np
from scipy.integrate import solve_ivp


def poincare_section(f, x0, tmax, plane, /, direction=0, discard=0.0,
                     rtol=1e-9, atol=1e-12, method="DOP853", **params):
    """Crossings of a trajectory with a plane ``x[index] = value``.

    plane      : (index, value), e.g. (1, 0.0) for the section y = 0.
    direction  : +1 upward crossings only, -1 downward only, 0 both.
    discard    : crossings before this time are dropped (transient).
    Returns (t, X): crossing times (n,) and states on the plane (n, dim).
    The crossings are located by root finding inside solve_ivp (events),
    so they are not limited by the output step.
    """
    index, value = plane

    def hit(t, x, *args):
        return x[index] - value
    hit.direction = direction

    sol = solve_ivp(lambda t, x: f(t, x, **params), [0.0, tmax],
                    np.asarray(x0, float), events=hit, rtol=rtol, atol=atol,
                    method=method)
    t = sol.t_events[0]
    X = sol.y_events[0].reshape(-1, len(x0))
    keep = t >= discard
    return t[keep], X[keep]


def stroboscopic_section(f, x0, period, n, /, phase=0.0, discard=0,
                         rtol=1e-9, atol=1e-12, method="DOP853", **params):
    """States sampled at times ``phase + k*period``, k = 1..n (forced systems).

    The first ``discard`` samples are dropped. Returns an (n - discard, dim)
    array.
    """
    t_eval = phase + period * np.arange(1, n + 1)
    sol = solve_ivp(lambda t, x: f(t, x, **params), [0.0, t_eval[-1]],
                    np.asarray(x0, float), t_eval=t_eval, rtol=rtol,
                    atol=atol, method=method)
    return sol.y.T[discard:]


def maxima(t, x, refine=True):
    """Local maxima of a sampled signal x(t).

    A sample is a maximum when x[j-1] < x[j] >= x[j+1]. With ``refine`` the
    time and height are corrected by a parabola through the three samples,
    which makes the result nearly independent of the sampling step.
    Returns (t_max, x_max).
    """
    t, x = np.asarray(t, float), np.asarray(x, float)
    j = np.where((x[1:-1] > x[:-2]) & (x[1:-1] >= x[2:]))[0] + 1
    if not refine:
        return t[j], x[j]
    xm, x0, xp = x[j - 1], x[j], x[j + 1]
    den = xm - 2 * x0 + xp
    shift = np.where(den != 0, 0.5 * (xm - xp) / np.where(den == 0, 1, den), 0.0)
    h = t[j] - t[j - 1]
    return t[j] + shift * h, x0 - 0.25 * (xm - xp) * shift


def _jac(f, t, x, /, h=1e-6, **params):
    """Central-difference Jacobian of f at (t, x)."""
    x = np.asarray(x, float)
    J = np.empty((len(x), len(x)))
    for k in range(len(x)):
        e = np.zeros(len(x))
        e[k] = h * max(1.0, abs(x[k]))
        J[:, k] = (np.asarray(f(t, x + e, **params), float)
                   - np.asarray(f(t, x - e, **params), float)) / (2 * e[k])
    return J


def effective_lyapunov(f, t, X1, X2, /, **params):
    """Instantaneous (effective) Lyapunov exponent of two nearby trajectories.

    X1, X2 are (n, dim) arrays sampled at times t. Evaluates
    Lambda_e = eps . J_S eps / eps . eps with eps = X2 - X1 and J_S the
    symmetric part of the Jacobian along X1, and also returns the sorted
    eigenvalues of J_S. Returns (Lambda_e (n,), local_rates (n, dim)).

    The second output, ``local_rates``, holds the *instantaneous* stretching
    rates of the flow. Lambda_e(t) always lies between the smallest and the
    largest of them, but their time averages are NOT the Lyapunov exponents
    (use :func:`lyapunov_spectrum_flow` for those); only the time average of
    Lambda_e tends to the largest Lyapunov exponent.
    """
    t = np.asarray(t, float)
    le = np.empty(len(t))
    local_rates = np.empty((len(t), X1.shape[1]))
    for i in range(len(t)):
        J = _jac(f, t[i], X1[i], **params)
        e = X2[i] - X1[i]
        le[i] = e @ J @ e / (e @ e)
        local_rates[i] = np.linalg.eigvalsh(0.5 * (J + J.T))
    return le, local_rates


def lyapunov_exponent(f, x0, tmax, /, dt=0.01, d0=1e-8, transient=0.0,
                      rtol=1e-9, atol=1e-12, **params):
    """Largest Lyapunov exponent of a flow by two-trajectory renormalisation.

    A companion trajectory is kept at distance d0; every dt the separation
    d is recorded and the companion is pulled back to distance d0. The
    exponent is the time average of ln(d/d0)/dt after ``transient``.
    """
    x = np.asarray(x0, float)
    rhs = lambda t, s: f(t, s, **params)
    if transient > 0:
        x = solve_ivp(rhs, [0, transient], x, rtol=rtol, atol=atol,
                      method="DOP853").y[:, -1]
    y = x + d0 * np.ones_like(x) / np.sqrt(len(x))
    total, nsteps = 0.0, int(round(tmax / dt))
    for _ in range(nsteps):
        x = solve_ivp(rhs, [0, dt], x, rtol=rtol, atol=atol,
                      method="DOP853").y[:, -1]
        y = solve_ivp(rhs, [0, dt], y, rtol=rtol, atol=atol,
                      method="DOP853").y[:, -1]
        d = np.linalg.norm(y - x)
        total += np.log(d / d0)
        y = x + (y - x) * (d0 / d)
    return total / (nsteps * dt)


def lyapunov_spectrum_flow(f, jac, x0, tmax, /, dt=0.1, transient=0.0,
                           rtol=1e-9, atol=1e-12, **params):
    """All Lyapunov exponents of a flow dx/dt = f(t, x, **params).

    Integrates the state together with the variational equations
    dQ/dt = J(t, x) Q, and re-orthonormalises Q by a QR decomposition
    every ``dt`` (the QR trick of the discrete case). The exponents are
    the long-time averages of ln|R_ii| / dt, returned from largest to
    smallest. ``jac(t, x, **params)`` returns the Jacobian matrix of f;
    pass ``None`` for central differences. The first ``transient`` time
    units are integrated but not averaged. For the Lorenz system
    (sigma = 10, r = 28, b = 8/3) the exponents are about
    (0.906, 0, -14.57): one exponent is zero (the direction of the flow)
    and they add up to the mean divergence -(sigma + 1 + b).
    """
    x = np.asarray(x0, float)
    d = len(x)
    if jac is None:
        jac = lambda t, x, **p: _jac(f, t, x, **p)

    def rhs(t, s):
        x, Q = s[:d], s[d:].reshape(d, d)
        return np.concatenate([np.asarray(f(t, x, **params), float),
                               (jac(t, x, **params) @ Q).ravel()])

    Q = np.eye(d)
    t = 0.0
    if transient > 0:
        nt = int(round(transient / dt))
        for _ in range(nt):
            s = solve_ivp(rhs, [t, t + dt], np.concatenate([x, Q.ravel()]),
                          rtol=rtol, atol=atol, method="DOP853").y[:, -1]
            x, Q = s[:d], np.linalg.qr(s[d:].reshape(d, d))[0]
            t += dt
    total = np.zeros(d)
    nsteps = int(round(tmax / dt))
    for _ in range(nsteps):
        s = solve_ivp(rhs, [t, t + dt], np.concatenate([x, Q.ravel()]),
                      rtol=rtol, atol=atol, method="DOP853").y[:, -1]
        x = s[:d]
        Q, R = np.linalg.qr(s[d:].reshape(d, d))
        total += np.log(np.abs(np.diag(R)))
        t += dt
    return np.sort(total / (nsteps * dt))[::-1]
