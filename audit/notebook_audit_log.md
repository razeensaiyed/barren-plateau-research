# Notebook audit log — barren-plateau project

Running record of what each experimental notebook did, what it found, and what is
wrong with it. Compiled by reading source and stored outputs only — no notebook was
re-executed, so every number quoted here is the number that was actually produced at
the time.

**Purpose.** These notebooks are a working record, not a released library. Several
contain methodological defects that were found and corrected later in the project.
Documenting those defects openly is deliberate: the sequence of failed metrics and
rejected hypotheses is part of how the final result was reached, and the corrections
are traceable.

**Audit status:** 3 of 20 notebooks reviewed.

| # | File | Status |
|---|---|---|
| 01 | `01_entanglement_vs_gradient_variance.ipynb` | audited |
| 02 | `02_tau_bp_and_observable_support_INCOMPLETE.ipynb` | audited |
| 03 | `03_kn_collapse_test_rejected.ipynb` | audited |
| 04–20 | `Untitled31__1_` … `Untitled41__6_` | pending |

Notebooks are numbered in execution order. Files still named `UntitledNN` have not yet
been audited and are left under their original names rather than given a descriptive
name that would presume a conclusion.

Severity key:
- **BLOCKER** — any number produced by this notebook is unsafe to cite
- **MAJOR** — affects numeric values or conclusions, must be fixed or caveated
- **MINOR** — reproducibility / hygiene / documentation

---

## Cross-cutting issues (appear in more than one notebook)

| ID | Issue | Severity | Seen in |
|---|---|---|---|
| X1 | `np.var(np.abs(grads))` instead of `np.var(grads)` — underestimates true variance by ~2.75x for zero-mean gradients. Shifts any threshold crossing. | MAJOR | 29, 29_2 (cells 7/15/20/31) |
| X2 | Gradients pooled across all parameters before taking variance, rather than tracking one parameter across samples (McClean 2018 convention) | MAJOR | 29, 29_2, 30 |
| X3 | No RNG seed anywhere — no run is reproducible | MINOR | 29, 29_2, 30 |
| X4 | `abs` applied inconsistently between notebooks (29/29_2 use it, 30 does not) — τ values from different notebooks are not on the same scale | MAJOR | 29 vs 30 |
| X5 | Observable is always a contiguous Z-block on qubits 0..k-1. Never tested elsewhere on the register. Scope condition for the paper. | MINOR | 29_2, 30 |

---

## 01 — Untitled29.ipynb
**Entanglement growth vs gradient collapse**

Setup: n=10, depth 1–20, 30 samples/depth, cost = <Z0>.
Compares three entangling topologies: full CNOT chain, sparse fixed pairs, brick-wall.
Measures bipartite entanglement entropy (5|5 split) and gradient variance at each depth.

Findings:
- Full chain: entropy saturates ~4.25 at depth 12 (Page value for 5|5 is ~4.28 → simulation correct); gradient variance falls 100x over the same range.
- Sparse: entropy flat ~0.4, gradient variance flat ~4e-2, no plateau ever forms.
- Brick-wall: intermediate on both. Establishes that *rate of entanglement spread*, not entanglement alone, drives onset.
- NEGATIVE RESULT (cell 11): σ² ∝ 2^(−S) does not hold. Slope ≈ −0.8 not −1, and past depth 12 entropy saturates while variance keeps falling 20x more. Entropy cannot be the predictor. Motivates the later switch to depth-based onset.

Defects:
| # | Issue | Severity |
|---|---|---|
| 29-1 | `Sparse_HEA` hardcoded to CNOTs on (0,1),(2,3),(4,5) while N_QUBITS=10 → qubits 6–9 never entangled. Leftover from a 6-qubit version. "Sparse HEA" is a misleading label for what ran. | MAJOR |
| 29-2 | X1 (abs before var) | MAJOR |
| 29-3 | X2 (pooled parameters) | MAJOR |
| 29-4 | X3 (no seed) | MINOR |
| 29-5 | Stale 6-qubit comments in cells 6, 12, 18. Cell 6 and 18 code is correct for n=10; only the comments are wrong. | MINOR |

---

## 02 — Untitled29__2_.ipynb
**Aborted rerun at higher sample count + first appearance of τ_BP and k**

Same three-ansatz setup as 01 but N_SAMPLES raised 30 → 50. The run was too slow and was
manually interrupted. Historically important because this is where two ideas first appear:
the τ_BP onset metric, and observable support size k.

What is new:
- Cells 23–24: τ_BP defined as *first depth where variance < threshold*. Threshold swept over 0.05 / 0.03 / 0.02 / 0.01.
- Cells 25–26: metric changed to an exponential-decay fit, Var(L) = A·e^(−αL), with τ_BP = 1/α, explicitly to remove threshold dependence.
- Cells 30–41: observable support size k introduced. Z0, Z0Z1, Z0Z1Z2Z3, and full global. This is the origin of the k in the final scaling law.
- Cell 28: scaling study over n ∈ {4,6,8,10,12} scaffolded.

