# Referee review: *From Stability to Chaos* — Python edition (branch `py/rollout`)

Reviewer's brief: a demanding but constructive reading of the whole Python edition as both scientist and teacher. Every finding gives a severity, a location, what is wrong, the evidence, and a proposed fix. **[V]** marks findings I verified myself (by derivation, by running code in `cbenv2`, or by looking at the built figure/HTML/PDF); **[J]** marks judgement calls. Every finding also carries a bucket tag: **[CONVERSION]** (introduced by or specific to the Python edition: code, regenerated figures, cross-references, labs, package, conversion wording) or **[BOOK]** (content shared by both editions: prose, maths, style, rigour, figure design, structure). Where in doubt I checked `maple/`; the two summary tables in Section 18 list every finding by bucket and severity. Line numbers refer to `py/rollout` at commit `29c3ef4`.

Totals: **2 critical, 35 major, 66 minor** (numbered findings; the language section is not counted per typo). By bucket: CONVERSION 1 critical-share, 8 major, 18 minor; BOOK 2 critical, 27 major, 48 minor (a few findings have a part in each bucket and are listed in both tables).

---

## 1. Executive summary

The Python edition is a real book: eight chapters that build from one-dimensional maps to strange attractors, fractals and a genuinely good closing chapter on chaos in practice; a small, generic `chaosbook` package; a lab per chapter that runs in the browser; a cookbook; and a standardised figure set. The learning-by-doing design works. The code in the chapters runs, the numbers that the conversion team checked are right, and the package tests pass (72/72). Chapters 7 (fractals) and 8 (practice) and the three appendices are well written and essentially clean.

The old prose, however, has not been refereed in twenty years, and it shows. The core problems are of four kinds.

1. **Conceptual errors in the parts students lean on most.** Chapter 5 (2-D flows) has the highest density: the trace/determinant formulas are wrong, the centre is said to be non-diagonalisable, the van der Pol origin becomes a "saddle" for μ>2 (it is an unstable node), the Lyapunov-function example concludes "stable node" for what is a linear centre, the subcritical Hopf is described as "losing a fixed point", the point-vortex example is not a gradient system of the stated potential, and the blue-sky figure's stability colouring contradicts its own phase portraits. Chapter 6 identifies the eigenvalues of the symmetric Jacobian with "the three Lyapunov exponents" of the Lorenz system; their time averages are (4.2, −2.3, −15.6), not (0.91, 0, −14.6), and the book's own figure shows it. Chapter 3's kicked-rotor derivation has a sign error, and uses "saddle node" for a saddle throughout. Chapter 4's first worked stability example has the wrong derivative (1−2x² for 1−3x²).

2. **Drafting residue that must not reach a public edition.** "(IS POINCARE BENDIXSON THEOREM IN C5?)", "NEEDS DIAGRAM", an unfilled "(r = …)", a `plt.savefig("b4.png")` inside a book listing, broken LaTeX `Poincar\'{e` in a section heading and in running text (visible in HTML and PDF), a raw `{eq}\mathtt{…}` in the text, raw `[Strogatz1994, Verhulst1996]` brackets, and `{URL}` placeholders in a lab notebook.

3. **Figure–text mismatches, some old and some from the redraw.** The conservative/gradient figure lacks the panels its caption and text describe (already so in the Maple edition); the ferromagnet spin figure shows one initial snapshot where the caption promises an evolution at two temperatures (also old); the three-body potential figure has one panel where the caption refers to two (old; the missing panel exists as `cont4d_3body_Vcut.png` in `maple/_static`); the cobweb explanation refers to dotted lines that the redrawn figure no longer has (new); the blue-sky stability diagram is coloured for the time-reversed system (new).

4. **A Lyapunov-exponent story that is inconsistent across chapters.** Chapter 2 quotes Λ(3.9) ≈ 0.6 from 25 iterations (converged value 0.50, and the chapter's own Λ(r) plot shows 0.5); chapter 3 never says that a generic perturbation grows at the *largest* exponent; chapter 6 then mislabels local stretching rates as Lyapunov exponents; chapter 8 computes a horizon of 10 while its figure marks 6.6.

The two newest chapters (7 and 8, written for the 2026 edition) read in a different voice from the 2005-era chapters 1–6, and they are rigorous in a different way: precise definitions and complete derivations, but fewer worked numbers and more assertion-with-citation. Section 14 compares them side by side; Section 15 rates every chapter on rigour and on the quality of its examples.

None of this is hard to fix, and almost all of it is local. The book-level recommendations in Section 2 order the work.

---

## 2. Book-level recommendations (in priority order)

1. **Make the Lyapunov-exponent thread consistent (chapters 2, 3, 6, 8).** Define Λ as a limit; label every finite-sample number as a finite-time estimate (chapter 2: 0.6 from 25 steps vs 0.50 converged); state in chapter 3 that a generic perturbation grows at the largest exponent; in chapter 6 rename the J_S eigenvalues "local/instantaneous stretching rates", add a QR-based spectrum for flows to the package and quote the real Lorenz spectrum (0.906, 0, −14.57); in chapter 8 reconcile the horizon number with the figure. Findings D1-4, D2-4, C3-1, PR-1.
2. **Strip drafting residue and broken markup before the edition becomes primary.** Findings C3-2, D1-7, D1-9, D1-10, C1-5, C2-17, L-1.
3. **Repair the chapter-5 cluster** (C2-1 … C2-11, C2-14). This chapter is the reference students will use for stability classification; it currently teaches several wrong things.
4. **A caption-versus-image pass by someone who did not make the figures.** Findings C2-8, C2-9, C1-3, C3-4, D1-13, C2-15, D2-13, C3-7.
5. **Terminology hygiene across the book**: "saddle" vs "saddle-node"; "centrifugal" vs "centripetal"; rotation number as a real number; potential V vs Hamiltonian H; "dimension of phase space" vs "degrees of freedom"; define the ⟨a,b⟩ open-interval notation once. Findings D2-2, D2-3, C3-5, C3-8, D1-16.
6. **Audit exercise prerequisites.** Add a half-page on ẋ = −V′(x) in chapter 4 and on the Bendixson–Dulac criterion in chapter 5; make the dripping-faucet dependency of chapter 7 explicit. Findings C1-4, C2-19, F-1.
7. **Re-read every paragraph adjacent to a converted code block.** Two of the worst text/code mismatches are Maple-era reasoning left under Python code (D1-3) or sentences written during the conversion (P1).
8. **Unify the package calling conventions.** Findings K-1 … K-4.
9. **One voice.** Decide the house style (Section 14) and move both halves of the book towards it; then copy-edit chapters 2–6 with a native-English editor (Section 16).
10. **Small content additions that would pay off:** the 1-D potential picture; Bendixson–Dulac; a sentence on the coexistence of the Lorenz attractor with the stable fixed points for 24.06 < r < 24.74; one explicit statement of the Λ = 0 direction along a flow; a worked numerical D_q or box-count on a real attractor inside chapter 7.

---

## 3. Chapter 1 — A start at the end (`python/phenomenon.md`)

A good opener: short, concrete, and the two examples (Lorenz, three-body) are exactly right.

- **P1 — major [V] [CONVERSION]** `phenomenon.md:92`. *"If ε is made small enough the solutions appear to stay together indefinitely; … Tightening the integration tolerances — for instance `rtol=1e-12, atol=1e-12` — restores the divergence."* Wrong. Evidence: with `rtol=1e-9`, ε = 10⁻¹⁴ still diverges, at t ≈ 37.6 (beyond the t = 30 window); with `rtol=1e-12` at t ≈ 36.8 — the tolerance changes nothing. For ε ≤ 10⁻¹⁶ the two initial conditions are identical in double precision (2 + 10⁻¹⁶ == 2.0) and never diverge at any tolerance. The Maple original said "Increasing the working precision — `Digits := 20`", which *is* true in Maple (software floats represent ε); the Python sentence transposed the idea into a false one. Fix: say that a longer `tend` reveals the divergence, and that below the machine resolution of x(0) = 2 (≈ 4·10⁻¹⁶) the two runs are the same run; this is also the answer to exercise e).
- **P2 — minor [V] [BOOK]** `phenomenon.md:227` and `_includes/phenomenon_exercises.md:55`: units of G given as N m² kg⁻¹; should be kg⁻². (The appendix has it right.)
- **P3 — minor [J] [BOOK]** `:15` "an early supercomputer": Lorenz used a Royal McBee LGP-30, a desk-sized machine doing ~60 multiplications per second — the story is better for saying so.
- **P4 — minor [V] [BOOK]** `:147` "As discussed during the first lecture" (lecture residue); `:175` "three variables each with six degrees of freedom" → three bodies; `:247` "Left row / Right row" → columns; exercise `:89` "the radii of earth and moon" → orbital radii about the centre of mass.
- **P5 — minor [J] [BOOK]** `:147` (and `app_twobody.md:37`) "Poincaré proved that the system cannot be solved analytically in general": he proved non-integrability; Sundman later gave a convergent series. "No closed-form solution" is defensible; "proved … cannot be solved analytically" is not quite.
- **Lab [V] [CONVERSION, minor]**: good; the three-body solver uses `atol=1.0` (metres, sensible) without a comment saying so. (Counted as L-6.)

