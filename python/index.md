# From Stability to Chaos

:::::{only} html

::::{grid} 1 1 2 2
:gutter: 4
:class-container: sfc-hero

:::{grid-item}
:columns: 12 12 7 7

<p class="sfc-subtitle">A Hands-On Introduction to Nonlinear Dynamics — Python edition</p>

<p class="sfc-authors"><a href="../about.html">Harmen J. Jonker</a> and <a href="../about.html">Maarten van Reeuwijk</a></p>

A hands-on tour from simple one-dimensional maps to strange attractors and
fractal geometry. Built around the idea of learning by doing, it develops the
theory alongside concrete computations in Python — with a live exercise lab
for every chapter, running right in your browser — so that each idea can be
explored, visualised and experimented with directly.

The Python edition is under construction: the first two chapters and the
cookbook are available, and further chapters follow.

```{button-ref} phenomenon
:ref-type: doc
:color: primary
:class: sfc-cta

Start reading →
```

```{button-link} chaosbook-python.pdf
:color: secondary
:outline:
:class: sfc-cta

Download PDF (draft)
```
:::

:::{grid-item}
:columns: 12 12 5 5

```{image} _static/phenomenon/phenomenon_lorenz_phasespace_far.png
:alt: The Lorenz attractor in phase space
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

The chapters converted so far, from first phenomena onwards.
:::

:::{grid-item-card} Exercise labs
:link: lite/lab/index.html
:link-type: url

Python in your browser — nothing to install, everything to change.
:::

:::{grid-item-card} Cookbook
:link: app_cookbook
:link-type: doc

A practical Python reference for the techniques used throughout.
:::

:::{grid-item-card} About
:link: ../about.html
:link-type: url

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
```

```{toctree}
:hidden:
:numbered:
:caption: Cookbook

app_cookbook
```

````{only} html
```{toctree}
:hidden:
:caption: References

references
```
````

% In HTML the bibliography lives on its own References page; in the PDF it is
% rendered here as an end-of-book "Bibliography" (avoids an empty chapter).
:::{only} latex
```{bibliography}
:cited:
```
:::
