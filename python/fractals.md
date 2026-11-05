(chap:fractals)=
# Fractal geometries

In the previous chapter we ran into a paradox. The Lorenz equations are dissipative: every volume of initial conditions in phase space shrinks to zero as $t\rightarrow\infty$. Yet the trajectories do not settle onto a fixed point or a limit cycle. They stay on the strange attractor, and on it they display a sensitive dependence on initial conditions. So the attractor can have no volume. But it cannot be a simple surface either, since a flow on a surface cannot be chaotic. We escaped from the paradox by claiming that the geometry of the attractor is *fractal*: its dimension is not an integer, but lies somewhere between two and three.

In this chapter we put this notion of a non-integer dimension on a firmer footing. We start with a few classical geometric constructions. For these the dimension follows analytically from the self-similarity of the object. We then turn to the more general *box-counting dimension* and the *correlation dimension*. Both can be determined numerically for an arbitrary set of points, such as a measured strange attractor. Finally we meet objects for which a single dimension is not enough, the *multifractals*, and characterize these by a whole spectrum of *generalized dimensions* $D_q$.

(sec:fractals:selfsimilar)=
## Self-similar fractals

A geometrical object is called *self-similar* when it is built up out of smaller copies of itself. The prototypical example is the *von Koch curve*. Its construction is sketched in {numref}`fig:fractals:koch`. One starts with a straight line segment of unit length, the *initiator*. This segment is replaced by four segments of length $1/3$, the middle two forming a triangular bump: this is the *generator*. The same operation is then applied to each of the four new segments, and so on *ad infinitum*. The limiting curve is continuous everywhere but differentiable nowhere. Its length is infinite, as we will see in a moment.

```{figure} _static/fractals/fractals_koch.png
:name: fig:fractals:koch

Construction of the von Koch curve. At each step every segment is replaced by four segments of one third of its length.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_selfsimilar.py)*
:::

The recursion is short to code, see the Python program below. We represent the points of the curve as complex numbers. The generator then replaces each segment by four; the extra vertex is the first third of the segment rotated over $\pi/3$, which raises the bump. The last line counts the segments and adds up their lengths.

````{admonition} Python
:class: python

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt

def gen(p, q):                                # Koch generator for one segment
    d = (q - p) / 3
    return [p, p + d, p + d + d * np.exp(1j * np.pi / 3), p + 2 * d]

pts = [0j, 1 + 0j]                            # unit segment (points as complex)
for k in range(4):                            # replace every segment, four times
    pts = [v for p, q in zip(pts[:-1], pts[1:]) for v in gen(p, q)] + [pts[-1]]
z = np.array(pts)
plt.plot(z.real, z.imag, "k")
plt.gca().set_aspect("equal")
print(len(pts) - 1, "segments, total length", np.abs(np.diff(z)).sum())
```
````

Run the program. After four generations it reports

```{code-block} text
256 segments, total length 3.160493827160494
```

Indeed, there are $4^4 = 256$ segments of length $3^{-4} = 1/81$ each, so the total length is $(4/3)^4 \approx 3.16$. Every generation multiplies the length by $4/3$. Now change the number of generations from 4 to 8 and run the program again. There are now 65536 segments and the length has grown to $(4/3)^8 \approx 9.99$, yet the curve on the screen looks exactly the same. This is the hallmark of self-similarity.

To assign a dimension to such an object, let us first recall how the ordinary dimension of a simple shape can be characterized. Cover the shape with smaller copies of itself, each scaled down by a factor $s<1$. A line segment of unit length needs $N=1/s$ copies of length $s$. A square needs $N=(1/s)^2$ copies of side $s$, and a cube $N=(1/s)^3$ copies. In each case the number of copies scales as

```{math}
:label: eq:fractals:similarity_scaling
N = \left(\frac{1}{s}\right)^{D},
```

where $D$ is the (integer) dimension of the object. Taking the logarithm of {eq}`eq:fractals:similarity_scaling` and solving for $D$ suggests the following definition of the *similarity dimension* of a self-similar object:

```{math}
:label: eq:fractals:similarity_dimension
D = \frac{\log N}{\log (1/s)},
```

where $N$ is the number of copies and $s$ the scaling factor of each copy. Note that nothing in {eq}`eq:fractals:similarity_dimension` forces $D$ to be an integer!

For the von Koch curve each segment is replaced by $N=4$ copies scaled down by $s=1/3$, so that

```{math}
:label: eq:fractals:koch_dimension
D = \frac{\log 4}{\log 3} \approx 1.2619.
```

The dimension is larger than one: the curve is so convoluted that it starts to fill the plane. But it is smaller than two, because the curve does not fill any area. This is exactly the kind of non-integer dimension that we anticipated for the strange attractor. One can also alter the generator, for instance by replacing the middle bump by four equal segments set at a different angle. In this way one constructs self-similar curves of any dimension between one and two. The dimension is a design parameter rather than a fixed number; the exercise *Fractal Curve* at the end of this chapter works this out.

