# Paper draft outline: Does Look-Ahead Bias Fake Good Risk Forecasts?

**How to use this file.** This is a section-by-section outline of the full paper. Each section lists the
claims, every number, the table and figure to point to, and the citations. It has no finished
sentences on purpose: NHSJS does not allow AI-written prose (see `paper/README.md`), so the authors
write every sentence themselves from these notes.

- Every number here is copied from `paper/tables.md` or `results/*.csv`/`*_log.txt`, which
  `make_paper_results.py`, `run_robustness.py`, `run_extras.py`, `run_improvements.py` and
  `crosscheck.py` write. If a script is rerun, re-check the numbers against `tables.md`.
- **Derived** means a number calculated in this outline from table values, not printed by a script.
  Recompute any derived number before quoting it.
- **Decision needed** marks a choice the authors still have to make.
- **Reviewer risk** marks a weakness a referee is likely to raise. Each comes with a suggested handling.

Target length (agreed): long draft with everything in, about 8-10k words. Trim to the journal limit
afterwards. Suggested main-text exhibits come from `paper/README.md`. Everything else goes in the appendix.

---

## 0. Title, keywords, one-sentence contribution

**Title options**
1. Does Look-Ahead Bias Fake Good Risk Forecasts? Measuring the Hindsight Premium in Regime-Switching Value-at-Risk
2. The Look-Ahead Premium: How Hindsight Inflates Hidden Markov Model Value-at-Risk Forecasts
3. Real-Time versus Hindsight Regimes: How Much of a Regime Model's Risk-Forecasting Skill Is Look-Ahead Bias?

**Keywords:** Value-at-Risk; hidden Markov model; regime switching; look-ahead bias; backtesting;
smoothed probabilities; filtered probabilities; Basel traffic light.

**One-sentence contribution (to rephrase):** a controlled, four-index, 21-year experiment that
splits the apparent skill of a 2-regime HMM VaR model into an honest part and a part that comes from
hindsight, and shows that hindsight accounts for a 15-27% lower forecast loss and moves the model from
regulatory yellow/red to green zones.

---

## 1. Abstract (about 250 words; write last)

Points in order:
- Problem: regime models (HMMs) look strong in backtests, but many evaluations use information that
  would not have been available at the time, such as smoothed regime probabilities or parameters fit on
  the full sample.
- Design: three versions of the same 2-regime Gaussian HMM, which differ only in what they may see:
  - A, honest: rolling 1,000-day refit every 21 days, filtered probabilities.
  - B, future-trained: parameters fit on the full sample, filtered probabilities.
  - C, retrospective: full-sample parameters and smoothed probabilities.
  - Benchmarks: historical simulation and GARCH(1,1)-t.
- Data: S&P 500, FTSE 100, Nikkei 225 and DAX daily log returns, 1990-2025. Forecasts run 2005-2025
  (about 5,100-5,300 days per index). VaR at 95% and 99%.
- Headline results:
  - Hindsight (C vs A) lowers quantile loss by 14.6-15.3% at 95% and 20.5-27.1% at 99%. All are
    significant (DM p < 0.05) and every 95% bootstrap CI excludes zero.
  - Future-trained parameters alone (B vs A) give only 1.3-2.3% at 95% and 4.2-10.1% at 99%, and most
    of those CIs include zero.
  - Version C is the only method whose 99% breach rate hits the 1% target (1.00% on the S&P 500).
    The honest model breaches 1.95% of days.
  - Basel green-zone share at 99%: C 84-95% of rolling windows vs A 60-68%.
  - The honest HMM loses to a plain GARCH-t on every index. On the S&P 500 at 99%, GARCH-t's advantage
    (20.5%) equals the look-ahead premium (20.5%).
- Mechanism: the real-time model takes a median 1-3 days, and a mean of 6-14 days, to notice a stormy
  regime. About 21-24% of days, those within 20 days of a regime switch, produce 51-69% of the premium.
- Robustness: holds across window lengths, random seeds, 3 regimes, fat-tailed emissions, four
  sub-periods, and an independent re-implementation in statsmodels.
- Takeaway: evaluations of regime-based risk models must use filtered probabilities and rolling
  re-estimation. Otherwise the reported skill is largely an artefact of hindsight.

---

## 2. Introduction

### 2.1 Motivation (paragraphs 1-2)
- VaR is the standard market-risk measure. Banks backtest it, and the Basel traffic light turns
  backtest breaches into capital multipliers (BCBS 1996).
- Regime-switching models capture calm vs stormy markets (Hamilton 1989; Ang & Timmermann 2012;
  Guidolin 2011). Regime VaR literature: Billio & Pelizzon (2000), Marcucci (2005), Guidolin &
  Timmermann (2006), Ardia et al. (2018).
