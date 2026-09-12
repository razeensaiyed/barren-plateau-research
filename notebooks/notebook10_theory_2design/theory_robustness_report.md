# Checkpoint 10 Post-Processing Robustness Analysis Report

## 1. Overview and Scope

This post-processing analysis evaluates the empirical barren plateau onset ($\tau_{BP}$) from `architecture_tau.csv` against the state frame-potential curves from `state_frame_potential_curves.csv` at individual non-censored `(architecture, n, k)` row level.
- Zero quantum simulations were re-run.
- No methodology inside Notebook 10 was modified.
- $\tau_{BP}$ values were strictly evaluated per $(n, k)$ pair without averaging over $k$.

### Metric Definitions:
1. **First Crossing (Threshold = 2.0):** First depth $L$ where $\mathcal{F}_2(L) / \mathcal{F}_2^{\text{Haar}} \le 2.0$.
2. **Persistent Crossing (Threshold = 2.0):** First depth $L$ where $\mathcal{F}_2(L) / \mathcal{F}_2^{\text{Haar}} \le 2.0$ and remains $\le 2.0$ for the next two measured depths ($L, L+1, L+2$).
3. **Persistent Crossing (Threshold = 1.5):** First depth $L$ where $\mathcal{F}_2(L) / \mathcal{F}_2^{\text{Haar}} \le 1.5$ and remains $\le 1.5$ for the next two measured depths ($L, L+1, L+2$). If not reached by $L=30$, reported as `NaN` (right-censored).

## 2. Summary Statistics: Overall and Architecture-Wise

| Group / Architecture | Criterion | Total BP Cases (N) | Cases with $\tau_{BP} < \tau_{\text{state2design}}$ | Fraction Precedes | Median $\tau_{BP} / \tau_{\text{state2design}}$ | Mean $\tau_{BP} / \tau_{\text{state2design}}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Overall (All 3 Architectures)** | First Crossing (Threshold 2.0) | 90 | 70 | **77.8%** | **0.442** | **0.604** |
| **Overall (All 3 Architectures)** | Persistent (Threshold 2.0) | 90 | 77 | **85.6%** | **0.406** | **0.529** |
| **Overall (All 3 Architectures)** | Persistent (Threshold 1.5) | 60 | 59 | **98.3%** | **0.196** | **0.270** |
| | | | | | | |
| All-to-All | First Crossing (Threshold 2.0) | 30 | 25 | 83.3% | 0.500 | 0.528 |
| All-to-All | Persistent (Threshold 2.0) | 30 | 29 | 96.7% | 0.388 | 0.459 |
| All-to-All | Persistent (Threshold 1.5) | 24 | 24 | 100.0% | 0.167 | 0.189 |
| 1D Brick-Wall | First Crossing (Threshold 2.0) | 30 | 22 | 73.3% | 0.500 | 0.727 |
| 1D Brick-Wall | Persistent (Threshold 2.0) | 30 | 25 | 83.3% | 0.406 | 0.572 |
| 1D Brick-Wall | Persistent (Threshold 1.5) | 6 | 6 | 100.0% | 0.523 | 0.538 |
| 2D Rectangular Grid | First Crossing (Threshold 2.0) | 30 | 23 | 76.7% | 0.429 | 0.557 |
| 2D Rectangular Grid | Persistent (Threshold 2.0) | 30 | 23 | 76.7% | 0.429 | 0.557 |
| 2D Rectangular Grid | Persistent (Threshold 1.5) | 30 | 29 | 96.7% | 0.189 | 0.281 |

## 3. Identification of $n=16$ Cases

- **Notebook 7 Source Status:** In `architecture_tau.csv`, zero records exist for $n=16$. Notebook 7's parameter grid simulated exclusively $n \in \{8, 10, 12, 14\}$.
- **Notebook 10 Frame Potential Status:** `state_frame_potential_curves.csv` generated full state frame-potential curves for $n=16$ up to depth $L=30$ across all 3 architectures:
  - **1D Brick-Wall ($n=16$):** $\tau_{\text{first\_crossing}} = 16$, $\tau_{\text{persistent\_2.0}} = 19$, $\tau_{\text{persistent\_1.5}} = \text{NaN}$ (not reached by $L=30$).
  - **2D Rectangular Grid ($n=16$):** $\tau_{\text{first\_crossing}} = 8$, $\tau_{\text{persistent\_2.0}} = 8$, $\tau_{\text{persistent\_1.5}} = 15$.
  - **All-to-All ($n=16$):** $\tau_{\text{first\_crossing}} = 7$, $\tau_{\text{persistent\_2.0}} = 7$, $\tau_{\text{persistent\_1.5}} = 12$.
