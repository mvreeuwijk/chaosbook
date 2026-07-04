## Exercises

### Hysteresis

**Downloads:** {download}`Hysteresis.mws <_static/exercises/Hysteresis.mws>`

Study the equation

$$
\dot{x} = r x + x^3 - x^5
$$

where $r$ is a parameter of the system. The system undergoes a subcritical bifurcation.

*Analytical approach*:

a) Find an expression for the fixed points $x^{\star}$ for arbitrary $r$.



b) Plot $x^{\star}(r)$ as a function of $r$ and give each branch a different color.

c) Determine the stability of the branches.

*Numerical approach*:

d) Take $r=0.3$ and $x(0) = 0.1$; determine the numerical solution and plot the evolution of the system. Repeat this for $r=-0.1$.



e) Create a bifurcation diagram by plotting the numerically computed 'large time solutions' as a function of $r \in [-0.5,0.5]$ Increase $r$ in small steps, calculate the corresponding 'large time solutions', and take as the initial conditions the equilibrium solution of the previous(!) step. In this way you simulate a *slow* change of the parameter $r$: the system has time to equilibrate to the fixed points belonging to the new value of $r$.



f) Repeat the procedure of (e) for $r$ *decreasing* from 0.5 to -0.5.

g) Plot the results of (e) and (f) in the same graph, and give an explanation. You may want to include the branches obtained in (b) in the same plot.


### Stability and bifurcations

**Downloads:** {download}`PitchforkBifurcation.mws <_static/exercises/PitchforkBifurcation.mws>`

Consider the system

$$
\dot{x} = \frac{(\nu+\frac{1}{2})x + (\nu-\frac{1}{2})x^3}{1+x^2}
$$

with $\nu \leq 1/2$ a parameter.

a) Find the fixed points.

b) Classify the stability of each fixed points in terms of $\nu$.

c) Does the system exhibit a bifurcation? If so, indicate for which value of $\nu$, classify the kind of bifurcation, and plot a bifurcation diagram.

d) Set $\nu = 1/4$ and determine with Maple the numerical solution for the initial conditions $x(0) = 10^{-4}$ and $x(0) = 3$ and plot the time evolution.


### Stability and bifurcations (2)

**Downloads:** {download}`StabilityBifurcationsExp.mws <_static/exercises/StabilityBifurcationsExp.mws>`

Consider the system

$$
\dot{x} = f_{r}(x) \,\,\,\,\,\,\,\,\,f_{r}(x) = -2 - x + r \exp(-x^2)
$$

for $r\in [-10,10]$.

a) Find (numerically) all fixed points for $r=3$,

b) and classify their stability.

c) Specify the attraction domains of each these fixed points.

d) Plot $f_{r}(x)$ for different values of $r$ and determine from the plots how many bifurcations the system undergoes within the range $r\in [-10,10]$? Give a qualitative characterisation the type of bifurcations (saddle-node, transcritical, etc).

e) Prove analytically that the system undergoes a bifurcation when the stable fixed-points have the values $x_{1}^{*} =-1 - \sqrt{2}/2$, or $x_{2}^{*}=-1+\sqrt{2}/2$. Calculate the critical values $r_1$ and $r_2$ corresponding to the bifurcations at, respectively, $x_{1}^{*}$ and $x_{2}^{*}$.

f) Can this system exhibit hysteresis? If so, give a detailed description of the hysteresis cycle, for example by drawing a sketch (pen and paper) or by a numerical method.


### Earth's heat balance

**Downloads:** {download}`EarthHeatBalance.mw <_static/exercises/EarthHeatBalance.mw>`

The latitude dependent temperature of the Earth results from a balance between short-wave radiation received from the sun, and a loss due to long-wave radiation. A simplified equation describing this process is

```{math}
:label: eq0094:balance
\dot{T} = -\epsilon (T+273)^4 + w(T) \cos(\theta)
```

where $T$ represents the temperature in Celcius and $\theta$ the latitude $\in [0,90^\circ]$. Time has been rescaled by a characteristic timescale involving the heat capacity of the earth. The parameter $\epsilon$ denotes the effective long-wave emissivity. The term $w(T)$ incorporates the net absorption of short-wave radiation and depends on the surface properties (ice absorbs sunlight much less than water) and therefore on the local temperature. We approximate

$$
w(T) = a + b \,\text{erf}(c T)
$$

with $\text{erf}()$ the standard error-function, $a = 4.4\cdot10^9$, $b = 1.3 \cdot10^9$, $c = 0.2$. Furthermore, $\epsilon=0.5$.



a) Calculate all fixed points and their stability for $\theta = 0^\circ$, $\theta = 45^\circ$ and $\theta=60^\circ$. If there is more than one stable fixed point, specify the domain of attraction.

b) Give a (concise) physical interpretation of the results of (a).

c) Determine and plot a potential function $V(T)$ for $\theta = 45^\circ$.

d) Plot the time evolution of the temperature at $\theta = 45^\circ$ for two initial conditions: $T(0) = -100^\circ\,C$ and $T(0)=+100^\circ\,C$. Take $t_\infty = 10^{-6}$ for the maximum time (recall that time was rescaled).



e) Find graphically the latitude(s) for which a bifurcation occurs (just to get an indication). Next, specify the exact criterion, and calculate (numerically) from this the critical value(s) for $\theta$. What is the type of the bifurcation?
