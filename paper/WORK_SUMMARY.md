# Work summary: look-ahead bias in regime-switching VaR

An internal record of everything done on this project up to 27 Oct 2026: what was built, why, what
each experiment found, how the results were checked, and what is still open. This document is for
the team, mentors and anyone reproducing the work. It is not part of the submission. The paper itself
is planned in `paper/draft_outline.md`, and its prose must be written by the student authors (NHSJS
does not accept AI-written prose).

Every number here comes from `paper/tables.md` or `results/`. Where the two could differ, the scripts
are the source of truth. Rerun them and never edit numbers by hand.

---

## 1. The question

Regime-switching models, here a hidden Markov model (HMM) with a calm and a stormy state, often look
very good in risk-forecasting backtests. An HMM can tell you which regime the market is in two ways:

- **Filtered:** using only returns up to today. This is what a risk manager actually has.
- **Smoothed:** using the whole sample, including days that have not happened yet. This is much cleaner,
  but it is hindsight.

A backtest that uses smoothed probabilities, or parameters fitted on the whole sample, quietly lets the
model see the future. The project asks how much of a regime model's apparent Value-at-Risk (VaR) skill
is real, and how much is this look-ahead bias. The percentage by which a biased model's forecast loss is
lower than the honest model's is called the **look-ahead premium**.

An analogy: grading a weather forecaster by letting them peek at tomorrow's newspaper. Version A never
peeks. Version B has read every past and future newspaper's description of what storms look like, but
not tomorrow's weather. Version C has read tomorrow's newspaper.

---

## 2. Timeline

| Date | Work | Commit |
|---|---|---|
| 2026-10-15 | Literature review across four strands, plus a novelty check (`literature/01`-`04`, `00-references.md`) | part of `247e04c` |
| 2026-10-18 | Core model code, three HMM versions, benchmarks, scoring, starter notebook, unit tests | `247e04c` |
| 2026-10-19 | Robustness: 4 indices, window lengths, seeds, 3 regimes, milder C variant, bootstrap CIs | `134832c` |
| 2026-10-19 | Paper tables and figures for NHSJS, with a caption-facts README | `981ef41` |
| 2026-10-20 | Independent statsmodels cross-check; Basel traffic light; detection delay; premium near regime switches | `9cc2521` |
| 2026-10-20 | Fat-tailed HMM, sub-period stability, Holm correction | `07ce8e1` |
| 2026-10-27 | Knowledge graph of the repo (`graphify-out/`, kept local); repo and Windows fixes (section 9); paper outline, this summary, `results/RESULTS.md`, new README, PDFs | PR #1 and follow-up |

The commits carry a `Co-Authored-By: Claude` trailer, so AI assistance with the code is on the record.
That is relevant to the journal's AI-use disclosure (section 10).

---

## 3. Data

- **Indices:** S&P 500 (^GSPC), FTSE 100 (^FTSE), Nikkei 225 (^N225) and DAX (^GDAXI), from Yahoo
  Finance via `yfinance`, using the adjusted close. The prices are cached in `data/*.csv`, so every run
  uses identical data.
- **Returns:** daily log returns in percent, from 1990 to the end of 2025. That gives 8,834-9,106
  trading days per index.
- **Forecast period:** 3 Jan 2005 to the end of 2025, so 5,138-5,331 forecast days per index. Starting
  in 2005 leaves at least 1,000 days of history for the first honest fit.
- **Distribution:** all four series are fat-tailed, with excess kurtosis from 5.9 (DAX) to 10.9
  (S&P 500), and negatively skewed (Table 1).
- **What the regimes look like on the S&P 500.** A full-sample 2-regime fit, used only to describe the
  data and never to forecast:

  | Regime | Mean daily return | Daily volatility | Average length | Share of days |
  |---|---|---|---|---|
  | Calm | 0.08% | 0.68% | 78 days | 71% |
  | Stormy | -0.08% | 1.82% | 32 days | 29% |