Two further classical constructions will accompany us throughout this chapter. The *Cantor set* ({numref}`fig:fractals:cantor`) is obtained by repeatedly removing the middle third of a line segment. The unit interval is replaced by its two outer thirds, each of these by their outer thirds, and so on. At each stage the set consists of $N=2$ copies scaled by $s=1/3$, so that

```{math}
:label: eq:fractals:cantor_dimension
D_{\text{Cantor}} = \frac{\log 2}{\log 3} \approx 0.6309.
```

The Cantor set is an example of a *dust*: its dimension lies between zero (a point) and one (a line). It contains uncountably many points, yet its total length is zero. Indeed, after $k$ stages one is left with $2^k$ segments of length $3^{-k}$, with a total length of $(2/3)^k \rightarrow 0$.

```{figure} _static/fractals/fractals_cantor.png
:name: fig:fractals:cantor

The middle-third Cantor set. At each stage the central third of every segment is removed.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_selfsimilar.py)*
:::

The two-dimensional analogue is the *Sierpinski gasket* ({numref}`fig:fractals:sierpinski`). An equilateral triangle is divided by the midpoints of its sides into four congruent sub-triangles, and the central, inverted one is removed. Each of the three remaining triangles is treated in the same manner, and so on. Here $N=3$ and $s=1/2$, so that

```{math}
:label: eq:fractals:sierpinski_dimension
D_{\text{Sierpinski}} = \frac{\log 3}{\log 2} \approx 1.5850.
```

As expected the dimension lies between one and two. The gasket is pierced by holes on every scale, yet what remains still branches too densely to be a mere curve.

```{figure} _static/fractals/fractals_sierpinski.png
:name: fig:fractals:sierpinski

The first iterations of the Sierpinski gasket.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_selfsimilar.py)*
:::

```{raw} html
<p><em>Zoom into the gasket yourself (scroll or drag a box; double-click to reset):</em></p>
<iframe src="_static/fractals/interactive/sierpinski_zoom.html" width="100%" height="480" style="border:none;"></iframe>
```

````{admonition} Example
:class: example

Self-similar reasoning can be applied to areas and perimeters at the same time. The *Koch island* is obtained by applying the von Koch construction to each of the three sides of an equilateral triangle ({numref}`fig:fractals:kochisland`). The perimeter is a von Koch curve, and therefore has fractal dimension $D=\log 4/\log 3$. Let the initial triangle have unit sides, so that the initial perimeter is $P_0=3$. After $n$ steps each side consists of $4^{n}$ segments of length $3^{-n}$, so that the perimeter

$$
P_n = 3\left(\frac{4}{3}\right)^{n} \xrightarrow{n\rightarrow\infty} \infty
$$

diverges. The enclosed area, on the other hand, stays finite. Let us work this out. Call the initial area $A_0$. At step $n$ a triangular bump is added to every one of the $3\cdot 4^{n-1}$ segments present at that moment. Each bump is an equilateral triangle with side $3^{-n}$, and therefore has area $9^{-n} A_0$. The area added at step $n$ is thus

$$
\Delta A_n = 3\cdot 4^{n-1}\, 9^{-n} A_0 = \frac{3}{4}\left(\frac{4}{9}\right)^{n} A_0 .
$$

Summing the geometric series gives

$$
A_\infty = A_0 + \frac{3}{4} A_0 \sum_{n=1}^{\infty} \left(\frac{4}{9}\right)^{n}
 = A_0 + \frac{3}{4}\cdot\frac{4/9}{1-4/9}\, A_0 = A_0 + \frac{3}{5} A_0 = \frac{8}{5} A_0 .
$$

Consequently the *hydraulic diameter* $D_n = 4A_n/P_n \rightarrow 0$: the island encloses a finite area behind an infinitely long, infinitely wrinkled coastline. This is the sense in which {cite:t}`Mandelbrot1967` famously asked how long the coastline of Britain really is.
````

