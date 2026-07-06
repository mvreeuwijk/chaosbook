## Exercises

### The predictability horizon

Consider the Lorenz equations with the standard parameters $\sigma=10$, $r=28$, $b=8/3$.

a) Starting from a point on the attractor, integrate an ensemble of $M=400$ initial conditions drawn from a small Gaussian blob of width $\delta_0$. Measure the ensemble spread $\delta(t)$ and verify that it grows as $\mathrm{e}^{\Lambda_e t}$ with $\Lambda_e \approx 0.9$, as in {numref}`fig:practice:horizon`.

b) Halve the initial spread $\delta_0$ and repeat. By how much does the predictability horizon increase? Explain, using the relation $t_{\text{h}} \approx \Lambda_e^{-1}\log(\delta_{\text{att}}/\delta_0)$, why improving the initial condition buys only a logarithmically longer forecast.

c) At what value of $\delta(t)$ does the exponential growth cease? Relate this saturation level to the size of the attractor.


### A Kalman filter for the Lorenz system

Reproduce the twin experiment of {numref}`fig:practice:assimilation`.

a) Integrate a "truth" trajectory and generate noisy observations of the full state at intervals $\Delta t_{\text{obs}} = 0.2$, adding Gaussian noise of standard deviation $1.5$ to each component. Starting from a deliberately wrong initial guess, run a free forecast (no assimilation) and confirm that it diverges from the truth within the predictability horizon.

b) Implement the extended Kalman filter of section {numref}`sec:practice:assimilation`, reusing the Jacobian $J$ of chapter {numref}`chap:cont3d` to propagate the covariance. Show that the analysis tracks the truth and that its RMS error stays well below that of the free forecast.

c) Study the effect of the observation frequency and noise. What happens as $\Delta t_{\text{obs}}$ is increased towards the predictability horizon? What happens if only the $x$-component is observed instead of the full state?


### Reduced-order structure

a) Build a synthetic field $u(x,t) = \sum_{k=1}^{3} a_k(t)\,\phi_k(x)$ from three fixed spatial patterns $\phi_k(x)$ whose amplitudes $a_k(t)$ are the three components of a Lorenz trajectory, and add a little noise. Form the snapshot matrix and compute its singular value decomposition.

b) Plot the singular values. How many modes are needed to capture $99\%$ of the energy, and how does this relate to the number of patterns you put in?

c) Reconstruct a single snapshot using one, two and three modes and compare with the full field, as in {numref}`fig:practice:pod`. What does the part that the leading modes fail to capture correspond to?
