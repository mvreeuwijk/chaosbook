(chap:practice)=
# Chaos in practice

The book began with a paradox – that simple, entirely deterministic equations can produce behaviour that is impossible to predict in the long run – and has since assembled the geometric machinery needed to understand it: phase space and flows, fixed points and their stability, bifurcations and the routes to chaos, Lyapunov exponents, strange attractors and, in the previous chapter, their fractal geometry. All of this was developed on deliberately small systems, from one-dimensional maps to the three equations of Lorenz, precisely so that every idea could be computed and drawn.

The purpose of this final chapter is to look outward. The same handful of concepts – a finite horizon of predictability, a cloud of trajectories in place of a single one, an attractor of far lower dimension than the space it lives in – are not merely of historical interest. They are the working machinery of modern computational science, from weather forecasting and climate reanalysis to the reduced-order modelling of turbulence and the analysis of measured signals. We shall introduce no new mathematics. Instead we show that the reader has acquired a *way of thinking* about nonlinear systems, and follow it along two complementary lines. Because prediction has a finite horizon, we must *predict with ensembles, correct with data, and reduce with structure*; and where chaos is an asset rather than an obstacle, we can turn it to advantage – to mix, to control, and to reconstruct. Throughout, the Lorenz equations of chapter {numref}`chap:cont3d` serve as a concrete laboratory in which each idea can still be run on a desktop.

(sec:practice:horizon)=
## Prediction in an uncertain world

It is worth pausing to see why a weather forecast belongs in this book at all. A numerical weather model solves the equations of motion of the atmosphere – conservation of mass, momentum and energy for a rotating, stratified, moist fluid – on a grid covering the globe. Collecting every field value (three velocity components, temperature, pressure, humidity, …) at every grid point into a single enormous column vector $\mathbf{x}$, the model is nothing other than a system of ordinary differential equations

```{math}
:label: eq:practice:system
\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}),
```

of exactly the form {eq}`eq:cont3d:system` that we have studied since chapter {numref}`chp:conttwodim`. The only difference is one of scale: where the Lorenz system has three components, a modern forecast model has a state vector $\mathbf{x}$ whose dimension is of order $10^{9}$ ({numref}`fig:practice:weathermodel`).

```{figure} _static/practice/practice_weathermodel.png
:name: fig:practice:weathermodel
:width: 100%

A weather model is a dynamical system. The discretised atmospheric fields are stacked into one state vector $\mathbf{x}$ of dimension of order $10^{9}$, whose evolution obeys $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$. The Lorenz system is the same kind of object at the opposite extreme of dimension.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_structure.py)*
:::

This is more than an analogy. As shown in appendix {numref}`app:lorenz`, the Lorenz equations were themselves obtained by Galerkin-truncating a convection model until only three modes remained. The tiny system the reader now knows intimately and the billion-dimensional weather model are therefore *the same construction* seen at two extremes of dimension. Everything the book has established about {eq}`eq:practice:system` carries over: the forced–dissipative atmosphere is drawn onto an attractor – the *climate* – on which the ever-changing *weather* is nothing but the trajectory itself; the motion on that attractor has a positive Lyapunov exponent, and hence a sensitive dependence on initial conditions. It was in contemplating exactly this that Lorenz was led to his three equations, and it is this that makes weather prediction hard. The rest of the chapter simply pushes the familiar ideas up in dimension.

The first of these ideas concerns the limits of prediction. The central lesson of chaos is not that prediction is impossible, but that every prediction has a *finite horizon*. Two trajectories that start a distance $\delta_0$ apart separate, on average, as $\delta(t) \sim \delta_0\, \mathrm{e}^{\Lambda_e t}$, where $\Lambda_e$ is the effective Lyapunov exponent of chapter {numref}`chap:cont3d`. A forecast remains useful only until this error grows to the size of the attractor itself. For the Lorenz system, with $\Lambda_e \approx 0.9$ (section {numref}`sec:cont3d:strangeattractor`), an initial uncertainty of $\delta_0 = 10^{-3}$ grows to order ten in a time

$$
t_{\text{h}} \approx \frac{1}{\Lambda_e}\, \log\frac{\delta_{\text{att}}}{\delta_0} \approx \frac{1}{0.9}\log\frac{10}{10^{-3}} \approx 10,
$$

after which the forecast retains no information about the specific initial condition. The atmosphere behaves in exactly the same way; it is only the numbers that differ, giving the familiar horizon of a week or two for weather. Its effective growth rate is not a single constant, however, but varies with the flow regime and with the spatial scale of the feature one is trying to predict, so this horizon is itself only a typical value.

Since the initial state is never known exactly, the honest response is to abandon the single deterministic forecast and to propagate instead a whole *cloud* of initial conditions, each an equally plausible estimate of the true state. This is the idea of *ensemble forecasting*. Rather than one trajectory, one integrates many, and reads off the forecast not as a single number but as the distribution of the ensemble. The butterfly effect thereby ceases to be a curiosity and becomes an operational quantity: the *spread* of the ensemble is the forecast's own estimate of its uncertainty.

{numref}`fig:practice:ensemble` shows a Lorenz ensemble: a tight blob of initial conditions is stretched into a filament along the attractor and, by $t=8$, smeared across it entirely. The blob's growth is quantified in {numref}`fig:practice:horizon`, which tracks the ensemble spread $\delta(t)$. It grows exponentially at the rate $\Lambda_e = 0.9$ set by the Lyapunov analysis, until it saturates at the size of the attractor. The time at which the spread becomes an appreciable fraction of the attractor is the predictability horizon: beyond it, the ensemble members are effectively uncorrelated and only the climatological distribution remains.

```{figure} _static/practice/practice_ensemble.png
:name: fig:practice:ensemble
:width: 100%