- An HMM can infer the current regime in two ways:
  - Filtered: uses returns up to today. This is the only option available in real time.
  - Smoothed: uses the whole sample, including the future. Smoothed probabilities look much cleaner
    (point to Figure 1).
- Many tutorials, blogs and some published ML work use smoothed or ex-post regime labels in backtests.
  Examples: Shu, Yu & Mulvey (2024b) flag that Gu & Mulvey (2021) and Uysal & Mulvey (2021) derived
  labels "all at once". Kapoor & Narayanan (2023) cover leakage across ML-based science.

### 2.2 Gap (paragraph 3)
- The literature recognises that in-sample identification and real-time forecasting differ:
  - Kole & van Dijk (2017): different methods win in-sample vs out-of-sample.
  - Shu et al. (2024a): about half a month of online detection lag, plus a footnote recommending
    tuning on online labels.
  - Chauvet & Piger (2008) and Hamilton (2011): real-time dating accuracy.
  - Cooper & Gulen (2006): pseudo-out-of-sample designs are not real-time.
  - Dacco & Satchell (1999): small regime misclassification erases forecast gains.
- No academic paper we found measures the look-ahead premium in VaR, meaning how much of a regime
  model's apparent risk-forecasting skill comes from hindsight (`literature/01-look-ahead-bias-real-time.md`,
  section G).
- Non-academic precedents that report smoothed-vs-filtered Sharpe gaps (returns, not risk):
  - The GitHub "lookahead ladder": Sharpe 1.74 vs 0.78.
  - A Danish OMX HMM repo: 1.39 vs 0.84.
  - Halley (Substack), the PyMC Labs blog and Quantpedia.
  - Acknowledge these as anecdotal precedent; a referee may know them.

### 2.3 Research question and contributions (paragraph 4, bulleted list in the paper is fine)
- RQ: by how much does look-ahead bias inflate the measured VaR performance of a 2-regime HMM, and
  through which channel?
- Contributions:
  1. A controlled A/B/C design that changes only the information set, and separates parameter
     look-ahead (B) from regime-label look-ahead (C), with C-mild as a further split.
  2. Results on four major indices over 21 years at two VaR levels, with block-bootstrap CIs, DM tests
     and a Holm correction.
  3. Regulatory translation: Basel traffic-light zones and capital multipliers.
  4. Mechanism: the detection delay, and the concentration of the premium after regime switches.
  5. Robustness, including fat-tailed emissions and an independent second implementation.
  6. Open, tested code. 25 unit tests, including tests proving the honest version cannot see the future.

### 2.4 Roadmap sentence
- Section 3 literature, 4 data, 5 method, 6 results, 7 mechanism, 8 robustness, 9 discussion,
  10 limitations, 11 conclusion.

**Reviewer risk: novelty framing.** The literature note concludes that a bare "smoothed vs filtered"
comparison is not novel on its own. What is novel is a formal decomposition into channels for VaR with
proper backtests and multiple-testing control. This paper decomposes two channels, parameters (B) and
regime labels (C, C-mild), and adds a third partially (3 regimes, without selecting the count).
- **Decision needed:** either (a) frame the paper as a two-channel decomposition and list
  regime-count selection and full-sample standardisation as future work, or (b) add those two
  experiments before submission. Option (a) is honest and enough for NHSJS. Option (b) strengthens
  the novelty claim.

---

## 3. Background and literature review

Source notes: `literature/01`-`04`, deep reads `05a`-`05e`, full list `literature/00-references.md`.

### 3.1 Regime-switching models in finance
- Hamilton (1989) Markov switching. Hamilton & Susmel (1994) SWARCH. Gray (1996). Ang & Bekaert (2002).
  Guidolin & Timmermann (2007, 2008). Ang & Timmermann (2012) survey.
- Estimation: Baum-Welch EM (hmmlearn) or direct maximum likelihood (statsmodels MarkovRegression),
  both used here.
- Filtered vs smoothed definitions: filtered P(S_t | r_1..r_t); smoothed P(S_t | r_1..r_T). Kim
  smoother / forward-backward.

### 3.2 Regime models for VaR and ES
- Billio & Pelizzon (2000), Marcucci (2005), Guidolin & Timmermann (2006), Ardia et al. (2018)
  large-scale MS-GARCH VaR study. Bauwens, Preminger & Rombouts (2010). Augustyniak (2014).
- Recent HMM-VaR and crypto papers (deep reads):
  - Saidane & Ben Mohamed (2026), MHMFA.
  - Gao, Ye & Guo (2022), regime-switching CAViaR.
  - Oprea & Bara (2026).
  - Malim Franco & Hotta (2026).
  - Kim (2026).
  - Note which ones state their inference type. Our notes flag possible look-ahead in Saidane,
    Malim Franco and Gao (full-sample preprocessing), but none is confirmed without the full text.
    Do not claim these papers are biased; say at most that their inference type is not stated.

