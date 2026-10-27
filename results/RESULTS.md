# Experiment results

This page explains every experiment in plain words: what we tested, what came out, and what it means.
The numbers are copied from the files in `results/` and `paper/tables.md`. Those files are made by
the scripts. If you rerun a script, the files change, and this page may need updating.

## How to read the numbers

- **Breach rate:** how often the real loss was worse than the VaR forecast. For 95% VaR the target is
  5% of days. For 99% VaR it is 1%.
- **Kupiec p:** a check of whether the breach rate is close enough to the target. Above 0.05 means
  "close enough". Below 0.05 means "too far off".
- **Christoffersen p:** the same, plus a check that breaches do not come in bunches. Above 0.05 passes.
- **Quantile loss:** one score for how good the forecasts are. **Lower is better.**
- **Premium:** how much lower (in %) a model's quantile loss is than the honest model's.
- **[low, high]:** the 95% confidence range. If it does not include 0, the difference is real and not
  luck.
- **DM p:** the Diebold-Mariano test. Below 0.05 means the two models really are different.
- `*` next to a number means DM p < 0.05.

The models:

| Name | What it is |
|---|---|
| A honest | HMM retrained every 21 days on the last 1,000 days. Sees only the past. |
| B future-trained | HMM trained once on all data, 1990-2025. Its settings know the future. |
| C retrospective | Same as B, and its calm/stormy guess also uses future days. The strongest cheat. |
| C mild | Like C, but it does not use the guess for the forecast day itself. |
| Historical sim | VaR = the 1-in-20 or 1-in-100 worst day of the last 250 days. |
| GARCH-t | A standard model that reacts quickly to recent swings. Retrained every 21 days. |

Forecasts run from 3 Jan 2005 to the end of 2025, one day ahead.

---

## Experiment 1. The data

**Script:** `make_paper_results.py`. **File:** `paper/table1_data_summary.csv`.

| Market | Days | Days forecast | Average day % | Typical swing % | Worst day % | Best day % | Fat tails* |
|---|---|---|---|---|---|---|---|
| S&P 500 | 9,066 | 5,283 | 0.032 | 1.14 | -12.8 | 11.0 | 10.9 |
| FTSE 100 | 9,092 | 5,303 | 0.015 | 1.08 | -11.5 | 9.4 | 7.8 |
| Nikkei 225 | 8,834 | 5,138 | 0.003 | 1.48 | -13.2 | 13.2 | 6.2 |
| DAX | 9,106 | 5,331 | 0.029 | 1.37 | -13.1 | 10.8 | 5.9 |

\* Excess kurtosis. 0 would be a normal bell curve. Higher means more extreme days than a bell curve
expects.

**What it means:** all four markets have many more extreme days than a bell curve predicts. Big
losses are also a bit more common than big gains (negative skew).

## Experiment 2. What the calm and stormy periods look like

**File:** `paper/table2_regimes.csv`. S&P 500, model trained on all data. This is used only to
describe the data, never to forecast.

| Period | Average day % | Typical swing % | Chance it continues tomorrow | Average length | Share of all days |
|---|---|---|---|---|---|
| Calm | 0.081 | 0.68 | 98.7% | 78 days | 71% |
| Stormy | -0.084 | 1.82 | 96.9% | 32 days | 29% |

**What it means:** stormy periods swing about 2.7 times as much as calm ones. Both kinds of period
last for weeks, so knowing which one you are in is very useful.

---

## Experiment 3. Main test on the S&P 500

**Script:** `starter_notebook.ipynb` and `make_paper_results.py`. **Files:** `results/main_results.csv`,
`paper/table3_main_results.csv`. 5,283 forecast days.