An ensemble forecast for the Lorenz system, shown in the $(x,z)$ projection. A tight blob of initial conditions (left) is stretched into a filament by the flow, and eventually spread over the whole attractor. The width of the cloud is the forecast uncertainty.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_ensemble.py)*
:::

```{figure} _static/practice/practice_horizon.png
:name: fig:practice:horizon
:width: 80mm

Growth of the ensemble spread $\delta(t)$ for the blob of {numref}`fig:practice:ensemble`. The spread grows as $\mathrm{e}^{\Lambda_e t}$ with $\Lambda_e = 0.9$ (dashed) until it saturates at the size of the attractor (dotted). The predictability horizon is reached when the two meet.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_ensemble.py)*
:::

```{raw} html
<p><em>The same ensemble in motion, with its spread &mdash; press play or drag the slider:</em></p>
<iframe src="_static/practice/interactive/ensemble_spread.html" width="100%" height="460" style="border:none;"></iframe>
```

````{admonition} Python
:class: python

The ensemble is generated by integrating the Lorenz equations from a set of perturbed initial conditions and measuring how the cloud spreads. Starting from a point `x0` already on the attractor (obtained as in chapter {numref}`chap:cont3d` by discarding a transient), we draw `M` nearby initial conditions and integrate each.

```{code-block} python
import numpy as np
from scipy.integrate import solve_ivp
import chaosbook as cb

# a point on the attractor: integrate away a transient
x0 = solve_ivp(cb.lorenz, [0, 50], [1, 1, 1], rtol=1e-10, atol=1e-12).y[:, -1]

M    = 400                                      # ensemble size
eps0 = 1e-3                                     # initial spread
rng  = np.random.default_rng(2)
ics  = x0 + eps0 * rng.standard_normal((M, 3))  # perturb the initial state

# integrate all members at once, as one system of 3M equations
f = lambda t, Y: np.ravel(cb.lorenz(t, Y.reshape(3, M)))
t = np.linspace(0, 22, 2201)
sol = solve_ivp(f, [0, t[-1]], ics.T.ravel(), t_eval=t, rtol=1e-9, atol=1e-11)
cloud = sol.y.reshape(3, M, -1)                 # cloud[:, m, i]: member m at t[i]