### 3.3 Look-ahead bias, leakage and real-time evaluation
- Kole & van Dijk (2017); Shu, Yu & Mulvey (2024a, 2024b); Nystrup, Kolm & Lindström (2020); Chauvet &
  Piger (2008); Hamilton (2011); Cooper & Gulen (2006).
- Leakage in ML generally: Kapoor & Narayanan (2023); Arnott, Harvey & Markowitz (2019); Bailey et al.
  (2017) backtest overfitting.
- Theory: Dacco & Satchell (1999), where misclassification destroys the forecast gain. Supports the
  mechanism section.

### 3.4 Evaluating VaR forecasts
- Coverage tests: Kupiec (1995) POF; Christoffersen (1998) conditional coverage; Christoffersen &
  Pelletier (2004) duration; Engle & Manganelli (2004) DQ test.
- Scoring: the quantile (tick) loss is consistent for the quantile (Gneiting 2011; Ehm et al. 2016),
  which is why it is the main ranking metric here. Coverage tests alone have low power.
- Comparison: Diebold & Mariano (1995), Giacomini-White, Model Confidence Set (Hansen, Lunde & Nason
  2011).
- Regulation: BCBS (1996) traffic light; FRTB (BCBS 2016, 2019) moves to ES at 97.5%.

**Citations to add to `00-references.md`** (used in the method, not yet in the list; check the
bibliographic details before citing):
- Bollerslev (1987), GARCH with Student-t errors.
- Künsch (1989), moving-block bootstrap.
- Holm (1979), step-down multiple-testing correction.
- Newey & West (1987), HAC variance used in the DM statistic.
- Rabiner (1989) or Baum et al. (1970), HMM forward-backward / EM.
- Koenker & Bassett (1978), the quantile-loss origin. Optional.

---

## 4. Data

- Source: Yahoo Finance via `yfinance`, adjusted close, cached in `data/*.csv` so every run uses the
  same prices. Tickers: ^GSPC, ^FTSE, ^N225, ^GDAXI.
- Returns: daily log returns in percent, r_t = 100 ln(P_t / P_{t-1}).
- Sample: 1990-01 to 2025-12. Forecast period starts 3 Jan 2005, which leaves at least 1,000 days of
  history for the first rolling fit.
- **Table 1** (main text). Days, forecast days, moments:

| Index | Days | Forecast days | Mean % | SD % | Min % | Max % | Skew | Excess kurt. |
|---|---|---|---|---|---|---|---|---|
| S&P 500 | 9066 | 5283 | 0.032 | 1.139 | -12.765 | 10.957 | -0.365 | 10.878 |
| FTSE 100 | 9092 | 5303 | 0.015 | 1.078 | -11.512 | 9.384 | -0.306 | 7.797 |
| Nikkei 225 | 8834 | 5138 | 0.003 | 1.480 | -13.234 | 13.235 | -0.185 | 6.158 |
| DAX | 9106 | 5331 | 0.029 | 1.374 | -13.055 | 10.797 | -0.207 | 5.881 |

- Points to make: all four series are fat-tailed (excess kurtosis 5.9-10.9) and negatively skewed.
  This motivates both the regime model and the fat-tailed robustness check (section 8.4).
- Index prices exclude dividends. This barely matters for one-day VaR; say so in one clause.
- Trading calendars differ across indices, so each series is analysed on its own calendar and no
  cross-index alignment is needed.

**Table 2** (main text or appendix). Full-sample 2-regime fit for the S&P 500, used for description
only:
- Calm: mean 0.081%, volatility 0.676%, stay probability 0.9872, average length 78 days, 70.7% of days.
- Stormy: mean -0.084%, volatility 1.818%, stay probability 0.9688, average length 32 days, 29.3% of days.
- Stormy volatility is about 2.7x calm (derived: 1.818 / 0.676).
- The average length is 1/(1 - p_stay).
- Stress in the text that this fit uses all data, so it describes the regimes and is never used to
  forecast.

---

## 5. Methodology

### 5.1 The 2-regime Gaussian HMM
- Hidden state S_t in {calm, stormy}, first-order Markov with transition matrix P.
- r_t | S_t = k ~ N(mu_k, sigma_k^2).
- Estimation: EM (hmmlearn `GaussianHMM`, diagonal covariance, up to 200 iterations, tol 1e-4), with
  5 random starts, keeping the best log-likelihood (`regime_var.fit_hmm`).
- Label switching: after every fit, states are sorted by variance so that state 0 is always calm.
  This keeps labels consistent across refits.

### 5.2 From regime probabilities to VaR
- One-day-ahead regime weights: w_t = (probability vector for day t-1) x P.
- The VaR at level alpha is the alpha-quantile of the mixture
  sum_k w_{t,k} N(mu_k, sigma_k^2), found by root-finding (Brent) on the mixture CDF
  (`mixture_quantile`).
