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

**Audit status:** complete — 20 of 20 notebook files reviewed (10 distinct experiments).

| # | File | Status |
|---|---|---|
| 01 | `01_entanglement_vs_gradient_variance.ipynb` | audited |
| 02 | `02_tau_bp_and_observable_support_INCOMPLETE.ipynb` | audited |
| 03 | `03_kn_collapse_test_rejected.ipynb` | audited |
| 04 | `04_repeatability_validation.ipynb` | audited |
| 05 | `05_bootstrap_exponent_CI.ipynb` | audited |
| 06 | `06_causal_cone_mechanism.ipynb` (from `Untitled34__2_`) | audited |
| — | `Untitled34`, `34__1_`, `34__3_` | duplicates of 06, not committed |
| 07 | `07_entropy_cut_sensitivity.ipynb` (from `Untitled36`) | audited |
| 08 | `08_cross_architecture_longrange_INVALID.ipynb` (from `Untitled38__1_`) | audited |
| — | `Untitled38` (crashed run) | history only |
| 09 | `09_qiskit_demo_deck_NOT_AN_EXPERIMENT.ipynb` (from `Untitled40`) | audited |
| 10 | `10_noise_sweep_INCOMPLETE.ipynb` (from `Untitled41__6_`) | audited |
| — | `Untitled41` ×6 (generation A + crash states) | history only |

Notebooks are numbered in execution order. Suggested names are given for the two
newly audited experiments; the files on disk are still `UntitledNN` and should be renamed
before the repo is shared.

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
| X6 | ~~Raw data files not stored alongside notebooks.~~ **Resolved** — CSVs supplied and verified against notebook 06. | resolved | 32 |
| X7 | Notebooks depend on functions and variables defined in *other* notebooks' kernel sessions. Several cannot be executed top-to-bottom in a fresh kernel. | MAJOR | 34 |
| X8 | No output file records the run parameters that produced it. Results cannot be attributed to a specific notebook, sample count, or threshold. | MAJOR | all CSVs |
| X9 | Censored values (no threshold crossing within MAX_DEPTH) written as `MAX_DEPTH + 1` into the same column as real measurements, then fitted as if measured. | BLOCKER | 38, 41 |
| X10 | Resumable checkpoints key completion on the configuration only, so results computed under different simulator backends and differentiation methods are merged into one dataset with no provenance field. | MAJOR | 41 |
| X11 | Sample count varies across the project with no stated justification: 15 (nb 10), 30 (nb 01, 06, 07, 08), 40 (nb 03), 50 (nb 02, 04). Directly responsible for P3. | MAJOR | all |

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

## 04 — Untitled31__1_.ipynb
**Repeatability validation of the threshold metric** (labelled "Notebook 10" internally)

First notebook using the final metric: τ_BP = first depth where Var(∂C) < 1e-2.
Brick-wall only. Two configurations, (n=14,k=2) and (n=10,k=6), each repeated 10 times
with MAX_DEPTH=25, 50 samples/depth. Reports per-repeat τ, pointwise coefficient of
variation CV(L) = σ(L)/μ(L), and a "safety margin" (threshold − μ)/σ at the mean τ.

Results as printed:

| config | τ per repeat | mean | std | max CV | safety margin |
|---|---|---|---|---|---|
| n=14, k=2 | 13,13,13,13,13,13,15,13,13,13 | 13.2 | 0.60 | 9.75% | +1.29 |
| n=10, k=6 | 4,5,3,5,4,3,5,4,5,5 | 4.3 | 0.78 | 14.17% | **−0.46** |

Cell 0 contains a written project retrospective confirming the metric history: the
1/α exponential fit was abandoned after the noise-floor diagnosis, and replaced by
the threshold crossing. Useful provenance text.

Defects:
| # | Issue | Severity |
|---|---|---|
| 31-1 | **Safety margin for (10,6) is negative (−0.46).** The formula is (threshold − μ[τ̄])/σ[τ̄]; a negative value means the mean variance curve has *not yet* crossed 1e-2 at the mean crossing depth. Averaging per-repeat crossing depths and crossing the averaged curve give different answers here. The (10,6) crossing is marginal, not robust. | MAJOR |
| 31-2 | Pointwise CV for (10,6) exceeds the notebook's own 10% acceptance line at 8 of 25 depths, peaking at 14.2%. The (14,2) case peaks at 9.75%, just inside. Only one of the two configurations passes the stated criterion. | MAJOR |
| 31-3 | The loop variable is named `seed` and the dict is `variance_by_seed`, but **no seed is ever set**. These are 10 unseeded independent repeats. Valid for estimating run-to-run spread; not reproducible, and the naming is misleading. | MAJOR |
| 31-4 | Only 2 of the ~15 (n,k) configurations in the dataset were tested for repeatability. Neither is a low-τ or high-τ extreme. | MINOR |
| 31-5 | X2 (pooled parameters) still present. Uses raw gradients, no `np.abs` — consistent with 03, inconsistent with 01/02 (X4). | MAJOR |

**Verdict:** supports the memoed claim of "±1 depth jitter" — the spread really is ±1.
But the negative safety margin at (10,6) means at least one configuration sits close
enough to the threshold that the reported τ could move with more samples. This should
be rechecked before the number enters the fit.

---

## 05 — Untitled32.ipynb
**Bootstrap confidence interval on the scaling exponent** (labelled "Notebook 11" internally)

First notebook that seeds its RNG (`np.random.seed(42)`).
Loads `bp_threshold_dataset.csv` (15 rows: n, k, fraction, tau), resamples rows with
replacement 5000 times, fits log τ = log A − c·log(nk) by OLS each time, and reports the
percentile CI.

Results as printed:

```
A = 1644.398   std = 1081.668   95% CI = [800.395, 3678.555]
c = 1.4404     std = 0.0971     95% CI = [1.2723, 1.6557]
relative uncertainty on c = 6.74%  -> "PASS : Stable exponent"
```

The visible head of the dataset (n=8 rows) shows τ falling as k rises — 21, 17, 10, 5, 3
for k = 2, 3, 5, 6, 8. This is the physically correct direction, and confirms the
threshold metric does not suffer the inversion that broke the 1/α metric in notebook 03.

