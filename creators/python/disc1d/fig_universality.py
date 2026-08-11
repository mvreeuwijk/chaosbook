"""Universality / Feigenbaum figures for "Chaos in Iterative Maps".

Produces (in python/_static/disc1d/):
  disc1d_doubling_logist.png / disc1d_doubling_sinmap.png
  disc1d_universality_logist.png / disc1d_universality_sinmap.png
  disc1d_not_so_universal.png   delta(eta) for f = r(1-|2x-1|^eta)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import chaosbook as cb

STYLE = Path(__file__).resolve().parents[1] / "book.mplstyle"
plt.style.use(STYLE)

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

RC_LOGIST, RC_SINE = 3.56994537, 0.86557928

# -- plain bifurcation diagrams with the accumulation point marked -----------
for f, rmin, rmax, rc, name in [
    (cb.logistic, 2.8, 4.0, RC_LOGIST, "disc1d_doubling_logist"),
    (cb.sine, 0.6, 1.0, RC_SINE, "disc1d_doubling_sinmap"),
]:
    fig, ax = plt.subplots(figsize=(4.2, 3.2))
    cb.bifurcation_diagram(f, rmin, rmax, nr=600, n=1000,
                           x0=0.57, discard=0.8, ax=ax)
    ax.annotate("", xy=(rc, 0.02), xytext=(rc, 0.14),
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0, 1)
    ax.set_xlabel("$r$")
    ax.set_ylabel("$x(r)$")
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()

# -- rescaled diagrams: a = -ln(r_inf - r) -----------------------------------
for f, rc, rmin, amax, name in [
    (cb.logistic, RC_LOGIST, 2.8, 10.2, "disc1d_universality_logist"),
    (cb.sine, RC_SINE, 0.3, 10.2, "disc1d_universality_sinmap"),
]:
    amin = -np.log(rc - rmin)
    plt.figure(figsize=(4.2, 3.2))
    for a in np.linspace(amin, amax, 501):
        r = rc - np.exp(-a)
        X = cb.orbit(f, x0=0.57, n=1000, r=r)
        plt.plot([a] * 201, X[800:], ",", color="black")
    plt.xlim(amin, amax)
    plt.ylim(0.33, 0.9)
    plt.xlabel("$a$")
    plt.ylabel("$x(a)$")
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


# -- delta(eta) via Newton-Raphson on superstable orbits ---------------------
def superstable_r(f, df, p_max, r_start):
    """r_p of superstable 2^p cycles via Newton-Raphson from x0 = 1/2.

    f(x, r) maxes out at f(0.5, r) = r, so the map only stays inside [0, 1]
    while r < 1; a Newton step that overshoots past r = 1 sends the orbit
    outside [0, 1], where |2x-1|^eta explodes under further iteration and
    NumPy quietly hands back inf/NaN.  Also, every already-found r_q (q < p)
    is *trivially* a root of the period-2**p condition too (a period-q orbit
    repeats after any multiple of q steps), so a poorly chosen starting
    guess for small p can converge right back onto it instead of the new,
    higher-period root.  We fix both: every r_p is known a priori to lie in
    (r_{p-1}, 1), so (a) low periods (p < 3, where the extrapolated Newton
    guess isn't available yet) are located by bracketing + bisection on
    that interval instead of guessing a fixed start, and (b) every Newton
    step is clamped below 1, with a bracket/bisect fallback if the clamped
    iteration still fails to converge inside (r_{p-1}, 1).
    """
    def orbit_end(m, r):
        x = 0.5
        for _ in range(m):
            x = f(x, r)
        return x

    def bracket_and_bisect(m, lo, hi, n_scan=2000, refine=2):
        # Two passes of a vectorized scan for a sign change of g(r) =
        # X[m](r) - 0.5, each narrowing onto the bracket found by the last,
        # to get enough resolution even when consecutive r_p are very close.
        a, b = lo, hi
        for stage in range(refine):
            cand = np.linspace(a, b, n_scan)
            if stage == 0:
                cand = cand[1:]  # drop r=lo itself: a trivial root
            with np.errstate(all="ignore"):
                x = np.full_like(cand, 0.5)
                for _ in range(m):
                    x = f(x, cand)
                    x = np.clip(x, -1e3, 1e3)  # keep finite for sign()
                g = np.nan_to_num(x - 0.5, nan=0.0)
            idx = np.where(np.diff(np.sign(g)) != 0)[0]
            if len(idx) == 0:
                return None
            a, b = cand[idx[0]], cand[idx[0] + 1]
        ga = orbit_end(m, a) - 0.5
        for _ in range(80):
            mid = 0.5 * (a + b)
            gm = orbit_end(m, mid) - 0.5
            a, ga, b = (mid, gm, b) if np.sign(gm) == np.sign(ga) else (a, ga, mid)
        return 0.5 * (a + b)

    rc = {0: 0.5}  # f(0.5, r) = r identically, so r_0 = 0.5 for every eta
    for p in range(1, p_max + 1):
        m = 2**p
        lo, hi = rc[p - 1], 1.0
        if p < 3:
            r, converged = None, False
        else:
            delta = (rc[p - 2] - rc[p - 3]) / (rc[p - 1] - rc[p - 2])
            r = min(rc[p - 1] + (rc[p - 1] - rc[p - 2]) / delta, hi - 1e-13)
            converged = False
            with np.errstate(all="ignore"):
                for _ in range(100):
                    X = np.zeros(m + 1)
                    X[0] = 0.5
                    for n in range(m):
                        X[n + 1] = f(X[n], r)
                    dg = 0.0
                    for n in range(1, m + 1):
                        dg = X[n] / r + df(X[n - 1], r) * dg
                    if dg == 0 or not np.isfinite(dg) or not np.isfinite(X[m]):
                        break
                    rnew = min(r - (X[m] - X[0]) / dg, hi - 1e-13)
                    if abs(rnew - r) < 1e-13:
                        r, converged = rnew, True
                        break
                    r = rnew
            converged = converged and lo < r < hi
        if not converged:
            r = bracket_and_bisect(m, lo, hi)
            if r is None:
                raise FloatingPointError(f"p={p}: could not bracket a root")
        rc[p] = r
    return rc


etas, deltas = [], []
for eta in np.arange(1.2, 4.01, 0.2):
    f = lambda x, r, e=eta: r * (1 - np.abs(2 * x - 1) ** e)
    df = lambda x, r, e=eta: (-r * e * np.abs(2 * x - 1) ** (e - 1)
                              * np.sign(2 * x - 1) * 2)
    try:
        rc = superstable_r(f, df, 8, 0.9)
        deltas.append((rc[6] - rc[5]) / (rc[7] - rc[6]))
        etas.append(eta)
    except (ZeroDivisionError, FloatingPointError, OverflowError) as exc:
        print(f"fig_universality: dropping eta={eta:.2f} "
              f"(superstable_r did not converge: {exc})")

plt.figure(figsize=(5.0, 3.5))
plt.plot(etas, deltas, "ko-", markersize=5)
plt.axhline(4.6692, color="gray", linewidth=0.8)
plt.xlabel("$\\eta$")
plt.ylabel("$\\delta$")
plt.tight_layout()
plt.savefig(OUT / "disc1d_not_so_universal.png", dpi=150)
plt.close()

print("fig_universality: assets written to", OUT)