- Notation: a VaR forecast q_t is stored as a negative return quantile. A breach occurs when r_t < q_t.
- Levels: alpha = 5% (95% VaR) and 1% (99% VaR).

### 5.3 The three information sets (core of the paper; consider a small schematic table)

| Version | Parameters estimated on | Regime probabilities | Uses future data? | Code |
|---|---|---|---|---|
| A honest | last 1,000 days, refit every 21 trading days | filtered up to t-1, pushed one step forward | no | `hmm_var_rolling` |
| B future-trained | full sample 1990-2025, fit once | filtered up to t-1, pushed one step forward | parameters only | `hmm_var_full_sample(smoothed=False)` |
| C retrospective | full sample, fit once | smoothed for day t itself (forward-backward) | parameters, and regime labels including day t's own return | `hmm_var_full_sample(smoothed=True)` |
| C mild | full sample, fit once | smoothed for day t-1, pushed one step forward | parameters and future labels, but not day t's own label | `smoothed_lag=True` |

- Decomposition logic:
  - B - A = parameter look-ahead channel.
  - C - B = regime-label channel.
  - C - C mild = the part due to C seeing day t's own return through its smoothed label.
- Version A details for reproducibility. Within each 21-day block, parameters stay fixed. The forward
  filter runs from the start of the training window to the day before each forecast day. Nothing at
  or after the forecast day is used.
- Leakage guarantees are unit-tested (`tests/test_regime_var.py`):
  - Scrambling all returns after day t leaves A's forecast for day t unchanged
    (`test_honest_version_ignores_the_future`).
  - The same holds for the same-day return (`test_honest_version_ignores_the_same_day_return`).
  - B and C do change (`test_biased_versions_do_use_the_future`).
  - The benchmarks are also clean (`test_benchmarks_ignore_the_future`).
  - These tests are worth a sentence in the paper: they show the honest version is honest by
    construction, not by assumption.

### 5.4 Benchmarks
- Historical simulation: the empirical quantile of the previous 250 returns.
- GARCH(1,1) with Student-t errors and a constant mean (Python `arch`), refit on the same schedule as
  A (1,000-day window, every 21 days). Between refits, parameters stay fixed and the variance
  recursion runs forward. VaR = mu + sigma_t x t_nu^{-1}(alpha).

**Reviewer risk: window mismatch.** Historical simulation uses 250 days while the HMM and GARCH use
1,000. 250 is the regulatory convention. Either justify it in one sentence, or add a 1,000-day
historical-simulation run to the appendix.

### 5.5 Evaluation
- Breach rate vs target.
- Kupiec (1995) unconditional coverage LR test, chi-squared(1).
- Christoffersen (1998) conditional coverage, chi-squared(2): coverage plus no breach clustering.
- Quantile (tick) loss L_t = (alpha - 1{r_t < q_t})(r_t - q_t). Lower is better. This is the primary
  ranking metric because it is a strictly consistent scoring function for quantiles (Gneiting 2011).
- **Look-ahead premium** = 100 x (1 - mean loss of the biased model / mean loss of A). Define this term
  clearly; it is the paper's key quantity.
- Confidence intervals: moving-block bootstrap with 20-day blocks and 2,000 resamples, percentile 95%
  CI. Blocks keep calm and stormy stretches together.
- Diebold-Mariano test on loss differences, Newey-West variance with lag floor(n^{1/3}), two-sided.
- Holm step-down correction over the 8 main S&P 500 comparisons (Table 6).
- Basel traffic light (99% VaR):
  - Breaches are counted in every rolling 250-day window.
  - Zones: green 0-4 breaches, yellow 5-9, red 10+.
  - Multiplier = 3 + plus factor: 0.40, 0.50, 0.65, 0.75, 0.85 for 5-9 breaches, and 1.0 for 10+.

**Reviewer risk: stars without correction.** Table 4 stars use unadjusted DM p-values across 4 indices
x 2 levels x 3 comparisons. Holm is applied only to the S&P 500 table. The C-vs-A results survive any
correction (p ~ 0), but the few starred B-vs-A cells (Nikkei and DAX at 99%) may not.
- **Decision needed:** either extend Holm to Table 4, or state in its caption that the stars are
  unadjusted.

### 5.6 Implementation and reproducibility
- Python. numpy, pandas, scipy, hmmlearn, arch, statsmodels (cross-check only), matplotlib, yfinance.
- Every table and figure is generated by `make_paper_results.py`; nothing is edited by hand.
- 25 automated tests, all passing.
- Fixed seeds; seed 0 in the main run.
- Runtimes: robustness about 15 minutes, improvements about 10 minutes.
- Code availability statement: repository URL. **Decision needed:** public GitHub link, or "available
  on request".