## 4. Chapter 2 — Chaos in iterative maps (`python/disc1d.md`)

The strongest teaching chapter; the ladder cobweb → fixed points → periodic orbits → bifurcations → Lyapunov → shift map → closed forms → pdf → universality is excellent and the Python examples are well chosen. It is let down by a dozen mathematical slips and one text/code contradiction.

- **D1-1 — major [V] [BOOK]** `:312`, `:463`. "period-2 solutions satisfy x_{n+2} = f(x_n)" and "a period-m solution satisfies x_{n+m} = f(x_n)". Both should read x_{n+2} = x_n and x_{n+m} = x_n. The defining property of a periodic orbit is wrong in the section that defines it.
- **D1-2 — major [V] [BOOK]** `:190`. "substituting x_n = x* + ε_n in {eq}`eq:disc1d:def_linear_map`" — that is the linear map; the substitution is into the general map `eq:disc1d:def_iterative_map`.
- **D1-3 — major [V] [CONVERSION]** `:1334` and the printed output `:1331`. *"Unfortunately this method breaks down for period 16 and higher … f^(m)(1/2) is a polynomial in r with leading order r^{2^m−1} … r^{65535}"* is the Maple `solve`-a-polynomial argument (it is in `maple/disc1d.md`); the Python code above uses `brentq` on a numerical function and does not break down: the same scan for m = 16, 32, 64 returns 3.56666738, 3.56924353, 3.56979529. The paragraph gives a false motivation for the Newton–Raphson method that follows. Also the printed output "2., 3.236…" is not what the code prints: r = 2 is on the grid boundary (F(2) = 0, so the sign-change test fails) and the list starts at 3.236067977. Fix: motivate Newton–Raphson by error control and the ever-finer grid; start the grid at 1.9; give the "Seed at x₀ …" paragraph (`:1336`) an opening sentence.
- **D1-4 — major [V] [BOOK]** `:682, :725, :783`. Λ ≈ 0.6 at r = 3.9 and "Λ = 0.61" from 25 values, used for a horizon N ≈ 27. The converged exponent is Λ(3.9) = 0.497; the first 25 iterates from x₀ = 0.1 give 0.58. The chapter's own Fig. `fig:disc1d:lyapunovdiagram` and the lab's Λ(r) sweep show ≈ 0.5 at r = 3.9. Keep the 25-step estimate as a finite-time estimate, quote the converged 0.50, note N ≈ 32, and write the definition at `:714` as a limit.
- **D1-5 — major [V] [BOOK]** `:1109` "Λ → ∞, consistent with … superstable" → Λ → −∞.
- **D1-6 — major [V] [BOOK]** `:1019` x_{n+1} = 4 r x_n(1−x_n): the r is spurious; `:1008` "(1−sin(z))²" → (1−sin²(z)).
- **D1-7 — major [V/J] [BOOK]** `:646`. (i) Unfilled placeholder "until for some critical value ($r=\ldots$)". (ii) "at r = 3.82… the period-3 solution loses its stability" — it is created with its unstable partner in a tangent (saddle-node) bifurcation at r = 1+√8 = 3.8284…; below that it does not exist. Anchor the intermittency discussion on the tangent bifurcation (Strogatz §10.4).
- **D1-8 — minor [V] [BOOK]** `:233` "positive and smaller than 0" → smaller than 1.
- **D1-9 — minor [V] [BOOK]** `:772` `{eq}\mathtt{eq:disc1d:lyap_period-m}` renders as literal text in HTML and PDF (present in `maple/` too).
- **D1-10 — minor [V] [BOOK]** `:1121-1123` broken paragraph "There is a variety of methods to elaborate (2.37)" / blank / ", but they are beyond our scope."
- **D1-11 — minor [V] [BOOK]** `table:shiftmapconcept` rows labelled y₀, y₁, y₃, y₄ (y₂ missing).
- **D1-12 — minor [V] [BOOK]** `:594` "r ∈ [0.1]" → [0,1]; `:1367` "period-0" → period-1; Feigenbaum table p = 0 row misaligned; `:1293` r_c vs r_∞; `:545` and `cont1d.md:281` "'bifurc' is the Latin word for fork" (Latin *furca*, *bifurcus*); `:29` r = −1 also "does nothing" in modulus.
- **D1-13 — minor [V] [CONVERSION]** `:95`. The cobweb text refers to "the solid line", "the vertical dotted line" and "in the latter two plots we refrained from plotting the dotted lines"; the redrawn `disc1d_logist_cobweb_r2_7.png` has no construction lines. Add them to panel (a) or rewrite the two sentences.
- **D1-14 — minor [J] [BOOK]** `:1242` "Feigenbaum proved mathematically" → discovered numerically and explained by renormalisation; rigorous proof Lanford (1982).
- **D1-15 — minor [J] [BOOK]** `:1125-1137` the pdf derivation silently uses that two y map to each x; one clause prevents the half-answer error.
- **D1-16 — minor [J] [BOOK]** Notation: f^{(m)} for iterates beside f′ for derivatives; the open-interval notation ⟨0,1⟩ is never defined.
- **D1-17 — minor [V] [BOOK]** Exercise "Discrete cubic map" b) "r must be within [−1,1]" where the exercise sets r ∈ [0,1]. Otherwise the exercises are well posed: the Newton–Raphson fixed point x* = 3/4 has σ = 1 − a/2 (loss of stability at a = 4, unstable at a = 6: a good exercise); the period-2 formula of the cubic map is correct (sympy residual 0).
- **Lab [V]**: matches the exercises; the Λ(r)-with-bifurcation explorer is a good addition.

## 5. Chapter 3 — Discrete mappings of higher order (`python/disc2d.md`)

Good material (Duffing, bouncing ball, Hénon, kicked rotor → circle and standard maps, manifolds). The bouncing-ball derivation is correct (re-derived `eq:ball_new_position`, the reflection law and both periodic orbits).

