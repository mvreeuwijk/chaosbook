# `MODELS.md` - canonical equations for the porting effort

Reference sheet of every dynamical system used to generate the book's figures, with the
standard form of the equations and the parameter values used in the text. Implement each
system **once** (see the suggested `chaos/maps.py` and `chaos/flows.py` in `README.md`); the
individual figures are then just different views of these systems.

> Parameter values marked *(confirm)* are the standard textbook values; verify against the
> corresponding worksheet in this folder, since the book occasionally uses its own scaling.
> The worksheet is always the ground truth for exact parameters, initial conditions and
> integration windows.

---

## 1. One-dimensional maps (`disc1d`)

Iterated as `x_{n+1} = f(x_n)`. Shared helpers to port: cobweb plot, time series, return
map (`x_{n+1}` vs `x_n`), bifurcation diagram, Lyapunov exponent `lambda = <log|f'(x)|>`,
invariant density (histogram of a long orbit).

### Logistic map  — `disc1d_logist_*`
$$ x_{n+1} = r\,x_n\,(1 - x_n), \qquad x\in[0,1],\; r\in[0,4]. $$
Representative `r` used in figure names: `r1_5`=1.5, `r2_0`=2.0, `r2_7`=2.7, `r3_2`=3.2,
`r3_5`=3.5, `r3_8`=3.8, `r3_9`=3.9. Fixed point `x*=1-1/r`; period-doubling cascade with
Feigenbaum constant `delta = 4.6692...`. Used for: series, cobweb, return map, p2/p3 graphs
(2nd/3rd iterate), stability, bifurcation (`disc1d_logist_bifur_theo`, `series_bifurcation`),
Lyapunov (`logist_lyap*`), invariant density (`logist_pdf`), analytical `r=4` solution
`x_n = sin^2(2^n pi theta_0)` (`logist_analytical`).

### Sine map  — `disc1d_*sinmap*`, `disc1d_sin3map_*`
$$ x_{n+1} = r\,\sin(\pi x_n), \qquad r\in[0,1]. $$
Second example of the same universality class as the logistic map (`universality_sinmap`,
`doubling_sinmap`). `sin3map` is used as an "unknown mapping" return-map example.

### Tent map  — `disc1d_tentmap_*`
$$ x_{n+1} = \mu\,\min(x_n,\,1-x_n) \quad\text{(or } \mu(1-|2x_n-1|)/? \text{)},\quad \mu\le 2. $$
Piecewise-linear; constant `|f'|=\mu` gives Lyapunov `log mu` directly. *(confirm exact form)*

### Shift / doubling map  — `disc1d_shiftmap_*`, `disc1d_doubling_*`
$$ x_{n+1} = 2 x_n \bmod 1. $$
Bernoulli shift; illustrates sensitive dependence via binary expansion.

### Feigenbaum / universality  — `feigen_newton_raphson_*`, `figtree_*`, `disc1d_universality_*`, `disc1d_not_so_universal`
Newton-Raphson location of superstable parameters and the Feigenbaum tree; ratio of
successive parameter gaps tends to `delta = 4.66920...`.

---

## 2. Two-dimensional maps (`disc2d`)

### Henon map  — `disc2d_Henon*`
$$ x_{n+1} = 1 - a\,x_n^2 + y_n, \qquad y_{n+1} = b\,x_n. $$
Classic parameters `a = 1.4`, `b = 0.3` *(confirm)*. Figures: strange attractor
(`HenonAttractor`), Lyapunov (`HenonLyap`), and the stretch-and-fold sequence
(`HenonStretch0..20`, `HenonFold0..5`) showing how a blob is stretched then folded each iterate.

### Standard (Chirikov) map / kicked rotor  — `disc2d_standardmap*`, `disc2d_kickedrotor`
$$ p_{n+1} = p_n + K\,\sin\theta_n, \qquad \theta_{n+1} = (\theta_n + p_{n+1}) \bmod 2\pi. $$
Area-preserving. Small `K`: invariant tori (`quasi`); larger `K`: chaotic sea (`chaos`).
`saddlenode` and `manifolds` figures show a periodic orbit's stable/unstable manifolds.

