# Discrepancy parking lot

Open contradictions found during the notebook audit. An item leaves this list only when a
later notebook, data file, or confirmation from Pratham explains it — not when it is merely
explained away.

**Last updated:** after auditing notebooks 01–10. **All 20 notebook files are now audited.**
There are no unread notebooks left, so any item still open below cannot be resolved by reading
further — it needs a re-run, a recovered file, or an answer from Pratham.

---

## OPEN

### P1 — Published constants do not match any available fit
**Found:** notebook 05 (`Untitled32`), confirmed notebook 06 (`Untitled34__2_`) and CSV.
**Substantially advanced by notebook 09 (`Untitled40`).**

The paper and `configs/default.yaml` carry A = 891.6, c = 1.31. The audit had been assuming
unweighted log-log OLS throughout, under which the constants were untraceable: the 15-row
dataset gives c = 1.4262, A = 1410.3, and an exhaustive subset search found no principled
row set landing on the published pair.

Notebook 09 shows the project also fits with `scipy.optimize.curve_fit` — least squares in
linear space on τ itself. Repeating the reconstruction across fit methods, same 15 rows:

| method | A | c |
|---|---|---|
| log-log OLS | 1410.33 | 1.4262 |
| log-log OLS, weighted by τ | 782.74 | 1.2491 |
| non-linear LS, unweighted | 521.15 | 1.1300 |
| non-linear LS, σ = τ | 1344.22 | 1.4326 |
| **non-linear LS, σ = √τ** | **932.94** | **1.3194** |
| **non-linear LS, σ = √τ, minus the τ=1 floor row** | **885.66** | **1.3028** |
| non-linear LS, σ = √τ, 17 rows (+ n=14) | 937.25 | 1.3173 |

τ is a count of layers, so σ = √τ is the natural weighting rather than an arbitrary one, and it
lands within 0.7% of A = 891.6 and 0.008 of c = 1.31.

**Revised reading: the constants are probably not wrong — the fit method is undocumented.**
The same data yields c anywhere in [1.13, 1.43] depending on estimator and weighting alone.

**Resolves if:** Pratham confirms the estimator and weighting, or the original fitting script
turns up. Reading notebooks cannot resolve it further — all 20 are now audited.
**Action:** state estimator + weighting in Methods, and re-run the bootstrap under that
estimator (see P9).

---

### P2 — Repeatability: zero variance vs ±1 jitter
**Found:** notebook 04 (`Untitled31__1_`) vs `repeatability_checkpoint_4.csv`.

| config | checkpoint CSV | notebook 04 |
|---|---|---|
| n=14, k=2 | 13 ×10, std 0.00 | 13,13,13,13,13,13,**15**,13,13,13 — std 0.63 |
| n=10, k=6 | 4 ×10, std 0.00 | 4,5,3,5,4,3,5,4,5,5 — std 0.82 |

Working hypothesis unchanged: either the checkpoint runs were seeded outside the repeat loop, or
they re-read one stored value. Notebook 08 demonstrates exactly the latter pattern — it sets a
seed, re-reads the same dataframe cell three times, prints `[3, 3, 3]`, and its own comment says
`# Simulating a quick re-run check logic`.

*Update (audit complete):* **no notebook in the set writes `repeatability_checkpoint_*.csv`.**
Notebook 10 writes `noise_partial.csv` and `noise_checkpoint.pkl`; nothing else writes a CSV at
all. The generating code is not in these 20 files.

**Resolves if:** Pratham supplies the script that wrote the checkpoint CSVs, or confirms seeding.
**Until then:** treat notebook 04's ±1 as the repeatability figure and do not cite std = 0.00.

---

### P4 — Variance convention inconsistent across notebooks
**Found:** notebooks 01, 02 vs 03, 04.

Three estimators are in use, all called "gradient variance":

1. Notebooks 01, 02 — pool all gradients, `np.var(np.abs(pooled))`
2. Notebooks 03, 04, **10** — pool all gradients, `np.var(pooled)`
3. Notebook 08 — `np.var` **within each sample's** gradient vector, then mean across samples