---

## 6. Results

### 6.1 Main results, S&P 500 (Table 3, main text; Figure 4 timeline, appendix or main)

| Method | 95% breach % | 99% breach % | 99% Kupiec p | 99% Christoffersen p | QL 95% | QL 99% |
|---|---|---|---|---|---|---|
| A honest | 5.70 | 1.95 | 0.000 | 0.000 | 0.1379 | 0.0463 |
| B future-trained | 5.96 | 1.82 | 0.000 | 0.000 | 0.1351 | 0.0444 |
| C retrospective | 4.49 | 1.00 | 0.981 | 0.008 | 0.1168 | 0.0368 |
| Historical sim | 5.49 | 1.78 | 0.000 | 0.000 | 0.1459 | 0.0491 |
| GARCH-t | 6.78 | 1.78 | 0.000 | 0.000 | 0.1256 | 0.0368 |

Points:
- Honest A breaches 99% VaR on 1.95% of days, almost twice the target. Kupiec rejects.
- C hits exactly 1.00% (Kupiec p = 0.98). To a naive backtest, C looks like a perfect model.
- C still fails Christoffersen at 99% (p = 0.008), so its breaches cluster even with hindsight. The
  hindsight model is not perfect; it only gets the breach count right.
- At 95%, C and historical simulation are the only methods Kupiec does not reject (p 0.08, 0.11).
- C's quantile loss at 99% (0.0368) is identical to GARCH-t's (0.0368). Hindsight makes the HMM look
  exactly as good as a standard GARCH model.
- Figure 4: breach timeline, 99% breach rates of 1.95 / 1.82 / 1.00 / 1.78 / 1.78%. Breaches cluster
  in 2008, 2020 and 2022 for all methods.

### 6.2 The look-ahead premium across four indices (Table 4 and Figure 3, both main text)

| Index | C vs A 95% | C vs A 99% | C mild vs A 95% | C mild vs A 99% | B vs A 95% | B vs A 99% |
|---|---|---|---|---|---|---|
| S&P 500 | 15.3 [11.8, 18.5]* | 20.5 [13.1, 27.1]* | 13.2 [9.7, 16.2]* | 19.2 [11.7, 25.8]* | 2.1 [-1.2, 4.9] | 4.2 [-4.0, 10.7] |
| FTSE 100 | 14.6 [11.7, 17.4]* | 23.4 [17.6, 28.9]* | 12.8 [10.0, 15.4]* | 21.8 [16.0, 27.3]* | 1.3 [-1.0, 3.4] | 6.7 [0.5, 12.5] |
| Nikkei 225 | 15.0 [12.0, 17.9]* | 24.2 [18.5, 28.7]* | 12.8 [9.9, 15.6]* | 22.3 [16.3, 27.1]* | 2.3 [-0.4, 4.9] | 8.6 [1.1, 14.6]* |
| DAX | 14.7 [12.0, 17.4]* | 27.1 [21.6, 31.9]* | 13.1 [10.5, 15.6]* | 25.6 [20.0, 30.5]* | 1.5 [-1.2, 4.3] | 10.1 [3.0, 16.4]* |

Points:
- The total premium is very stable across markets at 95% (14.6-15.3%) and larger at 99% (20.5-27.1%).
  The bias matters more in the tail, where regulators look.
- Every C-vs-A and C-mild-vs-A CI excludes zero.
- The parameter channel (B) is small. At 95% every CI includes zero. At 99% it is 4-10%, and
  significant only for Nikkei and DAX (unadjusted).
- Share of the total premium explained by parameters alone (derived, B / C): S&P 14% / 20%, FTSE
  9% / 29%, Nikkei 15% / 36%, DAX 10% / 37% (95% / 99%). So regime labels, not parameters, are the main
  channel.
- C mild keeps 85-89% of the 95% premium and 92-95% of the 99% premium (derived, C mild / C). So the
  premium is not mainly C "seeing today's return". It comes from knowing which regime the market was in
  using later data.
- Figure 3 shows this visually: orange C dots far above zero, blue B dots near zero with wide CIs.

### 6.3 Comparison with simple benchmarks (Table 5 main text, Table 6 appendix or main)
- GARCH-t beats honest A on all four indices at both levels: 4.3-8.9% lower loss at 95%, 11.4-20.5% at
  99%.
  - Significant at 95% for S&P, FTSE and DAX (DM p 0.006-0.020). Nikkei p = 0.059.
  - At 99%, significant for S&P (p = 0.046) and DAX (0.009).
- Honest A beats historical simulation at 95% on all four (3.7-6.5%, all p < 0.05). At 99% the
  difference is not significant (p 0.18-0.71).
