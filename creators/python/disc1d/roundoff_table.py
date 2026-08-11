"""Prints the round-off comparison table for the chapter: two
algebraically identical implementations of the logistic map,
r x (1 - x) versus r x - r x^2, iterated from the same x0."""

import numpy as np

N, r = 100, 3.9
X = np.zeros(N)
Y = np.zeros(N)
X[0] = Y[0] = 0.1
for n in range(N - 1):
    X[n + 1] = r * X[n] * (1 - X[n])
    Y[n + 1] = r * Y[n] - r * Y[n] ** 2

print("    n       X[n]          Y[n]        n      X[n]           Y[n]")
for n in range(25):
    print(f"   {n:2d}  {X[n]:12.10f}  {Y[n]:12.10f}    "
          f"{n + 75:2d}  {X[n + 75]:12.10f}  {Y[n + 75]:12.10f}")
