## Sensitive dependence on initital conditions in the Lorenz System

**Downloads:** {download}`LorenzSensitiveDependence_start.mws <_static/exercises/LorenzSensitiveDependence_start.mws>`, {download}`LorenzSensitiveDependence.mws <_static/exercises/LorenzSensitiveDependence.mws>`

Study the Lorenz system

```{math}
:label: eq0035:lorenzx
\begin{aligned}
\dot{x} &= \sigma(y-x)\\
\dot{y} &= rx - y -xz\\
\dot{z} &= xy-bz
\end{aligned}
```

with the parameters given $r=28,b=8/3,\sigma=10$.

Login on `Blackboard/ChaoticProcesses`, go to `Course Documents/01` and save the file  `LorenzSensitiveDependence_start.mws` on your computer. Start `Maple Classic` and load the file.

a) Execute the entire maple file once by clicking on the !!!*-button. Have a look at the time series of $x(t)$.

b) Plot the time series of $y(t)$ instead of $x(t)$. (Note: you only need to slightly modify the command `odeplot`). Study also $z(t)$.

c) Change the time range by modifying `tstart` and `tend`.

d) Delete the comment symbols `#‘ at the end of the file. Now you can study simultaneously the system’s behaviour for two different initial conditions. The difference between the initial values of $x$ is $\epsilon$. Reduce the value of $\epsilon$ and observe the effect.

e) Reduce $\epsilon$ until the solutions are no longer different. Increase `tend` to make sure. Can you understand this seemingly critical value of $\epsilon$?

f) Make a plot of the 3d-*phase-space* by plotting $[x(t),y(t),z(t)]$ instead of $[t,x(t)]$. Again you can do this with a minor change of the `odeplot`-command. You may want to increase `numpoints` as well, to get a smoother 3d-graph.

g) If everything went well you saw a so-called “strange attractor”. Why it is called *strange* will be dealt with later, but to see that the object is really attracting, change the initial condition $x(0) = 2$ to $x(0) = 100$ and look at the trajectories in phase-space. Study other initial conditions and verify that the trajectories converge upon the *attractor*.


## Classification of timeseries

**Downloads:** {download}`ClassifyingTimeseries.mws <_static/exercises/ClassifyingTimeseries.mws>`, {download}`SomeDatasets.mws <_static/exercises/SomeDatasets.mws>`

Open the Maple file `SomeDatasets.mws` to view different data sets `set1, set2, set3`. Find out which one is a: pure random noise, b: a one dimensional mapping, c: a higher order mapping. Explain your answer.


## Three body problem

**Downloads:** {download}`ThreeBody.mws <_static/exercises/ThreeBody.mws>`, {download}`ThreeBody_start.mws <_static/exercises/ThreeBody_start.mws>`, {download}`ex0036r03_fig1.pstex <_static/exercises/ex0036r03_fig1.pstex>`

Consider a satellite in space under influence of the gravitational pull of the earth and the moon.

```{figure} _static/exercises/ex0036r03_fig1.png
:name: fig:ex0036r03:ex0036r03_fig1
```

```{list-table}
:header-rows: 0
:class: noheader

* - gravitational constant
  - $G$
  - $6.67 \times 10^{-11}\ Nm^2 kg^{-1}$
* - distance between earth and moon
  - $R$
  - $3.84 \times 10^{8}\ m$
* - mass of earth
  - $m_1$
  - $5.97 \times 10^{24}\ kg$
* - mass of moon
  - $m_2$
  - $7.36 \times 10^{22}\ kg$
```

For simplicity, the orbits of earth and moon are assumed to be circular. Defining the position of the earth and moon as $\mathbf{x}_1$ and $\mathbf{x}_ 2$, respectively, and their mean distance as $R$, the motion is parametrized as

$$
\begin{gathered}
\mathbf{x}_1 =
 -r_1 \left[
 \begin{array}{c}
 \cos \omega t \\
 \sin \omega t
 \end{array} \right],\ \
 \mathbf{x}_2 =
 r_2 \left[
 \begin{array}{c}
 \cos \omega t \\
 \sin \omega t
 \end{array} \right], \\
 r_1 = R \frac{m_2}{m_1+m_2}, \ \ \
 r_2 = R \frac{m_1}{m_1+m_2}, \ \ \
 \omega = 2 \sqrt{\frac{G(m_1+m_2)}{R^3} },
\end{gathered}
$$

where $r_1$ and  $r_2$ are the radii of earth and moon, and $\omega$ denotes the angular frequency. Using the law of gravitation $F=G\frac{m m'}{r^2}$, the motion of the satellite is governed by

$$
\mathbf{\ddot{x}} = G m_1 \frac{\mathbf{x}_1 - \mathbf{x}} {\left|\mathbf{x}_1 - \mathbf{x}\right|^3} + G m_2 \frac{\mathbf{x}_2 - \mathbf{x}} {\left|\mathbf{x}_2 - \mathbf{x}\right|^3}.
$$

Remarkably, this relatively simple system has very complex and rich behavior. The worksheet `ThreeBody_start.mws` contains an implementation of this system and to magnify the chaotic behavior, we have increased the mass of the moon to $25 \%$ of the earth's mass.

a) Vary the satellite's initial position $x_0$ in the range $[-5\cdot10^8,5\cdot10^8]$ and determine for which interval the system behaves chaotic. Study also the system in a co-rotating reference frame.

b) Check the sensitive dependence on initial conditions. Take $x_0=2 \times 10^8$ m and set the perturbation $\epsilon=1$ m. How many days does it take before there is a visual difference between the satellite's original and perturbed trajectory?

c) In reality the mass of the moon is a factor $81$ lower than the earth's. If you change this, are there still chaotic trajectories? You may need to increase the initial velocity a bit.


## Attractor reconstruction

**Downloads:** {download}`LorenzReconstruct.mws <_static/exercises/LorenzReconstruct.mws>`, {download}`LorenzReconstructStart.mws <_static/exercises/LorenzReconstructStart.mws>`, {download}`LorenzConstruct.mws <_static/exercises/LorenzConstruct.mws>`, {download}`dataset1.txt <_static/exercises/dataset1.txt>`, {download}`dataset2.txt <_static/exercises/dataset2.txt>`

a) Study the data set `dataset1.txt`, which consists of a one-dimensional time series $xx[1]\ldots xx[N]$, “measured” with a constant sampling rate (i.e. with a constant time interval). Try to reconstruct the attractor by making a three-dimensional plot of the points $(xx[j], xx[j+\Delta j], xx[j + 2\Delta j])$, for all possible $j$. The maple command `spacecurve` may be useful in this respect. See also the file `LorenzReconstructStart.mws`. Change $\Delta j$ to get the best result.

b) Do the same for `dataset2.txt`, which has some additional noise superimposed.