- Ranking story: the honest regime model sits between historical simulation and GARCH-t. The biased C
  appears to match or beat GARCH-t. A researcher who used C would wrongly conclude that the regime
  model is state of the art.
  - S&P 500 99%: the GARCH-t advantage over A (20.5%) equals the C-vs-A premium (20.5%).
  - Other indices: the C premium (23-27%) exceeds the GARCH-t advantage (11-15%), so C would appear to
    beat GARCH-t outright.
- Table 6, Holm-corrected S&P 500 DM tests:
  - C vs A: significant at both levels (adjusted p ~ 0).
  - B vs A: not significant at either (adjusted 0.58).
  - A vs historical simulation, 95%: significant (adjusted p 0.026).
  - A vs GARCH-t: significant at 95% (adjusted p 0.029), not at 99% after correction (0.183).
  - Report honestly that GARCH-t's 99% advantage on the S&P is not significant after Holm.

### 6.4 Regulatory consequence: Basel traffic light (Table 9 and Figure 5, main text)

| Index | A green % | B green % | C green % | Hist. sim green % | GARCH-t green % |
|---|---|---|---|---|---|
| S&P 500 | 60.3 | 64.8 | 83.9 | 55.7 | 48.7 |
| FTSE 100 | 67.5 | 71.7 | 93.2 | 49.0 | 60.3 |
| Nikkei 225 | 63.5 | 75.5 | 94.8 | 58.6 | 65.0 |
| DAX | 64.6 | 68.9 | 86.2 | 53.1 | 74.8 |

- C spends 84-95% of windows in green. A spends 60-68%.
- Red zone: A 7-14% vs C 2.6-5.1%.
- Mean multiplier: A 3.22-3.28 vs C 3.05-3.12.
- Derived (S&P 500): the multiplier drops from 3.28 to 3.12, about 5% less capital for the same VaR
  level. Present this as an illustration; capital = multiplier x VaR, and the VaR levels also differ.
- Nuance: GARCH-t has the fewest red windows (0-3.4%) but is often yellow. GARCH-t's breaches are
  spread out; A's come in bursts. This links to the clustering result (Christoffersen) and to the
  mechanism in section 7.
- Number of windows: 5,034 (S&P), 5,054 (FTSE), 4,889 (Nikkei), 5,082 (DAX).

### 6.5 Crisis vs calm (Table 7, appendix)
- Crisis days: Sep 2008-Jun 2009, mid-Feb-Jun 2020 and all of 2022. 554 days on the S&P 500.
- In crises, GARCH-t dominates: 24.2% (95%) and 51.7% (99%) lower loss than A. C gains only 9.9% /
  10.9%.
- In calm periods (4,729 days), C's relative premium is larger: 17.4% / 25.9%. GARCH-t is only about
  3% better than A.
- Interpretation to discuss: much of C's advantage comes from correctly loosening VaR when calm
  returns and correctly tightening it at turns. GARCH-t's advantage is in fast volatility updating
  during crises. These are different skills.
- Caveat: crisis losses are about 3-5x larger in absolute terms (derived: 0.367 vs 0.111 at 95%), so
  the crisis days carry a lot of total loss.

---

## 7. Mechanism: why hindsight helps

### 7.1 Detection delay (Table 10, main or appendix; Figure 1 and Figure 2, main)
- Onset definition: smoothed P(stormy) crosses 0.5 and stays above for 10+ days after 20+ calm days.
  Delay = days until the real-time probability also crosses 0.5, capped at 60.
- Honest A: 18-21 onsets per index. Median delay 1-3 days, mean 5.8-13.7 days. 67-78% caught within
  5 days.
- The mean is far above the median, so a minority of onsets are caught very late. Those late
  episodes are where honest VaR is too loose and the breaches cluster.
- B has a lower mean delay (2.9-4.4) but a similar median.

**Reviewer risk: different reference model.** The delay reference is the full-sample smoothed series,
while A's probabilities come from a different, rolling-fitted model. Part of the measured delay can come
from model differences, not only from real-time vs hindsight. State this in the text. B is the cleaner
comparison because it uses the same model as the reference.

- Figure 1 (S&P 500, 2007-2010): the smoothed stormy probability switches cleanly and early, while the
  filtered one is noisy and lags.
- Figure 2: 99% VaR around 2008.
  - C is already near -4.3% from mid-2007, before the crash.
  - A deepens to about -6.5% only after the Sept-Oct 2008 losses, then overshoots.
  - This is the visual core of the paper.

### 7.2 Where the premium is earned (Table 11, main text)
- Switch = smoothed P(stormy) crosses 0.5. Window = the 20 days after each switch.
- 70-78 switches per index. These windows cover 21-24% of forecast days but produce 51-69% of the
  premium.
- Premium near switches: 25-39%. Elsewhere: 7-22%.
- Link back to Dacco & Satchell (1999): forecasts lose most at regime transitions, which is exactly
  where hindsight gives an unfair head start.