| Model | VaR | Breach rate % | Target % | Kupiec p | Christoffersen p | Quantile loss |
|---|---|---|---|---|---|---|
| A honest | 95% | 5.70 | 5 | 0.023 | 0.037 | 0.1379 |
| A honest | 99% | 1.95 | 1 | 0.000 | 0.000 | 0.0463 |
| B future-trained | 95% | 5.96 | 5 | 0.002 | 0.008 | 0.1351 |
| B future-trained | 99% | 1.82 | 1 | 0.000 | 0.000 | 0.0444 |
| C retrospective | 95% | 4.49 | 5 | 0.081 | 0.128 | 0.1168 |
| C retrospective | 99% | 1.00 | 1 | 0.981 | 0.008 | 0.0368 |
| Historical sim | 95% | 5.49 | 5 | 0.108 | 0.000 | 0.1459 |
| Historical sim | 99% | 1.78 | 1 | 0.000 | 0.000 | 0.0491 |
| GARCH-t | 95% | 6.78 | 5 | 0.000 | 0.000 | 0.1256 |
| GARCH-t | 99% | 1.78 | 1 | 0.000 | 0.000 | 0.0368 |

**What it means:**
- The honest model is beaten on 1.95% of days at 99% VaR, almost double the 1% target.
- The cheating model C hits exactly 1.00%. A simple check would call it perfect.
- C's breaches still come in bunches (Christoffersen p = 0.008), so even the cheat is not perfect.
- C's 99% score (0.0368) is the same as GARCH-t's. The cheat makes the HMM look as good as the
  standard model.

## Experiment 4. How big is the cheat's advantage? (four markets)

**Script:** `run_robustness.py`. **Files:** `results/robustness_premium.csv`,
`paper/table4_look_ahead_premium.csv`. Confidence ranges come from 2,000 re-samples of 20-day blocks.

| Market | C vs A, 95% | C vs A, 99% | C mild vs A, 95% | C mild vs A, 99% | B vs A, 95% | B vs A, 99% |
|---|---|---|---|---|---|---|
| S&P 500 | 15.3 [11.8, 18.5]* | 20.5 [13.1, 27.1]* | 13.2 [9.7, 16.2]* | 19.2 [11.7, 25.8]* | 2.1 [-1.2, 4.9] | 4.2 [-4.0, 10.7] |
| FTSE 100 | 14.6 [11.7, 17.4]* | 23.4 [17.6, 28.9]* | 12.8 [10.0, 15.4]* | 21.8 [16.0, 27.3]* | 1.3 [-1.0, 3.4] | 6.7 [0.5, 12.5] |
| Nikkei 225 | 15.0 [12.0, 17.9]* | 24.2 [18.5, 28.7]* | 12.8 [9.9, 15.6]* | 22.3 [16.3, 27.1]* | 2.3 [-0.4, 4.9] | 8.6 [1.1, 14.6]* |
| DAX | 14.7 [12.0, 17.4]* | 27.1 [21.6, 31.9]* | 13.1 [10.5, 15.6]* | 25.6 [20.0, 30.5]* | 1.5 [-1.2, 4.3] | 10.1 [3.0, 16.4]* |

**What it means:**
- The full cheat (C) lowers the error by about 15% at 95% and 20-27% at 99%, in every market. It is
  always clearly real (the range never touches 0).
- The cheat matters more at 99%, the level regulators care about most.
- Using future data only for the settings (B) helps much less: 1-2% at 95%, never clearly real, and
  4-10% at 99%.
- C mild keeps 85-95% of C's advantage. So the cheat is not mainly "seeing today's price". It is
  knowing, with hindsight, which period the market was in.

## Experiment 5. Honest HMM vs the simple models

**Script:** `run_robustness.py`. **File:** `paper/table5_benchmarks.csv`. A negative number means the
simple model **beats** the honest HMM.