### Circle map  — `disc2d_circlemap`, `disc2d_lincirclemap`
$$ \theta_{n+1} = \Big(\theta_n + \Omega - \tfrac{K}{2\pi}\sin(2\pi\theta_n)\Big)\bmod 1. $$
`K=0` is the linear (rigid) rotation (`lincircle*`, quasiperiodic for irrational `Omega`);
`K>0` gives mode-locking / Arnold tongues. Lyapunov figure `circlemap_lyapunov`.

### Duffing map  — `disc2d_Duffing*`
$$ x_{n+1} = y_n, \qquad y_{n+1} = -b\,x_n + a\,y_n - y_n^3. $$
Series, phase, and bifurcation-in-x/y figures. *(confirm a,b in worksheet)*

### Particle-in-a-bowl / kicked oscillator  — `disc2d_bowl_*`, `disc2d_Paraball`
Impact/kick map of a particle in a potential bowl; periodic vs chaotic and an energy plot.

---

## 3. One-dimensional flows & normal forms (`cont1d`)

Flows `dx/dt = f(x; mu)`. Port helpers: `f(x)` graph with fixed points, time evolution from
several `x0`, and a bifurcation branch (stable/unstable) vs `mu`.

### Generic 1-D flow  — `cont1d_generic_graphical`, `cont1d_cubic*`
Graphical analysis: plot `f(x)`, mark stable/unstable fixed points where `f=0`. Cubic example
`f(x) = ...` with one/three fixed points; `cont1d_cubic_numsolution` integrates it.

### Bifurcation normal forms  — `cont1d_saddle`, `cont1d_transcrit`, `cont1d_bifur_pitchfork`, `cont1d_pitchfork_sub`, `normalforms.mws`
$$ \text{saddle-node: } \dot x = \mu - x^2, \qquad \text{transcritical: } \dot x = \mu x - x^2, $$
$$ \text{pitchfork (super): } \dot x = \mu x - x^3, \qquad \text{pitchfork (sub): } \dot x = \mu x + x^3. $$
Figures show the `f(x)` families (`_1/_2/_3` = below/at/above the bifurcation) and the
bifurcation diagrams (`normalforms.mws` -> `*bifurcation`, `*plots`).

### Mean-field ferromagnet (Curie-Weiss)  — `cont1d_ferro_*`, `cont1d_FerroSpins.mw`
Order parameter `m` (magnetisation) relaxes to the self-consistent solution:
$$ \dot m = -m + \tanh\!\Big(\frac{J m + h}{T}\Big). $$
Zero field `h=0`: **pitchfork** at the Curie temperature `T_c = J` (`ferro_pitchfork*`,
`ferro_pitch_evolution*`). Nonzero field: **hysteresis** loop in `m(h)` for `T<T_c`
(`ferro_field_hysteresis*`, `ferro_field_hysdata_T_*` at `T`=0.5,0.75,1.0,1.25,1.5). Spin
snapshots `ferro_spin_T_*_a/b*` visualise micro-states at `T`=0.5 and 1.5. Field-driven
bifurcation `ferro_field_bifurcation*`.

### Energy-balance climate model  — `cont1d_climate_*`
Global-mean temperature `T` with albedo feedback:
$$ C\,\dot T = \frac{Q}{4}\big(1 - \alpha(T)\big) - \varepsilon\sigma T^4, $$
`alpha(T)` a decreasing (ice-albedo) function. Gives one or three fixed points
(`climate_single_fp`, `climate_multiple_fp`) -> warm / cold / unstable states.