---

## 4. What was built

### 4.1 Core library: `regime_var.py` (426 lines)

| Part | Functions | What it does |
|---|---|---|
| Data | `load_returns`, `_to_returns` | Downloads or loads cached prices and converts them to % log returns |
| HMM fitting | `fit_hmm`, `_sort_states_by_variance`, `hmm_params` | Gaussian HMM via hmmlearn EM with 5 random starts, keeping the best likelihood. States are sorted by variance so that state 0 is always calm, which stops the labels flipping between refits. |
| Filtering | `filtered_probs` | Hand-written forward filter. Row t uses only data up to t. |
| VaR | `mixture_quantile`, `_quantiles_from_weights` | The VaR is the quantile of the regime-weighted normal mixture, found by Brent root-finding |
| Fat tails | `weighted_quantile`, `_empirical_quantiles` | Alternative emission: each regime is the empirical distribution of past training returns, weighted by regime membership |
| Version A | `hmm_var_rolling` | Honest: refit every 21 days on the last 1,000 days, filtered probabilities pushed one step ahead |
| Versions B, C, C mild | `hmm_var_full_sample` | Biased by design: fit once on all data. B uses filtered probabilities, C uses smoothed probabilities for day t, C mild uses smoothed probabilities for t-1 pushed one step ahead. |
| Benchmarks | `historical_var`, `garch_var` | Historical simulation on a 250-day window; GARCH(1,1)-t via `arch`, refit on the same schedule as A |
| Scoring | `breaches`, `quantile_loss`, `kupiec_test`, `christoffersen_test`, `diebold_mariano`, `evaluate` | Breach rate, tick loss, coverage tests, and DM with Newey-West variance |
| Regulation | `basel_zones` | Basel traffic light on every rolling 250-day window: green 0-4 breaches, yellow 5-9, red 10+, plus the capital multiplier |
| Mechanism | `stormy_onsets`, `detection_delays` | When stormy episodes start in hindsight, and how long the real-time model takes to notice |
| Inference | `premium_with_ci` | Look-ahead premium with a moving-block bootstrap CI (20-day blocks, 2,000 resamples) |

### 4.2 Experiment scripts

| Script | Runtime | Writes | Purpose |
|---|---|---|---|
| `starter_notebook.ipynb` | minutes | `results/main_results.csv`, `look_ahead_premium.csv`, `diebold_mariano.csv`, `crisis_vs_calm.csv`, `breach_timeline.png` and the 2008 VaR chart | The original end-to-end walkthrough on the S&P 500 |
| `run_robustness.py` | about 15 min | `results/robustness_premium.csv`, `robustness_evaluation.csv` | 4 indices, 500/1,500-day windows, seeds 10-40, 3 regimes |
| `run_extras.py` | | `results/basel_traffic_light.csv`, `detection_delay.csv`, `premium_near_switches.csv`, Figure 5 | Regulatory and mechanism analyses |
| `run_improvements.py` | about 10 min | `results/fat_tail_*.csv`, `subperiod_premium.csv`, `dm_holm.csv` | Fat-tailed HMM, sub-periods, Holm correction |
| `crosscheck.py` | | `results/crosscheck.csv`, `crosscheck_log.txt` | Independent rebuild with statsmodels MLE and 5-day GARCH refits; hand-written GARCH vs `arch` |
| `make_paper_results.py` | | `paper/table1`-`13` (CSV and `tables.md`), `paper/figure1`-`5` (PNG at 300 dpi and PDF) | All paper exhibits. Never edit the outputs by hand. |

### 4.3 Tests: `tests/test_regime_var.py`

There are 25 tests (24 functions, one of them parametrised twice), and all of them pass in about 19
seconds. The tests fall into four groups.