```{figure} _static/fractals/fractals_kochisland.png
:name: fig:fractals:kochisland

Construction of the Koch island.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_selfsimilar.py)*
:::

(sec:fractals:boxcounting)=
## The box-counting dimension

The similarity dimension {eq}`eq:fractals:similarity_dimension` is only defined for objects that are exactly self-similar. A strange attractor from a numerical simulation or an experiment is not built by an explicit recursive rule. We therefore need a definition of dimension that can be applied to *any* set of points. The *box-counting dimension* provides exactly this. It is in fact the more fundamental of the two: it is defined for any bounded set, and it is what one actually *measures* from data. The similarity dimension is the special case in which exact self-similarity lets us count the boxes by hand.

The idea is as follows. Cover the object with a grid of boxes of size $\varepsilon$, and count the number $N(\varepsilon)$ of boxes that contain at least one point of the set. For a smooth curve of length $\ell$ one needs $N(\varepsilon)\sim \ell/\varepsilon = \ell\, \varepsilon^{-1}$ boxes. For a smooth surface of area $\mathcal{A}$ one needs $N(\varepsilon)\sim \mathcal{A}\, \varepsilon^{-2}$. In general one expects

```{math}
:label: eq:fractals:boxcount_scaling
N(\varepsilon) \sim \varepsilon^{-D_0} \qquad (\varepsilon\rightarrow 0),
```

which motivates the definition of the box-counting dimension

```{math}
:label: eq:fractals:boxcount_dimension
D_0 = \lim_{\varepsilon\rightarrow 0} \frac{\log N(\varepsilon)}{\log (1/\varepsilon)}.
```

For the exactly self-similar objects of the previous section the box-counting dimension coincides with the similarity dimension. Choose $\varepsilon = s^{k}$ at the $k$-th generation. Then one needs exactly $N=N_{\text{copies}}^{k}$ boxes, and {eq}`eq:fractals:boxcount_dimension` reproduces {eq}`eq:fractals:similarity_dimension`. The subscript $0$ in $D_0$ anticipates the family of generalized dimensions introduced in section {numref}`sec:fractals:multifractal`; the box-counting dimension is the member $q=0$ of that family.

In practice one cannot take the limit $\varepsilon\rightarrow 0$. A data set contains a finite number of points, and a numerically generated fractal is only self-similar down to some smallest scale. Instead one evaluates $N(\varepsilon)$ for a range of box sizes and estimates $D_0$ from the slope of $\log N(\varepsilon)$ against $\log(1/\varepsilon)$. According to {eq}`eq:fractals:boxcount_scaling`, a plot of $\log N$ against $\log\varepsilon$ should be a straight line of slope $-D_0$ over the range of scales where the object is fractal.

````{admonition} Example
:class: example

Box-counting the von Koch curve makes the yardstick idea precise. Cover the curve with boxes of size $\varepsilon = 3^{-k}$. Each of the $4^{k}$ segments of the $k$-th generation lands in a single box, so that $N(\varepsilon) = 4^{k}$ and

$$
D_0 = \frac{\log 4^{k}}{\log 3^{k}} = \frac{\log 4}{\log 3} \approx 1.26,
$$

exactly the similarity dimension {eq}`eq:fractals:koch_dimension`. Put differently, measuring the curve with a ruler of length $\varepsilon$ returns an apparent length $L(\varepsilon) = N(\varepsilon)\,\varepsilon \propto \varepsilon^{\,1-D_0}$, which diverges as $\varepsilon\rightarrow 0$. The finer the yardstick, the longer the coastline. This is what the program of section {numref}`sec:fractals:selfsimilar` showed us: a ruler of length $3^{-4}$ returned a length of $3.16$, and a ruler of length $3^{-8}$ a length of $9.99$. Now feed the points of the eight-generation curve to the box-counting program below. One finds $D_0 = 1.27$, close to the exact value of $1.26$.
````

The Python program below implements the box-counting procedure for a set of $N$ points $(x_n,y_n)$ in the plane. Such a set could be the return plot of an experimental time series, like the dripping-faucet data of chapter {numref}`sec:disc2d`. Here we test the program on an object whose dimension we know: the Sierpinski gasket. The points are generated by the *chaos game*. Start at a corner of the triangle, pick one of the three corners at random, and jump halfway towards it. Repeat this $N$ times; the points visited fill the gasket. The box size is then reduced in geometric steps from the extent of the data down to about one hundredth of it, and at every size the occupied boxes are counted.

````{admonition} Python
:class: python

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt
import chaosbook as cb

# any pair of arrays (x_n, y_n) will do; here the points of a Sierpinski gasket
X, Y = cb.chaos_game(n=10000, seed=1)
dim, boxsize, boxcount = cb.box_dimension(X, Y)   # dim = minus the fitted slope
print(f"D0 = {dim:.3f}   (log 3 / log 2 = {np.log(3) / np.log(2):.3f})")

plt.plot(np.log(boxsize), np.log(boxcount), "o")
plt.xlabel(r"$\log\varepsilon$")
plt.ylabel(r"$\log N(\varepsilon)$")
```
````

The least-squares fit at the end returns a line $y = a\,x + b$ with $x=\log\varepsilon$ and $y=\log N(\varepsilon)$. By {eq}`eq:fractals:boxcount_scaling` the box-counting dimension is $D_0 = -a$, i.e. minus the slope. The program prints

```{code-block} text
D0 = 1.586   (log 3 / log 2 = 1.585)
```