| Market | Simple model | VaR | Difference % | DM p |
|---|---|---|---|---|
| S&P 500 | GARCH-t | 95% | -8.9 [-14.7, -3.5] | 0.006 |
| FTSE 100 | GARCH-t | 95% | -5.6 [-10.2, -1.6] | 0.020 |
| Nikkei 225 | GARCH-t | 95% | -4.3 [-8.8, -0.8] | 0.059 |
| DAX | GARCH-t | 95% | -4.9 [-8.3, -1.6] | 0.008 |
| S&P 500 | GARCH-t | 99% | -20.5 [-35.1, -3.5] | 0.046 |
| FTSE 100 | GARCH-t | 99% | -14.1 [-25.8, -1.9] | 0.070 |
| Nikkei 225 | GARCH-t | 99% | -11.4 [-24.9, 0.4] | 0.163 |
| DAX | GARCH-t | 99% | -15.2 [-23.7, -6.4] | 0.009 |
| S&P 500 | Historical sim | 95% | 5.8 [1.9, 9.6] | 0.004 |
| FTSE 100 | Historical sim | 95% | 6.5 [3.1, 10.2] | 0.001 |
| Nikkei 225 | Historical sim | 95% | 3.7 [0.3, 7.5] | 0.034 |
| DAX | Historical sim | 95% | 4.5 [0.5, 8.8] | 0.030 |
| S&P 500 | Historical sim | 99% | 6.1 [-3.8, 17.8] | 0.220 |
| FTSE 100 | Historical sim | 99% | 4.8 [-5.0, 15.9] | 0.333 |
| Nikkei 225 | Historical sim | 99% | 8.1 [-3.7, 21.5] | 0.178 |
| DAX | Historical sim | 99% | 1.8 [-7.0, 13.0] | 0.711 |

**What it means:**
- GARCH-t beats the honest HMM everywhere, by 4-9% at 95% and 11-21% at 99%.
- The honest HMM beats historical simulation at 95%. At 99% the gap is too small to be sure.
- On the S&P 500 at 99%, GARCH-t is 20.5% better than the honest HMM, and the cheat makes the HMM
  20.5% better. The cheat exactly hides the HMM's weakness.

## Experiment 6. Stricter significance check (S&P 500)

**Script:** `run_improvements.py`. **Files:** `results/dm_holm.csv`, `paper/table6_diebold_mariano.csv`.
When you run many tests, some look "significant" by luck. The Holm correction adjusts for this
across all 8 tests.

| VaR | Comparison | DM statistic | p | p after Holm |
|---|---|---|---|---|
| 95% | C vs A | -7.84 | 0.000 | 0.000 |
| 95% | B vs A | -1.30 | 0.192 | 0.577 |
| 95% | A vs Historical sim | -2.86 | 0.004 | 0.026 |
| 95% | A vs GARCH-t | 2.76 | 0.006 | 0.029 |
| 99% | C vs A | -4.77 | 0.000 | 0.000 |
| 99% | B vs A | -1.09 | 0.278 | 0.577 |
| 99% | A vs Historical sim | -1.23 | 0.220 | 0.577 |
| 99% | A vs GARCH-t | 2.00 | 0.046 | 0.183 |

A negative statistic means the first model is better.

**What it means:** the cheat's advantage (C vs A) survives the stricter check easily. GARCH-t's win at
95% survives. Its win at 99% does not, so on the S&P 500 at 99% we cannot be sure GARCH-t is better.

## Experiment 7. Crisis days vs calm days (S&P 500)

**File:** `paper/table7_crisis_vs_calm.csv`. Crisis = Sep 2008-Jun 2009, mid-Feb-Jun 2020 and all of
2022 (554 days). Calm = all other days (4,729).

| Period | VaR | A honest | B | C | Historical sim | GARCH-t |
|---|---|---|---|---|---|---|
| Crisis | 95% | 0 | 6.3 | 9.9 | -1.8 | 24.2 |
| Crisis | 99% | 0 | 7.2 | 10.9 | 9.8 | 51.7 |
| Calm | 95% | 0 | 0.4 | 17.4 | -7.3 | 3.0 |
| Calm | 99% | 0 | 2.5 | 25.9 | -15.0 | 2.9 |

Numbers are % lower loss than the honest model.

**What it means:**
- In crises, GARCH-t is far better than the HMM. It reacts quickly to sudden swings.
- The cheat helps more, in relative terms, on calm days.
- Crisis days still carry much bigger losses in absolute terms (about 3-5 times bigger).

## Experiment 8. Does the result depend on our settings? (S&P 500)

**Script:** `run_robustness.py`. **File:** `paper/table8_robustness.csv`. % lower loss than A.