### Neural-network (Coolen) model  — `cont1d_NeuralNetwork*`, `cont1d_TonCoolen*` (files named `cont2d_TonCoolen*`)
Mean-field neural-network order-parameter dynamics (overlap `m`) of tanh/pitchfork type;
`P3` and `demo`/`v2` are variants. *(model details in worksheet)*

---

## 4. Two-dimensional flows (`cont2d`)

Phase-plane systems `d(x,y)/dt = f(x,y)`. Port helpers: trajectory integration, phase
portrait with nullclines (`implicitplot`), direction field (`fieldplot`), fixed-point
classification from the Jacobian eigenvalues.

### Lotka-Volterra predator-prey  — `cont2d_LV*.mws`
$$ \dot x = x\,(1 - y), \qquad \dot y = -\alpha\,y\,(1 - x), $$
book uses `alpha = 3/4`, initial condition `x(0)=y(0)=0.25` *(confirm scaling)*. Conserved
quantity `H = x + y - \ln(x^\alpha y)` (isocontours = orbits, `LV_E`). Figures: time series
(`LV_time`), phase portrait (`LV_phase`), constant of motion (`LV_E`).

### Lotka-Volterra with Allee effect  — `cont2d_LV_Allee*.mws`
LV with an Allee term added to the prey growth (extinction below a threshold): figures
`LV_Allee_extinct1/2`, stability `LV_Allee_stab_Re/Im`.

### van der Pol oscillator  — `cont2d_vdPol*.mws`
$$ \ddot x - \mu(1 - x^2)\dot x + x = 0 \;\Longleftrightarrow\; \dot x = y,\; \dot y = \mu(1-x^2)y - x. $$
Book uses `mu = 1`. Limit-cycle phase portrait (`vdPol_phase`).

### Hopf bifurcation  — `cont2d_Hopf*.mws`, `cont2d_Limit*.mws`, `cont2d_global*.mws`
Normal form (polar):
$$ \dot r = r(\mu - r^2), \qquad \dot\theta = \omega. $$
Supercritical Hopf: stable limit cycle of radius `sqrt(mu)` for `mu>0`. Figures: eigenvalues
crossing the axis (`Hopf_ev1/2`), before/after time series and phase (`Hopf_time*`,
`Hopf_phase*`), limit cycle (`Limit_time/phase`), global/relaxation behaviour (`global_*`).

### Conservative vs gradient systems  — `cont2d_conservative*.mws`, `cont2d_gradient*.mws`
Same surface `S(x,y)`, two dynamics:
$$ \text{conservative: } \dot x = \partial_y H,\ \dot y = -\partial_x H \quad(\text{orbits} = \text{level sets}); $$
$$ \text{gradient: } \dot{\mathbf x} = -\nabla S \quad(\text{flows downhill to minima}). $$
Double-well `S`; figures `conservative_E`, `gradient_ell1/2` (elliptic/min),
`gradient_hyp1/2` (saddle), `Esurface`.

### Pitchfork in 2-D  — `cont2d_pitchfork*.mws`
2-D system exhibiting a pitchfork: fixed-point branches (`pitchfork_fixed`), stability
(`pitchfork_stab`), phase portraits (`pitchfork_phase1/2`).

### Hand-drawn schematics (no worksheet)
`cont2d_phasespace`, `cont2d_classification`, `cont2d_classification2`,
`cont2d_phase_r1..r3`, `cont2d_phase_i1..i3` are the trace-determinant classification
diagrams - redraw with TikZ/matplotlib, no ODE integration needed. `cont2d_zoo` (gallery of
nonlinear phase portraits) has no located source - **confirm**.

---

## 5. Three-dimensional flows (`cont3d`)

