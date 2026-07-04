## Exercises

### Bouncing Ball

**Downloads:** {download}`BouncingBall.mws <_static/exercises/BouncingBall.mws>`, {download}`BouncingBallFixedPoint.mws <_static/exercises/BouncingBallFixedPoint.mws>`

The simplified and rescaled equations for the bouncing ball on an oscillating plate are

$$
\begin{aligned}
\phi_{n+1} &= (\phi_{n} + r v_{n})\,\text{mod}\, 2\pi \\
v_{n+1} &= k v_{n} + (1+k) \cos(\phi_{n+1})
\end{aligned}
$$

where $v_{n}$ represents the ball velocity after the bounce, $\phi_n$ the phase of the oscillating plate. The parameter $k$ is the collision parameter and is associated with the energy loss at a bounce ($0 < k \leq 1$). The parameter $r$ denotes the non-dimensional angular velocity of the plate.

a) Program these equation in `maple`. The modulo-function needs to be user-defined: `modf := (x,y) -> x - floor(x/y)*y`. Don't forget to put an `evalf(...)` in the loop.

b) Study the behaviour of this system by looking at the time series ($n,v_n$). Look also at plots of ($\phi_n,v_n$) and return plots of $v_n$. Set $k=0.3, r = 20$. Try also different values of $r$, and $k$.

c) Take $k = 0.545$ and $r=3.35$. Describe the behaviour of the system.

d) Take $k = 0.3$. Make a bifurcation diagram $v_n(r)$ for $r\in[1,10]$. Zoom in on $r\in[3,3.5]$.

e) Find a value for $r$ for which a fixed point is stable.

f) Prove analytically with `maple` that the fixed point is stable


### Dripping Faucet Model

**Downloads:** {download}`DrippingFaucetModel.mws <_static/exercises/DrippingFaucetModel.mws>`

Consider the following damped oscillation as a model for an oscillating droplet at (effective) position $y(t)$

$$
y(t) = \exp(-\delta
t) \left[ A \cos(\omega t) + B \sin(\omega t)\right]
$$

where $\delta$ is a damping factor, and $\omega$ the angular velocity. Differentiation with respect to $t$ yields an expression for the velocity $v(t)$. After expressing the constants $A$ and $B$ in terms of the initial position and velocity, $y^0$ and $v^0$, one arrives at the following system:

$$
\left( \begin{array}{c} y(t) \\ v(t) \end{array} \right) =
A(t) \left( \begin{array}{c} y^0 \\ v^0 \end{array} \right)
\,\,\,\,\,\text{with}\,\,\,
A(t) = \frac{e^{-\delta\,t}}{\omega}
\left( \begin{array}{cc}
\omega \cos\omega t + \delta \sin\omega t & \sin\omega t \\
-(\omega^2 + \delta^2) \sin\omega t & \omega \cos\omega t - \delta \sin\omega t
\end{array} \right)
$$

Remember that you may copy/paste from a previous exercise.

a) Program in maple the resulting equations for $y(t,y^0,v^0)$ and $v(t,y^0,v^0)$ as a function of three variables, i.e.

```{code-block} text
          y := (t,y0,v0) -> ....
          v := (t,y0,v0) -> ....
```

The droplet mass $m(t)$ is given by

$$
m(t) = m^{0} + \mu t
$$

where $\mu$ is the flow rate. Each droplet will snap at $t=T$ when $m(T) = m^c$.

The simplified and rescaled equations for a series of droplets $n=1\ldots N$ read

```{math}
:label: eq0090:t
\begin{aligned}
T_{n} &= \frac{m^c-m^{0}_{n}}{\mu}\\
m^{0}_{n+1} &= \frac{1}{2} m^c - \frac{1}{9} \,y(T_{n},y^{0}_{n},v^{0}_{n})\\
y^{0}_{n+1} &= 1\\
v^{0}_{n+1} &= v(T_{n},y^{0}_{n},v^{0}_{n})
\end{aligned}
```

Take $m^c = 1$, $\delta = 7.0$, $\omega = 60\pi$ and a flow rate of $\mu = 3$.

b) Program equations {eq}`eq0090:t` in maple and study the time series of $T_n$ for $\mu=3$. Take $m^{0}_{1} =\frac{1}{2} m^c$ $v^{0}_1 = 0$, $y^{0}_1 = 1$ to start the sequence. Take $N=200$. Show the time series and the return plot.

c) Set `Digits = 20`. Determine numerically an effective Lyapunov exponent $\Lambda$ for the system at these settings. To this end create a second series with $\tilde{v}^{0}_1 = v^{0}_1 + \epsilon$ with $\epsilon = 10^{-9}$ and find an for estimate $\Lambda$ from the differences between $\tilde{v}$ and $v$.