- **D2-1 — major [V] [BOOK]** `:806-807`. The kick relation `:797` is v_n⁺ = v_n⁻ + V(θ_n); eliminating it from `:786-787` gives (v_n⁻ **+** V), but the map, the matrix form and both limits carry (v_n⁻ **−** V). One sign must change (or define V with the opposite sign and say so).
- **D2-2 — major [V] [BOOK]** "saddle node" for a saddle *point*: `:1295`, `:1297`, `:1394`, `cont2d.md:1096`, `cont3d.md:649`, cookbook cell 97. In chapters 4–5 "saddle-node" is a bifurcation. Replace by "saddle (point)".
- **D2-3 — major [J] [BOOK]** `:968` and `[^fn2]`: "the standard simplification rules of fractions do not apply to w … 4/6 ≠ 2/3". A rotation number is a real number. For an invertible circle map (K ≤ 1) every periodic orbit has period equal to the denominator of w in lowest terms, so "for nonlinear maps a state like w = 4/6 can exist" holds only for K > 1 after period doubling. Also `:1009` "Ω = 0.464 would result in … w = 464/1000": the linear map with Ω = 58/125 has period 125. Define w ∈ ℝ and carry (R, m) separately when the period matters.
- **D2-4 — major [J] [BOOK]** `:586-612`. Λ₁ ≤ Λ_e ≤ Λ_m is stated, but never that a generic perturbation aligns with the most unstable direction so that Λ_e → Λ_max — the fact the book relies on twice (standard map Λ ≃ 0.4 vs Λ_max = 0.445; Lorenz Λ_e ≈ 0.9 = Λ_max). Two sentences, and a back-pointer from chapter 6.
- **D2-5 — major [V] [BOOK]** `:1335-1381` and `:1223-1234`. All panels of the nine-panel manifold figure and of the six-panel standard-map figure are referenced by one label, so the text reads "at n = 3 (Fig. 3.14) … (Fig. 3.14) … (Fig. 3.14)" and "Note the factor 10 difference in scale between Fig. X and Fig. X" (same in `maple/`). Reference panels (a)–(i).
- **D2-6 — minor [V] [BOOK]** `:1318` e₂ = (−0.35, 0.97) is not a unit vector: (−0.344, 0.939); the angle is 36.2°, "about 40°" is loose.
- **D2-7 — minor [V] [BOOK]** `:525` "X* = Y* = 0" → U* = 0; the map divides by U_n, so this orbit is a limit; the periodic orbits are written in dimensional lower-case (x₀,u₀,v₀) for dimensionless (X,U,V).
- **D2-8 — minor [V] [BOOK]** `:751, :759` "radial velocity" → tangential; `:753` "conservation of angular momentum, which states that the rate of change equals the torque" → balance; `:871` I(θ) → V(θ).
- **D2-9 — minor [V] [BOOK]** `:978` caption Ω = 10.17 vs the golden ratio in text and code; `:1088` [0.46301; 0.53698] vs the printed 0.46302; "judging from the fact that x = 0.25 and x = 0.75 are on the line y = x" is not the reason (they are fixed points of f itself).
- **D2-10 — minor [V] [BOOK]** `:248` "x* = y*"; `:541` "y_n = x₀ + ε₀" → y₀; `:987` "y₀ = y₀ + ε₀"; `:1234` stray space.
- **D2-11 — minor [J] [CONVERSION]** `:649` "Probably more sophisticated algorithms are available (the package's `cb.lyapunov_spectrum` … re-orthonormalises …)" — the added parenthesis answers the old sentence; rewrite as a statement.
- **D2-12 — minor [V] [CONVERSION]** `:1232` the chaotic standard-map orbit starts at (0.1, 0.1) in the text; the figure script uses (0.05, 0.4).
- **D2-13 — minor [V] [CONVERSION]** `:1230` "deviations seem to saturate at 10⁻⁵"; the regenerated `disc2d_standardmap_quasi_deviations.png` shows slow algebraic growth to ≈ 4·10⁻⁶ at n = 750, no saturation. "Grow only algebraically (not exponentially)" is truer and more instructive.
- **D2-14 — minor [V] [BOOK]** `:1387` caption "iterated 7 times" vs panels to N = ±6.
- **D2-15 — minor [V] [BOOK]** Exercises: dripping-faucet part d) ends mid-sentence ("when instead you base it on the"); "find an for estimate Λ"; the U-tube figure caption has μ = 4.17·10⁻³ while the exercise sets μ = 0.01. (The U-tube A, B, C and the faucet matrix are correct.)
- **L-1 — major [V] [CONVERSION]** `python/lite/files/disc2d_lab.ipynb` cells 7, 11, 15: "Full text: [in the chapter]({URL}#exercises)" — three unfilled `{URL}` placeholders, broken links in a student-facing notebook.

## 6. Chapter 4 — Continuous systems (`python/cont1d.md`)

Clear, with a good physical thread (ferromagnet, climate). The normal-form rescalings, the Taylor expansion of the ferromagnet and the climate numbers (T* = 288.5 K) all check.

- **C1-1 — major [V] [BOOK]** `:243` "f′(x) = 1 − 2x², so for x* = ±1 one has σ = −1". For f = x − x³, f′ = 1 − 3x² and σ(±1) = −2 — in the chapter's first worked stability example; the correct r − 3x² appears 30 lines later.
- **C1-2 — major [V] [BOOK; code comment CONVERSION]** `:676-683`. The flip probability ½[1 + tanh(s_i h_i/T)] → 1 for an *aligned* spin, contradicting the text two lines below and p ∼ exp(−s_i h_i/T); it should be ½[1 − tanh(·)]. H(s) = ½ Σ s_i J_ij s_j needs a minus sign for a ferromagnet. The Python listing is physically right only because it flips when `rng.random() > p` (probability 1 − p) while its comment calls `p` the "transition prob".
- **C1-3 — major [V] [BOOK]** `fig:cont1d_ferro_spin_evolution` (`:734-739`): a single 20×20 initial snapshot at 20 % width under a caption promising "Evolution … from two different initial states for two temperatures"; the mean-state figure likewise shows only T = 0.5. The 24 snapshots exist (`_a0…a5`, `_b0…b5`, both T) but are unused. Same in `maple/`. Build the panel the caption describes.
- **C1-4 — major [V] [BOOK]** `_includes/cont1d_exercises.md:112` asks for "a potential function V(T)"; ẋ = −dV/dx is never introduced for 1-D flows (first in chapter 5). Add a short subsection (it also motivates "catastrophe" and bridges to gradient systems) or drop part c).
- **C1-5 — minor [V] [CONVERSION]** `:491` `plt.savefig("b4.png", dpi=70); plt.close()` scratch line in a book listing (also in the PDF); debugging `print`s at the ends of several listings.
- **C1-6 — minor [V] [BOOK]** `:435` "the Infobox below" (none); `:1005` empty label `tab:cont1d:`; `:665` |z_i − z_i|; `:627` paragraph ends with a comma; `:906` T^* vs T_*; the old worksheet used β = 4·10⁸ while text/table/code use 4·10⁷ — confirm the quoted f′(T*) and the figures use 4·10⁷ [CONVERSION check].
- **C1-7 — minor [J] [BOOK]** the marginal case f′(x*) = 0 (ẋ = −x³, x³, x²) is never mentioned although chapter 2 treats the analogous |σ| = 1 and the normal-form section relies on it.
- **C1-8 — minor [J] [BOOK]** `:162` "x* = 0 has no attraction domain by definition" — its basin is {0}.
- **C1-9 — minor [V] [BOOK]** Exercise "Stability and bifurcations (2)" e) "when the *stable* fixed points have the values …" — at a saddle-node they are marginal (values correct: 2x² + 4x + 1 = 0).
- **Lab [V]**: good; the T/m explorer is exactly the right companion; heat-balance c) and e) are comment-only (L-5).

## 7. Chapter 5 — Two-dimensional continuous systems (`python/cont2d.md`)

The chapter with the most to fix. The Lotka–Volterra invariant, ρ, the Hamiltonian/gradient dichotomy and "no chaos in 2-D" are good; the linear-theory review and several examples will teach wrong things.