With $N=10^4$ points we thus recover the analytical value of the gasket to two decimals. Now reduce the number of points and run the program again. With $N=2000$ points we find $D_0 = 1.51$, and with $N=1000$ points only $D_0 = 1.43$. The reason is visible in the plot of the box counts: the box-counting method only works over the range of scales that is adequately sampled by the data. When $N$ is too small, the finest boxes each contain at most one point. $N(\varepsilon)$ then saturates at $N$, and the slope flattens out. Too few data points therefore always lead to an *underestimate* of the dimension at small $\varepsilon$ ({numref}`fig:fractals:boxcount_fit`). The remedy is more points, or a fit restricted to the range of box sizes that is well sampled. A complete, self-contained version of this pipeline – generating a self-similar point set, counting occupied boxes over a range of sizes, and extracting the slope by a least-squares fit – is worked through in the {doc}`cookbook <app_cookbook>`.

```{figure} _static/fractals/fractals_boxcount_fit.png
:name: fig:fractals:boxcount_fit

Determination of the box-counting dimension from the slope of $\log N(\varepsilon)$ against $\log\varepsilon$.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_dimensions.py)*
:::

The same procedure applies without modification to the strange attractors of the previous chapters, since a Poincaré section turns a continuous flow into a cloud of points in the plane. Let us try it on the Lorenz attractor. We take the plane $z = r-1 = 27$, which passes through the centres of both lobes, and keep the downward crossings only. Integrating for 4000 time units gives 5331 crossings; see the code below.

````{admonition} Python
:class: python

```{code-block} python
from scipy.integrate import solve_ivp

# a point on the attractor, then the crossings of the section z = 27 (downward)
x0 = solve_ivp(cb.lorenz, [0, 50], [1, 1, 1], rtol=1e-10, atol=1e-12).y[:, -1]
t, P = cb.poincare_section(cb.lorenz, x0, 4000, (2, 27.0), direction=-1)
D0, boxsize, boxcount = cb.box_dimension(P[:, 0], P[:, 1])
print(f"{len(P)} points, D0 = {D0:.2f}")
```
````

The section consists of thin, folded strands, and the program prints

```{code-block} text
5331 points, D0 = 1.09
```

The dimension of the section is a little above one. The attractor itself has one dimension more, the direction along the flow, so that its dimension is slightly above two. This confirms what we anticipated in chapter {numref}`chap:cont3d` and resolves the volume-contraction paradox with which this chapter opened. The estimate is a rough one: the strands of the section are so thin that the fractal structure across them is only resolved by a very large number of points. More careful calculations give a dimension of about $2.05$ for the Lorenz attractor; we state this without proof and refer to {cite:t}`Strogatz1994`.

(sec:fractals:correlation)=
## The correlation dimension

The box-counting method treats all occupied boxes on the same footing, whether a box contains a single point or a thousand. For experimental attractors it is often more robust to look at the density of pairs of points that lie close together. This leads to the *correlation dimension*.

For a set of $N$ points $\mathbf{x}_1,\ldots,\mathbf{x}_N$ one defines the *correlation integral*

```{math}
:label: eq:fractals:correlation_integral
C(r) = \lim_{N\rightarrow\infty} \frac{1}{N^{2}}
 \sum_{\substack{i,j=1\\ i\neq j}}^{N}
 \Theta\bigl(r - \|\mathbf{x}_i - \mathbf{x}_j\|\bigr),
```

where $\Theta$ is the Heaviside step function. In words: $C(r)$ is the fraction of all pairs of points whose separation is smaller than $r$. If the points lie on a fractal object, the number of neighbours within a distance $r$ of a given point scales as $r^{D_2}$. Hence

```{math}
:label: eq:fractals:correlation_scaling
C(r) \sim r^{D_2} \qquad (r\rightarrow 0),
```

which defines the correlation dimension

```{math}
:label: eq:fractals:correlation_dimension
D_2 = \lim_{r\rightarrow 0} \frac{\log C(r)}{\log r}.
```

As with box-counting, $D_2$ is estimated in practice from the slope of $\log C(r)$ against $\log r$ over the scaling range. The correlation dimension is generally somewhat smaller than the box-counting dimension, $D_2 \leq D_0$. Equality holds only when the points are spread uniformly over the object. $D_2$ is the member $q=2$ of the family of generalized dimensions, as we will see in the next section.

The Python fragment below computes the correlation integral for the gasket points of the previous section. For every point the distances to all earlier points are sorted, and a binary search then counts how many of them are smaller than each of a set of logarithmically spaced radii between $r_{\min}$ and $r_{\max}$. Adding up these counts over all points gives the cumulative count $C(r)$.

````{admonition} Python
:class: python

```{code-block} python
# X, Y: the data set, as above
D2, r, C = cb.correlation_dimension(X, Y)   # C(r): pairs closer than r, at log-spaced r
print(f"D2 = {D2:.3f}   D0 = {dim:.3f}")

