# Deep read: Oprea & Bara (2026)

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I read the full paper (31 pages, CC BY open access), including Algorithm 1 in Appendix A, which is an image I rendered and read. The snippet is wrong on its key point: the paper does no VaR/ES or CAViaR modelling at all. It forecasts Bitcoin returns and prices one day ahead and scores them with point-error metrics. The only CAViaR link is a citation of a different paper in the literature review. Overlap with our research question is low, and the paper is more useful to us as an example of a look-ahead-prone design.

## 1. Access
- Full text read. The source is `https://link.springer.com/content/pdf/10.1007/s10614-026-11338-3.pdf` (open access, CC BY 4.0, per Semantic Scholar and OpenAlex). A browser user-agent hit a bot challenge; a plain curl user-agent with a cookie jar got the PDF.
- Unpaywall rejected the placeholder email with HTTP 422. That did not matter, because Semantic Scholar and OpenAlex already gave the PDF link.
- Files are in `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/oprea/springer_pdf3/`: `paper.pdf`, `paper.txt` and `alg2-28.png` (the rendered Algorithm 1).
- Received 25 Oct 2025, accepted 4 Mar 2026.

## 2. What it actually does
- It forecasts one-day-ahead log returns and turns them into prices with P̂ₜ₊₁ = Pₜ·exp(r̂ₜ₊₁). Scoring uses MAE, RMSE and R² on the price level, plus a long/flat trading backtest.
- **The RS-CAViaR part of the snippet is wrong.** It comes from the literature review, which summarises Gao, Ye & Guo (2022, *Finance Research Letters*), "Jointly forecasting the VaR and ES of Bitcoin with a regime-switching CAViaR model". Trucíos & Taylor (2023) is also only cited. VaR and ES appear in the abbreviation list but are never modelled.
- **The XGBoost part is right in a different form.** XGBoost is a classifier that picks a forecasting model at each step. It chooses among three models, each tied to one regime: ARIMAX for bear, SARIMAX for sideways and NeuralProphet for bull.
- The "probabilistic generative model" in the title is just the Gaussian HMM.

## 3. Data and split
- Daily Bitcoin data from Investing.com, 01 Jan 2012 to 30 Jun 2025, 4,930 rows: price, OHLC, volume and % change.
- Features: rolling volatility, log volume, RSI, MACD, Bollinger Band width, and lags.
- The test window is 1 Jan to 30 Jun 2025 (about 180 days), reported month by month for March to June. The Fig. 6 caption says "Jan.-Jun. 2015" and the tables say "31 Jun" (both typos).
- The training window length W, the refit frequency and the validation window are never stated.
- The ablation runs over an unspecified "one-year" period. Its robustness check says models "trained on one market cycle (e.g., pre-2023) are evaluated on … 2024–2025", with no numbers given.

## 4. Regime detection
- A Gaussian HMM with K = 3 is fitted by EM to log returns only (§3.3, Eq. 13).
- States are decoded with the **Viterbi** path, "Ẑ₁:T = argmax p(Z₁:T | r₁:T)" (Eq. 15; Algorithm 1, lines 8–9).
- States are then labelled by mean return: lowest = bear, highest = bull, the remaining one = sideways. This labelling is "validated against known periods of bullish and bearish cycles".
- How K was chosen (§4.2): "we evaluated alternative HMM configurations with different numbers of hidden states (K = 2,3, 4,5). Model selection was performed using a combination of log-likelihood, BIC and **out-of-sample forecasting performance**." No numbers or table are given.
- Reported regime statistics: average durations of 14.8 days (bear), 22.4 (sideways) and 16.1 (bull). The transition-matrix diagonal is 0.92, 0.94 and 0.91. The paper does not say which sample these come from.

## 5. Regime inference at forecast time and leakage
- **The paper claims there is no leakage** (§3.1): "At each time step t, all model components, including regime detection, regime-specific forecasting models and the meta-learning selector, are trained solely on observations from the historical window [t − W, t]… No future data is used at any stage of training, model selection or evaluation, thereby eliminating any form of data leakage and preserving strict temporal causality."
- **Algorithm 1 does not match that claim.**
  - It fits the HMM once to {rₜ} and Viterbi-decodes over 1:T (lines 8–9).
  - It then trains each regime's model on Dz = {(rₜ,xₜ) | Ẑₜ = z} (line 13).
  - It trains XGBoost over "t = T−h to T−1" with "Label: zₜ" (lines 23–27), and only then forecasts (line 29).
  - It contains no rolling loop, so as written the regime labels are full-sample Viterbi labels.
- **What XGBoost is trained to predict is ambiguous.**
  - §3.1 says the target is "the forecasting model that historically minimized predictive error over similar periods".
  - Algorithm 1 writes "Label: zₜ", the same symbol it uses for the regime state.
  - If the target is the regime, XGBoost is learning hindsight Viterbi labels, and the current regime label is already one of its inputs.
