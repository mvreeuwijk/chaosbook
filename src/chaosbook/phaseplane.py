"""Phase-plane tools for two-dimensional flows  dx/dt = f(t, x, **params).

Every function works on any user-supplied right-hand side in the
``solve_ivp`` form ``f(t, state, **params)``; nothing here assumes the
bundled example systems in :mod:`chaosbook.flows2d`.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve


def jacobian(f, x, eps=1e-6, **params):
    """Numerical Jacobian of ``f(t, x, **params)`` at the state ``x``.

    Central differences; works for any dimension. Returns an (N, N) array
    with ``J[i, j] = d f_i / d x_j``.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    J = np.empty((n, n))
    for j in range(n):
        h = eps * max(1.0, abs(x[j]))
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        J[:, j] = (np.asarray(f(0.0, xp, **params), float)
                   - np.asarray(f(0.0, xm, **params), float)) / (2 * h)
    return J


def classify_fixed_point(J, tol=1e-9):
    """Eigenvalues and type of a fixed point from its 2x2 Jacobian.

    Returns ``(eigenvalues, kind)`` where ``kind`` is one of
    ``"stable node"``, ``"unstable node"``, ``"saddle"``, ``"stable spiral"``,
    ``"unstable spiral"``, ``"centre"`` or ``"degenerate"`` (a zero
    eigenvalue, where linearisation is inconclusive). The eigenvalues are
    sorted by decreasing real part. Real parts smaller than ``tol`` count
    as zero.
    """
    J = np.asarray(J, dtype=float)
    if J.shape != (2, 2):
        raise ValueError("classify_fixed_point expects a 2x2 Jacobian")
    ev = np.linalg.eigvals(J)
    ev = ev[np.argsort(-ev.real, kind="stable")]
    re, im = ev.real, ev.imag
    if abs(im[0]) > tol:  # complex-conjugate pair
        if abs(re[0]) <= tol:
            kind = "centre"
        else:
            kind = "stable spiral" if re[0] < 0 else "unstable spiral"
    elif np.any(np.abs(re) <= tol):
        kind = "degenerate"
    elif re[0] < 0:
        kind = "stable node"
    elif re[1] > 0:
        kind = "unstable node"
    else:
        kind = "saddle"
    return ev, kind


def fixed_points(f, guesses, tol=1e-8, **params):
    """Fixed points of ``f(t, x, **params)`` found by Newton from many guesses.

    ``guesses`` is an iterable of starting states. Returns an (m, N) array of
    the distinct converged roots (rows), sorted lexicographically.
    """
    roots = []
    for g in guesses:
        sol, _, ier, _ = fsolve(lambda s: f(0.0, s, **params), g,
                                full_output=True, xtol=1e-12)
        if ier == 1 and np.linalg.norm(f(0.0, sol, **params)) < tol:
            if not any(np.allclose(sol, r, atol=1e-6) for r in roots):
                roots.append(sol)
    return np.array(sorted(roots, key=tuple)) if roots else np.empty((0, len(guesses[0])))


def phase_portrait(f, xlim, ylim, ax=None, n=20, style="stream",
                   nullclines=False, trajectories=None, tmax=20.0,
                   colors=None, lw=2.0, color="0.45", **params):
    """Draw the phase portrait of a planar flow on ``ax`` and return the axes.

    * ``style="stream"`` draws streamlines of the vector field,
      ``style="quiver"`` draws a grid of ``n`` x ``n`` unit-length arrows
      (direction only), ``style=None`` draws no field.
    * ``nullclines=True`` adds the curves f_1 = 0 (solid) and f_2 = 0
      (dashed).
    * ``trajectories`` is a list of initial states; each is integrated for
      ``tmax`` with ``solve_ivp`` and drawn in ``colors`` (cycled).
    Extra keyword arguments are passed to ``f`` as parameters.
    """
    import matplotlib.pyplot as plt

    ax = ax if ax is not None else plt.gca()
    xs = np.linspace(*xlim, n)
    ys = np.linspace(*ylim, n)
    X, Y = np.meshgrid(xs, ys)
    U = np.zeros_like(X)
    V = np.zeros_like(X)
    for i in range(n):
        for j in range(n):
            U[i, j], V[i, j] = f(0.0, [X[i, j], Y[i, j]], **params)
    if style == "stream":
        ax.streamplot(X, Y, U, V, color=color, density=1.2, linewidth=0.8,
                      arrowsize=1.0)
    elif style == "quiver":
        norm = np.hypot(U, V)
        norm[norm == 0] = 1.0
        ax.quiver(X, Y, U / norm, V / norm, color="k", pivot="mid",
                  angles="xy", scale=n * 1.4, width=0.006)
    if nullclines:
        m = 200
        xf = np.linspace(*xlim, m)
        yf = np.linspace(*ylim, m)
        XF, YF = np.meshgrid(xf, yf)
        F = np.zeros((2, m, m))
        for i in range(m):
            for j in range(m):
                F[:, i, j] = f(0.0, [XF[i, j], YF[i, j]], **params)
        ax.contour(XF, YF, F[0], levels=[0], colors="tab:blue", linewidths=1.5)
        ax.contour(XF, YF, F[1], levels=[0], colors="tab:red", linewidths=1.5,
                   linestyles="--")
    colors = colors or ["tab:red", "tab:blue", "tab:green", "tab:orange"]
    for k, x0 in enumerate(trajectories or []):
        sol = solve_ivp(lambda t, s: f(t, s, **params), [0, tmax], x0,
                        rtol=1e-9, atol=1e-12,
                        t_eval=np.linspace(0, tmax, 4000))
        ax.plot(sol.y[0], sol.y[1], color=colors[k % len(colors)], lw=lw)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    return ax