| Setting | B vs A, 95% | B vs A, 99% | C vs A, 95% | C vs A, 99% |
|---|---|---|---|---|
| Main (1,000 days, seed 0, 2 periods) | 2.1 [-1.2, 4.9] | 4.2 [-4.0, 10.7] | 15.3 [11.8, 18.5] | 20.5 [13.1, 27.1] |
| 500-day training window | 2.4 [-2.4, 6.2] | 5.9 [-5.5, 14.7] | 15.6 [10.9, 19.8] | 21.9 [11.5, 30.9] |
| 1,500-day training window | 2.8 [-0.0, 5.4] | 5.4 [-2.1, 11.2] | 15.9 [12.8, 18.8] | 21.5 [15.2, 26.7] |
| Random seed 10 | 2.2 [-1.2, 5.0] | 4.4 [-3.7, 10.9] | 15.4 [11.9, 18.6] | 20.6 [13.3, 27.2] |
| Random seed 20 | 2.6 [-0.6, 5.4] | 4.2 [-3.7, 10.7] | 15.8 [12.2, 19.0] | 20.5 [13.0, 27.0] |
| Random seed 30 | 2.0 [-1.3, 4.8] | 4.1 [-4.1, 10.6] | 15.2 [11.7, 18.5] | 20.4 [12.9, 27.0] |
| Random seed 40 | 2.0 [-1.3, 4.8] | 4.1 [-4.1, 10.7] | 15.2 [11.7, 18.5] | 20.4 [12.9, 27.0] |
| 3 periods instead of 2 | 4.4 [0.9, 7.9] | 6.8 [-2.8, 15.0] | 19.8 [16.0, 23.5] | 29.7 [21.9, 36.0] |

**What it means:**
- The window length and the random starting point barely change anything.
- With 3 periods instead of 2, the cheat helps even more (about 20% and 30%). More complex models gain
  more from cheating.

## Experiment 9. The bank regulator's traffic light (99% VaR)

**Script:** `run_extras.py`. **Files:** `results/basel_traffic_light.csv`,
`paper/table9_basel_traffic_light.csv`, `paper/figure5_basel_zones.png`.

We count breaches in every 250-day window (about one trading year). Green = 0-4, yellow = 5-9,
red = 10 or more. Worse lights mean the bank must hold more money in reserve (the "multiplier").

| Market | Model | Windows | Green % | Yellow % | Red % | Avg. multiplier |
|---|---|---|---|---|---|---|
| S&P 500 | A honest | 5,034 | 60.3 | 25.4 | 14.3 | 3.28 |
| S&P 500 | B | 5,034 | 64.8 | 23.9 | 11.3 | 3.24 |
| S&P 500 | C | 5,034 | 83.9 | 11.0 | 5.1 | 3.12 |
| S&P 500 | Historical sim | 5,034 | 55.7 | 32.6 | 11.7 | 3.30 |
| S&P 500 | GARCH-t | 5,034 | 48.7 | 48.8 | 2.6 | 3.28 |
| FTSE 100 | A honest | 5,054 | 67.5 | 22.8 | 9.7 | 3.24 |
| FTSE 100 | B | 5,054 | 71.7 | 23.6 | 4.8 | 3.18 |
| FTSE 100 | C | 5,054 | 93.2 | 2.2 | 4.6 | 3.06 |
| FTSE 100 | Historical sim | 5,054 | 49.0 | 46.3 | 4.7 | 3.30 |
| FTSE 100 | GARCH-t | 5,054 | 60.3 | 36.3 | 3.4 | 3.24 |
| Nikkei 225 | A honest | 4,889 | 63.5 | 29.2 | 7.3 | 3.23 |
| Nikkei 225 | B | 4,889 | 75.5 | 19.9 | 4.6 | 3.14 |
| Nikkei 225 | C | 4,889 | 94.8 | 0.8 | 4.4 | 3.05 |
| Nikkei 225 | Historical sim | 4,889 | 58.6 | 36.8 | 4.6 | 3.29 |
| Nikkei 225 | GARCH-t | 4,889 | 65.0 | 34.7 | 0.3 | 3.19 |
| DAX | A honest | 5,082 | 64.6 | 26.1 | 9.4 | 3.22 |
| DAX | B | 5,082 | 68.9 | 21.0 | 10.1 | 3.21 |
| DAX | C | 5,082 | 86.2 | 11.3 | 2.6 | 3.09 |
| DAX | Historical sim | 5,082 | 53.1 | 38.9 | 8.0 | 3.30 |
| DAX | GARCH-t | 5,082 | 74.8 | 25.3 | 0.0 | 3.13 |

