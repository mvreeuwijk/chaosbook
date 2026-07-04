## Fixed Points and linearization

**Downloads:** {download}`FixedPointsLinearization.mws <_static/exercises/FixedPointsLinearization.mws>`

For each of the following systems, find the fixed points and classify them. Next plot the phase portrait with `maple`.

$$
\begin{aligned}
\dot{x} &= x-y,\,\,\,\dot{y} = x^2 - 4 \\
 \dot{x} &= 1+y-e^{-x},\,\,\,\dot{y} = x^3 - y\\
 \dot{x} &= xy-1,\,\,\,\dot{y} = x-y^3\\
\end{aligned}
$$


## Rabbits versus Sheep

**Downloads:** {download}`RabbitsSheep.mws <_static/exercises/RabbitsSheep.mws>`

A rabbit-sheep population with mutual competition can be modelled by the so-called Lotka-Volterra equations

$$
\begin{aligned}
\dot{N}_{1} &= r_1 N_1 \left( 1 - \frac{N_1}{K_1} \right) - a_1 N_1 N_2 \\
\dot{N}_{2} &= r_2 N_2 \left( 1 - \frac{N_2}{K_2} \right) - a_2 N_1 N_2
\end{aligned}
$$

where it is understood that always $N_1(t), N_2(t) \geq 0$. Furthermore $r_1, r_2 > 0$ and $b_1, b_2 \geq 0$.

a) Show that without loss of generality the equations can be rewritten to

$$
\begin{aligned}
\dot{x}_{1} &= r_1 x_1 ( 1 - x_1 ) - b_1 x_1 x_2\\
\dot{x}_{2} &= r_2 x_2 ( 1 - x_2 ) - b_2 x_1 x_2
\end{aligned}
$$

with  $x_1(t), x_2(t) \geq 0$.

b) Calculate all fixed points of this system. Give a biological interpretation of each fixed point.

In the sequel we take $r_1 = 3$, and $r_2 = 2$. (What do these value imply from a biological point of view?)



c) Look in the `cookbook.mws` for the command `phaseportrait` to make phase-plane plots. Do this for various values of $b_1$ and $b_2$. In particular, try $b_1 = 0, b_2 = 0$ (no competition); $b_1 = 1, b_2 = 2$; $b_1 = 3, b_2 = 1$; and $b_1 = 4, b_2 = 3$.

d) Calculate with `maple` the linear stability of the fixed points for the case studied in (c). See the `cookbook.mws` for calculating the eigenvalues of a matrix.

e) Take $b_1 = 1$. Find the critical value of $b_2$ such that the species can still co-exist.


## Predator-Prey with Alee effect

**Downloads:** {download}`PredatorPreyAlee.mws <_static/exercises/PredatorPreyAlee.mws>`

Consider the following *Predator-Prey* system

```{math}
:label: eq0055:2dc_n
\begin{aligned}
\frac{\mathrm{d} N}{\mathrm{d}t} &= r_1 N \left( \frac{N}{N+B} \right) -
\theta_{1} N P\\
\frac{\mathrm{d} P}{\mathrm{d}t} &= r_2 NP - \theta_{2} P^2
\end{aligned}
```

where $N(t) \geq 0$ is the number of prey and $P(t) \geq 0$ the number of predators at time $t$. The parameters $r_1, r_2, \theta_{1}, \theta_{2}$ are larger than 0. In the equations the factor $\left( \frac{N}{N+B} \right)$ represents the so-called Allee-effect, which takes into account the effect that larger populations have an advantage over small populations (“mate-finding”, for example, is easier). $B$ is a parameter ($\geq 0$).

a) Calculate the fixed points of the system ({eq}`eq0055:2dc_n`) in terms of the parameters $r_1, r_2, \theta_{1}, \theta_{2}, B$.

b) Show that without loss of generality one can also study the simpler system

```{math}
:label: eq0055:2dc_x
\begin{aligned}
\dot{x} &= \left( \frac{x^2}{x+b} \right) - \frac{xy}{a} \\
\dot{y} &= xy - y^2
\end{aligned}
```

and express the new parameters $a,b$ in terms of the old parameters $r_1, r_2, \theta_{1}, \theta_{2}, B$.

c) Calculate the fixed points of the system ({eq}`eq0055:2dc_x`).

Take $b = 1/2$ in the exercises below.

d) Calculate the stability-matrix $J$ of the non-zero fixed point. Find the characteristic polynomial of $J$ (use the maple command `CharacteristicPolynomial`($J$,$\lambda$)). Solve the eigenvalues $\lambda$ from the characteristic polynomial and express them in terms of the parameter $a$.

e) Can the system undergo a Hopf-bifurcation? If so, show analytically for which value of $a$?

f) Take $a = 0.75$. Show the phaseportrait of the system, together with the trajectory $\{x(t),y(t)\}$ for initial condition $x(0) = 0.4, y(0) = 0.25$.

g) Again take $a = 0.75$ and $x(0) =0.4$. Since the prey population at $t=0$ is larger than the equilibrium population, biologists have decided to intervene and increase the predator population to $y(0) = 0.25 + \delta$. However, to their utter disbelief they find both species to go rapidly extinct. Study the phaseportrait and trajectories for different $\delta$ and find an estimate for the minimal value of $\delta$ they must have used.


## Nuclear Reactor Cooling

**Downloads:** {download}`NuclearReactorCooling.mws <_static/exercises/NuclearReactorCooling.mws>`, {download}`NuclearReactorCooling.eps <_static/exercises/NuclearReactorCooling.eps>`

In a nuclear reactor, heat is carried away from the core by convection. Instead of actively forcing this convection by means of a pump, one can also make use of the density difference between the hot, boiling water in the riser and the cooled water in the downcomer to drive the system (see figure {numref}`fig:reactorsystem`). A large advantage of such an approach is that pump failure and resulting dangerous situations are avoided.

```{figure} _static/blank.png
:name: fig:reactorsystem

Natural convection reactor cooling
```

A simplified set of equations describing the change in mass flow rate and temperature in the riser is, respectively:

```{math}
:label: eqreactor1
\begin{gathered}
\dot{Q} = a T - b Q \\
 \dot{T} = c - d Q T
\end{gathered}
```

where $a$ accounts for the decrease in average density with higher temperatures, $b$ accounts for friction, $c$ is the normalized power $P$ and $d$ describes the loss of heat due to the outflow, all parameters being *always positive*.

a) Show that, without loss of generality, this set of equations can be written as:

```{math}
:label: eqreactor3
\begin{gathered}
\dot{x} = p^2 y - x \\
 \dot{y} = 1 - xy
\end{gathered}
```

b) Show that in the positive quadrant  $(x, y \geq 0)$, any fixed point is stable.

c) Find the value(s) for p where the stable fixed point changes in a stable spiral, and show phaseportraits of both cases.

d) Can you find a gradient system to rule out closed orbits? If so, which, and if not, why not?

e) Look at the sign of  $\nabla \cdot \dot{\mathbf{x}}$ in the positive quadrant. Can you explain in words why this makes closed orbits in this region impossible? (hint: use Green's theorem):

$$
\iint_A \nabla \cdot \dot{\mathbf{x}}\ \mathrm{d}A = \oint_S \dot{\mathbf{x}} \cdot \mathbf{n} \ \mathrm{d}s
$$