plt.loglog(r, C, "o")
plt.xlabel("$r$")
plt.ylabel("$C(r)$")
```
````

The slope of a straight-line fit to $\log C$ against $\log r$ yields the correlation dimension $D_2$ directly. For the gasket the program prints

```{code-block} text
D2 = 1.571   D0 = 1.586
```

The correlation dimension comes out slightly below the box-counting dimension of section {numref}`sec:fractals:boxcounting`, in line with the ordering $D_2 \leq D_0$. Here the two should in fact be equal, since the chaos game spreads its points uniformly over the gasket; the small difference is a finite-sample effect. For a set with a non-uniform density the two really differ, as we will see in the next section. For the dripping-faucet attractors the comparison is left as an exercise.

(sec:fractals:multifractal)=
## Multifractals and generalized dimensions

So far we have characterized a fractal object by a single number, its dimension. This is adequate when the points are distributed more or less uniformly over the object. Many attractors, however, are highly non-uniform. The trajectory spends far more time in some regions than in others, so that the *measure* is concentrated in a way that a purely geometric dimension cannot capture. Such objects are called *multifractals*. Their proper description requires not one dimension but a whole spectrum.

To make this quantitative, we cover the object with boxes of size $\varepsilon$ as before. But now we keep track of the fraction $p_i(\varepsilon)$ of the total measure that falls in box $i$. For a time series, $p_i$ is the fraction of time the trajectory spends in box $i$. We then form the partition sum

```{math}
:label: eq:fractals:partition_sum
Z(q,\varepsilon) = \sum_{i} p_i(\varepsilon)^{\,q},
```

where the sum runs over the occupied boxes and $q$ is a real parameter. Positive values of $q$ emphasize the densely populated boxes; negative values of $q$ emphasize the sparsely populated ones. In analogy with {eq}`eq:fractals:boxcount_scaling` one expects a power-law scaling $Z(q,\varepsilon)\sim \varepsilon^{(q-1)D_q}$, and one defines the *generalized dimension* of order $q$ as

```{math}
:label: eq:fractals:generalized_dimension
D_q = \frac{1}{q-1}\, \lim_{\varepsilon\rightarrow 0} \frac{\log \sum_i p_i^{\,q}}{\log \varepsilon}.
```

The prefactor $1/(q-1)$ is chosen such that $D_q$ reproduces the dimensions we already know for the special values of $q$:

- For $q=0$, $\sum_i p_i^{0}$ simply counts the number of occupied boxes
$N(\varepsilon)$, so that $D_0$ is the box-counting dimension {eq}`eq:fractals:boxcount_dimension`.
- For $q=2$, $\sum_i p_i^{2}$ is the probability that two randomly chosen
points fall in the same box, and $D_2$ is the correlation dimension {eq}`eq:fractals:correlation_dimension`.
- For $q\rightarrow 1$ the definition becomes indeterminate; taking the limit
carefully (l'Hôpital) yields the *information dimension*

```{math}
:label: eq:fractals:information_dimension
D_1 = \lim_{\varepsilon\rightarrow 0} \frac{\sum_i p_i \log p_i}{\log \varepsilon},
```

in which the numerator is (minus) the Shannon entropy of the box distribution.

The generalized dimensions form a non-increasing sequence, $D_q \geq D_{q'}$ for $q<q'$. For a *monofractal*, where the measure is spread uniformly, all $D_q$ are equal and the spectrum collapses to a single value. A genuine *multifractal* has a $D_q$ that decreases with $q$. The width of the spectrum, $D_{-\infty}-D_{+\infty}$, measures how non-uniform the object is.

(sec:fractals:binomial)=
### A binomial multifractal

The mechanism is best understood through an explicit construction. Consider the unit interval carrying a unit of “mass”. At the first step we split the interval into two equal halves. We give a fraction $p_1$ of the mass to the left half and $p_2 = 1-p_1$ to the right half. At the second step each half is again split in two, and its mass is redistributed in the same proportion $p_1 : p_2$, and so on. After $k$ steps the interval has been divided into $2^{k}$ sub-intervals of length $\varepsilon = 2^{-k}$. The measure in a sub-interval that is reached through a particular sequence of left/right choices is a product of the form

$$
p_i = p_1^{\,m}\, p_2^{\,k-m},
$$

where $m$ is the number of times the “left” branch was taken. This recursive assignment,

$$
[1] \rightarrow [p_1, p_2] \rightarrow [p_1^2,\, p_2 p_1,\, p_1 p_2,\, p_2^2] \rightarrow \ldots ,
$$

generates a self-similar *measure* on the interval ({numref}`fig:fractals:binomial`). For $p_1=p_2=\tfrac12$ the mass is spread uniformly and the object is monofractal. For $p_1\neq p_2$ it becomes increasingly spiky as $k$ grows, with the bulk of the measure concentrated on a vanishingly small fraction of the interval. Take for example $p_1 = 0.7$ and $k=9$, as in {numref}`fig:fractals:binomial`. The fullest of the 512 sub-intervals then carries a mass $0.7^{9} \approx 0.040$, the emptiest only $0.3^{9} \approx 2\cdot 10^{-5}$: a ratio of two thousand.

```{figure} _static/fractals/fractals_binomial.png
:name: fig:fractals:binomial