(1) and (2) differ by ~2.75x for zero-mean gradients. (3) is a different quantity again.

*Update (notebook 10):* the noise sweep uses convention (2), consistent with notebooks 03 and 04.
Convention (2) is therefore the majority and covers everything that plausibly fed the main
dataset. Convention (1) is confined to the two earliest notebooks and (3) to the invalid
notebook 08.

**Resolves if:** Methods states convention (2) and confirms nothing from notebooks 01/02/08
feeds the final fit.

---

### P5 — No mechanism quantity tracks τ_BP
**Found:** notebook 06 (`Untitled34__2_`).

The causal cone saturates well before τ for small k and *after* τ for two n=12 rows; the gap
ranges from +15 to −3 layers. Entanglement entropy (notebook 07) is also ruled out — at τ the
entropy is far below saturation and varies by ~1 full bit depending on where the cut is taken.

*Update (audit complete):* **no notebook proposes a third mechanism candidate.** Notebook 09's
"Backward Causal Cone" cell is a decorative scatter plot, not a computation, and it restates the
cone claim that notebook 06 had already disproved. Nothing in the project computes scrambling
time, frame potentials, 2-design convergence or effective dimension.

**Resolves if:** a new experiment finds a quantity that tracks τ. **This is now a gap in the
paper, not a pending read** — the Discussion has two documented dead ends and no mechanism.

---

### P6 — Sample counts are inconsistent and sometimes very low
**Found:** notebook 07 (`Untitled36`), accidental repeat measurements.

Notebook 07 measured the same quantity multiple times inside one run:

- n=12, k=12, cut 11, measured 3×: 0.3773 / 0.1848 / 0.2737 — **CV 34.6%**, max/min 2.04×
- n=10, k=6, cut 5, measured 2×: 0.5526 / 0.6049 — spread 9.0%

*Update (audit complete):* the full picture, now that every notebook has been read —

| N_SAMPLES | notebooks |
|---|---|
| 15 | 10 (the noise sweep) |
| 30 | 01, 06, 07, 08 |
| 40 | 03 |
| 50 | 02, 04 |

No notebook justifies its choice, and none reports a convergence check.

**Resolves if:** one count is adopted for everything that feeds the paper, with a stated
convergence check at that count.

---

### P7 — "Long-Range HEA" is disconnected; the attempted fix does not fix it
**Found:** notebook 08 (`Untitled38__1_`). **Confirmed still broken in notebook 10.**

`LongRange_HEA` couples only q to q+n/2, giving n/2 independent 2-qubit circuits. All τ values,
the fit (A=3319.98, c=1.736), AICc and LOOCV from notebook 08 are invalid.

*Update (notebook 10) — the fix was attempted and is ineffective.* `LongRange_HEA_noise` rewrites
the pairing with modular arithmetic and gives odd layers a different control:

```python
even: target  = (q + half_n) % n            for q in range(half_n)
odd:  control = (q+1) % n ; target = (control + half_n) % n
```

Edge sets over 25 layers are **identical to the broken version**: n=8 → 4 components, n=10 → 5,
n=12 → 6. The odd branch only relabels control/target and re-adds the pair (half_n, 0) that the
even layer already contains. Zero new edges.

Nothing invalid was published from it only because the Long-Range half of the sweep never ran.

**Resolves if:** the ansatz is rebuilt connected and the comparison re-run. Notebook 09's unused
`all_to_all` is genuinely connected and is the natural starting point.
**Add a guard:** assert the connectivity graph has exactly one component inside the ansatz itself.

---

### P8 — The noise claim has no measured backing anywhere
**Found:** notebook 09 (`Untitled40`) vs notebook 10 (`Untitled41` series). *New.*

Notebook 09 presents "Noise accelerates BP onset" with τ_k2 = [13,11,8] and τ_k4 = [4,3,2] across
p = 0, 0.01, 0.05. Those numbers are hardcoded in the cell.