# spread at each time t[i]: rms distance from the ensemble mean
dev   = cloud - cloud.mean(axis=1, keepdims=True)
delta = np.sqrt((dev**2).sum(axis=0).mean(axis=0))
```
````

````{admonition} Ensemble weather forecasting
:class: infobox

Operational weather centres run precisely this calculation, but with $\dim\mathbf{x}\sim 10^{9}$ instead of three. Because one cannot integrate millions of members, a modest ensemble of some 50 forecasts is launched from slightly perturbed initial conditions and slightly perturbed model physics {cite:p}`Lorenz1996,Bauer2015`. The spread of the ensemble at a given lead time *is* the forecast uncertainty: when the members agree, the forecast is confident; when they diverge, it is not. This is how a probability of rain is produced, and it is why forecasts now come with a horizon attached. The transformation of weather prediction from a single deterministic run into a routine estimate of its own uncertainty has been called a quiet revolution {cite:p}`Bauer2015`; at its root lies nothing more than the sensitive dependence on initial conditions of chapter {numref}`chap:cont3d`.
````

(sec:practice:assimilation)=
## Observations and models: data assimilation

A forecast needs a starting point, and here a second difficulty appears: the true state $\mathbf{x}$ is never known. We have instead a stream of noisy, incomplete *observations* – a scatter of measurements that constrains the state without determining it. Forecasting in practice is therefore a continuous cycle: *predict* the state forward with the model, *observe* it where measurements are available, and *correct* the prediction towards the observations, before predicting again. Combining a model with data in this way is called *data assimilation*, and it is once more an application of the dynamical system {eq}`eq:practice:system`.

The classical tool for the correction step is the *Kalman filter* {cite:p}`Kalman1960`. Its central idea is disarmingly simple: the corrected estimate, called the *analysis*, is a weighted average of the model forecast and the observation,

```{math}
:label: eq:practice:analysis
\mathbf{x}_a = \mathbf{x}_f + K\,(\mathbf{y} - H\mathbf{x}_f),
```

where $\mathbf{x}_f$ is the forecast, $\mathbf{y}$ the observation, and $H$ the operator that maps a state to the quantities actually measured. The quantity $\mathbf{y} - H\mathbf{x}_f$ is the *innovation*, the amount by which the observation surprises the forecast, and the *Kalman gain* $K$ is the weight applied to it. The gain is chosen by the relative confidence in model and data: writing $P$ for the covariance (the uncertainty) of the forecast and $R$ for that of the observations,

```{math}
:label: eq:practice:gain
K = P H^{\top}\,(H P H^{\top} + R)^{-1}.
```

When the observations are precise ($R$ small) the gain is large and the analysis follows the data; when the model is trusted ($P$ small) the gain is small and the analysis stays close to the forecast. The filter alternates two steps: a *forecast* step, in which both the state and its uncertainty $P$ are advanced by the model, and an *update* step {eq}`eq:practice:analysis`–{eq}`eq:practice:gain`, in which the incoming observation shrinks that uncertainty.

Advancing the uncertainty is the only subtlety. The textbook Kalman filter is linear, whereas $\mathbf{f}$ is not, so the covariance is propagated through the *linearisation* of the flow – and that linearisation is precisely the Jacobian $J$ already used to compute the Lyapunov exponents in chapter {numref}`chap:cont3d`. This is the *extended* Kalman filter. No new machinery is needed: over one assimilation window the forecast covariance evolves as $P_f = \Phi\, P_a\, \Phi^{\top} + Q$, where the state-transition matrix $\Phi$ is obtained by integrating $\dot{\Phi} = J\,\Phi$ with $\Phi(0)=I$, and $Q$ accounts for imperfections in the model.

{numref}`fig:practice:assimilation` shows the result of a *twin experiment* on the Lorenz system: we integrate a "truth" trajectory, generate noisy observations from it, and then try to recover it from a deliberately wrong initial guess. A free forecast, left to run without corrections, diverges from the truth within the predictability horizon of the previous section. The Kalman filter, fed the same noisy observations, locks onto the truth and tracks it indefinitely, its error held an order of magnitude below the free run. The finite horizon has not been abolished – it cannot be – but by repeatedly injecting information it is continually reset before the error can grow to saturation.

```{figure} _static/practice/practice_assimilation.png
:name: fig:practice:assimilation
:width: 100%

Data assimilation for the Lorenz system. Top: the $x$-component of the truth, a free forecast started from a wrong initial condition, and the Kalman-filter analysis fed noisy observations (dots). Bottom: the RMS error of the two estimates. The free forecast diverges within the predictability horizon; the analysis stays locked on.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_assimilation.py)*
:::

````{admonition} Python
:class: python

