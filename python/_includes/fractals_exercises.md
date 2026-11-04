## Exercises

::::{only} html
:::{button-link} lite/lab/index.html?path=fractals_lab.ipynb
:color: primary
:outline:

🧪 Launch the exercise lab — runs in your browser, nothing to install
:::
::::

### Correlation dimension

**Lab:** starter cell *Exercise: correlation dimension* in the exercise lab (button above).

a) Write a Python program to calculate the *correlation dimension* of a set of $N$ points $(x_n,y_n)$. Test it on $N=2000$ points of the Sierpinski gasket from the chaos game.

b) Calculate the correlation dimension of the dripping-faucet attractors of the exercise *Dripping Faucet Model* in chapter {numref}`sec:disc2d`. Compare the values with their box-counting dimension (section {numref}`sec:fractals:boxcounting`).


### Fractal Properties of the Forced Double Well Oscillator

**Lab:** starter cell *Exercise: fractal properties of the forced double-well oscillator* in the exercise lab (button above).

Consider a slender steel beam with a damping coefficient $f$ that is clamped in a rigid framework ({numref}`fig0121:3dc_sketch`). Two permanent magnets at the base pull the beam in opposite directions. The magnets are so strong that the beam buckles to one side or the other. The system is driven out of its equilibrium by shaking it with angular frequency $\omega$ and force $A$.

```{figure} _static/exercises/ex0121r00_fig1.png
:name: fig0121:3dc_sketch
:width: 80mm

Sketch of the mechanical system.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_exercises.py)*
:::

Written as an autonomous system of first order nonlinear differential equations, the system's behavior is defined by

```{math}
:label: eq0121:3dc_x
\begin{gathered}
\dot{x} = y, \\
\dot{y} = - f y + x - x^3 + A \cos z, \\
\dot{z} = \omega.
\end{gathered}
```

a) Run the starter cell for this exercise for $A=0.3$. This generates output like {numref}`fig0121:3dc_poincare`. What does this code-fragment do? What is the name of this plotting method? Why and when would this be useful?

b) Determine the box-dimension of this attractor.

```{figure} _static/exercises/ex0121r00_fig2.png
:name: fig0121:3dc_poincare
:width: 100mm

Result from executing the starter cell with $N=10000$.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_exercises.py)*
:::


### Fractal Curve

**Downloads:** {download}`FractalCurve.txt <_static/exercises/FractalCurve.txt>`

**Lab:** starter cell *Exercise: fractal curve* in the exercise lab (button above).

```{figure} _static/exercises/FractalCurve.png
:name: fig:ex0087r01:fractalcurve

Fractal Curve generation: first four recursive steps
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_exercises.py)*
:::

Consider the above sketched recursive generation of a family of fractal curves parameterized by $\phi$, with $0 \leq \phi \leq \pi/6$. Note that the three segments have equal size $a=a(\phi)$ and that $a\cos(\phi) \leq 1/2$.

a) Express the fractal dimension $d$ of the curve in terms of $\phi$ and plot the result.

b) Take $\phi = \pi/7$. After how many recursive steps is the length of the curve larger than 1 km?

c) The file `FractalCurve.txt` contains the points of a curve generated in this way (two columns, $x$ and $y$). Load the data set with `np.loadtxt` and calculate the fractal dimension of the curve using the box-counting method.


### Multi-fractals in threes

**Lab:** starter cell *Exercise: multi-fractals in threes* in the exercise lab (button above).

a) Generate a multi-fractal set with $N=3^6$ points, according to the formalism: $[1]\rightarrow [p_1,p_2,p_3] \rightarrow [p_{1}^{2}, p_{1}p_{2}, p_{1}p_{3}, \,p_{1}p_{2}, p_{2}^{2}, p_{2}p_{3}, \,p_{1}p_{3}, p_{2}p_{3}, p_{3}^{2}] \rightarrow \ldots$.

b) Take $p_{2} = 0$, and $p_{3} = p_{1} = 1/2$. Calculate analytically the fractal dimension (the box dimension).

c) Take $p_{2} = 0$, $p_{1} = 4/5$ and $p_{3} = 1/5$. Calculate analytically the generalized dimension $D(q)$.

d) Take $p_{2} = 0$, $p_{1} = 4/5$ and $p_{3} = 1/5$. Calculate the generalized dimension $D(q)$ by the box-counting procedure for $q \in [-10,10]$ (skip $q=1$). Plot the result and compare it with the analytical result of (c). (Hint: divide the boxes each time in three parts.)