- **Missing Data Summary:** Exactly **0 out of the 90** non-censored records in `architecture_tau.csv` represent $n=16$. All $n=16$ comparisons are unavailable because empirical $\tau_{BP}$ values for $n=16$ were not measured in the Notebook 7 architecture study.

## 4. Complete Row-Level Matching Table (First 20 Rows Sample)

| architecture   |   n |   k |   tau_BP |   tau_state2design_first_crossing |   tau_state2design_persistent |   tau_state2design_persistent_1.5 |   tau_BP_over_tau_state2design_first_crossing |   tau_BP_over_tau_state2design_persistent |   tau_BP_over_tau_state2design_persistent_1.5 |   F2_over_Haar_at_tau_BP |
|:---------------|----:|----:|---------:|----------------------------------:|------------------------------:|----------------------------------:|----------------------------------------------:|------------------------------------------:|----------------------------------------------:|-------------------------:|
| all_to_all     |   8 |   2 |        4 |                                 5 |                             5 |                               nan |                                         0.8   |                                  0.8      |                                   nan         |                  2.65021 |
| all_to_all     |   8 |   3 |        4 |                                 5 |                             5 |                               nan |                                         0.8   |                                  0.8      |                                   nan         |                  2.65021 |
| all_to_all     |   8 |   4 |        4 |                                 5 |                             5 |                               nan |                                         0.8   |                                  0.8      |                                   nan         |                  2.65021 |
| all_to_all     |   8 |   5 |        3 |                                 5 |                             5 |                               nan |                                         0.6   |                                  0.6      |                                   nan         |                  5.09818 |
| all_to_all     |   8 |   6 |        2 |                                 5 |                             5 |                               nan |                                         0.4   |                                  0.4      |                                   nan         |                 11.2147  |
| all_to_all     |   8 |   8 |        6 |                                 5 |                             5 |                               nan |                                         1.2   |                                  1.2      |                                   nan         |                  1.7713  |
| all_to_all     |  10 |   2 |        5 |                                 4 |                             6 |                                12 |                                         1.25  |                                  0.833333 |                                     0.416667  |                  2.44684 |
| all_to_all     |  10 |   3 |        5 |                                 4 |                             6 |                                12 |                                         1.25  |                                  0.833333 |                                     0.416667  |                  2.44684 |
| all_to_all     |  10 |   4 |        4 |                                 4 |                             6 |                                12 |                                         1     |                                  0.666667 |                                     0.333333  |                  1.49871 |
| all_to_all     |  10 |   5 |        4 |                                 4 |                             6 |                                12 |                                         1     |                                  0.666667 |                                     0.333333  |                  1.49871 |
| all_to_all     |  10 |   6 |        3 |                                 4 |                             6 |                                12 |                                         0.75  |                                  0.5      |                                     0.25      |                  4.29828 |
| all_to_all     |  10 |   8 |        2 |                                 4 |                             6 |                                12 |                                         0.5   |                                  0.333333 |                                     0.166667  |                  6.28094 |
| all_to_all     |  10 |  10 |        2 |                                 4 |                             6 |                                12 |                                         0.5   |                                  0.333333 |                                     0.166667  |                  6.28094 |
| all_to_all     |  12 |   2 |        4 |                                 8 |                             8 |                                12 |                                         0.5   |                                  0.5      |                                     0.333333  |                  5.84109 |
| all_to_all     |  12 |   3 |        3 |                                 8 |                             8 |                                12 |                                         0.375 |                                  0.375    |                                     0.25      |                  5.64132 |
| all_to_all     |  12 |   4 |        2 |                                 8 |                             8 |                                12 |                                         0.25  |                                  0.25     |                                     0.166667  |                  8.74843 |
| all_to_all     |  12 |   5 |        1 |                                 8 |                             8 |                                12 |                                         0.125 |                                  0.125    |                                     0.0833333 |                 15.1208  |
| all_to_all     |  12 |   6 |        4 |                                 8 |                             8 |                                12 |                                         0.5   |                                  0.5      |                                     0.333333  |                  5.84109 |
| all_to_all     |  12 |   8 |        3 |                                 8 |                             8 |                                12 |                                         0.375 |                                  0.375    |                                     0.25      |                  5.64132 |
| all_to_all     |  12 |  10 |        2 |                                 8 |                             8 |                                12 |                                         0.25  |                                  0.25     |                                     0.166667  |                  8.74843 |

*(Full dataset of all 90 rows is saved in `theory_robustness_analysis.csv`)*