- **C2-1 — major [V] [BOOK]** `:51` "y = θ₁/r₁" (missing P) and "α = θ₁/r₁". With x = (r₂/r₁)N, y = (θ₁/r₁)P, t′ = r₁t: ẋ = x(1−y), ẏ = y(x − θ₂/r₁), so α = θ₂/r₁ (sympy residuals 0).
- **C2-2 — major [V] [BOOK]** `:237` T = a + c, D = ac − bd → T = a + d, D = ad − bc.
- **C2-3 — major [V] [BOOK]** `:252` "Re(σ) = 0: two identical eigenvalues … not diagonalizable … center": the eigenvalues ±iβ are distinct and A is diagonalisable over ℂ; the non-diagonalisable case is the repeated real eigenvalue T² = 4D (degenerate node), which should be mentioned instead. `:249` "imaginary" → complex.
- **C2-4 — major [V] [BOOK]** `:689-704` point vortex: −∇ tan⁻¹(y/x) = (y/r², −x/r²); the text has (−y/r, x/r) — wrong power and sign — and concludes "the angular velocity u_θ = rθ̇ = 1 is constant" (u_θ is a velocity and a point vortex has u_θ ∝ 1/r). Use the velocity potential u = +∇φ, φ = Γθ/2π, and fix the conclusion.
- **C2-5 — major [V] [BOOK]** `:823` "For μ > 2 the fixed point becomes an unstable saddle": both eigenvalues ½(μ ± √(μ²−4)) are positive (2.618, 0.382 at μ = 3; D = 1 > 0): an unstable node. (The lab text has it right.)
- **C2-6 — major [V] [BOOK]** `:851-868`. "we conclude that x* = 0 is a stable node": the linearisation of ẏ = −(k/m)x − (μ/m)|y|y has eigenvalues ±i√(k/m) — a centre; the true fixed point is nonlinearly asymptotically stable, not a node. V̇ = −(μ/m)|y|y² vanishes on the x-axis, so the conclusion needs LaSalle; the definition `:839-842` with "almost all" is nonstandard. This example is the ideal illustration of why one wants a Lyapunov function (linearisation inconclusive) — if the conclusion is right.
- **C2-7 — major [J] [BOOK]** `:1202` subcritical Hopf: "the system loses a fixed point … without the development of a limit cycle". The fixed point persists and loses stability; an unstable limit cycle exists for μ < 0 and shrinks onto it (Strogatz §8.2). This matters in chapter 6, where the Lorenz Hopf is subcritical.
- **C2-8 — major [V] [BOOK equations; CONVERSION figure]** `:1209-1250` and `cont2d_global_fixed.png`. The Cartesian system `:1213` gives ṙ = μr + r³ − r⁵; the polar form `:1224` is ṙ = −μr − r³ + r⁵; the text describes the polar form (escape for μ = −0.26, trapped for −0.24). The figure script integrates the time-reversed system for (a,b) (trajectory from (0.15,0) spirals *out* to r ≈ 0.63) and plots the polar form in (c), but colours (d) for F = μr + r³ − r⁵ (origin stable for μ < 0, outer branch stable) — the opposite of (a,b). Fix the Cartesian signs [BOOK]; recolour (d): origin unstable, inner branch stable, outer unstable [CONVERSION]. Also `:1229` "three different values of r" → μ; `:1231` "μ = −0,25".
- **C2-9 — major [V] [BOOK]** `fig:cont2d:esurface` (`:542-551`): two bare 3-D surfaces, under a caption describing "Right figures: isolines of S (black lines; trajectories …) and −∇S (red vectors …)", with the text (`:540`, `:646`) referring to the black lines and red arrows. The Maple figure is also a bare surface, so this is old; the `_ell2.png`/`_hyp2.png` panels exist in both `_static` folders and are not included. Make it 2×2 and fix the caption (which begins ". " and lists "(a)…(b)…" twice).
- **C2-10 — major [V] [BOOK]** `:914-933` saddle-node table rows swapped (σ₁ = −2x: x* = −√μ is the saddle); `:1022` "normal form of the transcritical" → subcritical pitchfork; `:1031` "±i√μ" → ±√(−μ).
- **C2-11 — major [V] [BOOK]** `:1164` J(0,0) has −μ in the (1,1) entry; it is μ.
- **C2-12 — minor [V] [BOOK equation; CONVERSION code]** `:723-724` both limit-cycle equations use x/(4√·); with y in the second, ṙ = (1−r²)/4 holds exactly. The listing reproduces the typo (and uses `colors=["r","g"]` while figure and text have red/blue dashed). Numerically the attracting orbit is still r = 1, so the figure is fine, but printed system and printed polar form do not match.
- **C2-13 — minor [V] [BOOK]** `:654` "|∇V|² is negative by definition"; `:683` "the stability of the centers"; `:245-246` "y₁ direction … until y₁ is small enough" (undefined; node approach muddled); `:127` "cases" → causes.
- **C2-14 — major [J] [BOOK]** `:711-716`, `:873-880`. Limit cycle defined as a closed orbit that "is an attractor (or both a repellor and an attractor in exceptional cases)" — unstable cycles omitted; isolation is the defining property. Poincaré–Bendixson stated as "then this trajectory is a closed orbit": the theorem says it is closed *or spirals towards a closed orbit*. As stated it is false.
- **C2-15 — minor [V] [BOOK]** `fig:cont2d:classification` (`cont2d_phase_r1.png`) is one stable-node sketch, yet `:401` and `:430` send the reader there for the types of fixed points and for "saddle"/"center". Those pointers belong to the T–D diagram (`classification2`, which is correct).
- **C2-16 — minor [V] [BOOK]** `:1093` pitchfork-example eigenvalues missing √; `:1096` "saddle node".
- **C2-17 — minor [V] [BOOK]** `:825` "[Strogatz1994, Verhulst1996]" and `:1065` "[Crawford1991, Verhulst1996]" are raw text in HTML and PDF; `Verhulst1996` is not in `shared/refs.bib`.
- **C2-18 — minor [V] [BOOK]** exercises: "Alee" → Allee; rabbits/sheep uses a₁,a₂ in the equations and b₁,b₂ in the text.
- **C2-19 — minor [J] [BOOK]** reactor exercise e) is Bendixson's criterion, never stated in the chapter; d) "find a gradient system to rule out closed orbits" means a Lyapunov function. Add Bendixson–Dulac to §5.7.
- **Lab [V]**: good; the van der Pol explorer with nullclines and `classify_fixed_point` is a highlight; the Allee starter finds (a−b, a−b) and the Hopf at a = √b.

## 8. Chapter 6 — Chaos in continuous systems (`python/cont3d.md`)

Strong content (volume contraction, Lorenz map, Poincaré sections, Rössler, forced double well, restricted three-body), with the book's two critical items.

- **C3-1 — critical [V] [BOOK; package naming CONVERSION]** `:215-234`, `fig:cont3d:lorenzlyapcomprehensive` and caption. "we can associate the Lyapunov exponents with the eigenvalues of J_S", "the three Lyapunov exponents", "generally one is negative, one positive and one near zero", caption "Cumulative average … showing the convergence to Λ_e ≈ 0.9". The eigenvalues of the symmetric Jacobian are instantaneous stretching rates; their time averages are not Lyapunov exponents. Evidence: re-running the listing gives averaged J_S eigenvalues (−15.59, −2.27, +4.19), sum −13.67 = −(σ+1+b); the Lorenz spectrum is (0.906, 0, −14.57), same sum; the figure's bottom panel shows the cumulative averages converging to ≈ +4.7, −2.3, −16 — none near 0.9 or 0 — while only the black Λ_e line converges to ≈ 1, as it must since a generic perturbation grows at Λ_max. Keep the Rayleigh-quotient bound Λ₁(t) ≤ Λ_e(t) ≤ Λ₃(t) (correct instantaneously). Fix: rename "local growth rates"; say Lyapunov exponents are long-time averages along ε̇ = Jε, obtained by the QR trick of chapter 3; add `cb.lyapunov_spectrum_flow`; quote (0.906, 0, −14.57), explain the zero exponent (direction of the flow) and the sum rule; rewrite the caption. `cb.lyapunov_exponent` already gives 0.90.
- **C3-2 — critical [V] [BOOK]** Drafting residue and broken markup in the published text, all present in `maple/` too: `:100` "(IS POINCARE BENDIXSON THEOREM IN C5?)"; `:727` "NEEDS DIAGRAM"; `:395` "the *Poincar\'{e* map}", `:620` "stroboscopic Poincar\'{e* section}"; exercise heading `_includes/cont3d_exercises.md:12-16` "### Poincar\'{e" … "-section of the Rossler system}". All verbatim in `final_py/cont3d.html` (the heading in the sidebar TOC) and in the PDF ("6.6.1 Poincar'{e"). The diagram wanted is the geometry of the restricted problem (primaries, rotating frame, μ); otherwise delete the line.
- **C3-3 — major [V] [BOOK]** `:869` "In (a–c), H₀ < V_L1 and the trajectories orbit one of the two bodies." With the listing's initial conditions H₀ = −2.54, **−1.51**, −2.71, −1.94 and (V_L1, V_L2, V_L3) = (−1.86, −1.98, −1.68): orbit (b) has H₀ > V_L1 and is not confined. The confinement criterion is H₀ < V_L2, as `:819` itself says. Change (b)'s initial velocity or the sentence.
- **C3-4 — major [V] [BOOK]** `fig:cont4d:3body_v`: one panel, while the caption describes (a) isolines and (b) a cross-section at y = 0 and the text `:819` refers to "Fig. (b)". The missing panel exists as `maple/_static/cont3d/cont4d_3body_Vcut.png` and was simply never included. Add it (it is the panel that makes the energy thresholds visible).
- **C3-5 — minor [V] [BOOK]** `:774, :792` "centripetal" → centrifugal; "repelling centripetal force" is self-contradictory.
- **C3-6 — minor [J] [BOOK]** The L1/L2/L3 numbering (L1 beyond the light body) is the reverse of the common convention; say so in one sentence.
- **C3-7 — minor [V] [CONVERSION for t = 15; rest BOOK]** `:162` "At t = 15 the distance reaches the size of the attractor" — the regenerated figure saturates at t ≈ 18; `:871` "revelations" → revolutions; `:862` caption begins ". The" and has "(e)" twice; `:557-559` x-maxima vs "return plot of z_n"; `:729` "sun-moon-satellite"; `:725` Poincaré's work was 1889–92; `:14` stray ")"; `:386` stray parentheses; `:85` not a sentence; `:515`, `:380` wording.
- **C3-8 — minor [V] [BOOK]** `:636, :649` "potential V = x⁴/4 − x²/2 + y²/2" is the Hamiltonian H (code and caption say "total energy"); keep chapter 5's convention.
- **C3-9 — minor [J] [BOOK]** `:577` "immediate transition to chaos": the Hopf at 24.74 is subcritical; the attractor exists from r ≈ 24.06 and coexists with the stable fixed points (transient chaos from 13.93). One sentence (and "subcritical", tying to C2-7).
- **C3-10 — minor [V] [BOOK]** `:559` "a differentiable maximum" → quadratic maximum.
- **C3-11 — minor [J] [BOOK]** Exercises: BZ "malomic acid and ammonium nitrate" → malonic acid, cerium ammonium nitrate (catalyst). The Earth-magnetic-field fixed points check. The lab's optional three-body cell repeats the loose "H0 < V_L1: cannot escape" criterion (see C3-3) [CONVERSION, part of L-4].
- **C3-12 — minor [J] [BOOK]** New figure `cont3d_rosslertopology.png` (caption from commit `b22ccbf`; on `py/rollout` HEAD the reference is not in `cont3d.md` because `ff36174` moved the placement to its own PR). The schematic is clean and the caption is right, but the drawing does not yet make its point: the two labels sit inside one annulus with no visible boundary between the "normal band" and the "Möbius band", the half-twist of the folded sheet is hard to see, and the dashed lines at the left are unexplained. Suggest: shade the folded (Möbius) strip, draw the fold with a visible half-twist where it rejoins the inner edge, add the sense of rotation to the caption, and name it as the Rössler *template* (branched manifold) with a reference (Rössler 1976; Gilmore & Lefranc 2002). As a diagram placed beside the Möbius-strip sentence it is a clear improvement over none.