- **Leakage, the most important group:**
  - `test_honest_version_ignores_the_future`: scrambling every return after day t leaves Version A's
    forecast for day t unchanged.
  - `test_honest_version_ignores_the_same_day_return`: the same check for day t's own return.
  - `test_empirical_honest_version_ignores_the_future`: the same check for the fat-tailed honest model.
  - `test_benchmarks_ignore_the_future`: the same check for historical simulation and GARCH-t.
  - `test_biased_versions_do_use_the_future` (run for B and for C) and
    `test_milder_retrospective_version_also_leaks`: sanity checks that the biased versions really do
    leak, so that the experiment measures what it claims to.
- **Statistics:**
  - Kupiec gives exact p = 1 at the target rate, rejects far too many breaches, and handles zero
    breaches.
  - Christoffersen flags clustered breaches.
  - Quantile-loss values are correct.
  - DM has the right sign and gives a sensible result on identical inputs.
  - The bootstrap CI contains the estimate and detects a real gap, and it covers zero when there is
    none.
  - Basel zone boundaries are correct.
  - The detection-delay count is correct.
- **Model mechanics:**
  - States are sorted calm-first.
  - The hand-written filter matches hmmlearn on the last day.
  - A single-regime mixture quantile equals the normal quantile.
  - The weighted quantile matches the plain quantile when weights are equal.
  - Empirical-emission VaR is valid.
  - Every method forecasts every day.
  - The rolling model rejects too little history.
  - The rolling model can return stormy probabilities.
- **Fixtures:** synthetic calm/stormy returns with known parameters.

---

## 5. Key design decisions and why

1. **Same model, different information.** A, B and C share one HMM specification and one VaR formula.
   Only the information set changes, so any performance gap is caused by information and nothing else.
   This is the core of the identification strategy.
2. **Separate the channels.**
   - B vs A isolates the effect of seeing the future in the parameters.
   - C vs B isolates the effect of seeing it in the regime labels.
   - C mild was added to test whether C's advantage is only seeing day t's own return. It is not:
     C mild keeps 85-95% of the premium.
3. **Quantile loss as the main metric.** Coverage tests like Kupiec only count breaches and have low
   power. The tick loss is a strictly consistent scoring function for quantiles (Gneiting 2011), so it
   ranks forecasts properly. Coverage tests are reported alongside it.
4. **Block bootstrap for CIs.** Daily losses are autocorrelated and come in calm and stormy stretches.
   Resampling 20-day blocks keeps that structure. An i.i.d. bootstrap would give CIs that are too narrow.
5. **Label sorting by variance.** Without it, "state 0" can mean calm in one refit and stormy in the
   next, which would wreck the rolling model.
6. **Refit every 21 days.** A trading month, which keeps runtime manageable over 20 years and four
   indices. GARCH-t uses the same schedule so the comparison is fair. The cross-check with 5-day GARCH
   refits shows this choice barely matters (99% breach rate 1.80% vs 1.78%).
7. **Strong benchmark.** GARCH(1,1) with Student-t errors is the standard model practitioners beat
   first. Including it shows where the honest HMM really stands.
8. **Regulatory translation.** The Basel traffic light turns an abstract loss reduction into something
   a bank cares about: capital multipliers and supervisory zones.
9. **Independent re-implementation.** Rebuilding A-C with a different estimator (statsmodels MLE
   instead of hmmlearn EM) guards against a bug in, or a quirk of, one library.
10. **Reproducibility rules.** Cached data, fixed seeds, every exhibit generated by script, and tests
    that encode the no-leakage guarantee.

---

## 6. Results

### 6.1 Headline (S&P 500, 2005-2025, 5,283 days)

| Method | 99% breach rate | Kupiec p (99%) | Quantile loss 95% | Quantile loss 99% |
|---|---|---|---|---|
| A honest | 1.95% | 0.000 | 0.1379 | 0.0463 |
| B future-trained | 1.82% | 0.000 | 0.1351 | 0.0444 |
| C retrospective | **1.00%** | **0.981** | 0.1168 | 0.0368 |
| Historical sim | 1.78% | 0.000 | 0.1459 | 0.0491 |
| GARCH-t | 1.78% | 0.000 | 0.1256 | 0.0368 |

