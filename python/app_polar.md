(app:polars)=
# Transformation rules for polar coordinates

The relation between Cartesian coordinates and polar coordinates are

```{math}
:label: eq:polars:xy
x = r \cos (\theta), \quad y = r \sin (\theta)
```

Differentiating both sides with respect to time results in

```{math}
:label: eq:polars:dotx
\begin{aligned}
\dot{x} &= \dot{r} \cos (\theta) - r \sin (\theta) \dot{\theta} \\
 \dot{y} &= \dot{r} \sin (\theta) + r \cos (\theta) \dot{\theta}
\end{aligned}
```

Now note that

$$
\begin{aligned}
\sin(\theta) \dot{x} + \cos(\theta) \dot{y} &= \dot{r} \\
 \cos(\theta) \dot{y} - \sin(\theta) \dot{x} &= r \dot{\theta}
\end{aligned}
$$

Substituting $\sin{\theta}=y/r$ and $\cos(\theta) = x/r$ we obtain

```{math}
:label: eq:polars:dotr
\begin{aligned}
\dot{r} = \frac{x \dot{x} + y \dot{y}}{r} \\
 \dot{\theta} = \frac{x \dot{y} - y \dot{x}}{r^2}
\end{aligned}
```

Equations ({eq}`eq:polars:dotr`) are used to transform the ODE to polar coordinates. The inverse transform is defined by ({eq}`eq:polars:dotx`).