## 9. Chapter 7 — Fractal geometries (`python/fractals.md`)

The best-written chapter: definitions are precise, the analytic results are correct (similarity dimensions, Koch-island area 8/5, D_q formulas, TNTI generator m = √(1+4r²), r ≈ 0.32 for β = 1/3), and the infoboxes connect to the authors' research.

- **F-1 — minor [J] [BOOK]** `:174, :256` "the dripping-faucet data/attractors of chapter 3" and "gives values close to, but slightly below, the box-counting dimensions of section 7.2": no attractor or dimension is shown anywhere; the faucet is a chapter-3 exercise. Show one return plot with both dimensions, or make the exercise self-contained.
- **F-2 — minor [V] [BOOK]** `:195` "x = log δ" (ε elsewhere).
- **F-3 — minor [J] [CONVERSION]** `:240` "binned logarithmically … accumulated" describes a different algorithm from `cb.correlation_dimension` (sorted distances + `searchsorted`).
- Exercises **[V]**: well posed ("Fractal Curve" shows the 1 m initiator; "Multi-fractals in threes" matches the ternary example).

## 10. Chapter 8 — Chaos in practice (`python/practice.md`)

A genuinely good closing chapter; every idea has runnable code; the Kalman listing is correct.

- **PR-1 — major [V] [CONVERSION]** `:33-39` vs `practice_horizon.png`. Text: t_h ≈ (1/0.9) ln(10/10⁻³) ≈ 10. Figure: horizon marked at t ≈ 6.6 (script criterion "40 % of saturation"), with the spread visibly growing faster than e^{0.9t} early on. State the criterion, explain the faster transient growth (the blob is not aligned with the unstable direction; local rates reach +10 in Fig. 6.x), and make the two numbers agree.
- **PR-2 — minor [J] [BOOK]** `:315-322` the controller is a one-step targeting nudge; OGY proper nudges along the stable manifold. "In the spirit of Ott, Grebogi and Yorke".
- **PR-3 — minor [V] [BOOK]** exercises `:62` "xx[1]…xx[N]" 1-based indexing.

## 11. Appendices

- **A-1 — minor [V] [BOOK]** `app_lorenz.md:46-49`: z is both the vertical coordinate and the Lorenz amplitude in one formula; name a and b = 4/(1+a²) explicitly.
- **A-2 — minor [V] [BOOK]** `app_twobody.md:42` "100 : 1 : 10⁻¹⁹" matches neither the table nor any satellite mass; `:61, :78` "{eq}primaries1–{eq}primaries1".
- **A-3 — minor [J] [BOOK]** `app_twobody.md:37` as P5. Otherwise the appendices are clear and correct.

## 12. Cookbook and labs

- **CB-1 — minor [V] [BOOK]** cell 97 "saddle node" → saddle.
- **CB-2 — minor [V] [CONVERSION]** `src/chaosbook/__init__.py:1-5` "Every function here is introduced in the book's cookbook" is true for 6 of 48 exports. Add recipes for `solve_ivp` events (Poincaré section), the stroboscopic section, the two-trajectory Lyapunov estimate and the QR spectrum, or soften the claim.
- **CB-3 — minor [J] [CONVERSION]** The cookbook opens with `help(sum)`; the JupyterLite entry would be friendlier starting at "General".
- **L-2 — minor [J] [CONVERSION]** The labs were verified with `nbconvert --execute` locally, which does not exercise Pyodide/ipywidgets; one manual browser pass per lab before the edition becomes primary. (The wheel is bundled in `lite/pypi`, so `%pip install chaosbook` resolves locally — the name does not exist on PyPI; make that a conscious choice.)
- **L-3 — minor [V] [CONVERSION]** fractals lab: the dripping-faucet cell (b) is comment-only.
- **L-4 — minor [V] [CONVERSION]** cont3d lab: the optional three-body cell prints "H0 < V_L1: cannot escape" (loose criterion, see C3-3).
- **L-5 — minor [V] [CONVERSION]** cont1d lab: heat-balance parts c) and e) are comment-only.
- **L-6 — minor [V] [CONVERSION]** phenomenon lab: unexplained `atol=1.0`.

## 13. Cross-cutting: chapter code and the `chaosbook` package

Small, readable, generic in the right way; tests pass (72). The problems are of consistency.

- **K-1 — major [J] [CONVERSION]** Mixed calling conventions: maps and 1-D flow tools (`fixed_points`, `stability`, `fixed_point_branches`, `continuation_sweep`) take `f(x, **p)`; n-D flow tools (`jacobian`, `phase_portrait`, `poincare_section`, …) and `solve_ivp` take `f(t, x, **p)`. A student moving from chapter 4 to 5 must change every right-hand side; chapter 4 wraps with `lambda t, x: f(x)`. State one rule in the cookbook's package section or accept both.
- **K-2 — major [V] [CONVERSION]** `effective_lyapunov` returns `(Lambda_e, eigenvalues of J_S)` (honest docstring) but the chapter uses the second output as "the Lyapunov exponents" (C3-1). Add `lyapunov_spectrum_flow(f, jac, x0, tmax, dt, …)` (variational equations + QR) and rename the second output `local_rates`. Add a test against the known Lorenz spectrum — its absence is how C3-1 survived.
- **K-3 — minor [V] [CONVERSION]** `bifurcation_diagram`/`lyapunov_sweep` hard-code the parameter name `r` while `fixed_point_branches`/`continuation_sweep` take `pname`; the labs work around it with lambdas. Add `pname="r"`.
- **K-4 — minor [V] [CONVERSION]** `lyapunov`/`lyapunov_spectrum` require analytic derivatives while `stability`/`jacobian` fall back to differences. Allow `None` → central differences.
- **K-5 — minor [V] [CONVERSION]** `box_dimension` fits the whole log–log range including the saturated small-ε part the chapter warns about; expose the fit range.
- **K-6 — minor [V] [CONVERSION]** sympy aliased `sym` (ch. 2, 4, cookbook) vs `sp` (ch. 3, 5, 6, labs); mpmath imported two ways.
- **K-7 — minor [V] [CONVERSION]** Debug/scratch residue in listings (C1-5; sanity `print`s; `np.allclose` "agrees with the package" assertions as book text; listing colours ≠ figure, C2-12).
- **K-8 — minor [J] [CONVERSION]** `rtol`/`atol`/`DOP853`/`max_step` are never explained though listings switch between them; one cookbook paragraph on tolerances for chaotic flows.
- **K-9 — minor [V] [CONVERSION]** Positives: `threebody` defaults match the chapter; `standard_map` mod 1 both coordinates; `winding_number` documents the lift; `poincare_section` explains its positional-only signature. No action.

---

## 14. Writing style: chapters 7–8 versus chapters 1–6 **[BOOK]**

The author's suspicion is right, and the git history explains it: `fractals.md` and `practice.md` entered the repository with the 2026 "Initial commit: Maple edition" and read as texts written recently by one hand; chapters 1–6 are the 2005-era lecture notes. The conversion did not change this (the Maple and Python versions of chapters 7–8 differ only in code). The differences, with representative passages:

**Voice and register.** Chapters 1–6 are a lab manual spoken by a lecturer; 7–8 are an essay.

> *disc1d.md:38* — "Instead let us resort to a numerical approach and write a small Python program to calculate and plot the series for some values of r. Take for example r = 3.9 and 0 < x₀ < 1. Run the program and observe the chaos! Now try other values or r, like r = 3.4, r = 2.5, and r = 0.5, and execute the program again."

> *fractals.md:6* — "The purpose of this chapter is to put this notion of a non-integer dimension on a firmer footing. We will first introduce fractals through a number of classical geometric constructions, for which the dimension can be obtained analytically from the self-similarity of the object. We then turn to the more general *box-counting dimension* and the *correlation dimension* …"

> *cont2d.md:290* — "Linear systems are 'uninteresting' in the sense that no matter where you start in the phase space, the system behavior is exactly identical and is governed by (5.x)."

> *practice.md:213* — "The billion dimensions of a weather model are, in a sense, an illusion. The system is strongly dissipative, so its trajectories collapse onto an attractor of far lower dimension than the space that contains them – exactly as the Lorenz flow, living in three dimensions, is confined to an attractor of fractal dimension only slightly above two."

**Sentence length and rhythm.** Chapters 1–6 average 15–20 words per sentence, with imperatives, exclamation marks and "we see that"; 7–8 average 30–40, with em-dashes, semicolons and periodic structure ("It is worth pausing to see why a weather forecast belongs in this book at all." … "Because prediction has a finite horizon, we must *predict with ensembles, correct with data, and reduce with structure*"). The older chapters say "one observes", "let us", "clearly"; the newer ones say "it is precisely", "what is robust", "the practical art is".

**Explained versus asserted.** Chapters 1–6 derive almost everything on the page, sometimes three times (the period-3 stability is computed by g′, by the product rule and by hand). Chapters 7–8 derive the core (D_q of the binomial measure; the Kalman update) and *assert* the rest with a citation: the TNTI box's β ≈ 1/3 and D_f ≈ 7/3, the cloud D_s = 7/3, the whole of POD/DMD/Koopman ("In exchange for moving to a higher-dimensional space of observables, one recovers a linear description"), Takens. A student of chapters 1–6 is trained to expect a derivation and will find chapter 8 §3 opaque.

**Hands-on code.** In 1–6 the listing *is* the argument: "See the code below", then the output, then the interpretation ("It reveals that the period-2 solution is stable for a in …"). In 7–8 the code sits in an admonition after the figure, introduced by a sentence ("The ensemble is generated by integrating …"), and the prose never quotes a number that the listing produced — the reader is not asked to run anything mid-paragraph.

**Exercises.** Old: short imperatives with fixed parameters — "a) Take r = 0.97. Generate a series of N = 1000 points starting from x₀ = 0.2. Show the series and the return-plot." New: reasoning prompts — "b) Halve the initial spread δ₀ and repeat. By how much does the predictability horizon increase? Explain, using the relation …, why improving the initial condition buys only a logarithmically longer forecast."

**References.** Chapters 1–6 cite about once per section, as a pointer ("for a very nice 'pedestrian' treatment one is referred to Strogatz"); chapter 8 cites some fifteen papers as evidence in the modern style ({cite:p}`Lorenz1996,Bauer2015`), and chapter 7 cites the authors' own work.

**What would make one voice, and who moves where.** Pick the register of chapter 7 as the target — it is the better prose and it is what a 2026 reader expects — but keep the *behaviour* of chapters 1–6:

- Chapters 1–6 should move towards 7–8 in: precision of definitions (fixed point, periodic orbit, limit cycle, attractor — state each once, cleanly); signposted section openings (one paragraph saying what the section will do, as `fractals.md:6` does); removal of lecture residue and exclamation marks; citations as evidence where a claim is not derived (Feigenbaum, Lorenz 1963, Jensen–Bak–Bohr for the staircase); exercise prompts that ask "explain why" alongside "show the plot".
- Chapters 7–8 should move towards 1–6 in: sentence length (cut the 40-word sentences in two); one worked number per idea quoted in the prose and produced by the listing on the page (D₀ of the chaos game = 1.58 from the fit; D_q of the binomial measure at q = ±10; the Kalman RMS error; the horizon from the figure's criterion); "try it" prompts mid-section; fewer assertions — either derive (Takens can be *motivated* in five lines with the Lorenz x-series; POD can be shown as one SVD of a snapshot matrix with the singular values printed) or say explicitly "we state without proof".
- Everywhere: one house style for the four recurring elements — the Python admonition (always preceded by one sentence saying what it computes and followed by its result in the prose), the Example admonition, the infobox, and the exercise (numbered parts, one verb each). Chapter 7's infoboxes and chapter 8's "Python" admonitions with a lead sentence are the model.

## 15. Rigour and quality of the worked examples, chapter by chapter **[BOOK]**

Scale 1–5. *Rigour*: are claims derived or motivated, definitions precise, theorems stated correctly. *Examples*: do they demonstrate what they claim, with numbers put in context (convergence, sensitivity)? "Objection" = where a careful student stops.

| Chapter | Rigour | Examples | Justification and the careful student's objection |
|---|---|---|---|
| 1 Phenomenon | 3 | 4 | Narrative by design; claims are stated, not derived, which is fine for an opener. Lorenz and three-body examples do show sensitivity and attraction. Objection: "tighten the tolerances restores divergence" (P1) is testable and false; nothing says how ε relates to machine precision. |
| 2 Maps | 4 | 4 | Nearly everything derived (linearisation, period-2 stability, Λ, shift map, closed forms, pdf, Feigenbaum δ). Precision slips: periodic orbit defined by a wrong relation (D1-1); Λ defined as a finite sum, not a limit; "Feigenbaum proved". Examples are excellent and numerically explicit; Λ ≈ 0.6 is not put in context (D1-4) and the superstable scan is misdescribed (D1-3). Objection: "your Λ(r) plot says 0.5 at r = 3.9". |
| 3 Higher-order maps | 3 | 4 | Heuristic "average Jacobian" for Lyapunov exponents is motivated but not correct in general (eigenvalues vs singular values) and leaves out Λ_e → Λ_max (D2-4); rotation number defined inconsistently (D2-3); kicked-rotor sign (D2-1). Examples strong: the Hénon convergence study (N = 1, 10, 200) is the book's best treatment of numerical context; Duffing stability intervals verified against the bifurcation diagram; standard-map manifolds. Objection: "4/6 is 2/3". |
| 4 1-D flows | 4 | 4 | Normal forms derived properly; the marginal case omitted (C1-7); the spin model's flip probability and Hamiltonian wrong in sign (C1-2); the mean-field limit asserted ("one can derive"). Ferromagnet and climate examples are physically grounded and numerically explicit (T_c, x_c; ε-folds); the spin-evolution figure does not deliver (C1-3). Objection: "f′ of x − x³ is 1 − 3x²". |
| 5 2-D flows | 2 | 3 | Linear theory misstated (T, D; centre diagonalisability); limit cycle and Poincaré–Bendixson stated incorrectly; Lyapunov function definition loose and the example's conclusion wrong; subcritical Hopf wrong. Lotka–Volterra (invariant, ρ) and the Hopf example are good; the point vortex is not what it claims (C2-4); the blue-sky example contradicts its own figure (C2-8); the van der Pol example mislabels its node (C2-5). Objection: almost every page. |
| 6 Chaos in flows | 2.5 | 4 | Volume contraction derived; attractor defined operationally and honestly; Lorenz-map argument with a candid footnote; Poincaré map example solved analytically — good. But the J_S/Lyapunov identification (C3-1) is a conceptual error carried through a figure and the package, and the Lorenz Hopf discussion omits subcriticality/coexistence (C3-9). Examples (Lorenz map, Rössler doubling, forced double well, three-body sections) demonstrate their claims; the three-body energies do not (C3-3). Objection: "the cumulative averages in your figure converge to 4.7, −2.3 and −16". |
| 7 Fractals | 4 | 3 | Definitions precise (similarity, box-counting, correlation, D_q), derivations complete (binomial D_q, Koch island), convergence discussed (box-count saturation, under-sampling at large |q|). Fewer worked numbers in the prose; the dripping-faucet comparison is asserted, not shown (F-1); the TNTI/cloud boxes assert from references. Objection: "where is the attractor whose dimension you quote?" |
| 8 Practice | 3 | 4 | Kalman filter derived to the gain and correctly coded; ensembles and horizon motivated; POD/DMD/Koopman/Takens asserted with citations and no operational detail; "OGY" is a simplified scheme. Every idea has a working listing — the examples are the chapter's strength — but the one quantitative claim in the text (t_h ≈ 10) disagrees with the figure (PR-1). Objection: "how does the linear operator on observables get approximated from data?" |
| App. two-body | 5 | – | Every quantity defined, every step shown; the model for the rest of the book. |
| App. Lorenz | 3 | – | The truncation is asserted ("Substituting … these amplitudes are found to obey"); z double-used (A-1). |
| App. polar | 5 | – | Correct and complete. |
| Cookbook | 4 | 4 | Clear recipes with results; "saddle node" slip (CB-1); the package claim overstated (CB-2). |

Overall: the two newest chapters are the most *rigorous* in definition and derivation but the least *demonstrative*; chapters 2–4 are the most demonstrative; chapter 5 is the outlier in both and should be rewritten rather than patched.

## 16. Language **[BOOK]**

Scale of the copy-editing need:

| Chapter | Need | Typical density |
|---|---|---|
| 1 phenomenon | light | a few per page (lecture residue, "row/column") |
| 2 disc1d | full pass | 2–4 per page: "monotically", "straigtforward", "accumlating", "deteministic", "inpection", "facinating", "follwowing", "Findig", "prodcut", "managable", "succesive" |
| 3 disc2d | full pass | 3–5 per page: "Unfortunaly", "particur", "Lyaponov", "assiocated", "devations", "determinig", "instanteneously", "resions", "nonlineary", "does not allows", "square square" |
| 4 cont1d | full pass | 2–3 per page: "exactely", "onseself", "occuring", "braches", "suddden", "implemtation", "Boltmann", "Physicist tend" |
| 5 cont2d | full pass | 2–4 per page: "simultanous", "cases", "neigbourhood", "discernable", "hear-rhythms", "oter", "multi=valued", "he potential", "A systematic was" |
| 6 cont3d | full pass | 2–3 per page: "strobocopic", "succesive", "revelations", "singularies", "focussed", "of simply" |
| 7 fractals, 8 practice, appendices, cookbook | light | essentially clean |

The 20 language problems that most obscure meaning (all **[V]**):

1. `disc1d.md:233` "positive and smaller than 0".
2. `disc1d.md:312/463` "x_{n+m} = f(x_n)".
3. `disc1d.md:1336` "Seed at x₀ where x₀ satisfies …" begins a method with no introduction.
4. `disc1d.md:1121-1123` the broken "variety of methods" paragraph.
5. `disc2d.md:902` "corresponds a constant rotation number rate of the rotor which is sampled periodically".
6. `disc2d.md:751, 759` "radial velocity".
7. `disc2d.md:1088` "judging from the fact that x = 0.25 and x = 0.75 are on the line y = x …".
8. `disc2d.md:968` "the standard simplification rules of fractions do not apply to w".
9. `cont1d.md:435` "in the Infobox below".
10. `cont1d.md:627` sentence ending in a comma.
11. `cont2d.md:245` "move in the y₁ direction until y₁ is small enough".
12. `cont2d.md:654` "|∇V|² is negative by definition".
13. `cont2d.md:1202` "the system loses a fixed point".
14. `cont2d.md:1229` "three different values of r".
15. `cont3d.md:85` "However, that both conservative and dissipative systems may display chaotic behaviour."
16. `cont3d.md:100` the parenthetical drafting question.
17. `cont3d.md:792` "the repelling centripetal force".
18. `cont3d.md:871` "only full revelations are considered".
19. `_includes/disc2d_exercises.md:95` the truncated part d).
20. `_includes/cont3d_exercises.md:12-16` the split "Poincar\'{e … -section" heading.