Defects:
| # | Issue | Severity |
|---|---|---|
| 32-1 | **The 1.31 vs 1.44 exponent discrepancy originates here.** The bootstrap mean slope is 1.4404; the value carried into `configs/default.yaml` and the paper is 1.31. For OLS, the bootstrap mean of a slope should sit close to the point estimate on the full sample — the standard reading of a gap this size is that it *is* the bootstrap's own bias estimate (bias ≈ +0.13, implying a bias-corrected c ≈ 1.18). Three candidate explanations, all testable once the CSV is available: (a) the 1.31 fit used a different row set, weighting, or model; (b) genuine small-sample bootstrap bias from a high-leverage point; (c) a transcription error. **This must be resolved before submission.** | BLOCKER |
| 32-2 | **A and c cannot be quoted from different fits.** In a log-log regression the intercept and slope are strongly anti-correlated: any change in c is compensated by a change in A. The pair (A=891.6, c=1.31) is internally coherent; (A=891.6, c=1.44) is not. Check: for n=8,k=2 (nk=16), A=891.6 with c=1.31 predicts τ≈23.6 against a measured 21; the same A with c=1.44 predicts τ≈16.4. | BLOCKER |
| 32-3 | A's 95% CI spans [800, 3679] — a factor of 4.6. Quoting A = 891.6 to four significant figures is not supportable by this data. The notebook's own commentary (cell 7) correctly notes that exponentiating the intercept inflates spread, but then treats the matter as closed rather than propagating the uncertainty. | MAJOR |
| 32-4 | **The bootstrap resamples configurations, not measurement error.** Each τ is treated as an exact integer. Notebook 04 established that τ carries ±1 run-to-run jitter. A two-level bootstrap (resample rows, then perturb τ within its measured jitter) would give an honest CI; the current one understates uncertainty. | MAJOR |
| 32-5 | τ is a small integer (values as low as 3). Taking logs of a discretized response and fitting unweighted OLS gives the low-τ rows an outsized and unmodelled relative error. Weighting or a discrete-response model should at least be considered. | MAJOR |
| 32-6 | **`bp_threshold_dataset.csv` is not present in the project files.** The dataset behind the paper's headline result is not currently preserved with the notebooks. It must be located and committed. | BLOCKER |
| 32-7 | Cell 7 is prose commentary pasted into a code cell, apparently LLM-generated. Its explanation of A's spread is correct as far as it goes, but it does not address 32-1 and asserts the chain of evidence is complete. Not a source of truth. | MINOR |

**Verdict:** the bootstrap itself is competently done and the exponent is well
identified — 6.74% relative uncertainty is genuinely good. But two blockers sit here:
the exponent discrepancy, and the missing dataset file.

---

## 06 — Untitled34 / 34__1_ / 34__2_ / 34__3_
**Causal-cone mechanism study** (labelled "Notebook 12A/12B" internally)

Four files. `34__2_` and `34__3_` are byte-identical (md5 5826947d...); `34` (7 cells) and
`34__1_` (11 cells) are earlier partial saves of the same session. **`34__2_` is the file of
record**; the other three are redundant snapshots.

Purpose: test whether τ_BP can be explained by the geometric causal cone — the set of qubits
that can influence the measured observable at a given depth.

### Finding A — the dataset is recovered here

Cell 11 hardcodes the full 15-row dataset that `bp_threshold_dataset.csv` contains:

| n | k values | τ values |
|---|---|---|
| 8 | 2, 3, 5, 6, 8 | 21, 17, 10, 5, 3 |
| 10 | 2, 4, 6, 8, 10 | 17, 11, 4, 2, 2 |
| 12 | 2, 5, 7, 10, 12 | 15, 6, 2, 2, 1 |

Confirmed identical to the CSV by re-running notebook 05's bootstrap on these rows: the
result reproduces bit-for-bit (c mean 1.4404, std 0.0971, CI [1.2723, 1.6557]; A mean
1644.40, std 1081.67, CI [800.39, 3678.55]). Blocker 32-6 is downgraded — the data is
recovered — but Pratham should still confirm the CSV matches before it is treated as canonical.

### Finding B — c = 1.31 and A = 891.6 do not come from this dataset

Unweighted OLS of log τ against log(nk) on all 15 rows gives:

```
c = 1.4262    A = 1410.33    R2 = 0.9397
```

The bootstrap bias is only +0.014, so small-sample bias is ruled out as an explanation —
the bootstrap is fully consistent with its own point estimate. Candidate variants tested:

| variant | rows | c | A | R² |
|---|---|---|---|---|
| all rows | 15 | 1.4262 | 1410.3 | 0.940 |
| drop τ≤2 (floor rows) | 10 | 1.2741 | 855.7 | 0.882 |
| drop τ≤2, add n=14 | 11 | 1.2796 | 877.1 | 0.884 |
| drop k=n rows | 12 | 1.3627 | 1146.2 | 0.919 |
| weighted by τ | 15 | 1.2491 | 782.7 | 0.913 |

An exhaustive search over all removals of up to 5 rows finds no principled subset that
lands on (1.31, 891.6); the nearest matches require dropping five rows with no coherent
rationale. Notebook 13 (`Untitled38`) hardcodes both constants with the comment
`# User provided Brick-Wall reference constants` — they were pasted in, not fitted there.

**Conclusion: the paper's headline constants cannot currently be traced to any dataset in
these notebooks.** They most likely come from a later or larger re-run not present here.

### Finding C — the causal cone does not predict τ_BP

Cells 3–4 implement the cone as a static graph and take connected components. This is
wrong: it ignores time ordering, and reports the cone covering all 10 qubits at depth 2.
Cell 6 replaces it with correct backward layer-by-layer propagation, giving the expected
Lieb-Robinson growth of one qubit per layer. Good self-correction, worth keeping in the record.

Cells 8–9 then evaluate cone size *at depth τ* and find cone_fraction ≈ 1.0 for 13 of 15
rows (mean 0.967). The notebook reads this as confirmation. It is not — recomputing the
depth at which the cone first saturates shows it happens long *before* τ:

| n | k | τ | cone saturates at | gap |
|---|---|---|---|---|
| 8 | 2 | 21 | 6 | +15 |
| 8 | 3 | 17 | 5 | +12 |
| 8 | 5 | 10 | 3 | +7 |
| 10 | 2 | 17 | 8 | +9 |
| 10 | 4 | 11 | 6 | +5 |
| 10 | 6 | 4 | 4 | 0 |
| 12 | 2 | 15 | 10 | +5 |
| 12 | 5 | 6 | 7 | −1 |
| 12 | 7 | 2 | 5 | −3 |

