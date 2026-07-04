## Exercises

### Poincar\'{e

**Downloads:** {download}`PoincareSectionRossler.mws <_static/exercises/PoincareSectionRossler.mws>`

-section of the Rossler system}

Consider the Rössler system

```{math}
:label: eq0097:rosslerx
\begin{aligned}
\dot{x} &= -y-z\\
\dot{y} &= x+ay\\
\dot{z} &= b+z(x-c)
\end{aligned}
```

for $a=b=0.2, c=5$. Check out the `Cookbook.mws` how to obtain the numerical data in `Array` format. Integrate the system and remove the transient. (Take $dt=0.02$).

a) Calculate a Poincaré-section by selecting those instance when the trajectories traverse the $y=0$ plane from positive to negative. To this end loop through the data-points $n=1 \ldots N$, check when the condition $y[n-1]>0$ *and* $y[n]\leq 0$ is satisfied and store the *crossing*-coordinates $x_c = x[n],z_c = z[n]$ in a new array or list. Plot the point-series thus obtained in the $x-z$ plane.

b) Display the Poincaré-section and the attractor in the same plot.

c) Repeat the procedure for different values of $c$ between 2 and 6.


### Earth Magnetic Field

**Downloads:** {download}`EarthMagneticField.mws <_static/exercises/EarthMagneticField.mws>`

Consider the following system that was inpired on a simplified version of the equations governing the Earth's magnetic field.

$$
\begin{aligned}
\dot{x} &= -\frac{3}{4}x + zy \\
\dot{y} &= -b y +(z-1)x\\
\dot{z} &= 1-xy
\end{aligned}
$$

with $b>0$.

a) Show that this system is dissipative.

b) Substitute

$$
b=-\frac{1}{3}+\frac{(-3+2k^2)^2}{12k^4}\,\,\,\,\,\,\,\,\,\,\,\,\,\,k>0
$$

and show that $\{x_* = 1/k, y_* = k, z_* = 3/(4k^2)\}$ and $\{x_* = - 1/k, y_* = -k, z_* = 3/(4k^2)\}$ are both fixed points of the system. These turn out to be the only fixed points.

(eq0101:stab)=

c) Calculate the stability of the fixed points at $k=0.72$, and $k=0.75$.

d) Based on your stability analysis, was there a bifurcation between $k=0.72$ and $k=0.75$. If so, what kind?

(eq0101:num)=

e) Take $k=0.72$ and calculate a numerical solution for $t=500\ldots 1000$, starting with initial conditions in the neighbourhood of one of the fixed points: $x(0) = x_* + \epsilon, y(0) = y_* + \epsilon, z(0) = z_* + \epsilon$. Try $\epsilon = 0.5$ and $\epsilon = 1.0$ and plot the attractor in phase space.

f) Discuss the results of question {ref}`eq0101:num <eq0101:num>` with respect to the stability analysis conducted in question {ref}`eq0101:stab <eq0101:stab>`.


### Belousov-Zhabotinski reaction

**Downloads:** {download}`BelousovZhabotinski.mws <_static/exercises/BelousovZhabotinski.mws>`

The Belousov-Zhabotinski (BZ) reaction is a well-known chemical oscillator. It can be made by dissolving malomic acid and ammonium nitrate in sulfuric acid. When sodium bromate is added, the solution will oscillate between yellow and clear. The behaviour of the BZ-oscillator can be modeled by the Gaspard-Nicolis equations, which are given by

$$
\begin{gathered}
\dot{x}=\frac{1}{\epsilon} (z - a x^3 + b x^2 - c x), \\
\dot{y}=y (z + s x - l), \\
\dot{z}=z (d z - f y - x + g).
\end{gathered}
$$

Here $x,y,z$ are variables and the parameters have the values

$$
\begin{gathered}
a=0.5; b=3.0; c=5.0; \\
f=0.5; g=0.6; l=1.3; \\
s=0.3; \epsilon=0.01,
\end{gathered}
$$

and $d \in [0,1]$ is an adjustable control parameter. Use the initial conditions $x(0)=1$, $y(0)=1$ and $z(0)=1$.

a) Vary $d$ and plot a time series of $y$ with periodic behavior.

b) Vary $d$ and characterize the attractors by visualizing phase-space.

c) Calculate the fixed-points of the system as a function of $d$. Complex solutions and/or solutions with `RootOf` can be dismissed.

d) Use the fixed point with $d$-dependence and classify it for $d=0.25$ and $d=0.35$. What is the name of this bifurcation?

e) What does it mean when a dynamical system is called dissipative? Find an appropriate measure for the 'dissipativeness' of the system and plot its time-evolution for $d=0.5$.


### Signal transmission in neurons

**Downloads:** {download}`BVP.mws <_static/exercises/BVP.mws>`, {download}`ex0089r01_1.eps <_static/exercises/ex0089r01_1.eps>`

Neurons are a major class of cells in the nervous system whose main role is to process and transmit neural information. Normally, information is received through the dendrites and is sent through the axon, which can be tens to thousands of times the size of the cell body. The cell membrane in the axon and cell body contain voltage-gated ion channels which allow the neuron to generate and propagate an electrical impulse (an action potential).

```{figure} _static/exercises/ex0089r01_1.png
:name: fig:ex0089r01:ex0089r01_1
:width: 65mm
```

The axon can be modeled by combining the equations for an excitable membrane with the differential equations for an electrical core conductor cable, which gives a set of coupled non-linear partial differential equations. When the spatial variation of the voltages is negligible, these equations reduce to a set of coupled ordinary differential equations, known as the Bonhoeffer-van der Pol oscillator:

```{math}
:label: eq0089:xdot
\begin{gathered}
\dot{x} = x - \frac{1}{3} x^3 - y + A + B \cos(z), \\
 \dot{y} = \frac{1}{5} x -\frac{3}{10} y, \\
 \dot{z} = \omega.
\end{gathered}
```

Here $x$ represents the voltage over the membrane and $y$ a recovery variable. $z$ represents the phase angle of the excitation and $\omega$ is the angular frequency. The parameter $A \in [-1, 1]$ represents the DC-bias over the membrane, and $B \in [0, \frac{1}{2} ]$ the amplitude of the AC part of the excitation.

a) Convert this system to its non-autonomous equivalent.

b) In the following questions use the autonomous system. Take $A=0$ and $B=0$. Find the fixed points and determine their stability.

c) Can this system with $A=0$ and $B=0$ feature chaotic behavior? Explain your answer.

d) Take $A \in [-1, 1]$, $B=0$. For which range of $A$ are there three fixed points? Use `allvalues` if necessary.

e) Take $A=0$, $\omega=1$ and $B=0.25$. Create a plot of the solution of {eq}`eq0089:xdot` in the $(x,y)$-phase space. As initial conditions, use $x_0=0,y_0=1,z_0=0$. Does this become a periodic trajectory?



f) Take $A=0$, $\omega=1$ and $B \in [0, \frac{1}{2}]$. Create a stroboscopic Poincaré section by sampling the signal at $t_n = 2 \pi n$ and plotting the ($x_n, y_n$) phase-space. Over which interval of $B$ is the system chaotic?

g) Calculate the effective Lyapunov exponent for $B=0.38$.

h) Discuss the relationship between the Jacobian and the effective Lyapunov exponent.