## 17. What I did and did not do

Read in full: all eight chapters, three appendices, the exercises, the cookbook, the eight labs, the package and tests, and the corresponding `maple/` files where provenance mattered. Ran: the test suite; sympy/numpy re-derivations for every [V] equation; the listings behind the disputed numbers (Λ(3.9); the Broer round-off table, which reproduces exactly; the superstable scan; the J_S averages; the three-body energies; the ε/tolerance claim; the LV scaling; the vortex gradient; the van der Pol eigenvalues; the limit-cycle radius; the sine-map r₁; the cubic-map period-2 formula). Looked at ~27 figures where a caption or sentence made a checkable claim, including the new Rössler schematic, and the built HTML and PDF text for leftover markup. Not done: running the labs in a browser; reading the 17 interactive companions beyond confirming they exist; checking all ~300 figures against their captions (the ones I checked had a one-in-four hit rate).

## 18. Summary tables by bucket

### 18a. [CONVERSION] — Python-edition fixes (rollout PR)

| Severity | ID | Location | One-line fix |
|---|---|---|---|
| critical (part) | C3-1 | `src/chaosbook/poincare.py` `effective_lyapunov` + `cont3d.md:290` | rename second output `local_rates`; add `lyapunov_spectrum_flow`; quote real spectrum (with K-2) |
| major | P1 | `phenomenon.md:92` | replace the "tighten tolerances restores divergence" sentence (longer `tend`; machine resolution of x(0)) |
| major | D1-3 | `disc1d.md:1331-1336` | rewrite the "breaks down at period 16" paragraph; grid from 1.9 so "2." is printed; introduce the Newton–Raphson paragraph |
| major | L-1 | `lite/files/disc2d_lab.ipynb` cells 7, 11, 15 | fill the `{URL}` placeholders |
| major | C2-8 (fig) | `creators/python/cont2d/fig_global.py`, `cont2d_global_fixed.png` | recolour panel (d) for the time-reversed system (origin unstable, inner branch stable) |
| major | PR-1 | `practice.md:33-43`, `practice_horizon.png` | make text horizon and figure criterion agree; explain the faster transient growth |
| major | K-1 | package | one calling convention for maps/1-D flows/n-D flows, documented in the cookbook |
| major | K-2 | package | `lyapunov_spectrum_flow` + a test against the Lorenz spectrum |
| minor | D1-13 | `disc1d_logist_cobweb_r2_7.png` / `disc1d.md:95` | add construction lines or reword |
| minor | D2-11 | `disc2d.md:649` | rewrite the added parenthesis as a statement |
| minor | D2-12 | `disc2d.md:1232` vs `fig_standardmap.py` | same chaotic initial condition in text and script |
| minor | D2-13 | `disc2d.md:1230` / `..._quasi_deviations.png` | "grow algebraically", not "saturate at 10⁻⁵" |
| minor | C1-2 (code) | `cont1d.md:710-712` | comment: `p` is the probability of *not* flipping |
| minor | C1-5 | `cont1d.md:491` and listing-end `print`s | remove scratch `savefig`/debug prints |
| minor | C1-6 (β) | `cont1d.md:922, 982` | confirm quoted f′(T*) and figures use β = 4·10⁷ |
| minor | C2-12 (code) | `cont2d.md:754-762` | fix the y-equation; colours to match the figure |
| minor | C3-7 (t) | `cont3d.md:162` | "t ≈ 18" to match the regenerated figure |
| minor | F-3 | `fractals.md:240` | describe the algorithm the package uses |
| minor | CB-2 | `src/chaosbook/__init__.py` docstring, cookbook cell 122 | add recipes or soften the claim |
| minor | CB-3 | cookbook cells 4–6 | start at "General" |
| minor | L-2 | all labs | one browser (Pyodide) pass per lab; decide on the PyPI name |
| minor | L-3 | `fractals_lab.ipynb` cell 7 | give the faucet cell a starter |
| minor | L-4 | `cont3d_lab.ipynb` cell 19 | criterion H₀ < V_L2 for confinement |
| minor | L-5 | `cont1d_lab.ipynb` cell 16 | starters for c) and e) |
| minor | L-6 | `phenomenon_lab.ipynb` cell 11 | comment on `atol=1.0` |
| minor | K-3 | `bifurcation.py`, `lyapunov.py` | add `pname="r"` |
| minor | K-4 | `lyapunov.py` | numerical-derivative fallback |
| minor | K-5 | `fractal.py` | expose the fit range of `box_dimension` |
| minor | K-6 | chapters 2–6 listings | one sympy alias; one mpmath import |
| minor | K-7 | listings | remove `allclose` assertions/debug prints from book text |
| minor | K-8 | cookbook | a paragraph on solver tolerances |

### 18b. [BOOK] — content fixes (both editions)