The filter is a short loop over the observation times. Between observations the state is advanced with `solve_ivp` and the covariance with the Jacobian `jac`; at each observation the analysis and its covariance are updated using the Kalman gain {eq}`eq:practice:gain`. The Jacobian is the same one used for the Lyapunov exponents in chapter {numref}`chap:cont3d`.

```{code-block} python
import numpy as np
from scipy.integrate import solve_ivp
import chaosbook as cb

sigma, r, b = 10.0, 28.0, 8/3
def jac(x, y, z):                                  # Jacobian of the Lorenz equations
    return np.array([[-sigma, sigma,  0],
                     [r - z,  -1,    -x],
                     [y,       x,    -b]])

def forecast(xa, dtobs):
    """Advance the state and solve dPhi/dt = J Phi over one window."""
    def rhs(t, s):
        Phi = s[3:].reshape(3, 3)
        return np.concatenate([cb.lorenz(t, s[:3]), (jac(*s[:3]) @ Phi).ravel()])
    s0 = np.concatenate([xa, np.eye(3).ravel()])   # Phi(0) = identity
    s = solve_ivp(rhs, [0, dtobs], s0, rtol=1e-9, atol=1e-11).y[:, -1]
    return s[:3], s[3:].reshape(3, 3)

# twin experiment: a "truth" run supplies the noisy observations y[k]
dtobs, Nobs = 0.2, 60
rng  = np.random.default_rng(7)
x0   = solve_ivp(cb.lorenz, [0, 50], [1, 1, 1], rtol=1e-10, atol=1e-12).y[:, -1]
tobs = dtobs * np.arange(1, Nobs + 1)
truth = solve_ivp(cb.lorenz, [0, tobs[-1]], x0, t_eval=tobs,
                  rtol=1e-9, atol=1e-11).y.T
y = truth + 1.5 * rng.standard_normal((Nobs, 3))

H  = np.eye(3)                                     # full state observed
R  = 1.5**2 * np.eye(3)                            # observation error
Q  = 0.01   * np.eye(3)                            # model error
I3 = np.eye(3)

xa = x0 + 8.0                                      # wrong first guess
Pa = 4.0 * np.eye(3)                               # its uncertainty

Xa = np.zeros((Nobs, 3))
for k in range(Nobs):
    # --- forecast: advance state and covariance over one window ---
    xf, Phi = forecast(xa, dtobs)
    Pf = 1.03 * Phi @ Pa @ Phi.T + Q               # (mild inflation)
    # --- update: blend the forecast with observation y[k] ---
    S  = H @ Pf @ H.T + R
    K  = Pf @ H.T @ np.linalg.inv(S)               # Kalman gain
    xa = xf + K @ (y[k] - H @ xf)                  # analysis
    Pa = (I3 - K @ H) @ Pf                         # reduced uncertainty
    Xa[k] = xa
```
````

Because the Lorenz system has only three variables, its error covariance $P$ is a $3\times 3$ matrix that can be stored and propagated exactly. This is what makes the example transparent, but it is also exactly what is *impossible* in an operational model, where $P$ would be a $10^{9}\times 10^{9}$ matrix that can be neither stored nor propagated. The extended Kalman filter is thus the natural nonlinear extension in principle but is unusable for global forecasting in practice, and overcoming this is the central technical problem of modern data assimilation. Two families of practical methods have emerged. *Ensemble* methods replace the explicit covariance with the sample covariance of a modest ensemble (section {numref}`sec:practice:horizon`), giving the *ensemble Kalman filter* {cite:p}`Evensen2003`, supplemented by localisation and inflation to control sampling error. *Variational* methods, on which the major operational centres principally rely, instead fit the model trajectory to a whole window of observations by numerical optimisation (the technique known as 4D-Var), and are increasingly combined with ensembles into hybrid schemes {cite:p}`Bauer2015`. The Kalman filter of {eq}`eq:practice:analysis` is best regarded as the conceptual prototype for all of these rather than the operational algorithm itself; what they share is unchanged from it – predict, observe, and correct in proportion to confidence.

Run this same cycle continuously on a model of one *specific* engineered system – an aircraft engine, a bridge, a patient's circulation – kept synchronised to its physical counterpart by a live stream of sensor data, and one has what engineering now calls a *digital twin*: data assimilation applied not to the planet but to a single machine, and often accelerated by the reduced-order surrogates of the next section.