The gap ranges from +15 to −3. For small k the cone covers the register 15 layers before
the plateau arrives; for two n=12 rows the plateau arrives *before* the cone saturates.
Finding cone_fraction ≈ 1 at τ is therefore vacuous — the cone had saturated regardless.

This contradicts the working framing that τ_BP is the cone-crossing depth. Cone saturation
is plausibly *necessary* for a plateau but is clearly not *sufficient*, and it is not the
quantity τ_BP measures.

Defects:
| # | Issue | Severity |
|---|---|---|
| 34-1 | **Cone-saturation depth and τ_BP differ by −3 to +15 layers.** The mechanism claim as stated is not supported by the notebook's own data. Needs reframing before it enters the paper. | BLOCKER |
| 34-2 | Cells 3–4 static-graph cone ignores gate time-ordering and is incorrect. Superseded by cell 6 but left in the notebook without annotation. | MAJOR |
| 34-3 | Cell 8 uses `dataset` before cell 11 defines it. The notebook cannot be re-run top to bottom — it depends on kernel state from an earlier session. | MAJOR |
| 34-4 | Cell 12 calls `BrickWall_HEA` and `make_observable`, neither defined in this notebook. Same kernel-state dependency. | MAJOR |
| 34-5 | `GRAD_EPS = 1e-4` for "effective gradient support" is unjustified and unswept. grad_fraction results (CV 17.2%) depend directly on it. | MAJOR |
| 34-6 | Gradient support uses only 30 samples, below the 50 used elsewhere. | MINOR |
| 34-7 | Four near-duplicate files; two byte-identical. Only `34__2_` should be committed. | MINOR |

**Verdict:** the most valuable notebook so far and the most concerning. It recovers the
dataset, but its central mechanism claim does not survive checking, and it exposes that the
published constants are untraceable.

---

## Data files — verification pass

Six CSVs accompany the notebooks. `repeatability_checkpoint_1` and `_2` are byte-identical,
as are `noise_partial` and `noise_partial_1`. Commit one of each.

### Verified

- **`bp_threshold_dataset.csv` matches notebook 06 cell 11 exactly** (all 15 rows, n/k/tau).
  The hardcoded copy and the CSV are the same data.
- **Fit on the real CSV confirms the earlier reconstruction:** c = 1.4262, A = 1410.3,
  R² = 0.9397. The published pair (c = 1.31, A = 891.6) remains untraceable to this file.
- Adding the two n=14 rows from `repeatability_checkpoint_4.csv` moves the fit to
  c = 1.3884, A = 1238.7, R² = 0.9485 — closer to the published value but still not it.

### Contradiction 1 — repeatability: three different answers

`repeatability_checkpoint_4.csv` reports **zero** run-to-run variation across all five
configurations (10 runs each, std = 0.00 for every one, including n=14,k=2 → 13 ten times).
Notebook 04 reports the same configurations with genuine jitter:

| config | checkpoint CSV | notebook 04 |
|---|---|---|
| n=14, k=2 | 13 ×10, std 0.00 | 13,13,13,13,13,13,**15**,13,13,13 — std 0.63 |
| n=10, k=6 | 4 ×10, std 0.00 | 4,5,3,5,4,3,5,4,5,5 — std 0.82 |

Same n, same k, same metric, different answers. The CSV is presumably the earlier run
referenced in notebook 04's retrospective ("You already showed CV = 0"), and notebook 04
was the stronger re-test that found the jitter. If so the CSV's zero-variance result is
superseded and should not be cited — but which run used which sample count and threshold
is not recorded anywhere.

### Contradiction 2 — the noiseless baseline disagrees with the main dataset

`noise_partial.csv` at noise = 0.0 covers the same Brick-Wall n=8 configurations as the
main dataset. Four of five disagree:

| n | k | noise_partial | bp_threshold_dataset | diff |
|---|---|---|---|---|
| 8 | 2 | 19 | 21 | −2 |
| 8 | 3 | 18 | 17 | +1 |
| 8 | 5 | 8 | 10 | −2 |
| 8 | 6 | 7 | 5 | +2 |
| 8 | 8 | 3 | 3 | 0 |

Two independent noiseless runs of identical configurations differ by up to ±2 depths.

*Update (notebook 10): resolved.* `noise_partial.csv` is written by the `Untitled41` noise
sweep, which runs at `N_SAMPLES = 15` against the 30–50 used elsewhere. The ±2 is sampling
scatter at a low sample count, not a disagreement between two comparable runs. See section 10,
Finding A.

**Taken together, the three sources give τ measurement uncertainty of 0, ±1, and ±2.**
This has to be settled: the noise study in particular cannot detect a noise-induced shift
in τ smaller than its own baseline scatter, and ±2 is larger than several τ values in the
dataset.

Sensitivity check: refitting with the `noise_partial` values substituted into the n=8 rows
moves the exponent from 1.4262 to 1.4091 — a shift of 0.017. So measurement scatter of
this size does **not** explain the 1.31 discrepancy, which is roughly 0.11.

Defects:
| # | Issue | Severity |
|---|---|---|
| D-1 | Repeatability CSVs (std = 0.00) and notebook 04 (std ≈ 0.6–0.8) disagree on the same configurations. Provenance of each run is unrecorded. | BLOCKER |
| D-2 | `noise_partial.csv` noiseless baseline disagrees with `bp_threshold_dataset.csv` by up to ±2 on 4 of 5 shared rows. τ uncertainty is larger than previously assumed. | BLOCKER |
| D-3 | No CSV records the parameters that produced it (N_SAMPLES, threshold, seed, date, source notebook). None can be attributed to a specific run. | MAJOR |
| D-4 | `repeatability_checkpoint_1`/`_2` identical; `noise_partial`/`noise_partial_1` identical. Numbered checkpoints 1,2,4 with no 3. | MINOR |

---

## 07 — Untitled36.ipynb
**Entropy cut sensitivity at τ_BP** (labelled "Notebook 13A" internally)

Asks whether the bipartite entanglement entropy measured *at* τ_BP is a meaningful quantity,
by measuring it at four different cut positions (k−1, k, k+1, middle) for four representative
configurations. Brick-wall ansatz, 30 samples per point.