- **The input regime is hindsight-decoded.** The "Current regime label Ẑₜ" is fed into XGBoost and is its top feature (importance 0.31; Table 8). Even if the HMM were refitted within each window, it comes from a Viterbi path, not a filtered P(Zₜ | r₁:ₜ). The paper never mentions filtered, smoothed or forward probabilities.
- **Training and forecasting see regimes differently.** The regime-specific models are trained on segments labelled with full-path Viterbi decoding. At forecast time the regime is inferred from data up to t only, and the paper never addresses this.
- **Label switching** is handled by re-sorting states by mean return after each fit.
- **Other gaps:** data-availability lags are not discussed, and nothing indicates whether preprocessing was fitted within each window.
- The paper has no look-ahead-bias discussion beyond the §3.1 sentence quoted above.

## 6. Benchmarks and metrics
- Benchmarks: NeuralProphet, ARIMAX and SARIMAX, each run without regimes on "lagged initial regressors".
- **There is no random-walk or no-change benchmark.**
- Metrics: MAE, RMSE and R² on the price level, and a Diebold–Mariano test.
- Economic test: a sign-based long/flat strategy against Buy & Hold, an SMA 20/100 crossover and baseline NeuralProphet.
- There are no VaR/ES backtests, no FZ/AL losses, no model confidence set and no density or interval scoring. The paper shows confidence bands but never evaluates them.

## 7. Main results

| Model, 1 Jan – 30 Jun 2025 | RMSE | MAE | R² |
|---|---|---|---|
| Regime-aware | 942.89 | 708.76 | 0.91 |
| NeuralProphet, no regimes | 2255.77 | 1599.98 | 0.82 |
| ARIMAX, no regimes | 2587.91 | 1601.96 | 0.61 |
| SARIMAX, no regimes | 2597.26 | 1594.29 | 0.64 |

- Monthly regime-aware MAE runs from 613 to 717. March is the weakest month for the baseline: NeuralProphet R² is 0.07 there, against 0.90 for the regime-aware model.
- Diebold–Mariano statistics against NeuralProphet, ARIMAX and SARIMAX: 3.21 (p = 0.001), 4.05 (p < 0.001) and 3.47 (p = 0.001).
- Ablation (Table 5): the chosen mapping gives MAE 736 / R² 0.93, against 1893/0.59, 1375/0.67 and 1274/0.71 for the alternatives. Only one row of the table is filled in.
- XGBoost picks the model matching the current regime 82% (bear), 76% (sideways) and 84% (bull) of the time (Table 9).
- Six-month backtest (Table 10):

| Strategy | Return | Max drawdown | Sharpe |
|---|---|---|---|
| Proposed regime-aware | 0.19 | 0.19 | 1.01 |
| Buy & Hold | 0.16 | 0.32 | 0.72 |
| SMA crossover 20/100 | 0.13 | 0.26 | 0.78 |
| Baseline NeuralProphet | 0.10 | 0.24 | 0.69 |

## 8. Overlap verdict: **LOW threat**
- **No overlap on the target.** They forecast price and return points, not VaR/ES, and they have no tail-risk loss functions or backtests.
- **No overlap on the contribution.** They have no look-ahead decomposition and no comparison of filtered vs smoothed regimes. They assert causality rather than testing it.
- **Shared ground:** Bitcoin, an HMM, and XGBoost on top of regimes. That is enough that a referee might cite it, so we should cite it and say how we differ.

**Red flags we can cite.** These are in the paper as written, but be careful how strongly we phrase any claim of actual leakage:
1. **Viterbi over 1:T.** Algorithm 1 decodes over the full sample, Ẑ₁:T = argmax p(Z₁:T | r₁:T), which contradicts the rolling-window causality claim in §3.1.
2. **The regime label is the top input to XGBoost** (importance 0.31), and the XGBoost target may itself be the regime label ("Label: zₜ").
3. **Regime-specific models are trained on Viterbi-segmented data,** with no filtered inference at forecast time.
4. **K was chosen partly on "out-of-sample forecasting performance".** That is the hyperparameter-selection-on-test-data channel in our taxonomy.
5. **Important settings are undisclosed:** W, refit frequency and validation window.
6. **No random-walk benchmark,** and point accuracy is judged by R² on price levels, which persistence alone pushes up.
7. **The error levels look too good.** This one is my inference, not something the paper reports. A regime-aware MAE of about 709 USD on a price near 85–108k is roughly a 0.7% daily absolute error. That is likely below a no-change forecast for BTC in H1 2025, since typical absolute daily moves are around 1.5–2%. The baselines (MAE about 1,600) are probably no better than a random walk. Results that implausible are a typical sign of look-ahead, and the gap is the size our "look-ahead premium" is meant to measure. We should check it against the actual 2025 data before stating it in print.

For our literature review, the papers that matter more on regime-switching VaR/ES for Bitcoin are Gao, Ye & Guo (2022, FRL, doi 10.1016/j.frl.2022.102826) and Trucíos & Taylor (2023, J. Forecasting, doi 10.1002/for.2929). Both are cited in this paper.