- The hindsight model hits the 1% target exactly. The honest one breaches almost twice as often.
- C ties GARCH-t on 99% loss (0.0368 each). With hindsight, the HMM looks as good as the standard model.
- C still fails the Christoffersen test at 99% (p = 0.008). Its breaches still cluster.

### 6.2 Look-ahead premium, four indices (% lower quantile loss than A, 95% CI)

| Index | C vs A 95% | C vs A 99% | B vs A 95% | B vs A 99% |
|---|---|---|---|---|
| S&P 500 | 15.3 [11.8, 18.5] | 20.5 [13.1, 27.1] | 2.1 [-1.2, 4.9] | 4.2 [-4.0, 10.7] |
| FTSE 100 | 14.6 [11.7, 17.4] | 23.4 [17.6, 28.9] | 1.3 [-1.0, 3.4] | 6.7 [0.5, 12.5] |
| Nikkei 225 | 15.0 [12.0, 17.9] | 24.2 [18.5, 28.7] | 2.3 [-0.4, 4.9] | 8.6 [1.1, 14.6] |
| DAX | 14.7 [12.0, 17.4] | 27.1 [21.6, 31.9] | 1.5 [-1.2, 4.3] | 10.1 [3.0, 16.4] |

- The total premium is about 15% at 95% and 20-27% at 99%. It is significant everywhere and very stable
  across markets.
- The parameter channel (B) is small: 1-2% at 95%, where it is never significant, and 4-10% at 99%.
- The regime-label channel carries most of the premium: 63-91% of it, depending on index and level
  (derived as 1 - B/C).

### 6.3 Benchmarks
- GARCH-t beats the honest HMM on all four indices at both levels: 4-9% lower loss at 95%, 11-21% at 99%.
- On the S&P 500 at 99%, GARCH-t's advantage (20.5%) equals the look-ahead premium (20.5%).
- After the Holm correction, GARCH-t's S&P 500 advantage is significant at 95% (adjusted p 0.029) but
  not at 99% (adjusted p 0.183).
- The honest HMM beats historical simulation at 95% on all four indices (4-7%, significant), but not
  significantly at 99%.

### 6.4 Basel traffic light (99% VaR, rolling 250-day windows)
- Version C is in the green zone in 84-95% of windows. Honest A is green in 60-68%.
- A is in the red zone in 7-14% of windows; C in 2.6-5.1%.
- Mean capital multiplier: A 3.22-3.28, C 3.05-3.12.
- A bank backtesting the hindsight model would believe it had a clean model.

### 6.5 Mechanism
- **Detection delay.** The honest model notices a new stormy regime after a median of 1-3 days, but
  after a mean of 6-14 days. Most onsets are caught fast, a minority very late. 67-78% are caught within
  5 days.
- **Concentration.** The 20 days after each regime switch make up 21-24% of days but produce 51-69% of
  the premium. Near switches, the premium is 25-39%; elsewhere it is 7-22%.
- **Figure 2.** Around 2008, C's 99% VaR is already deep (about -4.3%) from mid-2007. A only deepens
  (to about -6.5%) after the Sept-Oct 2008 losses.

### 6.6 Crisis vs calm (S&P 500)
- In crisis periods (554 days), GARCH-t is far ahead of A: 24% lower loss at 95%, 52% at 99%. C gains
  only about 10%.
- In calm periods, C's relative premium is larger: 17% at 95%, 26% at 99%.
- So hindsight and GARCH help in different places. GARCH-t reacts fast to volatility spikes; hindsight
  helps most at regime transitions and in loosening VaR in calm stretches.

### 6.7 Robustness
- **Window length.** 500 and 1,500 days give a premium of 15.6-15.9% at 95% and 21.5-21.9% at 99%.
- **Seeds.** Seeds 10, 20, 30 and 40 give 15.2-15.8% and 20.4-20.6%. EM initialisation does not matter.
- **3 regimes.** The premium rises to 19.8% / 29.7%, and the parameter channel becomes significant at
  95% (4.4% [0.9, 7.9]). More complex regime models are more exposed to the bias.