A binomial multifractal measure obtained by repeatedly redistributing the mass of each sub-interval in the ratio $p_1:p_2$.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_dimensions.py)*
:::

The generalized dimensions of this measure can be obtained analytically. The $2^{k}$ sub-intervals realize every combination of left/right choices, and there are $\binom{k}{m}$ of them with $m$ left choices. The partition sum {eq}`eq:fractals:partition_sum` therefore factorizes:

$$
Z(q,\varepsilon) = \sum_i p_i^{\,q} = \sum_{m=0}^{k} \binom{k}{m} \left(p_1^{\,m} p_2^{\,k-m}\right)^{q} = \left(p_1^{\,q} + p_2^{\,q}\right)^{k},
$$

where the last step uses the binomial theorem. With $\varepsilon = 2^{-k}$ we have $\log\varepsilon = -k\log 2$, and substitution into {eq}`eq:fractals:generalized_dimension` gives the closed-form result

```{math}
:label: eq:fractals:binomial_dq
D_q = -\,\frac{\log \left(p_1^{\,q} + p_2^{\,q}\right)}{(q-1)\,\log 2}.
```

One verifies immediately that $D_0 = \log 2/\log 2 = 1$: the measure lives on the whole interval, so the *support* is one-dimensional. The information about the non-uniformity is carried entirely by the dependence of $D_q$ on $q$. For $p_1=p_2=\tfrac12$ equation {eq}`eq:fractals:binomial_dq` gives $D_q = 1$ for all $q$ (monofractal). For $p_1\neq p_2$ the dimension $D_q$ decreases monotonically from $D_{-\infty}$ to $D_{+\infty}$, producing the characteristic sigmoidal $D_q$ curve of {numref}`fig:fractals:dq`. The two limits are easily found. Let $p_1 > p_2$. For $q\rightarrow +\infty$ the term $p_1^{\,q}$ dominates the sum, so that $D_{+\infty} = -\log p_1/\log 2$; for $q\rightarrow -\infty$ it is $p_2^{\,q}$ that dominates, and $D_{-\infty} = -\log p_2/\log 2$. For $p_1 = 0.7$ this gives $D_{+\infty} = 0.515$ and $D_{-\infty} = 1.737$, the two plateaus in {numref}`fig:fractals:dq`. In between we find for instance $D_2 = -\log(0.49+0.09)/\log 2 = 0.786$, markedly below $D_0 = 1$: here box-counting and correlation dimension really differ.

```{figure} _static/fractals/fractals_Dq.png
:name: fig:fractals:dq

The generalized-dimension spectrum $D_q$ of the binomial multifractal, comparing the analytical result with the box-counting procedure.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_dimensions.py)*
:::

```{raw} html
<p><em>Change the ratio $p_1:p_2$ and watch the measure and its $D_q$ spectrum:</em></p>
<iframe src="_static/fractals/interactive/binomial_slider.html" width="100%" height="440" style="border:none;"></iframe>
```

### Numerical determination of $D_q$

The generalized dimensions of an arbitrary measure are computed by a straightforward extension of the box-counting algorithm. For each box size $\varepsilon = 2^{-p}$ one accumulates the measure $p_i$ in every box, forms the partition sum $Z(q,\varepsilon)=\sum_i p_i^{q}$, and records $\log Z$ against $\log\varepsilon$. Repeating this over a range of box sizes and fitting a straight line gives the slope, from which $D_q = \text{slope}/(q-1)$ follows for each $q$. The Python program below does this for the binomial measure with $p_1 = 0.7$ and $k = 9$, and prints $D_q$ for a few values of $q$.

````{admonition} Python
:class: python

```{code-block} python
import numpy as np
import chaosbook as cb

# binomial measure on [0,1]: split the mass p1 : p2 = 0.7 : 0.3, k = 9 times
p1, k = 0.7, 9
mass = np.array([1.0])
for _ in range(k):
    mass = np.ravel(np.column_stack([p1 * mass, (1 - p1) * mass]))
x = (np.arange(2**k) + 0.5) / 2**k              # position of each sub-interval

qs = [q for q in range(-10, 11) if q != 1]     # q = 1 is singular, skip it
Dq = cb.generalized_dimensions(x, qs=qs, pmin=2, pmax=k, weights=mass,
                               origin=0.0, size=1.0)   # boxes of size 2**-p
for q, D in zip(qs, Dq):
    if q in (-10, -2, 0, 2, 10):
        print(f"q = {q:3d}   D_q = {D:.3f}")