| Severity | ID | Location | One-line fix |
|---|---|---|---|
| critical | C3-1 | `cont3d.md:215-234`, fig `lorenzlyapcomprehensive` caption | J_S eigenvalues are local growth rates, not Lyapunov exponents; quote (0.906, 0, −14.57) |
| critical | C3-2 | `cont3d.md:100, 395, 620, 727`; `cont3d_exercises.md:12-16` | remove drafting notes; fix `Poincar\'{e` markup (heading and text) |
| major | D1-1 | `disc1d.md:312, 463` | x_{n+m} = x_n |
| major | D1-2 | `disc1d.md:190` | reference the general map |
| major | D1-4 | `disc1d.md:682, 714, 725, 783` | finite-time estimate vs converged Λ = 0.50; limit definition |
| major | D1-5 | `disc1d.md:1109` | Λ → −∞ |
| major | D1-6 | `disc1d.md:1008, 1019` | (1−sin²z); drop the spurious r |
| major | D1-7 | `disc1d.md:646` | fill "(r = …)"; tangent bifurcation at 1+√8 |
| major | D2-1 | `disc2d.md:806-867` | sign of V in the kicked-rotor map |
| major | D2-2 | `disc2d.md:1295, 1297, 1394`; `cont2d.md:1096`; `cont3d.md:649`; cookbook | "saddle", not "saddle node" |
| major | D2-3 | `disc2d.md:968, 1009`, fn 2 | rotation number as a real number; (R, m) when the period matters |
| major | D2-4 | `disc2d.md:586-612` | state Λ_e → Λ_max for generic perturbations |
| major | D2-5 | `disc2d.md:1223-1234, 1335-1381` | reference panels (a)–(i) |
| major | C1-1 | `cont1d.md:243` | f′ = 1 − 3x², σ = −2 |
| major | C1-2 | `cont1d.md:674-683` | ½[1 − tanh]; H with a minus sign |
| major | C1-3 | `cont1d.md:734-765` | build the two-temperature evolution figure from the existing snapshots |
| major | C1-4 | `cont1d_exercises.md:112` + chapter | introduce ẋ = −V′(x) or drop c) |
| major | C2-1 | `cont2d.md:51` | y = (θ₁/r₁)P, α = θ₂/r₁ |
| major | C2-2 | `cont2d.md:237` | T = a + d, D = ad − bc |
| major | C2-3 | `cont2d.md:249-252` | centre is diagonalisable; degenerate node at T² = 4D |
| major | C2-4 | `cont2d.md:689-704` | correct gradient of atan(y/x); u_θ ∝ 1/r |
| major | C2-5 | `cont2d.md:823` | unstable node for μ > 2 |
| major | C2-6 | `cont2d.md:839-868` | standard Lyapunov definition; LaSalle; not a "stable node" |
| major | C2-7 | `cont2d.md:1202` | subcritical Hopf: unstable cycle shrinks onto a persisting fixed point |
| major | C2-8 (eqs) | `cont2d.md:1213-1231` | Cartesian signs to match the polar form; "r" → μ; "−0,25" |
| major | C2-9 | `cont2d.md:542-551` | include the isoline/arrow panels; fix caption |
| major | C2-10 | `cont2d.md:914-933, 1022, 1031` | swap saddle-node rows; "subcritical pitchfork"; ±√(−μ) |
| major | C2-11 | `cont2d.md:1164` | J₁₁ = μ |
| major | C2-14 | `cont2d.md:711-716, 873-880` | limit cycle = isolated closed orbit; Poincaré–Bendixson stated correctly |
| major | C3-3 | `cont3d.md:869, 891` | H₀ of orbit (b); criterion H₀ < V_L2 |
| major | C3-4 | `cont3d.md:794-799` | add the y = 0 cross-section panel (exists as `cont4d_3body_Vcut`) |
| minor | P2 | `phenomenon.md:227`, exercises | N m² kg⁻² |
| minor | P3 | `phenomenon.md:15` | LGP-30, not a supercomputer |
| minor | P4 | `phenomenon.md:147, 175, 247`; exercise `:89` | lecture residue; bodies; columns; orbital radii |
| minor | P5 / A-3 | `phenomenon.md:147`, `app_twobody.md:37` | non-integrability, not "cannot be solved analytically" |
| minor | D1-8 | `disc1d.md:233` | "smaller than 1" |
| minor | D1-9 | `disc1d.md:772` | fix the `{eq}` role |
| minor | D1-10 | `disc1d.md:1121-1123` | join the paragraph |
| minor | D1-11 | `table:shiftmapconcept` | row labels y₀…y₃ |
| minor | D1-12 | `disc1d.md:29, 545, 594, 1293, 1367`, table | small slips; Latin "furca" |
| minor | D1-14 | `disc1d.md:1242` | "discovered … explained by renormalisation" |
| minor | D1-15 | `disc1d.md:1125-1137` | two-branch remark in the pdf derivation |
| minor | D1-16 | ch. 2 | define ⟨a,b⟩; iterate notation |
| minor | D1-17 | `disc1d_exercises.md:121` | r ∈ [0,1] |
| minor | D2-6 | `disc2d.md:1318` | e₂ = (−0.34, 0.94); 36° |
| minor | D2-7 | `disc2d.md:525-535` | U* = 0; dimensionless symbols; map singular at U = 0 |
| minor | D2-8 | `disc2d.md:751-759, 871` | tangential velocity; momentum balance; V(θ) |
| minor | D2-9 | `disc2d.md:978, 1081-1088` | Ω value; digits; reason for excluding period-1 roots |
| minor | D2-10 | `disc2d.md:248, 541, 987, 1234` | typos |
| minor | D2-14 | `disc2d.md:1387` | iteration count in caption |
| minor | D2-15 | `disc2d_exercises.md:93-95, 177` | finish part d); "estimate for Λ"; μ in the U-tube caption |
| minor | C1-6 | `cont1d.md:435, 627, 665, 906, 1005` | dangling Infobox; comma; z_j; T_*; table label |
| minor | C1-7 | `cont1d.md:230-243` | mention f′(x*) = 0 |
| minor | C1-8 | `cont1d.md:162` | basin {0} |
| minor | C1-9 | `cont1d_exercises.md:84` | "marginal", not "stable" |
| minor | C2-12 (eq) | `cont2d.md:723-724` | y in the second equation |
| minor | C2-13 | `cont2d.md:127, 245, 654, 683` | wording/sign |
| minor | C2-15 | `cont2d.md:255-260, 401, 430` | point to the T–D diagram, or make a gallery |
| minor | C2-16 | `cont2d.md:1093, 1096` | √; "saddle" |
| minor | C2-17 | `cont2d.md:825, 1065`; `shared/refs.bib` | cite roles; add Verhulst1996 |
| minor | C2-18 | `cont2d_exercises.md:27-66` | Allee; a vs b |
| minor | C2-19 | `cont2d.md` §5.7; exercise d), e) | add Bendixson–Dulac; reword d) |
| minor | C3-5 | `cont3d.md:774, 792` | centrifugal |
| minor | C3-6 | `cont3d.md:819` | note the Lagrange-point numbering convention |
| minor | C3-7 (rest) | `cont3d.md:14, 85, 380, 386, 515, 557-559, 725, 729, 862, 871` | wording, caption, dates |
| minor | C3-8 | `cont3d.md:636, 649` | H, not V |
| minor | C3-9 | `cont3d.md:571-577` | subcritical Hopf; coexistence for 24.06 < r < 24.74 |
| minor | C3-10 | `cont3d.md:559` | quadratic maximum |
| minor | C3-11 | `cont3d_exercises.md:81` | malonic acid; catalyst |
| minor | C3-12 | `cont3d_rosslertopology.png` + caption | shade the Möbius strip; show the half-twist; call it the Rössler template; cite |
| minor | F-1 | `fractals.md:174, 256`, exercise | show (or drop) the dripping-faucet comparison |
| minor | F-2 | `fractals.md:195` | ε |
| minor | PR-2 | `practice.md:315` | "in the spirit of" OGY |
| minor | PR-3 | `practice_exercises.md:62` | 0-based indexing |
| minor | A-1 | `app_lorenz.md:46-49` | rename the vertical coordinate; define a, b |
| minor | A-2 | `app_twobody.md:42, 61, 78` | mass ratio; duplicate eq refs |
| minor | CB-1 | cookbook cell 97 | "saddle" |
| — | §14, §15, §16 | whole book | one voice; rigour of ch. 5–6; copy-edit ch. 2–6 |