Entropy at τ, by cut:

| config | k−1 | k | k+1 | middle | spread |
|---|---|---|---|---|---|
| n=8, k=2, τ=21 | 0.929 | 1.742 | 2.483 | 2.734 | 1.805 |
| n=10, k=6, τ=4 | 0.553 | 0.809 | 0.549 | 0.605 | 0.260 |
| n=12, k=12, τ=1 | 0.377 | 0.185 | 0.274 | ~0 | 0.377 |
| n=14, k=2, τ=13 | 0.858 | 1.483 | 1.868 | 2.411 | 1.553 |

Average spread across cuts: 0.999 bits. Per-cut CV ranges from 38% (k−1) to 93% (middle).

### Finding A — entropy at τ_BP is low, and cut-dependent

For n=8 the maximum possible entropy at a 4|4 cut is 4.0; the measured value at τ is
0.93–2.73 depending where the cut is taken. The state is nowhere near maximally entangled
when the plateau arrives. Combined with notebook 01 (where entropy saturates near the Page
value and gradients keep falling afterwards), this closes the loop: **entanglement entropy
is neither a sufficient nor a well-defined predictor of τ_BP** — it depends on an arbitrary
choice of cut, and varies by a full bit across reasonable choices.

Useful for the Discussion as a documented dead end. Not useful as a mechanism.

### Finding B — accidental repeat measurements quantify sampling noise

The cut-position dictionary clamps values, so several "different" cuts collapse to the same
cut and were measured more than once in the same run:

- **n=12, k=12: cut = 11 measured three times** → 0.3773, 0.1848, 0.2737.
  Mean 0.279, std 0.096, **CV 34.6%**, max/min = 2.04×.
- **n=10, k=6: cut = 5 measured twice** → 0.5526, 0.6049. Spread 9.0%.

Same quantity, same circuit, same depth, same run — answers differing by a factor of two.
This is an unintended but clean measurement of sampling noise at N_SAMPLES = 30, and it is
large. Directly relevant to the τ-uncertainty question (parking lot P2/P3): if a 30-sample
entropy estimate scatters by 35%, a 30-sample *variance* estimate near a fixed threshold can
easily move a crossing by a depth or two.

Defects:
| # | Issue | Severity |
|---|---|---|
| 36-1 | Cut dictionary silently collapses distinct labels onto the same cut for k near n (all three of k−1, k, k+1 become 11 for n=12,k=12). The table reports them as different cuts. | MAJOR |
| 36-2 | N_SAMPLES = 30, against 50 in notebooks 04 and 05. Sampling noise of ~35% at this count (Finding B). | MAJOR |
| 36-3 | Cell 2 calls `BrickWall_HEA` before cell 3 defines it — X7 again. Cannot run top to bottom. | MAJOR |
| 36-4 | Middle-cut entropy for n=12,k=12 returns −9.6e−17. Numerical, harmless, but should be clamped to zero before display. | MINOR |
| 36-5 | No seed. Only 4 of 15 configurations tested. | MINOR |

**Verdict:** a clean negative result on entropy as a mechanism, plus an accidental and
valuable noise measurement. No new τ values; nothing here feeds the fit.

---

## 08 — Untitled38.ipynb / Untitled38__1_.ipynb
**Cross-architecture comparison: Brick-Wall vs "Long-Range" HEA** (labelled "Notebook 14" internally)

Two files. `Untitled38` **crashed** (`NameError: make_observable is not defined`) and produced
no results. `Untitled38__1_` is the successful re-run and is the file of record.

In both files, the saved cell source does **not** match the code that actually executed —
the traceback in `Untitled38` references variables (`k_obs`, `def lr_cost(params, depth, n=n_val)`)
that do not appear in the saved source (`current_k`, `depth_val`), and cell 2 of both files
calls `longrange_df` while cell 1 defines `lr_df`. The notebooks were edited after running.

Long-Range results as printed (`Untitled38__1_`):

| n | k=... | τ |
|---|---|---|
| 8 | 2, 3, 5, 6, 8 | 26, 26, 2, 3, 4 |
| 10 | 2, 4, 6, 8, 10 | 26, 3, 2, 2, 2 |
| 12 | 2, 5, 7, 10, 12 | 26, 1, 1, 1, 1 |

Reported fit: `A = 3319.98, c = 1.736, AICc = 30.12, LOOCV MSE = 0.3980`.

### Finding A — the "Long-Range HEA" is four disconnected two-qubit circuits

`LongRange_HEA` applies CNOTs only between q and q+n/2:

```
even layers: (q, q+half) for q in range(half)
odd layers:  (q, q+half) for q in range(1, half)
```

Building the connectivity graph over 25 layers gives:

| n | connected components | qubit 0 can ever reach |
|---|---|---|
| 8 | 4 → [0,4] [1,5] [2,6] [3,7] | {0, 4} |
| 10 | 5 → [0,5] [1,6] [2,7] [3,8] [4,9] | {0, 5} |
| 12 | 6 → [0,6] [1,7] [2,8] [3,9] [4,10] [5,11] | {0, 6} |

The odd/even distinction changes nothing — both layers use the same pairing. Qubit 0 never
interacts with qubits 1, 2, or 3 at any depth. **This is the same defect as the sparse ansatz
in notebook 01**: an architecture that is nominally "long-range" but is in fact a product of
independent 2-qubit circuits.

`Untitled38` contains a verification step that prints
`n=8: BW even=4 odd=3 | LR even=4 odd=3 | Match=True` — it checks that the two ansätze use the
same *number* of CNOTs, not that the long-range one is connected. Gate count is not topology.

Everything downstream is therefore invalid: the τ values, the fit (A=3319.98, c=1.736), the
AICc, and the LOOCV. The comparison does not test what it claims to test.

### Finding B — the fit was run on censored data

`compute_tau_bp_threshold` returns `None` when no crossing occurs, and the caller substitutes
`MAX_DEPTH + 1 = 26`. Four rows are 26 — (8,2), (8,3), (10,2), (12,2) — meaning *no crossing
was found within 25 depths*. These are censored observations, not measurements, and they were
fed into the OLS fit as if they were real τ values. With 4 of 15 rows censored at the ceiling,
the reported exponent is meaningless independently of Finding A.

### Finding C — the repeatability check does not re-run anything

