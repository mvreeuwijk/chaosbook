(app:twobody)=
# From the three-body problem to the planar restricted system

In the section on celestial uncertainties ({numref}`sec:phenomenon:celestial`) we studied the motion of a light satellite in the gravitational field of the earth and the moon. There we simply stated the four-dimensional set of equations that was integrated numerically. The purpose of this appendix is to show, step by step, how that compact system follows from Newton's law of gravitation together with three physically motivated simplifications. Along the way we take care to define every quantity that appears.

(app:twobody:full)=
## The full three-body problem

Consider three point masses $m_1$, $m_2$ and $m_3$ at time-dependent positions $\mathbf{x}_1(t)$, $\mathbf{x}_2(t)$ and $\mathbf{x}_3(t)$. Each position is a vector in three-dimensional space, so the complete state of the system is described by the three position vectors together with the three velocity vectors $\dot{\mathbf{x}}_i = \mathrm{d}\mathbf{x}_i/\mathrm{d}t$. As each of these six vectors has three components, the phase space of the full problem has dimension 18.

The only force acting is mutual gravitation. Newton's law of gravitation states that the attractive force exerted on body $i$ by body $j$ has magnitude

$$
f_{ij} = G\,\frac{m_i m_j}{\left|\mathbf{x}_j - \mathbf{x}_i\right|^2},
$$

where $G = 6.67\cdot 10^{-11}\,\text{N m}^2\,\text{kg}^{-2}$ is the universal gravitational constant and $\left|\mathbf{x}_j - \mathbf{x}_i\right|$ is the distance between the two bodies. The force points from body $i$ towards body $j$, i.e. along the unit vector $(\mathbf{x}_j - \mathbf{x}_i)/\left|\mathbf{x}_j - \mathbf{x}_i\right|$. Multiplying the magnitude by this unit vector and summing the contributions of the other two bodies, Newton's second law ($\text{mass}\times\text{acceleration} = \text{force}$) gives the equations of motion

```{math}
:label: eq:app:twobody:full
\begin{aligned}
m_1 \ddot{\mathbf{x}}_1 &= G m_1 m_2 \frac{\mathbf{x}_2 - \mathbf{x}_1}
 {\left|\mathbf{x}_2 - \mathbf{x}_1\right|^3}
 \,\,+\,\, G m_1 m_3 \frac{\mathbf{x}_3 - \mathbf{x}_1}
 {\left|\mathbf{x}_3 - \mathbf{x}_1\right|^3}\\
 m_2 \ddot{\mathbf{x}}_2 &= G m_2 m_1 \frac{\mathbf{x}_1 - \mathbf{x}_2}
 {\left|\mathbf{x}_1 - \mathbf{x}_2\right|^3}
 \,\,+\,\, G m_2 m_3 \frac{\mathbf{x}_3 - \mathbf{x}_2}
 {\left|\mathbf{x}_3 - \mathbf{x}_2\right|^3}\\
 m_3 \ddot{\mathbf{x}}_3 &= G m_3 m_1 \frac{\mathbf{x}_1 - \mathbf{x}_3}
 {\left|\mathbf{x}_1 - \mathbf{x}_3\right|^3}
 \,\,+\,\, G m_3 m_2 \frac{\mathbf{x}_2 - \mathbf{x}_3}
 {\left|\mathbf{x}_2 - \mathbf{x}_3\right|^3}.
\end{aligned}
```

Here the cube in the denominator arises because the $1/r^2$ magnitude is multiplied by the unit vector $(\mathbf{x}_j - \mathbf{x}_i)/\left|\mathbf{x}_j - \mathbf{x}_i\right|$, which contributes one more power of the distance. It is this coupled, nonlinear system of second-order equations that Poincaré proved cannot be solved in closed form in general.

(app:twobody:restricted)=
## Simplification 1: a negligible satellite mass