````{admonition} Reanalysis: replaying the atmosphere
:class: infobox

Apply the same assimilation cycle to the historical record and one obtains a *reanalysis*. The model is run *forward* through decades of past observations, its state corrected within each assimilation window to be consistent with the measurements collected there – surface stations, radiosondes, aircraft, satellites. The ERA5 reanalysis {cite:p}`Hersbach2020` does this for the whole atmosphere since 1940 using incremental 4D-Var, combining model forecasts with the millions of observations of the global observing network into a statistically optimal, physically consistent reconstruction of the past atmosphere comprising hundreds of millions of prognostic variables. It rests on the same Bayesian philosophy as {eq}`eq:practice:analysis` – combining an imperfect model with imperfect data – scaled up to the whole planet, and it underlies much of what is quantitatively known about the changing climate.
````

(sec:practice:structure)=
## Finding simplicity in complexity

The billion dimensions of a weather model are, in a sense, an illusion. The system is strongly dissipative, so its trajectories collapse onto an attractor of far lower dimension than the space that contains them – exactly as the Lorenz flow, living in three dimensions, is confined to an attractor of fractal dimension only slightly above two (chapter {numref}`chap:fractals`). More generally, the essential dynamics of a high-dimensional dissipative system often unfold on a low-dimensional *manifold* ({numref}`fig:practice:manifold`), and the practical art is to find coordinates that expose it. This is the aim of *reduced-order modelling*. The picture should be read with some care: the precise object may be an attractor, an inertial, centre or slow manifold, and for a system as intricate as turbulence one can rarely prove that the dynamics collapse onto a single smooth low-dimensional manifold. What is robust – and what reduced-order modelling exploits – is that the *effective* number of active degrees of freedom is far smaller than the dimension of the state vector.

```{figure} _static/practice/practice_manifold.png
:name: fig:practice:manifold
:width: 85mm

Trajectories of a dissipative system, launched from scattered initial conditions in a high-dimensional state space, collapse onto a low-dimensional attracting manifold. Reduced-order models seek coordinates on this manifold.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_structure.py)*
:::

The oldest and most widely used of these methods is *proper orthogonal decomposition* (POD), known in other fields as principal component analysis. Given a collection of snapshots of a field – successive velocity fields of a turbulent flow, say – POD finds the fixed spatial patterns, or *modes*, ordered so that the first captures as much of the variance (the energy) as possible, the second as much of the remainder, and so on {cite:p}`Berkooz1993`. For flows with coherent structure, the energy is concentrated in a mere handful of modes, and the field can be reconstructed from them to good accuracy ({numref}`fig:practice:pod`). The high-dimensional field is thereby reduced to the evolution of a few modal amplitudes – a small dynamical system of the kind studied in this book.

```{figure} _static/practice/practice_pod.png
:name: fig:practice:pod
:width: 100%

Proper orthogonal decomposition of a field with low-dimensional structure. Left: the energy is captured almost entirely by the first three modes. Right: a single snapshot, reconstructed with one, two and three modes, converges rapidly to the full field; the residual is noise.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_structure.py)*
:::

POD organises a field by energy, but says nothing about its dynamics. A complementary idea is to seek modes that evolve simply *in time*. *Dynamic mode decomposition* (DMD) extracts from a sequence of snapshots the patterns that grow, decay and oscillate at definite rates {cite:p}`Schmid2010`, and is closely tied to the *Koopman* viewpoint ({numref}`fig:practice:koopman`): although the flow $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x})$ is nonlinear in the state, it acts *linearly* on functions of the state, the *observables* {cite:p}`Mezic2005`. In exchange for moving to a higher-dimensional space of observables, one recovers a linear description – with all the eigenvalues and modes that linearity brings – of a nonlinear system.