Defects:
| # | Issue | Severity |
|---|---|---|
| 29_2-1 | **Cells 23 and 24 printed τ_BP values computed on truncated arrays.** Cell 7 was interrupted at depth 15 (14 values stored); cell 20 was interrupted at depth 3 (2 values stored). "HEA τ_BP = 6" used 14 of 20 depths; "Brick-Wall τ_BP = >2" and "Sparse τ_BP = >2" are meaningless — those arrays had 2 entries. Python did not error because the sentinel return path masked it. | BLOCKER |
| 29_2-2 | Cell 26 raised `ValueError: shapes (20,) (14,)` — this is the truncation surfacing. Cell 27 raised `TypeError: expected x and y to have same length` for the same reason. Both were left in the notebook without rerun. | BLOCKER |
| 29_2-3 | Cell 31's exponential fit runs over depths 1..25 inclusive, i.e. across the entire curve including the flat noise-floor tail — not the declining region. Cell 26's version at least started at the peak. The later, worse version is the one that got reused. | BLOCKER |
| 29_2-4 | Cell 40 uses `all_grads.extend(grads)` with no `np.abs`, while cell 31 uses `np.abs(grads)`. Two τ_BP values in the same notebook computed on different scales. | MAJOR |
| 29_2-5 | Cell 32 interrupted → cells 33–36 never produced valid output. | MINOR |
| 29_2-6 | Cell 35 calls `cost_global(params, 5)` using a `params` left over from an unrelated earlier loop. | MINOR |
| 29_2-7 | Cell 37 contains the prose "creating new model ?" inside a code cell. | MINOR |
| 29_2-8 | X1, X2, X3 all still present. | MAJOR |

**Verdict:** no number in this notebook should be cited. Value is purely as provenance for
when τ_BP and k entered the project.

---

## 03 — Untitled30__1_.ipynb
**k/n scaling-collapse test — the hypothesis that was rejected**

Setup: brick-wall only. n ∈ {8,10,12}, k chosen as round(frac·n) for frac ∈ {0.2,0.4,0.6,0.8,1.0},
depth 1–25, 40 samples/depth. τ_BP from the exponential fit (1/α).

Hypothesis under test: does τ_BP depend only on the ratio k/n? If yes, all three n-curves
collapse onto one line and the paper has a single-variable law.

Result — the hypothesis fails. Curves do not collapse:

| k/n | n=8 | n=10 | n=12 |
|---|---|---|---|
| ~0.2 | 11.06 | 10.55 | 9.97 |
| ~0.4 | 11.14 | 9.01 | 8.87 |
| ~0.6 | 13.86 | 9.75 | 7.68 |
| ~0.8 | 14.49 | 11.43 | 10.23 |
| 1.0 | 23.95 | 19.95 | 15.08 |

This is the direct experimental basis for the memoed decision that "n and k independently
affect onset", which motivated the two-variable model and eventually the Product Model.

Defects:
| # | Issue | Severity |
|---|---|---|
| 30-1 | **τ_BP *increases* with k across the board, most sharply at k=n (8 → 24 for n=8).** This is physically backwards: a larger observable should make barren plateaus set in *earlier*, not later. The raw variance dump in cell 10 explains it — at k=10 the variance has already fallen to ~1.6e-3 and gone flat by depth 8, while k=2 is still declining at 2.1e-2. Fitting a single exponential across depths 1–25 therefore averages a steep early drop with a long flat tail and returns a small α, hence a large τ. **The 1/α metric is measuring the noise floor, not the onset.** | BLOCKER |
| 30-2 | `compute_tau_bp_fit` (cell 5) fits over every depth with variance > 1e-12, i.e. the whole curve. No peak detection, no declining-region restriction. Root cause of 30-1. | BLOCKER |
| 30-3 | The n=8 k/n=1.0 point (τ=23.95) is near MAX_DEPTH=25. The fit is extrapolating past the data. | MAJOR |
| 30-4 | Uses raw gradients (no `np.abs`), unlike notebooks 01 and 02 → X4. | MAJOR |
| 30-5 | X2, X3, X5 present. | MAJOR |

**Verdict:** the *conclusion* (k/n collapse rejected) survives, because it rests on curves
failing to overlap rather than on the absolute τ values. But every τ number in the table is
produced by a metric now known to be broken, so the table itself cannot go in the paper.
This notebook is the smoking gun for why the metric was replaced.

---

## Notebooks 04–20

Not yet audited. Entries will be appended in execution order.

---

## Open items for Pratham

Flags raised by the audit that require an experimental or methodological decision.
Listed in the order they were found, not by priority.

1. **Which variance convention is correct** — `np.var(np.abs(grads))` (notebooks 01, 02)
   or `np.var(grads)` (notebook 03)? These differ by roughly 2.75x for zero-mean
   gradients. Any τ_BP defined by a fixed threshold is sensitive to this factor, so the
   two conventions cannot be mixed across the dataset that produced the final fit.
2. **Whether to pool gradients across parameters** or track a single parameter across
   random samples, per McClean et al. 2018. Current notebooks pool. Either is defensible;
   the choice needs to be stated in Methods.
3. **Seeding.** No notebook seeds its RNG. Nothing produced so far is exactly reproducible.
4. **Observable placement.** Every observable is a contiguous Z-block on qubits 0..k-1.
   Whether the scaling law holds for observables placed elsewhere on the register is
   untested, and is a scope condition for the paper.
