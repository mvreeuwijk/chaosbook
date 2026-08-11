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

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "disc1d"
OUT.mkdir(parents=True, exist_ok=True)

RC_LOGIST, RC_SINE = 3.56994537, 0.86557928

# -- plain bifurcation diagrams with the accumulation point marked -----------
for f, rmin, rmax, rc, name in [
    (cb.logistic, 2.8, 4.0, RC_LOGIST, "disc1d_doubling_logist"),
    (cb.sine, 0.6, 1.0, RC_SINE, "disc1d_doubling_sinmap"),
]:
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    cb.bifurcation_diagram(f, rmin, rmax, nr=600, n=1000,
                           x0=0.57, discard=0.8, ax=ax)
    ax.annotate("", xy=(rc, 0.02), xytext=(rc, 0.14),
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()

# -- rescaled diagrams: a = -ln(r_inf - r) -----------------------------------
for f, rc, rmin, amax, name in [
    (cb.logistic, RC_LOGIST, 2.8, 10.2, "disc1d_universality_logist"),
    (cb.sine, RC_SINE, 0.3, 10.2, "disc1d_universality_sinmap"),
]:
    amin = -np.log(rc - rmin)
    plt.figure(figsize=(5.4, 3.8))
    for a in np.linspace(amin, amax, 501):
        r = rc - np.exp(-a)
        X = cb.orbit(f, x0=0.57, n=1000, r=r)
        plt.plot([a] * 201, X[800:], ",", color="black")
    plt.xlim(amin, amax)
    plt.ylim(0.33, 0.9)
    plt.xlabel("a")
    plt.ylabel("x(a)")
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.png", dpi=150)
    plt.close()


# -- delta(eta) via Newton-Raphson on superstable orbits ---------------------
def superstable_r(f, df, p_max, r_start):
    """r_p of superstable 2^p cycles via Newton-Raphson from x0 = 1/2."""
    rc = {}
    for p in range(p_max + 1):
        m = 2**p
        if p >= 3:
            delta = (rc[p - 2] - rc[p - 3]) / (rc[p - 1] - rc[p - 2])
            r = rc[p - 1] + (rc[p - 1] - rc[p - 2]) / delta
        else:
            r = r_start
        for _ in range(100):
            X = np.zeros(m + 1)
            X[0] = 0.5
            for n in range(m):
                X[n + 1] = f(X[n], r)
            dg = 0.0
            for n in range(1, m + 1):
                dg = X[n] / r + df(X[n - 1], r) * dg
            rnew = r - (X[m] - X[0]) / dg
            if abs(rnew - r) < 1e-13:
                r = rnew
                break
            r = rnew
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
    except (ZeroDivisionError, FloatingPointError, OverflowError):
        pass

plt.figure(figsize=(5.2, 3.6))
plt.plot(etas, deltas, "ko-", markersize=5)
plt.axhline(4.6692, color="gray", linewidth=0.8)
plt.xlabel("eta")
plt.ylabel("delta")
plt.tight_layout()
plt.savefig(OUT / "disc1d_not_so_universal.png", dpi=150)
plt.close()

print("fig_universality: assets written to", OUT)
