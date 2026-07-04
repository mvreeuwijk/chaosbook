# From Stability to Chaos

:::::{only} html

::::{grid} 1 1 2 2
:gutter: 4
:class-container: sfc-hero

:::{grid-item}
:columns: 12 12 7 7

<p class="sfc-subtitle">A Hands-On Introduction to Nonlinear Dynamics</p>

<p class="sfc-authors"><a href="about.html">Harmen J. Jonker</a> and <a href="about.html">Maarten van Reeuwijk</a></p>

A hands-on tour from simple one-dimensional maps to strange attractors and
fractal geometry. Built around the idea of learning by doing, it develops the
theory alongside concrete computations in Maple — with a weekly exercise for
every topic — so that each idea can be explored, visualised and experimented
with directly.

```{button-ref} phenomenon
:ref-type: doc
:color: primary
:class: sfc-cta

Start reading →
```

```{button-link} chaosbook.pdf
:color: secondary
:outline:
:class: sfc-cta

Download PDF
```
:::

:::{grid-item}
:columns: 12 12 5 5

```{image} _static/cont3d/cont3d_doublewell_poincare.png
:alt: Poincaré section of the forced double-well oscillator
:class: sfc-cover
```
:::

::::

<h2 class="sfc-cards-heading">Explore</h2>

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} Text
:link: phenomenon
:link-type: doc

The seven chapters, from first phenomena to fractal geometry.
:::

:::{grid-item-card} Exercises
:link: exercises
:link-type: doc

Hands-on problems for each chapter, with Maple worksheets.
:::

:::{grid-item-card} Cookbook
:link: app_cookbook
:link-type: doc

A practical Maple reference for the techniques used throughout.
:::

:::{grid-item-card} About
:link: about
:link-type: doc

The authors, and how the book came to be.
:::

::::

:::::

```{toctree}
:hidden:
:numbered:
:caption: Text

phenomenon
disc1d
disc2d
cont1d
cont2d
cont3d
fractals
```

````{only} html
```{toctree}
:hidden:
:numbered:
:caption: Cookbook

app_cookbook
```

```{toctree}
:hidden:
:numbered:
:caption: Appendices

app_twobody
app_lorenz
app_polar
```

```{toctree}
:hidden:
:caption: References

references
```
````

```{toctree}
:hidden:
:caption: About

about
```

% In HTML the bibliography lives on its own References page; in the PDF it is
% rendered here as an end-of-book "Bibliography" (avoids an empty chapter).
:::{only} latex
```{bibliography}
:cited:
```
:::
