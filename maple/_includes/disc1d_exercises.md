## Newton-Raphson method

**Downloads:** {download}`NewtonRaphson.mw <_static/exercises/NewtonRaphson.mw>`, {download}`ex0093r00.eps <_static/exercises/ex0093r00.eps>`, {download}`NewtonRaphson.fig <_static/exercises/NewtonRaphson.fig>`

The Newton-Raphson method provides a fast way to find solutions to equations like $3\tanh(x) = x^3$. More in general it will yield a zero-crossing $x^*$ of a function $g(x)$, i.e. a value of $x$ for which $g(x^*) = 0$. In the example above one would take $g(x) = 3\tanh(x) - x^3$. Starting with the initial value $x_0$ sufficiently close to $x^*$, the recipe for finding $x^*$ is to iterate the one-dimensional discrete map

```{math}
:label: eq0093:newtonraphson
x_{n+1} = f(x_{n})\,\,\,\,\,\,\,\,\,\text{with}\,\,\,\,\,\,\,\,f(x) = x - \frac{g(x)}{g'(x)}
```

Note that $x^*$ is a fixed point for the map $f$.

```{figure} _static/exercises/ex0093r00.png
:name: fig:ex0093r00:ex0093r00
:width: 70mm

A sketch of how the Newton-Raphson method iteratively locates a zero-crossing of $g(x)$.
```



a) Take $g(x) = 3\tanh(x) - x^3$ and program the Newton-Raphson method in `maple` by iterating the map {eq}`eq0093:newtonraphson` until $N = 20$. Start with $x_0 = 1.0$ and show the series.

b) Calculate the stability of the fixed point $x^*$. Does this answer explain the rapid convergence of the method?



c) Determine more in general the stability of the fixed point (zero crossing) $x^*$ for *arbitrary* functions $g$.

We will now study the method for the following function

```{math}
:label: eq0093:example
g(x) = \left[ \cosh\left( 4-\frac{3}{x} \right) - 1 \right]^{1/a}
```



d) Take $a =6$ and use the same program of question (a). Start with $x_0 = 0.4$ and show the series until $N = 100$. Show also the return-plot.

e) What is the stability of the fixed point $x^*=3/4$? How can you match this answer with your answer to question (c)?

f) Show a bifurcation diagram for $a=2\ldots 6$. At which value of $a$ is the fixed point no longer stable?

g) Study the bifurcation diagram and look for a value of $a$ for which a period-2 solution occurs. Prove its stability for this particular value of $a$.


## Cubic map

**Downloads:** {download}`CubicMap.mws <_static/exercises/CubicMap.mws>`

Consider the variation on the logistic map:

$$
x_{n+1} = \lambda x_n \left (1 - \frac{x^2_n}{\lambda} \right ) \,\,\,\,\,\,\,0 < \lambda < 3
$$

$\lambda$ is the free parameter of the mapping; we will take here $0 < \lambda < 3$.$\{ x_n \}$ is real valued.

a) Determine the fixed points. Discuss the role of $\lambda$ on the number of fixed points. Determine the stability of the fixed points (except for $\lambda = 1$).

b) Determine the maximum value of the initial condition $x_0$ for which the series $\{x_n\}$ stays finite for all $n$ (hint: use the cobweb diagram).

c) $\lambda = 1$ is a special case. Use the cobweb diagram to discuss the stability of the fixed point(s) for the case $\lambda = 1$. Calculate the region of attraction of the fixed point(s).

d) Consider the case $\lambda = 1.5$. Discuss the regions of attraction of the stable fixed point(s).

e) Consider the case $\lambda = 1.5$. Is a period 2 solution of the mapping possible? If yes, find the initial conditions for which the period 2 solution is found. Discuss the stability of the trajectory. If no, provide a proof that this is not possible.

f) Consider the case $\lambda = 2.2$. Is a period 2 solution of the mapping possible? Discuss the stability of the period 2 solution.

g) Discuss the possibility of a period 3 solution, $x_n \rightarrow x_{n+1} \rightarrow x_{n+2} \rightarrow x_{n+3} = x_n$, with $x_n \neq x_{n+1}$ and $x_n \neq x_{n+2}$ for $\lambda = 2.5$.


## Universality revisited

**Downloads:** {download}`UniversalityCounterExamples.mws <_static/exercises/UniversalityCounterExamples.mws>`

a) Make bifurcation diagrams of the following map:

$$
x_{n+1} = r (1- |2x-1|^{\eta}) \,\,\,\,\,\,x_0\in[0,1]\,\,\,\,\,\,r\in[0,1]
$$

for $\eta = 2$, and $\eta = 0.75$. For which values of $\eta$ do you observe the universal period doubling route, i.e. obeying Feigenbaum's constant? Explain your findings. Study other values of $\eta$. What about $\eta = 10$?

b) Investigate the following map within the context of universal behaviour

$$
x_{n+1} = 3.5 r(1-r) \sin(\pi x_n)\,\,\,\,\,\,x_0\in[0,1]\,\,\,\,\,\,r\in[0,1]
$$

Discuss your results.


## Discrete Cubic Map

**Downloads:** {download}`DiscreteCubicMap.mws <_static/exercises/DiscreteCubicMap.mws>`

Consider the following discrete map

```{math}
:label: eq0100:map
x_{n+1} = rx_{n}(3-4x_{n}^{2})
```

with $x_0 \in [-1,1]$ and $r \in [0,1]$.

a) Take $r=0.97$. Generate a series of $N=1000$ points starting from $x_0= 0.2$. Show the series and the return-plot.

b) Argue why $r$ must be within $[-1,1]$ to guarantee that all $x_n \in [-1,1]$ when $x_0 \in [-1,1]$.

c) Find the fixed-points of {eq}`eq0100:map` for $r\in[0,1]$, and determine their stability.

d) Show that

$$
x^{(2)} = \frac{\sqrt{2r(3r-\sqrt{9r^2-4})}}{4r}
$$

is a period-2 solution. Find the region of $r$ where this period-2 solution is stable.

e) Show a bifurcation diagram of the map over the range $r \in [0,1]$.

f) Take $r=1$ and set `Digits:=40`. Generate two series from slightly different initial conditions and estimate the Lyapunov-exponent.

We conjecture that for $r=1$ the following closed form can be obtained:

```{math}
:label: eq0100:solution
x_{n} = \sin(3^n \theta)
```

where $\theta$ is such that $x_{0} = \sin(\theta)$ is satisfied.

g) Show that {eq}`eq0100:solution` indeed satisfies {eq}`eq0100:map` for $r=1$. Does this imply that there is no predictability problem in this case? What can you say about the Lyapunov-exponent?