```python
for s in seeds:
    np.random.seed(s)
    rep_results.append(lr_df[(lr_df['n']==10) & (lr_df['k']==4)]['tau'].values[0])
```

This sets a seed and then reads the same stored value from the dataframe three times. No
circuit is executed. The printed result `[3, 3, 3]` is the same number repeated, not three
independent runs agreeing. The source comment acknowledges it:
`# Simulating a quick re-run check logic`.

**This is a strong candidate explanation for parking-lot item P2** — if the same pattern
produced the repeatability checkpoint CSVs, their zero variance is an artifact of re-reading
one value rather than evidence of stability.

### Finding D — a third variance convention

```python
grads = [float(np.var(qml.grad(lr_cost)(p, depth))) for p in params]
variances.append(np.mean(grads))
```

This computes the variance *within* each sample's gradient vector, then averages across
samples. Notebooks 01–02 pool all gradients then take one variance of absolute values;
notebooks 03–04 pool then take one variance of raw values. Three different estimators are
now in use across the project, all called "gradient variance".

Defects:
| # | Issue | Severity |
|---|---|---|
| 38-1 | `LongRange_HEA` is disconnected — n/2 independent 2-qubit circuits. All results invalid. | BLOCKER |
| 38-2 | Censored values (τ=26 = MAX_DEPTH+1) fed into the OLS fit as measurements. 4 of 15 rows. | BLOCKER |
| 38-3 | Repeatability check re-reads a stored value instead of re-running. Printed `[3,3,3]` is not evidence of stability. | BLOCKER |
| 38-4 | Third variance convention (per-sample variance then mean). | MAJOR |
| 38-5 | Saved source does not match executed code in either file; tracebacks reference variables absent from the saved cells. | MAJOR |
| 38-6 | τ non-monotonic in k for n=8 long-range (26, 26, 2, 3, 4 — rises from k=5 to k=8), a further symptom of 38-1. | MAJOR |
| 38-7 | Cell 2 references `longrange_df`, cell 1 defines `lr_df`. Kernel-state dependency (X7). | MAJOR |
| 38-8 | N_SAMPLES = 30 (P6). No seed on the main sweep. | MAJOR |
| 38-9 | `Untitled38` crashed and produced nothing; keep as history, do not cite. | MINOR |

**Verdict:** the cross-architecture comparison must be re-run from scratch with a genuinely
connected long-range ansatz, censored rows handled explicitly, and a real repeatability check.
It does not resolve P1 — the constants are again hardcoded, not derived. It does, however,
give the most likely explanation for P2.

---

## 09 — Untitled40.ipynb
**Qiskit demonstration deck — no experiment is run here**

Setup: Qiskit (every other notebook in the project uses PennyLane). 15 cells. Defines a
brick-wall ansatz and an all-to-all ansatz, draws both at n=4, then presents eight
"findings" as plots plus a summary dashboard.

**This notebook computes no gradient and simulates no variance.** It is a presentation of
results obtained elsewhere. Every quantity plotted is synthetic or pasted in:

| cell | what it displays | where the numbers come from |
|---|---|---|
| 7 | gradient-variance decay, k=2 vs k=4 | `np.exp(-0.18*d)` and `np.exp(-0.38*d)` plus uniform noise. Source comment: "Representative curves mimicking the research findings" |
| 8 | τ_BP for those curves | thresholding the synthetic curves |
| 9 | scaling-law fit | τ = [21,17,15,13] hardcoded for n = 8,10,12,14 at k=2 |
| 10 | "backward causal cone" | a decorative scatter plot; no cone is computed |
| 11 | noise robustness | τ_k2 = [13,11,8], τ_k4 = [4,3,2] hardcoded |
| 12 | brick-wall vs all-to-all | brick = [21,11,6,3], all-to-all = [13,7,4,2] hardcoded |

The brick-wall implementation (cell 3) is structurally faithful to the `BrickWall_HEA` used
elsewhere — RY layer, then alternating CNOTs — so the circuit drawings are honest. Only the
numbers are not.

### Finding A — the notebook's own threshold demo returns None, and the slide underneath says otherwise

Cell 8's stored output:

```
k=2  τBP = None
k=4  τBP = None

Observation:
Smaller observable support remains trainable longer.
```

Re-running cell 7 under its stated seed gives min(var_k2) = 0.1724 and min(var_k4) = 0.0253 —
both above the 1e-2 threshold at every depth 1–10 — so `tau()` correctly returns `None` twice.
The "Observation" beneath it is an unconditional `print`, not a result. As rendered, this is a
slide asserting a finding immediately below the evidence that failed to produce it.

### Finding B — a fourth (A, c) pair, from a fit that cannot see k

Cell 9 is the only cell touching real data: τ = 21, 17, 15, 13 at n = 8, 10, 12, 14 with k = 2.
The first three rows match `bp_threshold_dataset.csv`; the fourth matches
`repeatability_checkpoint_4.csv`. It fits with `scipy.optimize.curve_fit` and printed:

```
A = 219.21
c = 0.85
```

Reproduced exactly. But **k is fixed at 2 for all four points**, so nk varies only through n
(16, 20, 24, 28). The fit cannot separate n-dependence from k-dependence; it is an n-only fit
presented as the (nk) law. Extrapolating it to k=n is unsupported.

The project now carries four different (A, c) pairs:

| source | A | c | method |
|---|---|---|---|
| paper / `configs/default.yaml` | 891.6 | 1.31 | undocumented |
| notebook 05 bootstrap mean | 1644.4 | 1.4404 | log-log OLS, 15 rows |
| notebook 06 point estimate | 1410.3 | 1.4262 | log-log OLS, 15 rows |
| notebook 09 cell 9 | 219.2 | 0.85 | non-linear LS, 4 rows, k=2 only |

### Finding C — `all_to_all` is written but never measured

`all_to_all` (cell 5) applies a CNOT to every pair (i,j) in every layer, so unlike the
"Long-Range" ansatz of notebook 08 it is genuinely connected. It is drawn at n=4 and then never
used for any computation — the brick-wall vs all-to-all comparison in cell 12 is hardcoded.
**This is a candidate fix for P7 that was written but never run.**