Notebook 10 is the real noise sweep. It completed **15 of 120 configurations, every one of them at
p = 0**. No noisy configuration ever finished — the last run died at depth 5 of the first one.

So the project asserts a noise result while every noisy data point it has is either hardcoded or
absent. `noise_partial.csv` contains only p = 0.0 rows, consistent with this.

**Resolves if:** the noise sweep is re-run to completion, or the claim is removed from the paper.

---

### P9 — The quoted confidence interval belongs to a different estimator
**Found:** notebook 05 (`Untitled32`) read against P1's revised finding. *New.*

Notebook 05's bootstrap resamples rows and refits by **log-log OLS**, giving c = 1.4404,
CI [1.2723, 1.6557], and "relative uncertainty 6.74% → PASS: Stable exponent".

If the published c = 1.31 comes from weighted non-linear least squares (P1), then that CI is the
sampling distribution of a *different estimator* and does not describe the published number's
uncertainty. Worse, the estimator choice alone moves c across [1.13, 1.43] — wider than the
interval being quoted as the uncertainty.

**Resolves if:** the bootstrap is re-run under whichever estimator the paper uses. Notebook 32's
other open weaknesses still apply to the re-run: it resamples configurations but not measurement
error, and treats each τ as exact when notebook 04 shows ±1 jitter.

---

## RESOLVED

### P3 — Noiseless baseline disagrees with main dataset — **RESOLVED (notebook 10)**
**Found:** `noise_partial.csv` vs `bp_threshold_dataset.csv`. **Explained by notebook 10.**

| k | noise_partial | main dataset | diff |
|---|---|---|---|
| 2 | 19 | 21 | −2 |
| 3 | 18 | 17 | +1 |
| 5 | 8 | 10 | −2 |
| 6 | 7 | 5 | +2 |
| 8 | 3 | 3 | 0 |

`noise_partial.csv` is written by the `Untitled41` sweep, after every configuration, in loop
order — Brick-Wall, p=0.000, n=8, k ascending. The five rows in the repo are exactly its first
five configurations. That sweep runs at **`N_SAMPLES = 15`**, the lowest count in the project;
the main dataset was produced at 30–50.

This is sufficient on its own. Notebook 07 measured CV = 34.6% for a 30-sample estimator, roughly
49% at 15 samples; notebook 01 puts the variance decay near 0.24 per layer. A ±50% multiplicative
error on the variance moves a fixed-threshold crossing by ln(1.5)/0.24 ≈ 1.7 layers — the ±2 that
was observed. The circuits are structurally identical at p = 0 (depolarizing channels are inserted
only when p > 0), so nothing else differs.

**Not a contradiction between two measurements of the same thing** — one measurement at 15 samples
and another at 30–50.

**Residual action (does not reopen the item):** `noise_checkpoint.pkl` on Google Drive holds the
*complete* 15-sample noiseless sweep — all 15 configurations plus every variance curve — against
the repo's stale 5-row snapshot. Recovering it converts this from an argument into a measured
uncertainty on τ. Note it is a mixture of two backends (see notebook 10, Finding C) and should be
re-run under one before use as a control.

---

## Notes for whoever picks this up

- **τ measurement uncertainty is still unknown**, and this is the thread running through P1, P2,
  P6 and P9. Three sources said 0, ±1 and ±2; P3 explains the ±2 as a sample-count artifact, and
  P2 makes the 0 an artifact of not re-running. **±1, from notebook 04, is the only figure with a
  real experiment behind it, and it rests on two configurations.**
- No output file records the settings that produced it. This is the root cause of P2 and P3 and
  probably P1.
- Two mechanism candidates have been tested and both failed (P5). The paper currently has a
  scaling law with no mechanism.
- The audit log (`notebook_audit_log_9.md`) holds the full per-notebook detail; this file tracks
  only unresolved contradictions.