- **Sub-periods (2005-09, 2010-14, 2015-19, 2020-25).** The premium is positive in all 32 cells. Only
  the S&P 500 2005-09 cell at 99% has a CI that includes zero.
- **Fat-tailed HMM.**
  - It fixes honest A's 95% coverage, but its 99% breach rate is still too high.
  - Its loss is essentially unchanged.
  - The premium persists at 14% and 21-25%.
  - GARCH-t still wins.
  - Fat-tailed C at 99% is too conservative (0.4-0.5% breaches), yet it has the lowest loss. Coverage
    tests and loss functions can disagree.
- **Independent cross-check.**
  - statsmodels MLE gives a premium of 15.8% / 21.6%, against 15.3% / 20.5% in the main pipeline.
  - The parameter channel comes out at 2.7% / 5.5%, against 2.1% / 4.2%.
  - The hand-written GARCH recursion and t-quantile match `arch` to about 1e-16.

---

## 7. Literature review summary

The review is in `literature/`, with about 190 references in `00-references.md`, each marked with its
verification status. It covers four strands, plus deep reads of five recent competing papers:

1. **Look-ahead bias, real-time estimation, novelty** (`01`).
   - Closest academic work: Kole & van Dijk (2017); Shu, Yu & Mulvey (2024a, b); Nystrup et al. (2020);
     Chauvet & Piger (2008); Hamilton (2011); Cooper & Gulen (2006). Theory: Dacco & Satchell (1999).
   - Verdict: no academic paper measures the look-ahead premium in VaR/ES. Practitioner repos and blogs
     report smoothed-vs-filtered Sharpe gaps, but only for returns and only anecdotally.
   - The verdict also warns that a bare smoothed-vs-filtered comparison is not novel. The contribution
     must be framed as a formal decomposition into channels.
2. **Econometric regime models for VaR/ES** (`02`): Hamilton, MS-GARCH (Ardia et al. 2018; Marcucci
   2005; Bauwens et al. 2010), and regime VaR (Billio & Pelizzon 2000; Guidolin & Timmermann 2006).
3. **ML regime detection** (`03`): jump models, clustering, changepoint detection, ensemble HMMs, and
   supervised learning on ex-post labels.
4. **Evaluation and regulation** (`04`):
   - Coverage tests: Kupiec, Christoffersen, DQ.
   - Scoring: tick and FZ0 losses, Murphy diagrams.
   - Comparison: DM, Giacomini-White, MCS.
   - ES backtests.
   - Basel and FRTB rules.
5. **Deep reads** (`05a`-`05e`): Saidane & Ben Mohamed (2026), Gao, Ye & Guo (2022), Oprea & Bara (2026),
   Malim Franco & Hotta (2026) and Kim (2026). Possible look-ahead is flagged in three of them, but none
   is confirmed without the full text. Do not claim in the paper that these papers are biased.

---

## 8. Knowledge graph (27 Oct)

`graphify-out/` holds a knowledge graph of the whole repo: code, literature, tables and figures.

- Size: 537 nodes, 1,223 edges, 20 communities. Open `graphify-out/graph.html` in a browser.
  `GRAPH_REPORT.md` has the audit report.
- Most-connected concepts: the literature strands, Value at Risk, the HMM, look-ahead bias, and
  filtered vs smoothed probabilities.
- Useful for navigating how a concept, such as the Basel traffic light, links code, results and
  citations.
- Uncertain links are flagged AMBIGUOUS in the report. These include possible look-ahead in the
  competing papers and an unconfirmed latency figure cited by Shu et al.
- Building it also turned up the two repo problems fixed in section 9.

---

## 9. Fixes made on 27 Oct