We now specialise to the earth–moon–satellite setting. The satellite ($m_3$) is extraordinarily light compared with the earth ($m_1$) and the moon ($m_2$); for the values in {numref}`table:phenomenon_3bodyconstants` the mass ratio is $m_1 : m_2 : m_3 = 100 : 1 : 10^{-19}$. Every term in {eq}`eq:app:twobody:full` that describes the pull of the satellite on a heavy body is proportional to $m_3$ and is therefore utterly negligible. Dropping those terms, the equations for the two heavy bodies (the *primaries*) decouple completely from the satellite:

```{math}
:label: eq:app:twobody:primaries1
\begin{aligned}
m_1 \ddot{\mathbf{x}}_1 &= G m_1 m_2 \frac{\mathbf{x}_2 - \mathbf{x}_1}
 {\left|\mathbf{x}_2 - \mathbf{x}_1\right|^3} \\
m_2 \ddot{\mathbf{x}}_2 &= G m_2 m_1 \frac{\mathbf{x}_1 - \mathbf{x}_2}
 {\left|\mathbf{x}_1 - \mathbf{x}_2\right|^3} ,
\end{aligned}
```

while the satellite still feels both of them,

```{math}
:label: eq:app:twobody:m3
\ddot{\mathbf{x}}_3 = G m_1 \frac{\mathbf{x}_1 - \mathbf{x}_3} {\left|\mathbf{x}_1 - \mathbf{x}_3\right|^3} \,\,+\,\, G m_2 \frac{\mathbf{x}_2 - \mathbf{x}_3} {\left|\mathbf{x}_2 - \mathbf{x}_3\right|^3} .
```

The problem has thus split into two parts: a self-contained two-body problem for the primaries, {eq}`eq:app:twobody:primaries1`–{eq}`eq:app:twobody:primaries1`, and the motion of the satellite, {eq}`eq:app:twobody:m3`, which is driven by the (now known) motion of the primaries. This is why the setting is called the *restricted* three-body problem.

(app:twobody:reduction)=
## Simplification 2: solving the two-body problem

The classical way to solve a two-body problem is to change to two new sets of coordinates: the *relative position* of the primaries,

$$
\mathbf{r} = \mathbf{x}_2 - \mathbf{x}_1 ,
$$

which is the vector pointing from the earth to the moon, and the *centre of mass*,

$$
\mathbf{r}_c = \frac{m_1 \mathbf{x}_1 + m_2 \mathbf{x}_2}{m_1 + m_2} ,
$$

which is the mass-weighted average position of the two primaries. Adding {eq}`eq:app:twobody:primaries1` and {eq}`eq:app:twobody:primaries1` makes the right-hand sides cancel, while subtracting them (after dividing each by its mass) combines the two attractions into a single term. The result is a pair of decoupled equations,

```{math}
:label: eq:app:twobody:rceq
\begin{aligned}
\ddot{\mathbf{r}}_c &= 0 ,\\
\ddot{\mathbf{r}} &= -G\,(m_1 + m_2)\,\frac{\mathbf{r}}{\left|\mathbf{r}\right|^3} .
\end{aligned}
```

{eq}`eq:app:twobody:rceq` states that the centre of mass is not accelerated at all: it moves in a straight line at constant velocity. We are free to observe the system from a frame of reference that moves along with the centre of mass, and in that frame we may set $\mathbf{r}_c = \dot{\mathbf{r}}_c = \mathbf{0}$ without any loss of generality. {eq}`eq:app:twobody:rceq` then describes a single fictitious body at position $\mathbf{r}$ attracted to the origin — exactly the mathematical form of a one-body central-force problem.

The bounded and unbounded solutions of {eq}`eq:app:twobody:rceq` are the well-known conic sections: circles, ellipses, parabolas and hyperbolas. We do not need their general form here. What matters is that once the relative motion $\mathbf{r}(t)$ is known, the individual orbits of the two primaries follow directly from the definitions of $\mathbf{r}$ and $\mathbf{r}_c$ (with $\mathbf{r}_c=\mathbf{0}$):