plt.plot(qs, Dq, "o")
plt.xlabel("$q$")
plt.ylabel("$D_q$")
```
````

The value $q=1$ is skipped in the loop because of the $1/(q-1)$ singularity; the information dimension {eq}`eq:fractals:information_dimension` would have to be evaluated separately. The program prints

```{code-block} text
q = -10   D_q = 1.579
q =  -2   D_q = 1.239
q =   0   D_q = 1.000
q =   2   D_q = 0.786
q =  10   D_q = 0.572
```

Compare this with the analytical expression {eq}`eq:fractals:binomial_dq`: for $q=2$ we found $0.786$ above, and for $q=10$ the formula gives $-\log(0.7^{10}+0.3^{10})/(9\log 2) = 0.572$. The agreement is perfect to the digits shown, and the same holds at every $q$ in {numref}`fig:fractals:dq`. This is no surprise. The measure is exactly self-similar at every box size $2^{-p}$, so the partition sum is exactly $(p_1^{\,q}+p_2^{\,q})^{p}$ at every level and the points of the fit lie on a perfect straight line. The test is nevertheless a stringent one for the box-counting implementation.

In practice one does not have the measure itself, but a finite sample of points drawn from it, like the points of a trajectory. Then the under-sampling problem of section {numref}`sec:fractals:boxcounting` returns, and it bites hardest at large $|q|$. Try it: draw $N = 10^4$ points at random from the measure, each sub-interval being chosen with probability $p_i$, and feed the box-counting program the points alone, with equal weights.

````{admonition} Python
:class: python

```{code-block} python
rng = np.random.default_rng(1)
xs = rng.choice(x, size=10000, p=mass)         # 10^4 points drawn from the measure
Dq = cb.generalized_dimensions(xs, qs=qs, pmin=2, pmax=k, origin=0.0, size=1.0)
for q, D in zip(qs, Dq):
    if q in (-10, -2, 0, 2, 10):
        print(f"q = {q:3d}   D_q = {D:.3f}")
```
````

Now we find $D_2 = 0.786$ and $D_{10} = 0.572$ as before, but $D_{-2} = 1.219$ and $D_{-10} = 1.452$, well below the exact values of $1.239$ and $1.579$. Extreme values of $q$ weight either the most or the least populated boxes, and the least populated ones are the most poorly sampled. The emptiest sub-intervals carry a mass of $2\cdot 10^{-5}$, so with $10^4$ points most of them receive no point at all, and those that do receive one are credited with a weight $10^{-4}$, five times too much. Negative $q$ then sees a distorted measure. Now increase $N$ to $10^5$ and run the program again: $D_{-2}$ moves up to $1.29$, and $D_{-10}$ even overshoots to $1.69$. The negative-$q$ side of the spectrum converges slowly and is to be trusted only with a great many points.

````{admonition} Example
:class: example

The construction generalizes to any number of branches. Splitting each interval into three parts with weights $p_1,p_2,p_3$ leads, by the same argument, to

```{math}
:label: eq:fractals:ternary_dq
D_q = -\,\frac{\log \left(p_1^{\,q} + p_2^{\,q} + p_3^{\,q}\right)} {(q-1)\,\log 3}.
```

Setting one of the weights to zero prunes the corresponding branch at every stage. The support of the measure then becomes a Cantor-like dust rather than the full interval. Take for instance $p_2=0$ and $p_1=p_3=\tfrac12$. The measure is uniform on the two surviving thirds, and {eq}`eq:fractals:ternary_dq` reduces for $q=0$ to $D_0 = \log 2/\log 3$, exactly the dimension {eq}`eq:fractals:cantor_dimension` of the middle-third Cantor set. Choose instead $p_2=0$, $p_1=\tfrac45$, $p_3=\tfrac15$. This gives a genuine multifractal supported on the Cantor set, whose spectrum $D_q$ again follows {eq}`eq:fractals:ternary_dq`: for example $D_0 = \log 2/\log 3 = 0.631$ as before, but $D_2 = -\log(16/25 + 1/25)/\log 3 = 0.351$. The exercise *Multi-fractals in threes* lets you verify this numerically.
````

````{admonition} Fractal geometry of turbulence
:class: infobox

Fractals are not merely mathematical constructions; turbulent flows produce them in abundance. A striking example is the *turbulent/non-turbulent interface* (TNTI). This is the sharp but intricately folded surface that separates the rotational, turbulent fluid in a jet, wake or gravity current from the irrotational fluid around it {cite:p}`Corrsin1954`. It is convoluted across the whole range of eddy sizes, from the integral scale $l_o$ down to a few Kolmogorov lengths $l_i$. Box-counting (section {numref}`sec:fractals:boxcounting`) of the interface area yields a power law {cite:p}`Sreenivasan1989,Mandelbrot1982`

$$
A_\eta(\lambda) \propto \lambda^{\,2-D_f}, \qquad l_i \lesssim \lambda \lesssim l_o,
$$

where $D_f$ is the fractal dimension of the surface. A planar cut through it is a fractal curve whose length scales as $L(\lambda)\propto \lambda^{-\beta}$ with $\beta = D_f-2$. Measurements in high-Reynolds-number flows give $\beta \approx 1/3$, i.e. $D_f\approx 7/3$ {cite:p}`deSilva2013,Sreenivasan1991`; we take this experimental result as given. It matters because the interface area controls *entrainment*: the more convoluted the interface, the faster the turbulence engulfs and mixes the surrounding fluid.

What sets $\beta$? A self-similar model in the spirit of section {numref}`sec:fractals:selfsimilar` is revealing ({numref}`fig:fractals:tnti`). A segment of length $l_n$ is replaced by two segments meeting at a vertex displaced a distance $r\,l_n$ off its midpoint; the side alternates so that the mean position is preserved. Each new segment is the hypotenuse of a right triangle with legs $l_n/2$ and $r\,l_n$, so its length is

$$
l_{n+1} = \sqrt{\left(\tfrac12 l_n\right)^2 + (r\,l_n)^2} = \tfrac12 m\, l_n, \qquad m=\sqrt{1+4r^2},
$$

and there are twice as many. The curve thus consists of $N=2$ copies of itself scaled by $s=m/2$, and its dimension follows straight from the similarity dimension {eq}`eq:fractals:similarity_dimension`:

$$
D = \frac{\log 2}{\log(2/m)}, \qquad \beta = D-1 = \frac{\log m}{\log(2/m)}.
$$

This is the von Koch construction with a tunable bump. One checks that $r = 0.32$ gives $m = 1.187$ and $\beta = \log 1.187/\log(2/1.187) = 0.33$, which reproduces $\beta=1/3$; a smaller $r$ gives a flatter, lower-dimensional interface ($r=0.2$ gives $\beta = 0.12$).

The anisotropy parameter $r$ – the height of the interface bulges relative to their width – is where the physics enters. In a stratified gravity current a stable density gradient suppresses the vertical excursions of the interface, while its streamwise extent stays fixed by the shear layer. So $r$ decreases as the stratification (measured by the Richardson number) grows. Through the relation above this lowers $\beta$, shrinks the interface area $A_\eta$, and throttles the entrainment of ambient fluid {cite:p}`Krug2017`. In the limit $\beta\to0$ the interface becomes smooth and mixing collapses to molecular diffusion. The fractal dimension is thus a genuine control parameter for turbulent mixing in the ocean and atmosphere. (Should $r$ itself vary with scale, the interface is no longer a simple fractal but a multifractal of the kind met in section {numref}`sec:fractals:multifractal`.)
````

```{figure} _static/fractals/fractals_tnti.png
:name: fig:fractals:tnti