```{figure} _static/practice/practice_koopman.png
:name: fig:practice:koopman
:width: 90mm

The Koopman viewpoint. The flow is nonlinear in the state $\mathbf{x}$, but by lifting to a space of observables $g(\mathbf{x})$ it can be represented by a linear operator $\mathcal{K}$. Dynamic mode decomposition approximates this operator from data.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_structure.py)*
:::

POD, DMD and the Koopman operator are best seen not as competing techniques but as three expressions of a single idea: *finding low-dimensional structure in a high-dimensional system*. It is this idea, rather than any particular algorithm, that endures – and it is a direct descendant of the observation, made throughout this book, that dissipative chaotic systems live on attractors far smaller than their phase space.

The same idea underlies the more recent, and more fashionable, use of machine learning in dynamical systems. It is best regarded not as a replacement for the theory of this book but as one more way to do two familiar things: to *approximate* the nonlinear operator $\mathbf{f}$ of {eq}`eq:practice:system` when it is unknown or too expensive to evaluate, and to *discover* low-dimensional coordinates for a complex system when the linear modes of POD are not flexible enough. A neural-network surrogate that emulates an expensive model is doing the former; an autoencoder that compresses a high-dimensional field to a few latent variables is doing the latter, and its latent space is simply a nonlinear version of the attracting manifold of {numref}`fig:practice:manifold`. Presented this way, the methods are variations on the themes of the previous sections rather than a new subject, and we do not dwell on them here; the monograph of {cite:t}`Brunton2019` develops the connection between machine learning, dynamical systems and control at length.

(sec:practice:harness)=
## Harnessing chaos

The chapter so far has treated chaos as an adversary – something to be predicted around, corrected for, or compressed away. Yet the very properties that make a chaotic system hard to predict can also be put to use. Sensitive dependence stretches and folds, which is exactly what is needed to *mix*; the dense set of unstable orbits buried in an attractor makes it exquisitely *controllable*; and the way a single variable carries the imprint of the whole attractor lets us *reconstruct* the dynamics from one measured signal. We take these three in turn.

Stirring milk into coffee mixes it in seconds, but at the small scales of a microfluidic channel the flow is smooth and slow, and molecular diffusion alone would take an age. The way out is that a fluid element's *position* can behave chaotically even when the flow itself is simple and laminar – this is *chaotic advection* {cite:p}`Aref1984,Aref1986`. A convenient model advects each element $(x_n,y_n)$ on the unit square through one period of a time-periodic flow by two successive shears,

```{math}
:label: eq:practice:mixing
\begin{aligned}
x_{n+1} &= x_n + A\sin(2\pi y_n), \\
y_{n+1} &= y_n + A\sin(2\pi x_{n+1}),
\end{aligned}
```

with both coordinates taken modulo one so that the fluid stays on the square. This is a close relative of the standard map of chapter {numref}`sec:disc2d`: each shear merely slides fluid along one direction and so preserves area, as an incompressible flow must, yet for an amplitude $A$ of order one the map stretches and folds a blob of dye into ever finer filaments ({numref}`fig:practice:mixing`), until diffusion across the thin lamellae finishes the job. Shaping a real channel so that its flow is chaotic in this way is now a standard route to efficient micromixers for drug delivery and diagnostics, and the same mechanism stirs the mantle, the oceans and the atmosphere.

```{figure} _static/practice/practice_mixing.png
:name: fig:practice:mixing
:width: 100%

Chaotic mixing. Two blobs of dye advected by a simple time-periodic flow are stretched and folded into ever finer filaments and, within a few periods, interleaved throughout the domain – efficient mixing produced by a smooth, laminar flow.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_harness.py)*
:::

````{admonition} Python
:class: python

The map {eq}`eq:practice:mixing` is just the two shears applied in turn; the modulo operator `%` keeps the dye on the unit square by taking each coordinate modulo one. Iterating it on a thin streak of points reproduces the filaments of {numref}`fig:practice:mixing`.

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt

A = 0.9
def step(p):                                       # one period of the flow
    xn = (p[:, 0] + A * np.sin(2 * np.pi * p[:, 1])) % 1.0   # horizontal shear
    return np.column_stack([xn, (p[:, 1] + A * np.sin(2 * np.pi * xn)) % 1.0])

k = np.arange(101)
blob = np.column_stack([np.full(101, 0.25), 0.40 + 0.2 * k / 100])  # a thin streak of dye
for n in range(5):
    blob = step(blob)