**What it means:**
- The cheating model is green 84-95% of the time. The honest model is green only 60-68%.
- A bank that tested with the cheat would think its model was safe, and would hold less reserve money
  than it should.
- GARCH-t is rarely red, but often yellow. Its misses are spread out. The honest HMM's misses come in
  bunches, which pushes it into red.

## Experiment 10. How long does the honest model take to notice a storm?

**Script:** `run_extras.py`. **Files:** `results/detection_delay.csv`, `paper/table10_detection_delay.csv`.

A storm "starts" when the hindsight view says stormy for at least 10 days in a row, after at least 20
calm days. We count the days until the real-time model also says stormy (at most 60).

| Market | Model | Storms | Middle delay (days) | Average delay (days) | Caught within 5 days % |
|---|---|---|---|---|---|
| S&P 500 | A honest | 21 | 2 | 13.7 | 66.7 |
| S&P 500 | B | 21 | 3 | 2.9 | 95.2 |
| FTSE 100 | A honest | 18 | 3 | 9.8 | 77.8 |
| FTSE 100 | B | 18 | 3 | 3.2 | 88.9 |
| Nikkei 225 | A honest | 19 | 1 | 5.8 | 73.7 |
| Nikkei 225 | B | 19 | 3 | 4.2 | 63.2 |
| DAX | A honest | 19 | 2 | 7.6 | 68.4 |
| DAX | B | 19 | 4 | 4.4 | 79.0 |

**What it means:**
- Most storms are noticed within 1-3 days.
- A few storms are noticed very late, which pulls the average up to 6-14 days. Those late storms are
  where the honest model fails most.
- Note: the hindsight view comes from a model trained on all data, while A is trained differently.
  So part of A's delay may come from that difference. B uses the same model, so its delays are the
  cleaner comparison.

## Experiment 11. Where does the cheat's advantage come from?

**Script:** `run_extras.py`. **Files:** `results/premium_near_switches.csv`,
`paper/table11_premium_near_switches.csv`.

We mark the 20 days after every switch between calm and stormy (by hindsight). Then we ask how much of
C's advantage comes from those days.

| Market | VaR | Switches | Share of days near a switch % | Share of the advantage from those days % | Advantage near switches % | Advantage elsewhere % |
|---|---|---|---|---|---|---|
| S&P 500 | 95% | 78 | 22.6 | 62.3 | 29.6 | 8.5 |
| S&P 500 | 99% | 78 | 22.6 | 61.6 | 34.3 | 12.4 |
| FTSE 100 | 95% | 70 | 21.3 | 68.6 | 30.7 | 6.8 |
| FTSE 100 | 99% | 70 | 21.3 | 60.4 | 39.0 | 14.6 |
| Nikkei 225 | 95% | 78 | 23.8 | 57.7 | 24.7 | 9.8 |
| Nikkei 225 | 99% | 78 | 23.8 | 52.2 | 32.9 | 18.8 |
| DAX | 95% | 72 | 22.8 | 58.5 | 26.4 | 9.1 |
| DAX | 99% | 72 | 22.8 | 50.8 | 35.9 | 21.6 |

**What it means:** about a fifth of all days, the ones right after the market changes mood, give
between half and two-thirds of the cheat's advantage. Hindsight helps most exactly when the market
turns.

## Experiment 12. A model with fatter tails

**Script:** `run_improvements.py`. **Files:** `results/fat_tail_evaluation.csv`,
`results/fat_tail_premium.csv`, `paper/table12_fat_tailed_scores.csv`,
`paper/table12b_fat_tailed_premium.csv`.

Normal HMMs assume bell curves. Here each period instead uses the real spread of past returns, so
extreme days are allowed.

Scores (breach rate %, Kupiec p, quantile loss):