### Lorenz system  — `cont3d_lorenz.mw` (and `phenomenon_lorenz.mw`, `new.mw`)
$$ \dot x = \sigma(y - x), \quad \dot y = x(\rho - z) - y, \quad \dot z = xy - \beta z, $$
classic `sigma = 10`, `rho = 28`, `beta = 8/3`. Figures: attractor (`lorenz_attractor`,
`attractoryz`), time series (`lorenz_time`, and the two-trajectory sensitivity runs
`phenomenon_lorenz_xt_two_series_em3/em5` started `1e-3`/`1e-5` apart), successive-maxima map
`z_n -> z_{n+1}` (`lorenz_map`, `zmax`), Poincare (`lorenz_poincare`), Lyapunov
(`lorenz_lyapunov*`, `LorenzLyapEffective/Comprehensive/Cumulative`), `r`-bifurcation
(`lorenzbifurcation`).

### Rossler system  — `cont3d_rossler.mw`
$$ \dot x = -y - z, \quad \dot y = x + a\,y, \quad \dot z = b + z(x - c). $$
Typical `a = b = 0.2`, `c` swept (period-doubling route to the folded-band attractor)
*(confirm)*. Figures: attractor & topology (`rosslerattractor`, `rosslertopology`), period-1/2/3/4
windows (`rosslerperiod1a..4b`), return map (`rosslerreturn`), Poincare (`rosslerpoincare`),
bifurcation (`rosslerbifurcation`).

### Poincare-section example  — `cont3d_poincare_example.mw`
Illustrates the Poincare-section construction: 3-D flow (`poincaresection`), example phase
(`poincare_exphase`), the induced map (`poincare_exmap`) and sequence (`poincare_exseq`).

### Forced / double-well oscillator  — `cont3d_forced.mws`
Periodically forced double-well (Duffing-type) oscillator in the extended 3-D
(`x, v, phase`) space: `doublewell`, `doublewell_phasespace`, `doublewell_poincare`.

### Restricted three-body problem  — `cont4d_3body.mw`, `phenomenon_3body_examples.mw`
Two primaries + massless test particle in the rotating frame; potential `V` and cut
(`cont4d_3body_V/Vcut`), several trajectories (`traj1..4`), Poincare
(`cont4d_3body_Poincare`), and the intro sensitivity examples
(`phenomenon_3body_example1a..3b`, `_sensitivity`, `_sensitivity_corot`). Effective potential
in the rotating frame includes the centrifugal term; use a high-accuracy symplectic or
`solve_ivp(rtol=1e-10)` integrator. The bare `3body` schematic is hand-drawn.

---

## Quick model -> figure lookup

| Model | Chapter(s) | Scripts (prefix) |
|-------|-----------|------------------|
| Logistic map | disc1d | `disc1d_logist_*`, `disc1d_doubling_logist` |
| Sine map | disc1d | `disc1d_*sinmap*`, `disc1d_sin3map_pdf` |
| Tent / shift map | disc1d | `disc1d_tentmap`, `disc1d_shiftmap_series` |
| Henon map | disc2d | `disc2d_Henon*` |
| Standard map / kicked rotor | disc2d | `disc2d_standardmap*`, `disc2d_kickedrotor` |
| Circle map | disc2d | `disc2d_circlemap`, `disc2d_lincirclemap` |
| Duffing map | disc2d | `disc2d_Duffing*` |
| Normal forms | cont1d | `cont1d_saddle`, `cont1d_transcrit`, `cont1d_*pitchfork*`, `normalforms` |
| Mean-field ferromagnet | cont1d | `cont1d_ferro_*`, `cont1d_FerroSpins` |
| Climate model | cont1d | `cont1d_climate_*` |
| Lotka-Volterra (+Allee) | cont2d | `cont2d_LV*` |
| van der Pol | cont2d | `cont2d_vdPol*` |
| Hopf / limit cycle | cont2d | `cont2d_Hopf*`, `cont2d_Limit*`, `cont2d_global*` |
| Conservative / gradient | cont2d | `cont2d_conservative*`, `cont2d_gradient*` |
| Lorenz | phenomenon, cont3d | `*_lorenz*` |
| Rossler | cont3d | `cont3d_rossler` |
| Restricted 3-body | phenomenon, cont3d | `*_3body*`, `cont4d_3body` |