plt.plot(blob[:, 0], blob[:, 1], ".", markersize=2)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
```
````

````{admonition} Coherent structures and ocean transport
:class: infobox

The same template scales up to the planet. In the ocean and atmosphere the stretching and folding organise themselves around hidden curves and surfaces – the *Lagrangian coherent structures* – that act as the transport barriers and conduits of the flow, the moving skeleton along which tracers are funnelled {cite:p}`Haller2015`. Computed from satellite-derived surface currents, they predict where an oil slick will spread or where a person lost at sea will drift; attracting structures were found to coincide with the observed extent of the *Deepwater Horizon* spill, and the same calculation now guides search-and-rescue operations and the tracking of drifting plastic. The fractal, folded interfaces of chapter {numref}`chap:fractals` and these coherent structures are two views of the one stirred, chaotic flow.
````

The second use turns sensitivity into control. A chaotic attractor is far from structureless: threaded through it is a dense set of *unstable periodic orbits*, each a perfectly regular motion that the system shadows briefly before sensitive dependence throws it off. Because the trajectory passes close to any chosen orbit sooner or later, and because sensitive dependence means a *tiny* nudge has a large effect, one can stabilise that orbit with vanishingly small, well-timed adjustments of a parameter – the method of {cite:t}`Ott1990`. {numref}`fig:practice:control` demonstrates it on the logistic map $x_{n+1} = r\,x_n(1-x_n)$ of chapter {numref}`sec:disc1d`. The target is its unstable fixed point $x^{*} = 1 - 1/r$, and the control at step $n$ is the change in growth rate that would send the current state exactly there; solving $(r+\delta r_n)\,x_n(1-x_n) = x^{*}$ gives

```{math}
:label: eq:practice:ogy
\delta r_n = \frac{x^{*}}{x_n(1-x_n)} - r,
```

applied only while it stays small, $|\delta r_n| \le \delta r_{\max}$. Because the orbit repeatedly strays near $x^{*}$, and a per-cent-level nudge is then enough to catch it, the once-chaotic iteration is captured onto the fixed point and held there indefinitely. A regular system would need a large control to be moved so far; it is precisely the chaos that makes such delicate steering possible. The same idea has been used to suppress the arrhythmic beating of cardiac tissue {cite:p}`Garfinkel1992` and to tame the flickering output of lasers.

```{figure} _static/practice/practice_control.png
:name: fig:practice:control
:width: 90mm

Controlling chaos. Left of the marker the logistic map ($r=3.9$) iterates chaotically. Once control is enabled it waits until the orbit strays near the target fixed point $x^{*}$ and then, with the minuscule parameter nudges $\delta r_n$ shown below, locks the motion onto it.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_harness.py)*
:::

````{admonition} Python
:class: python

Controlling the logistic map costs only a few lines: at each step, if the state is near the target $x^{*}$, nudge $r$ by the small amount {eq}`eq:practice:ogy` that would map it exactly onto the fixed point.

```{code-block} python
import matplotlib.pyplot as plt
import chaosbook as cb

r = 3.9
xstar, drmax = 1 - 1/r, 0.05                       # target orbit and largest nudge
x, orbit = 0.2, []
for n in range(1, 241):
    rr = r
    if n > 100:                                    # switch the controller on
        dr = xstar / (x * (1 - x)) - r             # nudge that would hit x*
        if abs(dr) <= drmax:
            rr = r + dr
    x = cb.logistic(x, rr)
    orbit.append((n, x))
plt.plot(*zip(*orbit), ".", markersize=6)
plt.xlabel("$n$")
plt.ylabel("$x_n$")
plt.show()
```
````

The third use reads chaos from data. In an experiment one seldom measures the full state; more often a single scalar is recorded – a voltage, a velocity at one point, the interval between drips of the faucet of chapter {numref}`sec:disc2d`. Remarkably, that lone time series is enough. *Takens' theorem* {cite:p}`Takens1981` guarantees that the vectors built from delayed copies of one coordinate, $(x_t,\, x_{t+\tau},\, x_{t+2\tau},\ldots)$, trace out a faithful copy of the original attractor, with the same dimension, Lyapunov exponents and topology. {numref}`fig:practice:reconstruction` rebuilds the Lorenz attractor from its $x$-coordinate alone. This *delay embedding* is what lets the box-counting and correlation dimensions of chapter {numref}`chap:fractals` be measured from a real signal, and it underpins the analysis of chaotic data across science – detecting the approach of an epileptic seizure from an EEG, diagnosing incipient faults in rotating machinery, and forecasting ecological and physiological records.