Defects:
| # | Issue | Severity |
|---|---|---|
| 40-1 | **Every plotted number is synthetic or hardcoded.** Nothing in this notebook is a measurement. The output is visually indistinguishable from the real experiment notebooks and carries no marking that says so. | BLOCKER |
| 40-2 | Cell 8 prints `τBP = None` twice and is immediately followed by a hardcoded conclusion stating the opposite. | BLOCKER |
| 40-3 | Cell 9 fits four points that all share k=2, then labels the result the (nk) scaling law. A = 219.21, c = 0.85 cannot be compared with any other fit in the project. | MAJOR |
| 40-4 | Cell 13's "Research Dashboard" marks eight findings "✅ Demonstrated", including External Validation, Bootstrap Confidence Intervals and Repeatability Analysis, which the same cell then says are "omitted here for runtime". | MAJOR |
| 40-5 | Cell 10 is captioned "Backward Causal Cone Expansion" and prints "Finding: Observable influence expands layer-by-layer". It is a scatter plot of `range(depth+2)`; no circuit or cone is involved. Notebook 06 showed this claim does not hold in the form stated. | MAJOR |
| 40-6 | Cell 11 asserts "Noise accelerates BP onset" from three hardcoded pairs. The real noise sweep (notebook 10) never completed a single noisy configuration, so this claim has no measured backing anywhere in the project. | MAJOR |
| 40-7 | Qiskit-only notebook in an otherwise PennyLane project; ansatz definitions are duplicated rather than imported, so the two can drift apart silently. | MINOR |
| 40-8 | `all_to_all` defined and drawn but never executed for measurement. | MINOR |

**Verdict:** this is a talk or viva deck, not an experiment, and it should be renamed to say so
before it is stored beside the experimental notebooks. Its one real contribution is negative:
it establishes that `scipy.optimize.curve_fit` — non-linear least squares in linear space — is
part of this project's fitting toolbox, which turns out to matter a great deal for P1 (below).

---

## Re-examination of P1 — it is the fit *method*, not the dataset

Every reconstruction of the published constants so far assumed unweighted **log-log OLS**, and
on that assumption A = 891.6, c = 1.31 was untraceable: the 15-row dataset gives 1.4262, and an
exhaustive search over subsets found nothing principled landing on the published pair. Notebook
09 shows the project also uses `curve_fit`, i.e. least squares **in linear space on τ itself**.
Repeating the reconstruction across fit methods on the same 15 rows:

| method | A | c |
|---|---|---|
| log-log OLS (assumed until now) | 1410.33 | 1.4262 |
| log-log OLS, weighted by τ | 782.74 | 1.2491 |
| non-linear LS, unweighted | 521.15 | 1.1300 |
| non-linear LS, σ = τ | 1344.22 | 1.4326 |
| **non-linear LS, σ = √τ (Poisson weighting)** | **932.94** | **1.3194** |
| non-linear LS, σ = √τ, dropping the single τ=1 row | **885.66** | **1.3028** |
| non-linear LS, σ = √τ, 17 rows (+ n=14) | 937.25 | 1.3173 |

τ is a count of layers, so σ = √τ is the natural weighting, not an arbitrary one. It reproduces
the published pair to within **0.7% in A and 0.008 in c** once the single floor row (n=12, k=12,
τ=1) is excluded — an exclusion the project already applies elsewhere.

This is a reconstruction, not proof: it is not exact, and the original script has still not been
found. But it changes the diagnosis. **P1 is most likely not a wrong number — it is an
undocumented weighting choice.** Two consequences follow immediately:

1. **The bootstrap CI in notebook 05 does not apply to the published exponent.** That CI,
   [1.2723, 1.6557], is the sampling distribution of the *log-log OLS* estimator. If the paper's
   c = 1.31 comes from weighted non-linear LS, quoting the OLS bootstrap CI alongside it pairs an
   estimate with another estimator's uncertainty. The bootstrap must be re-run under whichever
   fit the paper actually uses.
2. **Methods must state the estimator and the weighting**, not just the model. The same 15 rows
   yield c anywhere from 1.13 to 1.43 depending on that choice alone — a range far wider than the
   6.74% relative uncertainty notebook 05 reports.

Defects:
| # | Issue | Severity |
|---|---|---|
| P1-a | The fit method behind the published constants is undocumented, and the choice moves c across [1.13, 1.43] on identical data. | BLOCKER |
| P1-b | Notebook 05's bootstrap CI is computed for a different estimator than the one that most plausibly produced c = 1.31, but is quoted as its uncertainty. | BLOCKER |
| P1-c | The audit's earlier statement that "no principled subset reproduces (1.31, 891.6)" was correct only for unweighted log-log OLS. Corrected here. | — |

---

## 10 — Untitled41 series (7 files)
**Depolarizing-noise sweep — stopped at 15 of 120 configurations; this is the notebook that wrote `noise_partial.csv`**

Seven saves of one Colab session. All seven are distinct files — no byte-identical pair, unlike
the notebook 06 group. They fall into two code generations:

| file | sweep-cell size | generation | outcome of the sweep cell |
|---|---|---|---|
| `Untitled41.ipynb` | 3 cells only | A | scaffold, never run |
| `Untitled41 (1)` | 6229 | A | no stored output |
| `Untitled41 (2)` | 6319 | A | `AttributeError`: partially initialised `pennylane` (circular import) |
| `Untitled41 (3)` | 6319 | A | resumed at 6/120, printed `Running: Brick-Wall p=0.0 n=10 k=4`, then nothing |
| `Untitled41 (4)` | 4897 | B | `QuantumFunctionError`: `default.mixed` does not support adjoint |
| `Untitled41 (5)` | 5009 | B | `TypeError`: `grad.__init__() got an unexpected keyword argument 'argnum'` |
| `Untitled41 (6)` | 5048 | B | **ran** — 9 further configs completed, died inside the 16th |

**`Untitled41 (6).ipynb` is the file of record for what executed.** Generation A is the file of
record for what was *intended*: it is the only generation that defines `noise_df`, without which
the analysis block cannot run (defect 41-3).

Design: SYSTEMS = {8,10,12} with the same SUPPORTS as the main dataset, MAX_DEPTH = 25,
THRESHOLD = 1e-2, NOISE_LEVELS = [0.000, 0.005, 0.020, 0.050], two architectures
(Brick-Wall, Long-Range) — 120 configurations, checkpointed to Google Drive after every one.
Depolarizing channels are inserted on both qubits after each CNOT, and only when p > 0, so the
p = 0 circuit is structurally identical to `BrickWall_HEA`.