1. **`requirements.txt`: added `statsmodels`.** `crosscheck.py` imports it, so a clean install from the
   old file would fail on the cross-check. The local venv already had it (0.15.0).
2. **`README.md`: test count corrected from 19 to 25.** The suite has grown since the README was
   written. Verified with pytest: 25 passed.
3. **`requirements.txt`: added `tabulate` and `notebook`.** `make_paper_results.py` calls
   `DataFrame.to_markdown`, which needs `tabulate`, and the README's notebook step needs `notebook`.
   Neither was listed, so a clean install could not run either step.
4. **Windows support.**
   - `make_paper_results.py` now writes `tables.md` with `encoding="utf-8"`. Windows otherwise uses its
     local code page.
   - Script docstrings say `python script.py`, not the Mac/Linux-only `.venv/bin/python`.
   - The README gives Windows and Mac/Linux commands side by side.
   - The code itself was already portable: forward-slash relative paths, `if __name__ == "__main__"`
     guards, no shell calls, no multiprocessing, and no non-ASCII characters in the source. It has not
     yet been run on an actual Windows machine.
5. **`.gitignore`:** added `.DS_Store` and `graphify-out/`.
6. **New `results/RESULTS.md`:** every experiment explained in plain words with its full result tables.
7. **README rewritten** in simple language, with a glossary and a troubleshooting table.

---

## 10. Open issues and decisions

These are carried over to `draft_outline.md`, where each is attached to the section it affects.

| # | Issue | Why it matters | Suggested handling |
|---|---|---|---|
| 1 | Only two leakage channels are decomposed (parameters, labels) | The novelty verdict says the contribution must be a multi-channel decomposition | Frame as two channels with the others as future work, or add regime-count selection and full-sample standardisation experiments |
| 2 | B confounds future information with a much longer training sample (35 years vs 1,000 days) and no refits | "B vs A" is an upper bound on pure parameter look-ahead | State as a limitation; optionally add an expanding-window honest variant |
| 3 | Significance stars in Table 4 (and 12b) are unadjusted DM p-values | Many comparisons are tested; Holm covers only the S&P 500 (Table 6) | Extend Holm to all tables, or say "unadjusted" in the caption |
| 4 | Historical simulation uses a 250-day window; HMM and GARCH use 1,000 | Benchmark comparability | Justify (regulatory convention) or add a 1,000-day run |
| 5 | Detection delay compares A against a different (full-sample) model's smoothed probabilities | Part of the delay may be model difference | Note it; B gives the clean same-model comparison |
| 6 | No expected shortfall | FRTB uses ES at 97.5% | Limitation and future work |
| 7 | Figure numbering (file names give the breach timeline as Figure 4 and Basel as Figure 5) vs main-text order | Exhibit numbering must follow reading order | Renumber in `make_paper_results.py` once the main-text set is fixed |
| 8 | AI-use disclosure | Commits are co-authored by Claude, and NHSJS restricts AI-written prose | Check the current NHSJS policy; disclose AI help with code and analysis; authors write all prose |
| 9 | Six method citations missing from `00-references.md` (Bollerslev 1987, Künsch 1989, Holm 1979, Newey & West 1987, Rabiner 1989, Koenker & Bassett 1978) | Needed for the methods section | Add and verify |
| 10 | SSRN not searched in the novelty check | A recent working paper could exist | One targeted title search before submission |

---

## 11. How to reproduce everything

Activate the environment first, then type `python`. Without activation, use
`.venv\Scripts\python` on Windows or `.venv/bin/python` on Mac/Linux in place of `python`.

```
python -m venv .venv
# Windows:      .venv\Scripts\activate
# Mac / Linux:  source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest                 # 25 tests, about 20 s
python run_robustness.py         # about 15 min
python run_extras.py
python run_improvements.py       # about 10 min
python crosscheck.py
python make_paper_results.py     # writes paper/ tables and figures
```

Data comes from `data/*.csv`, so no network access is needed after the first download.