A self-similar model of the turbulent/non-turbulent interface (after Krug et al., 2017). (a) The generator: a segment of length $l_n$ is replaced by two segments meeting at a vertex displaced by $r\,l_n$ off the midpoint. (b) Curves after five iterations for $r=0.3$ and $r=0.2$; the smaller $r$ produces a smoother, lower-dimensional interface. (c) The fractal exponent $\beta = \log m/\log(2/m)$ as a function of the anisotropy $r$, with the neutral-turbulence value $\beta=1/3$ marked.
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_tnti.py)*
:::

````{admonition} Fractal clouds
:class: infobox

The boundary of a cumulus cloud is one of the most familiar fractals in Nature. Satellite images show that the cloud perimeter has a fractal dimension close to $4/3$ over four orders of magnitude in size. Assuming isotropy, this means that the cloud *surface* scales as $A\sim L^{D_s}$ with $D_s\simeq 7/3$. {cite:t}`Siebesma2000` tested this with a computer model of the atmosphere (a *large-eddy simulation*). They measured the dimension of individual simulated clouds using exactly the tools of this chapter: the volume–surface scaling $A\sim L^{D_s}$ and the correlation integral {eq}`eq:fractals:correlation_integral`. Both gave $D_s = 2.3\ldots$, in striking agreement with the observations ({numref}`fig:fractals:clouds`).

The value $7/3$ is no accident. It is precisely the surface dimension for which the turbulent transport of heat and moisture across the (unresolved) cloud edge becomes *independent* of the grid resolution. We state this without proof; the argument is given by {cite:t}`Siebesma2000`. So it is the fractal geometry of the interface that makes the mixing, or *entrainment*, come out right. The fractal cloud boundary is really the turbulent/non-turbulent interface of the previous box, now seen from the sky.
````

```{figure} _static/fractals/fractals_cloudscaling.png
:name: fig:fractals:clouds

Surface area $A$ against linear size $L=V^{1/3}$ for a population of simulated cumulus clouds (schematic, after Siebesma \& Jonker, 2000). The clouds obey $A\sim L^{D_s}$ with $D_s\simeq 7/3$ (solid line), well above the $D_s=2$ of smooth, Euclidean shapes (dashed line).
```

:::{only} html
*[Code behind this figure](https://github.com/mvreeuwijk/chaosbook/blob/main/creators/python/fractals/fig_exercises.py)*
:::

```{include} _includes/fractals_exercises.md
```