Variance convention: `grads_all.extend(...)` then `np.var(grads_all)` — pooled, raw, no `np.abs`.
This matches notebooks 03 and 04 (convention 2 of P4). Worth recording as a point of consistency.

### Finding A — P3 is explained: `noise_partial.csv` is a 15-sample run

The sweep writes `noise_partial.csv` after each configuration, in loop order: Brick-Wall first,
p = 0.000 first, n = 8 first, k ascending. The five rows in the repo are exactly the first five
configurations of that loop, and they are the five rows that disagree with the main dataset.

**`N_SAMPLES = 15`** — the lowest count anywhere in the project, against 30 in notebooks 01/06/07,
40 in notebook 03 and 50 in notebooks 02/04. This is a sufficient explanation for P3 without
invoking any error: notebook 07 measured a coefficient of variation of 34.6% on a 30-sample
estimator, which scales to roughly 49% at 15 samples; notebook 01 puts the variance decay at
about 0.24 per layer (a factor of 100 over 19 layers). A ±50% multiplicative error on the
variance therefore moves a fixed-threshold crossing by ln(1.5)/0.24 ≈ 1.7 layers — the ±2 that
was observed.

P3 was never a contradiction between two measurements of the same thing. It is one measurement at
15 samples and another at 30–50, and the 15-sample one is the noise study's own baseline.

### Finding B — the completed noiseless sweep exists, but not in this repo

`Untitled41 (6)` resumed from a checkpoint holding 6 finished configurations and went on to
complete n=10 (k=4,6,8,10) and all of n=12 (k=2,5,7,10,12) — **all 15 noiseless Brick-Wall
configurations**, matching the main dataset's grid exactly. It then started the first noisy
configuration (p=0.005, n=8, k=2) on `default.mixed` and the output ends at depth 5.

τ is never printed, so those 15 values cannot be recovered from the notebook. They are in
`/content/drive/MyDrive/Quantum_Experiments/noise_checkpoint.pkl`, together with every variance
curve — **a data file that is not in the repo**. The repo's `noise_partial.csv` is a stale
five-row snapshot; the Drive copy should hold fifteen.

Recovering that pickle would settle P3 outright: a complete 15-sample noiseless replicate of the
main dataset, with curves, is exactly the control needed to convert "τ has some unknown
uncertainty" into a measured number.

### Finding C — the checkpoint silently merges two code generations

The 6 resumed configurations were produced by an earlier run; the 9 new ones by generation B.
Between generations the backend and the differentiation method both changed:

| generation | device at p = 0 | diff_method |
|---|---|---|
| A | `default.mixed` | `backprop` |
| B | `lightning.qubit` | `parameter-shift` |

`completed` is keyed only on (architecture, p, n, k), so a configuration finished under one
generation is never recomputed under the next. The 15-row noiseless block in the pickle is
therefore **a mixture of two simulators and two gradient methods**, with no record of which row
came from which. Whatever is recovered from Drive must be re-run under one configuration before
it is used as a control.

### Finding D — the P7 fix does not fix P7

`LongRange_HEA_noise` was rewritten against notebook 08's version, replacing the plain `q+n/2`
pairing with modular arithmetic and giving odd layers a different control:

```python
even: for q in range(half_n):        target = (q + half_n) % n
odd:  for q in range(half_n):        control = (q+1) % n ; target = (control + half_n) % n
```

Building the edge set over 25 layers:

| n | edges | components |
|---|---|---|
| 8 | (0,4) (1,5) (2,6) (3,7) | 4 |
| 10 | (0,5) (1,6) (2,7) (3,8) (4,9) | 5 |
| 12 | (0,6) (1,7) (2,8) (3,9) (4,10) (5,11) | 6 |

Identical to notebook 08. The odd-layer branch relabels which qubit of a pair is the control and
adds the pair (half_n, 0), which the even layer already contains — **zero new edges**. The
architecture is still n/2 independent two-qubit circuits and qubit 0 still never interacts with
qubits 1–3.

The rewrite looks like a targeted fix and is not one. Nothing invalid was published from it only
because the Long-Range half of the sweep never ran.

### Finding E — the analysis block was never executed, in any of the seven files

The 8903-character analysis cell (fit, LOOCV, Wilcoxon, six figures, CSV export) is byte-identical
across all seven files and has **no output and no execution count in any of them**. Its defects
are therefore latent rather than realised — but the same machinery produced the `AICc = 30.12`
and `LOOCV MSE = 0.3980` reported in notebook 08, so they are worth recording:

- The model is fitted in log space with `sm.OLS(log τ, const + log nk)`, but `R2` is then computed
  with `r2_score(τ, predicted τ)` in **linear** space, while `AIC`/`BIC` are taken from the
  **log-space** regression. These are put in one comparison table. AIC and BIC are not comparable
  across different response transformations, and an R² from one space does not describe a fit in
  the other.
- The AICc correction uses `k_params = 2`. For an OLS model the variance is an estimated parameter
  too, so the small-sample correction should use 3; with n = 15 this understates it.
- MAPE is reported on τ values as low as 1.
- `stats.wilcoxon(base_tau, noisy_tau)` pairs the two arrays **positionally**, relying on
  `groupby` returning both in the same (n,k) order rather than merging on keys. It also runs on
  data where τ is censored at 26 and heavily tied.
- Figure 1 pads short curves with `var_data.extend(...)` where `var_data` **is** the list stored in
  `variance_curves`. This mutates the checkpointed data in place; re-running the cell lengthens the
  stored curves again.
- Cell 8 writes `noise_df.csv` and `noise_model_summary.csv` to `./results` — Colab-local, not
  Drive. In a notebook built entirely around Drive persistence, the final outputs are the only
  things not persisted, which is very likely why neither file exists.