```{math}
:label: eq:app:twobody:x1x2gen
\mathbf{x}_1(t) = -\frac{m_2}{m_1+m_2}\,\mathbf{r}(t) , \qquad\qquad \mathbf{x}_2(t) = \frac{m_1}{m_1+m_2}\,\mathbf{r}(t) .
```

Each primary therefore traces out a scaled copy of the relative orbit, on opposite sides of the common centre of mass, with the lighter body (the moon) swinging out over the larger distance.

(app:twobody:circular)=
## Simplification 3: circular primary orbits in a plane

Of all the conic-section solutions we choose the simplest, a *circular* orbit of the primaries about their centre of mass,

```{math}
:label: eq:app:twobody:rcirc
\mathbf{r}(t) = R\left[\begin{array}{c} \cos\omega t \\ \sin\omega t \end{array}\right] ,
\qquad
\omega = \sqrt{\frac{G(m_1+m_2)}{R^3}} ,
```

where $R = \left|\mathbf{r}\right|$ is the (constant) earth–moon distance and $\omega$ is the angular frequency of the orbit. Substituting {eq}`eq:app:twobody:rcirc` into {eq}`eq:app:twobody:rceq` confirms that this is indeed a solution: the centripetal acceleration $\omega^2 R$ of the circular motion is exactly balanced by the gravitational attraction $G(m_1+m_2)/R^2$, which is the origin of the expression for $\omega$.

The final simplification concerns the satellite. If the satellite starts in the orbital plane of the two primaries and its initial velocity has no component out of that plane, then the gravitational pull it experiences always lies in the plane, and its trajectory can never leave it. We may therefore describe the satellite by two coordinates only. Dropping the subscript $3$ and writing $\mathbf{x}_3(t) = (x(t),\,y(t))$ for the satellite position, and introducing its velocity components $u = \dot{x}$ and $v = \dot{y}$, the second-order equation {eq}`eq:app:twobody:m3` becomes the first-order, four-dimensional system

```{math}
:label: eq:app:twobody:final
\dot{x} &= u \\
 \dot{y} &= v \\
 \dot{u} &= G m_1\,[x_1 - x]/d_{1}^{3} \,\,+\,\, G m_2\,[x_2 - x]/d_{2}^{3} \\
 \dot{v} &= G m_1\,[y_1 - y]/d_{1}^{3} \,\,+\,\, G m_2\,[y_2 - y]/d_{2}^{3} ,
```

in which $d_1$ and $d_2$ are the instantaneous distances from the satellite to the earth and to the moon,

```{math}
:label: eq:app:twobody:distances
d_1 = \sqrt{(x_1 - x)^2 + (y_1 - y)^2} , \qquad\qquad d_2 = \sqrt{(x_2 - x)^2 + (y_2 - y)^2} .
```

The primary positions $(x_1,y_1)$ and $(x_2,y_2)$ are prescribed by the circular solution {eq}`eq:app:twobody:rcirc` together with {eq}`eq:app:twobody:x1x2gen`:

```{math}
:label: eq:app:twobody:x1x2
\left[\begin{array}{c} x_1 \\ y_1 \end{array}\right]
 = -\frac{m_2 R}{m_1+m_2}
 \left[\begin{array}{c} \cos\omega t \\ \sin\omega t \end{array}\right] ,
 \qquad
 \left[\begin{array}{c} x_2 \\ y_2 \end{array}\right]
 = \frac{m_1 R}{m_1+m_2}
 \left[\begin{array}{c} \cos\omega t \\ \sin\omega t \end{array}\right] .
```

Because these positions depend explicitly on time, the satellite moves in a time-dependent force field; it is precisely this time dependence that opens the door to the chaotic behaviour observed in {numref}`sec:phenomenon:celestial`.

Equations {eq}`eq:app:twobody:final`–{eq}`eq:app:twobody:x1x2` are the compact, four-dimensional model quoted in the main text. Although the order of the system has been reduced from eighteen to four, it still cannot be solved analytically, and we resort to numerical integration to explore its rich dynamics.
