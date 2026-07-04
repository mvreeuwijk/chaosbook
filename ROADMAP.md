# Roadmap

Development plan for *From Stability to Chaos: A Hands-On Introduction to
Nonlinear Dynamics*. This is a living document; check the boxes as items land.

## Strategy: one mono-repo, several editions

The repository is the canonical home for the whole project — source text, the
Maple edition, the future Python edition, figures, build system, releases and
documentation. Editions live **side by side** in one repo rather than in
separate repositories, so shared material stays shared and the project stays
coherent.

The repo supports three long-term identities:

1. the book as a whole;
2. the Maple edition;
3. the Python edition.

**Current priority: stabilise the open-source Maple edition.** The Python
edition comes later and must be added *without disrupting* the existing
structure.

---

## Now — stabilise the Maple edition

### 1. Public front door (README)

- [x] Title, purpose, current status, "read online", build, and how to report issues in the README.
- [x] License and (planned) citation clearly stated.
- [ ] Add a Zenodo DOI badge once the first release is archived.

### 2. GitHub Pages

- [x] Automatic public HTML build via GitHub Actions (`.github/workflows/pages.yml`).
- [x] PDF (book + cookbook) built and published alongside the site.
- [x] Pages enabled and the public URL resolves:
      <https://mvreeuwijk.github.io/chaosbook/>.

The site does not need to be elaborate yet — the point is a stable public URL.

### 3. Zenodo DOI

- [ ] Enable the GitHub–Zenodo integration for the repo.
- [ ] Cut GitHub **releases only for stable public versions** (e.g. `v0.1-maple`,
      `v1.0-maple`); let Zenodo archive them and mint DOIs.
- [x] Add `CITATION.cff` (DOI/version fields left as placeholders until a release exists).
- [ ] Add the DOI badge to the README and record the DOI in `CITATION.cff`.
- [ ] In the README, distinguish "latest development version" from the archived DOI version.

### 4. Creators as audit trail

- [x] `creators/` documents which worksheet generates which figure
      (`figure_maple_map.csv`, `porting_manifest.csv`, `MODELS.md`).
- [ ] Track, per figure: which are used in the book, which need attention, and
      which are candidates for the Python port (extend the manifest — see *Later §5*).

### 5. Project hygiene

- [x] License (CC BY-NC-SA 4.0 for prose/figures; MIT for code).
- [x] `CITATION.cff`.
- [x] Contribution guidelines (`CONTRIBUTING.md`).
- [x] Issue templates (erratum + general).
- [x] Build instructions (README + CONTRIBUTING).
- [x] Short explanation of the edition structure (README + `shared/README.md`).
- [ ] Release notes / `CHANGELOG.md` once releases begin.

### 6. Usability of the current book

- [~] Learning-by-doing philosophy and edition context are covered by the
      landing page (`maple/index.md`) and the [About page](maple/about.md).
- [ ] Decide whether a dedicated "How to use this book" preface adds enough over
      those two to be worth a separate page; if so, add it.
- [x] A clear channel for readers to report errata/contribute (see §5).

---

## Later — add the Python edition as a parallel edition

Introduce Python as a *parallel implementation inside the same repo*, not a
separate repository. A possible structure (names adjustable):

```text
maple/                     # Maple edition (exists)
python/                    # Python edition (new)
shared/                    # shared math/text/bib/styles (exists)
creators/
  maple/  python/          # figure sources per edition
notebooks/
  author/  student/        # figure-generation vs exploration notebooks
src/chaosbook/             # small reusable Python package
```

Guiding principle: shared material is `shared/`; Maple- and Python-specific
material is isolated; generated assets are edition-specific; the mono-repo keeps
everything coherent.

### 1. Define edition boundaries

- Shared: chapter structure, mathematical exposition, exercises, bibliography,
  model definitions, conceptual narrative.
- Edition-specific: code fragments, figure-generation workflows, notebooks,
  computational comments, install instructions, numerical libraries.

### 2. Python creators

- A Python counterpart to the Maple creators workflow that generates the
  Python-edition figures, selected code snippets, and any numerical tables/values
  used in the text. Notebooks are computational laboratories, **not** the source
  of truth for prose.

### 3. Small Python package (`src/chaosbook/`)

- Reusable machinery: maps, ODE systems, Lyapunov tools, bifurcation utilities,
  Poincaré-section tools, plotting helpers. Keeps notebooks free of boilerplate
  and makes the numerics testable. (See the sketch in `creators/README.md`.)

### 4. Author vs student notebooks

- **Author** notebooks: generate book figures; part of the reproducibility
  pipeline; may be verbose.
- **Student** notebooks: clean, exploration-oriented, linked from the chapters.

### 5. Manifest-driven porting

- Extend the porting manifest to track the transition figure by figure, e.g.
  `figure_id, chapter, maple_source, python_source, book_location,
  python_status, validation_status, reviewer, notes`. The goal is not just to
  translate code but to **validate** that the Python version reproduces the
  intended mathematics and pedagogy.

### 6. Build commands

- Edition-aware targets, e.g. `make maple`, `make python`, `make maple-figures`,
  `make python-figures`, `make all`. (`make maple`/`make python` already exist.)

### 7. Testing & CI

- CI checks that the book builds, required figures exist, Python creators run,
  notebooks smoke-test, and core functions pass unit tests. For chaotic systems,
  test **qualitative/aggregate** properties, not exact trajectory matching.

### 8. DOI & releases with multiple editions

- Decide whether releases are edition-specific or whole-project. Practical
  mono-repo approach: GitHub releases archive the whole repo, the release name
  identifies the edition/status (`v1.0-maple`, `v0.1-python`, `v1.0-python`,
  `v1.1` for a combined release), Zenodo mints a DOI per stable release, and the
  README maps releases to editions. Cite the version used.

### 9. Long-term website

- Keep using GitHub Pages for now (DOI badge + clear links to latest/archived
  versions). Consider a custom domain (e.g. `stabilitytochaos.org`) only once the
  title and identity are stable.

---

*This roadmap was adapted from a planning brainstorm; it has been reconciled with
the repository's current state (Pages CI, PDF build and the creators manifests
already exist).*