---

## 8. Robustness (Tables 8, 12, 12b, 13; cross-check; mostly appendix, with a one-paragraph summary in the main text)

### 8.1 Window length, seeds, number of regimes (Table 8, S&P 500)
- 500-day window: C vs A 15.6 / 21.9. 1,500 days: 15.9 / 21.5. Main run (1,000 days): 15.3 / 20.5.
- Seeds 10, 20, 30, 40: C vs A 15.2-15.8 at 95% and 20.4-20.6 at 99%. Insensitive to EM initialisation.
- 3 regimes: the premium grows to 19.8 / 29.7. B vs A also grows (4.4, CI [0.9, 7.9] at 95%). More
  regimes give more ways to misclassify in real time, so the bias increases with model complexity.
  This is an important point for ML regime models with many states.

### 8.2 Sub-periods (Table 13)
- C vs A is positive in all 32 cells (4 indices x 2 levels x 4 periods).
- Only one CI includes zero: S&P 500 2005-09 at 99%, 13.9 [-6.9, 30.7]. That period has few breaches
  and a wide CI.
- Largest premiums are at 99% in 2020-25: DAX 37.1, FTSE 35.8.
- The premium is not driven by one crisis.
- The fat-tailed version gives similar numbers (`results/subperiod_premium.csv`).

### 8.3 Independent cross-check (`crosscheck.py`, `results/crosscheck_log.txt`)
- Versions A-C rebuilt with statsmodels MarkovRegression (direct MLE instead of EM), and GARCH-t refit
  every 5 days instead of 21.
- Premium: C vs A 15.8 / 21.6 (ours 15.3 / 20.5); B vs A 2.7 / 5.5 (ours 2.1 / 4.2).
- GARCH-t 99% breach rate: 1.80% (ours 1.78%).
- A hand-written GARCH recursion and t-quantile match the arch package to 1e-16.
- The results do not depend on one library's estimator.

### 8.4 Fat-tailed HMM (Tables 12 and 12b)
- Each regime's distribution is the weighted empirical distribution of past training returns, not a
  normal curve. Weights are the regime probabilities of the training days.
- Effect on honest A: 95% coverage is fixed (Kupiec p becomes 0.11-0.67 on all four indices). 99% still
  breaches too often (1.36-1.70%, Kupiec rejects on all four).
- Quantile loss barely changes: fat-tailed A vs normal A is between -0.2% and +2.3%, every CI includes
  zero.
- The premium survives intact: C vs A 14.2-14.7% (95%) and 21.2-25.4% (99%), all significant.
- GARCH-t still beats fat-tailed A: 4.6-8.5% at 95%, 9.3-18.8% at 99%.
- Notable: fat-tailed C at 99% breaches only 0.39-0.53% of days, which is too conservative, and Kupiec
  rejects. Yet its quantile loss is the lowest. Coverage tests and loss functions can disagree. Discuss
  briefly: the tick loss rewards a tighter fit away from the tail too.
- Conclusion: the premium comes from information, not from the normal-distribution assumption.

---

## 9. Discussion

- Main message: about 15% (95%) to 20-27% (99%) of a regime HMM's measured VaR quality is an artefact
  of hindsight. Almost all of it enters through the regime labels, not the parameters.
- Practical rules for researchers and practitioners:
  1. Never evaluate with smoothed or Viterbi probabilities. Use filtered or one-step predictive ones.
  2. Re-estimate on rolling or expanding windows. Full-sample parameters are a smaller but real leak,
     and a bigger one with more regimes.
  3. Report a GARCH-t benchmark. An honest HMM does not beat it here.
  4. Test the information set directly, as with the unit tests that scramble the future.
- Why the parameter channel is small: daily return regimes are persistent and well identified by
  1,000 days. The hard part is knowing the current state, not knowing what each state looks like.
- Regulatory reading:
  - A bank backtesting a hindsight model would see a green zone and a near-perfect 1% breach rate.
  - The honest model would be yellow or red about a third of the time, with higher capital multipliers.
- Relation to the literature:
  - Consistent with Kole & van Dijk (2017), Shu et al.'s observed online lag, and Dacco & Satchell's
    misclassification theory.
  - Quantifies for VaR what the practitioner repos showed for Sharpe ratios.
- Extending to ML regime models: methods that train on ex-post labels (trend-filter, jump-model and
  clustering labels) carry the same channel. The 3-regime result suggests the bias grows with model
  flexibility.

---

## 10. Limitations

- Only one model family: a 2-regime (and 3-regime) Gaussian or empirical HMM. MS-GARCH, jump models
  and supervised ML are not tested.
- Only VaR. No expected shortfall, though FRTB uses ES at 97.5%. FZ0 joint loss and the Acerbi-Szekely
  tests are natural extensions.