d) What value of $\Lambda$ do you find when instead you base it on the

e) Set $\mu=1$. Create a data set and show that a stationary situations is reached. Show that the system can be reduced to the second-order system

$$
\begin{aligned}
T_{n+1} &= f(T_n,v^{0}_{n})\\
 v^{0}_{n+1} &= g(T_{n},v^{0}_{n})
\end{aligned}
$$

and determine $f$ and $g$. Use this to show that the fixed point is indeed stable.


### Kicked U-tube

**Downloads:** {download}`KickedBubble.mws <_static/exercises/KickedBubble.mws>`, {download}`KickedBubble_Phase.mws <_static/exercises/KickedBubble_Phase.mws>`

Consider a U-tube filled with water in which air bubbles are injected at regular time intervals at the bottom. The waterlevel relative to the equilibrium level in the right leg is denoted by $\delta = h_2 - h_{eq}$. When the water is brought out of equilibrium, the system will respond by a damped oscillation which is governed by

$$
\ddot{\delta} + 2 \mu \dot{\delta} + \delta = 0,
$$

with $\mu \in [0,1]$ a frictional parameter.

```{figure} _static/exercises/ex0082r00_1.png
:name: fig:ex0082r00:ex0082r00_1
:width: 25mm
```

a) Verify that the solution to this equation is given by

$$
\begin{gathered}
\delta(t) = A(t) \delta_0 + B(t) \dot{\delta}_0, \\
 \dot{\delta}(t) = -B(t) \delta_0 + C(t) \dot{\delta}_0,
\end{gathered}
$$

with $\delta_0, \dot{\delta}_0$ the initial conditions and coefficients $A, B, C$ given by

$$
\begin{gathered}
A = e^{-\mu t}
 \frac{\mu \sin(\omega
t) + \omega \cos(\omega t)}{\omega} \\
 B = e^{-\mu t} \frac{\sin(\omega t)}{\omega} \\
 C = -e^{-\mu t}
\frac{\mu \sin(\omega
t) - \omega \cos(\omega t)}{\omega }.
\end{gathered}
$$

Here $\omega=\sqrt{1-\mu^2}$.

b) The bubbles are injected at regular time intervals $\tau$. A bubble entering the tube chooses one of the sides immediately, depending on the direction of the flow at that moment. Therefore, the waterlevel changes instantly in one of the legs and the water velocity is unchanged. This can be mathematically represented by

$$
\dot{\delta}_{new} = \dot{\delta}_{old},\ \ \ \ \ \delta_{new} = \delta_{old} - K \textrm{sgn}(\dot{\delta}_{old})
$$

Show that the dynamics of the U-tube with the bubbles are governed by the following discrete mapping:

$$
\begin{gathered}
\delta_{n+1} = A(\tau) \delta_n + B(\tau) \dot{\delta}_n - K
\textrm{sgn}(\dot{\delta}_{n+1}) \\
 \dot{\delta}_{n+1} = -B(\tau) \delta_n + C(\tau) \dot{\delta}_n
\end{gathered}
$$

Use the Maple command `signum` for the $\textrm{sgn}$ operator, and set `_Envsignum0 := 1` to change the default behavior of `signum(0)=0` to `signum(0)=1`.

c) Take $\mu=0.01$, $K=0.1$ and iterate at least 1000 steps to remove transients. Plot $(\delta_n, \dot{\delta}_n)$ for various $\phi \in [0, 1]$. Here $\phi$ is the ratio of bubble injection time and the oscillation time: $\phi = T_k / T_o = \tau / 2\pi$.

d) Create a bifurcation diagram at $K=0.1$ and $\mu=0.01$ for $\phi \in [0, 1]$. Is this an example of Feigenbaum's universality?

e) Take $\mu=0.01$, $K=0.1$ and $\phi=0.76$ and vary the initial conditions. Can this sensitive dependence on initial conditions be called chaos?

```{figure} _static/exercises/ex0082r00_2.png
:name: fig:ex0082r00:ex0082r00_2
:width: 80mm

Dependence of solution on initial conditions for $K=0.1$, $\mu=4.17 \times 10^{-3}$ and $\phi=0.76$.
```

f) Use the file `KickedBubble_Phase.mws` to study the behavior of the system in the phase space. For $K=0.1$, $\mu=0.01$ and $\phi=0.76$,  calculate the rotation number $\#revolutions/\#kicks$ for various initial conditions.

g) Take $K=0.1$ and calculate the period-1 solution. Note that there are two possibilities due to the `sgn` operator. Plot the locations in the plane for $\mu=0.01$, $\phi=0.76$ and verify numerically that this is indeed a fixed point.

h) Calculate the stability of the period-1 solutions and show (graphically or mathematically) that this solution is stable for all $\mu$ and $\tau$.
