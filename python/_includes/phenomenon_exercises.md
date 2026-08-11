## Exercises

### Sensitive dependence on initial conditions in the Lorenz System

Study the Lorenz system

```{math}
:label: eq0035:lorenzx
\begin{aligned}
\dot{x} &= \sigma(y-x)\\
\dot{y} &= rx - y -xz\\
\dot{z} &= xy-bz
\end{aligned}
```

with the parameters given $r=28,b=8/3,\sigma=10$. Start from the script shown in this chapter (or build it yourself from the {ref}`cookbook <app:cookbook>` recipes).

a) Run the script once and have a look at the time series of $x(t)$.

b) Plot the time series of $y(t)$ instead of $x(t)$ (you only need to change `sol1.y[0]` to `sol1.y[1]`). Study also $z(t)$.

c) Change the time range by modifying `tstart` and `tend`.

d) Add the second initial condition from the chapter so that you can study simultaneously the system's behaviour for two different initial conditions. The difference between the initial values of $x$ is `epsilon`. Reduce the value of `epsilon` and observe the effect.

e) Reduce `epsilon` until the solutions are no longer different. Increase `tend` to make sure. Can you understand this seemingly critical value of `epsilon`?

f) Make a plot of the 3d-*phase-space* by plotting $(x(t),y(t),z(t))$ instead of $(t,x(t))$, as shown in the chapter.

g) If everything went well you saw a so-called "strange attractor". Why it is called *strange* will be dealt with later, but to see that the object is really attracting, change the initial condition $x(0) = 2$ to $x(0) = 100$ and look at the trajectories in phase-space. Study other initial conditions and verify that the trajectories converge upon the *attractor*.

### Three body problem

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
 \omega = \sqrt{\frac{G(m_1+m_2)}{R^3} },
\end{gathered}
$$

where $r_1$ and  $r_2$ are the radii of earth and moon, and $\omega$ denotes the angular frequency. Using the law of gravitation $F=G\frac{m m'}{r^2}$, the motion of the satellite is governed by

$$
\mathbf{\ddot{x}} = G m_1 \frac{\mathbf{x}_1 - \mathbf{x}} {\left|\mathbf{x}_1 - \mathbf{x}\right|^3} + G m_2 \frac{\mathbf{x}_2 - \mathbf{x}} {\left|\mathbf{x}_2 - \mathbf{x}\right|^3}.
$$

Remarkably, this relatively simple system has very complex and rich behavior. `cb.threebody` implements this system (see the code linked beneath {numref}`fig:phenomenon_3body_some_examples`), and to magnify the chaotic behavior, we have increased the mass of the moon to $25 \%$ of the earth's mass.

a) Vary the satellite's initial position $x_0$ in the range $[-5\cdot10^8,5\cdot10^8]$ and determine for which interval the system behaves chaotic. Study also the system in a co-rotating reference frame (`cb.corotating`).

b) Check the sensitive dependence on initial conditions. Take $x_0=2 \times 10^8$ m and set the perturbation $\epsilon=1$ m. How many days does it take before there is a visual difference between the satellite's original and perturbed trajectory?

c) In reality the mass of the moon is a factor $81$ lower than the earth's. If you change this (`m2=7.36e22`), are there still chaotic trajectories? You may need to increase the initial velocity a bit.