- Only two channels decomposed (parameters and labels). Regime-count selection, full-sample
  standardisation and hyperparameter selection are not tested (see the novelty decision in section 2).
- B confounds two things: it sees the future, and it also trains on about 35 years instead of 1,000
  days with no refits. So "B vs A" is an upper bound on pure parameter look-ahead under this design.
  An expanding-window variant would separate the two.
- Equity indices only. Four developed markets, price returns.
- Detection-delay reference model differs from A's model (section 7.1).
- Unadjusted significance stars in the multi-index tables (section 5.5).
- No transaction costs or portfolio use. Risk forecasting only.

---

## 11. Conclusion (3-5 sentences of points)
- Restate the RQ and the A/B/C design.
- Two numbers: a 15% / 20-27% premium, and C's green-zone share of 84-95% vs 60-68%.
- Channel: labels, not parameters.
- Recommendation: filtered probabilities, rolling refits, a GARCH-t benchmark, and leakage tests.
- Future work: ES, more channels, ML regime models, crypto (link to the 05a-05e deep reads).

---

## 12. Figures and tables plan

| Exhibit | Main/Appendix | File | Caption facts (from `paper/README.md`) |
|---|---|---|---|
| Figure 1 | Main | `figure1_regime_probabilities` | S&P 500 returns 2007-2010; filtered (blue) vs smoothed (orange) P(stormy); 2-regime HMM fit 1990-2025, for illustration only |
| Figure 2 | Main (recommended addition) | `figure2_var_2008` | 99% VaR of A (blue) and C (orange) over returns (grey), Jun 2007-Dec 2009; A refits every 21 days on 1,000 days |
| Figure 3 | Main | `figure3_premium_by_index` | % lower quantile loss vs A for C (orange) and B (blue), 4 indices, 95% and 99%; dots = estimates, lines = 95% block-bootstrap CI (20-day blocks, 2,000 resamples); 2005-2025 |
| Figure 4 | Appendix | `figure4_breach_timeline` | Days the S&P 500 loss exceeded 99% VaR by method; 5,283 days; target 1% |
| Figure 5 | Main | `figure5_basel_zones` | Share of rolling 250-day windows green/yellow/red, 99% VaR, S&P 500; 5,034 windows |
| Table 1 | Main | `table1_data_summary` | Return statistics |
| Table 2 | Appendix | `table2_regimes` | Full-sample regimes, description only |
| Table 3 | Main | `table3_main_results` | S&P 500 scores, all 5 methods |
| Table 4 | Main | `table4_look_ahead_premium` | Premium with CIs, 4 indices |
| Table 5 | Main | `table5_benchmarks` | Benchmarks vs honest HMM |
| Table 6 | Appendix | `table6_diebold_mariano` | DM with Holm |
| Table 7 | Appendix | `table7_crisis_vs_calm` | Crisis vs calm |
| Table 8 | Appendix | `table8_robustness` | Window, seeds, 3 regimes |
| Table 9 | Main | `table9_basel_traffic_light` | Basel zones, 4 indices |
| Table 10 | Appendix | `table10_detection_delay` | Detection delay |
| Table 11 | Main | `table11_premium_near_switches` | Premium near switches |
| Tables 12, 12b | Appendix | `table12_*` | Fat-tailed HMM |
| Table 13 | Appendix | `table13_subperiods` | Sub-periods |

- Numbering: the figure file names give the breach timeline as Figure 4 and Basel as Figure 5. If only
  Figures 1, 2, 3 and 5 go in the main text, renumber in reading order.
- **Decision needed:** whether to keep the file names or renumber in `make_paper_results.py`.

---

## 13. Appendix plan

- A1. HMM equations: forward filter, one-step prediction, forward-backward smoother.
- A2. Pseudocode for Version A's rolling loop (block refit, filter to t-1).
- A3. Unit-test list as evidence of no leakage (25 tests; names in `paper/WORK_SUMMARY.md`).
- A4. Full tables 2, 6, 7, 8, 10, 12, 12b, 13 and Figure 4.
- A5. Cross-check results table (`results/crosscheck.csv`).
- A6. Software versions. Run `python -m pip freeze` with the virtual environment active.

---

## 14. Pre-submission checklist

- [ ] Authors write all prose and captions. Check NHSJS's current AI-use policy and its disclosure
  wording for code and analysis help.
- [ ] Resolve the four "Decision needed" items: novelty framing, Holm on Table 4, code link,
      figure numbering.
- [ ] Add the 6 method citations to `literature/00-references.md` and verify them.
- [ ] One targeted SSRN title search for "look-ahead" plus "regime" plus "VaR" (gap noted in
      `literature/01`, section G).
- [ ] Rerun `make_paper_results.py` once from a clean venv and confirm `tables.md` is unchanged.
- [ ] Check the reference style against NHSJS author guidelines.