Defects:
| # | Issue | Severity |
|---|---|---|
| 41-1 | **`N_SAMPLES = 15`**, the lowest in the project, used for the noise study's own noiseless baseline. Root cause of P3. | BLOCKER |
| 41-2 | `LongRange_HEA_noise` is still disconnected — n/2 independent 2-qubit circuits, edge-for-edge identical to notebook 08. The rewrite reads as a fix and changes nothing. | BLOCKER |
| 41-3 | Generation B (`(4)`, `(5)`, `(6)` — the only generation that ran) never defines `noise_df`, which the analysis block's first line requires. As saved, the file of record cannot produce any analysis. | BLOCKER |
| 41-4 | The checkpoint's `completed` set is keyed only on (arch, p, n, k), so results computed under different backends and differentiation methods are merged into one dataset with no provenance field. | MAJOR |
| 41-5 | τ censored at `MAX_DEPTH + 1 = 26` when no crossing occurs, as a plain value in the same column as real measurements — the identical defect to 38-2, carried forward unchanged. | MAJOR |
| 41-6 | Linear-space R² and log-space AIC/BIC reported in one model-comparison table; AICc uses `k_params = 2`. Same machinery produced notebook 08's reported AICc and LOOCV. | MAJOR |
| 41-7 | Wilcoxon test pairs arrays positionally instead of merging on (n,k), on censored and heavily tied data. | MAJOR |
| 41-8 | Figure 1's padding mutates the stored `variance_curves` in place, corrupting the checkpoint on re-run. | MAJOR |
| 41-9 | No RNG seed anywhere (X3), despite the notebook being built around resumable checkpoints — a resumed run cannot reproduce the configurations already stored. | MAJOR |
| 41-10 | Final results are written to Colab-local `./results` while every intermediate is synced to Drive. | MAJOR |
| 41-11 | Seven near-duplicate saves, three of them stored crash states. `(6)` is the file of record for execution, generation A for intent. | MINOR |
| 41-12 | Generation A runs `default.mixed` with `backprop` even at p = 0 — a density-matrix simulation where a state-vector one would do, at n = 12 and depth 25. Likely why the earlier runs never finished. | MINOR |

**Verdict:** the noise study does not exist as a result — 15 of 120 configurations ran, all of them
noiseless, and no noisy configuration ever completed. Its value to the audit is diagnostic and
large: it identifies the notebook that wrote `noise_partial.csv`, explains P3 through sample count
alone, locates a complete noiseless replicate sitting in a Drive pickle, and shows that the
attempted repair of the long-range ansatz did not change the circuit. Any claim in the paper about
noise accelerating barren-plateau onset currently rests on notebook 09's hardcoded demo numbers.


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

5. **Resolve c = 1.31 vs c = 1.44** (defect 32-1). Highest priority open item. Needs the
   original `bp_threshold_dataset.csv` and the script that produced the 1.31 point estimate.
   — *Update: most likely a fit-method difference, not a data difference. See "Re-examination
   of P1" above and item 15.*
6. **Locate `bp_threshold_dataset.csv`** (defect 32-6) and commit it to the repo. — *Done; the
   file is in `data/` and matches notebook 06 cell 11.*
7. **Re-check the (n=10, k=6) threshold crossing** (defect 31-1). Its safety margin is
   negative, meaning the crossing is marginal at the reported depth.
8. **Decide whether A should be quoted at all**, given a 95% CI spanning a factor of 4.6
   (defect 32-3). If quoted, it must come from the same fit as c, with its CI stated.

9. **Where did A = 891.6 and c = 1.31 come from?** (defect 34-1 / 32-1). The 15-row dataset
   gives 1.4262 / 1410.3. No principled subset reproduces the published pair, and notebook 13
   hardcodes it as a "user provided" constant. Either a larger dataset exists that is not in
   these files, or the constants are wrong. **This is now the single highest-priority question
   in the project.** — *Update: superseded by item 15. Poisson-weighted non-linear least
   squares on the same 15 rows gives (885.7, 1.303) once the τ=1 floor row is dropped, within
   0.7% of the published pair. The constants are probably right and the method undocumented.*
10. **Reframe or drop the causal-cone mechanism claim** (defect 34-1). Cone saturation precedes
    τ_BP by up to 15 layers and in two cases follows it. τ_BP is not the cone-crossing depth.

11. **Reconcile the three repeatability results** (defect D-1). The checkpoint CSVs say τ is
    perfectly stable; notebook 04 says ±1. Which run is authoritative, and what settings did
    each use?
12. ~~**Reconcile the noiseless baseline** (defect D-2).~~ **Resolved (notebook 10):**
    `noise_partial.csv` comes from the `Untitled41` sweep at `N_SAMPLES = 15`, against 30–50 for
    the main dataset. The ±2 is sampling scatter at a low count. Superseded by items 14 and 16.
13. **Record run provenance with every output file** (defect X8) — sample count, threshold,
    seed, source notebook, date. Ideally a header comment or a sidecar JSON.

14. **Recover `noise_checkpoint.pkl` from Google Drive**
    (`/content/drive/MyDrive/Quantum_Experiments/`). It holds a complete 15-sample noiseless
    Brick-Wall sweep over all 15 configurations, plus every variance curve. This is the single
    highest-value missing file in the project and it settles P3 directly. The repo's
    `noise_partial.csv` is a stale five-row snapshot of the same run.
15. **State the fit method and weighting in Methods** (defects P1-a, P1-b). On the same 15 rows,
    c ranges from 1.13 to 1.43 depending on estimator and weighting alone. Poisson-weighted
    non-linear least squares reproduces the published pair to within 0.7%; confirm this is what
    was used, then re-run the notebook 05 bootstrap under that same estimator, because the CI
    currently quoted belongs to log-log OLS.
16. **Re-run the noise study.** 15 of 120 configurations completed and every one of them was
    noiseless. There is currently no measured evidence anywhere in the project that noise shifts
    τ_BP; notebook 09's noise plot is hardcoded. Reduce the grid if needed — `default.mixed` at
    n=12, depth 25 is what killed every run.
17. **Fix `LongRange_HEA` properly** (defect 41-2). The rewrite in notebook 10 produces an
    edge-for-edge identical circuit to the broken one in notebook 08. Notebook 09's unused
    `all_to_all` is genuinely connected and is the obvious starting point. Add a connectivity
    assertion — number of connected components must be 1 — to the ansatz itself, so this class of
    defect cannot recur silently.
18. **Decide how censored τ are handled** (defect X9). Four rows in notebook 08 and any future
    noisy run will fail to cross within MAX_DEPTH. Either raise MAX_DEPTH, or record them as
    censored and fit accordingly — writing 26 into the τ column is not an option.
19. **Rename or relocate `Untitled40`** (defect 40-1). It is a demonstration deck whose plots are
    synthetic, stored beside notebooks whose plots are measurements, with nothing distinguishing
    them. At minimum rename the file; better, move it out of `notebooks/`.