```{figure} _static/practice/practice_reconstruction.png
:name: fig:practice:reconstruction
:width: 100%

Attractor reconstruction. From the single recorded coordinate $x(t)$ of the Lorenz system (left), the delay-coordinate vectors $(x_t, x_{t+\tau}, x_{t+2\tau})$ trace out a reconstruction (right) with the same two-lobed topology as the original – the content of Takens' theorem.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_harness.py)*
:::

````{admonition} Python
:class: python

Reconstruction needs only a single recorded coordinate. If the array `X` holds the sampled values $x(t_i)$ of a Lorenz run, the delay vectors are formed and plotted directly.

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import chaosbook as cb

# X: the sampled values x(t_i) of a Lorenz run (after a transient)
sol = solve_ivp(cb.lorenz, [0, 130], [1, 1, 1],
                t_eval=np.arange(50, 130, 0.01), rtol=1e-9, atol=1e-11)
X = sol.y[0]

tau = 18                                           # delay, in samples
N   = len(X) - 2 * tau
emb = np.column_stack([X[:N], X[tau:N + tau], X[2 * tau:N + 2 * tau]])
ax = plt.figure().add_subplot(projection="3d")
ax.plot(*emb.T, linewidth=0.3)
plt.show()
```
````

````{admonition} Fingerprinting a chemical reactor
:class: infobox

The delay-embedding idea is not confined to the laboratory. Industrial *fluidised beds* and *bubble columns* – workhorses of the chemical industry – are strongly nonlinear and, in many operating regimes, chaotic. A single, cheaply measured pressure signal is enough to reconstruct their attractor, and the shape of that attractor, together with a measure of its unpredictability (the Kolmogorov entropy), serves as a *fingerprint* of the hydrodynamic state ({numref}`fig:practice:reactor`) {cite:p}`vandenBleek2002`. The chaotic-processes group at Delft – the very setting from which this book grew, with Floris Takens himself involved – turned this fingerprint into a suite of industrial tools: characterising flow regimes and their transitions, guiding the scale-up of reactors by matching attractors, and even *controlling* the bubbling. A small, energy-neutral feedback adjustment of the gas supply forces the bed onto a chosen unstable periodic orbit – the control idea of this section applied to a reactor – and was shown to raise the yield of a catalytic reaction by more than ten per cent. The same fingerprint drives an early-warning system: by continuously comparing the live attractor with a healthy reference one, the onset of particle *agglomeration* is caught long before a conventional pressure-drop alarm would trip, in time to keep the reactor from clogging solid.
````

```{figure} _static/practice/practice_reactor.png
:name: fig:practice:reactor
:width: 100%

The Takens route in industry (illustrative). A single measured signal – here a noisy chaotic time series standing in for the pressure in a fluidised-bed reactor (left) – is turned by delay embedding into a reconstructed attractor (right). The shape of this "fingerprint" characterises the operating regime, and changes in it give early warning of malfunction.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/practice/fig_harness.py)*
:::

(sec:practice:outlook)=
## Why nonlinear dynamics matters

The applications sketched here are far from solved problems. Predicting the coupled ocean–atmosphere system across the many scales of climate, closing the equations of turbulence, modelling living systems and steering large engineered networks all remain among the hardest challenges in computational science. What they share is the difficulty this book has been about from the start: they are nonlinear, high-dimensional and sensitive to their initial conditions, so that brute-force prediction fails and one must instead reason about ensembles, attractors and reduced descriptions.

We began by asking how a system as simple as a one-dimensional map or three coupled equations could defeat prediction. In answering it, you have acquired something more general than a catalogue of chaotic phenomena. The finite horizon that forces us to forecast with ensembles, the correction of models by data, the low-dimensional structure hidden inside high-dimensional systems, and the recognition that the same sensitivity can be turned to advantage – to mix, to control, to reconstruct – are not facts about the Lorenz equations; they are habits of thought that apply wherever nonlinear systems are modelled. You have not merely learned about chaos – you have learned to think about nonlinear systems, and that is a tool for the whole of modern science and engineering.

```{include} _includes/practice_exercises.md
```