| Market | Model | 95% breach | 95% Kupiec p | 99% breach | 99% Kupiec p | 95% loss | 99% loss |
|---|---|---|---|---|---|---|---|
| S&P 500 | A honest (normal) | 5.70 | 0.023 | 1.95 | 0.000 | 0.1379 | 0.0463 |
| S&P 500 | A honest (fat tails) | 5.38 | 0.216 | 1.70 | 0.000 | 0.1373 | 0.0454 |
| S&P 500 | C (fat tails) | 4.60 | 0.176 | 0.53 | 0.000 | 0.1177 | 0.0357 |
| FTSE 100 | A honest (normal) | 5.34 | 0.266 | 1.53 | 0.000 | 0.1231 | 0.0408 |
| FTSE 100 | A honest (fat tails) | 5.13 | 0.667 | 1.36 | 0.013 | 0.1231 | 0.0407 |
| FTSE 100 | C (fat tails) | 4.11 | 0.002 | 0.47 | 0.000 | 0.1056 | 0.0306 |
| Nikkei 225 | A honest (normal) | 5.70 | 0.024 | 1.69 | 0.000 | 0.1670 | 0.0551 |
| Nikkei 225 | A honest (fat tails) | 5.49 | 0.114 | 1.56 | 0.000 | 0.1674 | 0.0538 |
| Nikkei 225 | C (fat tails) | 4.22 | 0.009 | 0.43 | 0.000 | 0.1434 | 0.0414 |
| DAX | A honest (normal) | 5.98 | 0.001 | 1.63 | 0.000 | 0.1494 | 0.0480 |
| DAX | A honest (fat tails) | 5.40 | 0.183 | 1.37 | 0.010 | 0.1496 | 0.0476 |
| DAX | C (fat tails) | 4.46 | 0.068 | 0.39 | 0.000 | 0.1277 | 0.0355 |

Advantage, % lower loss:

| Market | Fat-tailed A vs normal A, 95% | 99% | C vs A (both fat-tailed), 95% | 99% | GARCH-t vs fat-tailed A, 95% | 99% |
|---|---|---|---|---|---|---|
| S&P 500 | 0.5 [-0.5, 1.3] | 2.0 [-2.7, 6.0] | 14.2 [10.8, 17.6]* | 21.2 [13.1, 27.9]* | 8.5 [3.1, 14.2]* | 18.8 [4.1, 32.6]* |
| FTSE 100 | -0.0 [-0.9, 0.8] | 0.3 [-1.6, 1.9] | 14.2 [11.6, 16.9]* | 24.9 [19.1, 29.9]* | 5.6 [1.3, 10.5]* | 13.9 [2.1, 25.2] |
| Nikkei 225 | -0.2 [-0.9, 0.3] | 2.3 [-0.6, 5.0] | 14.3 [11.5, 17.1]* | 23.0 [17.6, 27.4]* | 4.6 [1.0, 9.0]* | 9.3 [-2.1, 21.9] |
| DAX | -0.1 [-1.0, 0.7] | 0.9 [-1.7, 4.3] | 14.7 [12.0, 17.3]* | 25.4 [18.9, 31.0]* | 5.0 [1.3, 9.0]* | 14.4 [6.2, 22.6]* |

**What it means:**
- Fat tails fix the honest model's 95% breach rate (Kupiec now passes in all four markets). At 99% it
  still misses too often.
- The overall score barely changes.
- The cheat's advantage stays the same size: about 14% and 21-25%. So the cheat works through
  information, not through the bell-curve assumption.
- GARCH-t still beats the honest HMM.
- Odd result: fat-tailed C is too careful at 99% (0.4-0.5% breaches instead of 1%), yet it has the
  best score. Different ways of grading can disagree.

## Experiment 13. Is the result the same in every period?

**Script:** `run_improvements.py`. **Files:** `results/subperiod_premium.csv`,
`paper/table13_subperiods.csv`. C vs A, % lower loss, normal HMM.

