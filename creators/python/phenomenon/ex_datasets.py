"""Data sets for the "Classification of timeseries" exercise.

set1.txt  uniform random noise
set2.txt  a one-dimensional mapping (logistic, r = 3.9)
set3.txt  a higher-order mapping (Henon x-coordinate)
"""

from pathlib import Path

import numpy as np

import chaosbook as cb

OUT = Path(__file__).resolve().parents[3] / "python" / "_static" / "exercises"
OUT.mkdir(parents=True, exist_ok=True)

N = 1000
rng = np.random.default_rng(seed=1)

np.savetxt(OUT / "set1.txt", rng.uniform(0, 1, N))

np.savetxt(OUT / "set2.txt", cb.orbit(cb.logistic, 0.4, N - 1, r=3.9))

x, y = np.zeros(N), np.zeros(N)
x[0], y[0] = 0.1, 0.1
for n in range(N - 1):
    x[n + 1] = 1 - 1.4 * x[n] ** 2 + y[n]
    y[n + 1] = 0.3 * x[n]
np.savetxt(OUT / "set3.txt", x)

print("ex_datasets: written to", OUT)