| Market | VaR | 2005-2009 | 2010-2014 | 2015-2019 | 2020-2025 |
|---|---|---|---|---|---|
| S&P 500 | 95% | 11.2 [2.6, 19.6] | 16.8 [9.8, 22.3] | 16.7 [8.4, 22.8] | 17.2 [12.5, 22.4] |
| S&P 500 | 99% | 13.9 [-6.9, 30.7] | 21.2 [10.3, 30.5] | 27.2 [12.9, 39.9] | 23.3 [16.6, 31.9] |
| FTSE 100 | 95% | 9.8 [4.5, 15.2] | 14.5 [9.7, 19.2] | 16.5 [11.5, 20.9] | 18.2 [12.2, 23.9] |
| FTSE 100 | 99% | 13.2 [2.0, 23.5] | 16.7 [9.8, 24.0] | 24.3 [14.8, 33.8] | 35.8 [26.5, 43.3] |
| Nikkei 225 | 95% | 14.5 [8.0, 19.9] | 11.7 [6.6, 16.8] | 15.9 [10.2, 22.2] | 17.5 [12.3, 22.4] |
| Nikkei 225 | 99% | 25.9 [14.1, 33.8] | 10.8 [1.5, 20.4] | 30.7 [21.3, 38.9] | 27.2 [17.4, 34.6] |
| DAX | 95% | 13.2 [7.8, 17.8] | 11.1 [5.0, 17.7] | 14.1 [9.8, 17.7] | 19.2 [14.2, 23.9] |
| DAX | 99% | 26.6 [13.9, 35.4] | 17.5 [9.3, 25.3] | 18.5 [10.8, 25.6] | 37.1 [28.8, 43.1] |

**What it means:** the cheat helps in all 32 cases. Only one range touches 0 (S&P 500, 2005-2009,
99%). The result is not driven by a single crisis. The fat-tailed model gives similar numbers.

## Experiment 14. Independent cross-check

**Script:** `crosscheck.py`. **Files:** `results/crosscheck.csv`, `results/crosscheck_log.txt`.

We rebuilt models A, B and C with a different library and method (statsmodels, maximum likelihood),
and retrained GARCH-t every 5 days instead of every 21.

| | Our code | Independent rebuild |
|---|---|---|
| C vs A, 95% | 15.3% | 15.8% |
| C vs A, 99% | 20.5% | 21.6% |
| B vs A, 95% | 2.1% | 2.7% |
| B vs A, 99% | 4.2% | 5.5% |
| GARCH-t 99% breach rate | 1.78% | 1.80% |

We also wrote the GARCH formulas by hand and compared them with the `arch` package. The largest
difference was 0.0000000000000004, which is just computer rounding.

**What it means:** a different method and library give almost the same answers. The results are not
caused by a bug or by one library's quirks.

---

## Figures

| File | What it shows |
|---|---|
| `paper/figure1_regime_probabilities.png` | S&P 500, 2007-2010. The hindsight storm signal (orange) is clean and early. The real-time one (blue) is noisy and late. |
| `paper/figure2_var_2008.png` | 99% VaR around 2008. The cheating model is already cautious in mid-2007. The honest model reacts only after the crash, then overshoots. |
| `paper/figure3_premium_by_index.png` | The cheat's advantage in all four markets, with confidence ranges. C is far above 0. B is near 0. |
| `paper/figure4_breach_timeline.png` | Every day each model's 99% VaR was beaten. Misses bunch up in 2008, 2020 and 2022. |
| `paper/figure5_basel_zones.png` | Traffic-light shares for each model, S&P 500. |
| `results/breach_timeline.png`, `results/var_lines_2008.png` | Early versions of Figures 4 and 2 from the notebook. |

## Summary of all results

1. The cheat lowers the error by about **15%** (95% VaR) and **20-27%** (99% VaR) in every market.
2. Most of it comes from **hindsight about the market's mood**, not from the model's settings.
3. The cheat turns a "yellow/red light" model into a **"green light"** model.
4. The honest HMM **loses to GARCH-t**. The cheat hides that.
5. The advantage is earned **right after the market changes mood**, when the honest model is still
   catching up.
6. The result holds across **settings, random seeds, fat tails, time periods and an independent
   rebuild**.
