# Strand: Look-ahead bias, real-time estimation, novelty check

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I found and checked 51 entries, plus one flagged item at the end. None of the academic papers I could find measures the gap between smoothed/ex-post and filtered/real-time regime inference as a performance quantity for VaR/ES, or for regime-based forecasting in general. The only head-to-head numbers come from non-academic sources: two GitHub repos, a Substack post and a vendor blog, all from 2026. Section G has the full verdict.

On verification: "VERIFIED" means I opened the URL listed (IDEAS/RePEc, arXiv, publisher or repository page) and confirmed authors, venue and the abstract's content. Where a page gave no abstract, the summary is from my own knowledge and I say so. Several finer details (exact refit rules, footnotes) come from reading the arXiv HTML full text, and those are marked.

---

## A. Closest academic work (look-ahead / real-time regime inference in finance)

**1. Kole, E. & van Dijk, D. (2017). "How to Identify and Forecast Bull and Bear Markets?" *Journal of Applied Econometrics* 32(1), 120–139. doi:10.1002/jae.2511**
- URL: https://ideas.repec.org/a/wly/japmet/v32y2017i1p120-139.html
- Summary: Compares rule-based dating (Lunde-Timmermann and Pagan-Sossounov style) with Markov-switching models for bull/bear states on the S&P 500. It uses statistical measures and investor-utility measures built to handle the fact that the state is latent. Rule-based methods win at in-sample identification, while Markov-switching models win at out-of-sample forecasting, because volatility as well as the mean drives the forecasts. The differences are significant.
- Relevance: This is the closest formal academic statement that the best in-sample identifier is not the best real-time forecaster. It frames the gap as a choice of method, not as look-ahead bias, and it does not cover VaR/ES. Cite it as the nearest precedent.
- Status: VERIFIED.

**2. Shu, Y., Yu, C. & Mulvey, J.M. (2024). "Downside risk reduction using regime-switching signals: a statistical jump model approach." *Journal of Asset Management* 25(5), 493–507. doi:10.1057/s41260-024-00376-x (arXiv:2402.05272)**
- URLs: https://ideas.repec.org/a/pal/assmgt/v25y2024i5d10.1057_s41260-024-00376-x.html ; https://arxiv.org/html/2402.05272v3
- Summary: A jump-model (JM) regime strategy that cuts equity exposure in bad regimes, tested out of sample on US, German and Japanese indices from 1990 to 2023, with transaction costs and a 1-day delay. It beats both an HMM strategy and buy-and-hold on volatility, maximum drawdown and Sharpe ratio.
  - From the full text: the JM is refit every 6 months on a 3000-day window, and online labels come from re-optimising over the lookback window. The HMM is refit daily, uses the last Viterbi state, and is smoothed with a k-day rolling mean. The jump penalty is re-selected monthly on an 8-year validation window of online-inferred labels.
  - Footnote 14 explicitly recommends tuning on online labels, not in-sample labels, "given the noted discrepancy between in-sample fitting and online inference".
  - The only quantification is the COVID example: online detection lags the in-sample regime by about half a month at both onset and end. It also cites a 25-day median latency from Nystrup et al.
- Relevance: Acknowledges the in-sample-versus-online discrepancy and the hyperparameter-selection channel, but never measures the performance gap and never uses the term "look-ahead". It is a strong motivating citation.
- Status: VERIFIED.

**3. Shu, Y., Yu, C. & Mulvey, J.M. (2024). "Dynamic Asset Allocation with Asset-Specific Regime Forecasts." arXiv:2406.09578 (v2, Aug 2024)**
- URL: https://arxiv.org/html/2406.09578v2
- Summary: A 2-state JM is fit per asset on an 11-year window and refit every 6 months. Its labels are shifted forward one day and used as targets for an XGBoost forecaster. The jump penalty is tuned on a separate validation window "preventing any potential look-ahead bias."
  - Footnote 8 contrasts this with Uysal & Mulvey (2021) and Gu & Mulvey (2021), where "regime labels were derived all at once by applying the trend-filtering algorithm."
  - Results: 0/1 LargeCap maximum drawdown improves from −55% to −18%, and MinVar Sharpe rises from 0.70 to 1.12.
  - Remaining issue: labels inside each 11-year training window are still smoothed, because the JM decodes the whole sequence jointly. The paper does not address this.
- Relevance: The clearest published example of item 4, supervised ML trained on regime labels with the leakage problem named explicitly. Even this fix leaves in-window smoothing leakage, which our paper can measure.
- Status: VERIFIED (arXiv; journal version not checked).

**4. Gu, J. & Mulvey, J.M. (2021). "Factor Momentum and Regime-Switching Overlay Strategy." *Journal of Financial Data Science* 3(4), 101–129. doi:10.3905/jfds.2021.1.072**
- URL: https://collaborate.princeton.edu/en/publications/factor-momentum-and-regime-switching-overlay-strategy/
- Summary: Labels historical regimes with ℓ1 trend filtering, uses ML to forecast crash probability, and applies a regime-based risk-parity allocation plus a factor-momentum overlay. It reports large gains in risk-adjusted returns.
- Relevance: A concrete case of ex-post labels used as supervised targets. Its own coauthors later flagged that the labels were derived all at once (entry 3).
- Status: VERIFIED (abstract).

**5. Uysal, A.S. & Mulvey, J.M. (2021). "A Machine Learning Approach in Regime-Switching Risk Parity Portfolios." *Journal of Financial Data Science* 3(2), 87–108. doi:10.3905/jfds.2021.1.057**
- URL: https://collaborate.princeton.edu/en/publications/a-machine-learning-approach-in-regime-switching-risk-parity-portfolios/
- Summary: Supervised ML, including random forests, on a large macro dataset predicts recessions and stock-market contractions over 1973–2020, then drives a risk-parity overlay. It reports better risk-adjusted returns than plain risk parity.
- Relevance: The second case cited in entry 3 as using labels derived all at once.
- Status: VERIFIED (abstract). That the labels came from ex-post trend filtering rests on entry 3's statement; the abstract page does not describe label construction.

**6. Mulvey, J.M. & Liu, H. (2016). "Identifying economic regimes: Reducing downside risks for university endowments and foundations." *Journal of Portfolio Management* 43(1), 100–108.**
- URL: details came from a search snippet of https://collaborate.princeton.edu/en/publications/identifying-economic-regimes-reducing-downside-risks-for-universi/ ; I did not open the page.
- Summary: Trend-filtering regime identification feeding multi-regime simulation. Its downside-risk estimates are more accurate than those from static models.
- Relevance: The origin of the ex-post trend-filter labelling approach in this line of work, and a downside-risk application.
- Status: PARTIALLY VERIFIED (metadata from search result only).

**7. Nystrup, P., Kolm, P.N. & Lindström, E. (2020). "Greedy Online Classification of Persistent Market States Using Realized Intraday Volatility Features." *Journal of Financial Data Science* 2(3), 25–39. doi:10.3905/jfds.2020.2.3.025**
- URL: https://orbit.dtu.dk/en/publications/greedy-online-classification-of-persistent-market-states-using-re/
- Summary: An online classifier assigns each new observation to a state without re-parsing history, using a jump penalty. In simulations it is more accurate than correctly specified maximum likelihood in most settings, more robust to misspecification, and more persistent both in and out of sample.
- Relevance: Directly addresses real-time regime labelling and gives an online benchmark method. It does not measure the gain from look-ahead.
- Status: VERIFIED.

**8. Nystrup, P., Madsen, H. & Lindström, E. (2018). "Dynamic portfolio optimization across hidden market regimes." *Quantitative Finance* 18(1), 83–95. doi:10.1080/14697688.2017.1342857**
- URL: https://ideas.repec.org/a/taf/quantf/v18y2018i1p83-95.html
- Summary: Model predictive control on forecasts from an HMM with time-varying (adaptive) parameters. It beats static allocation and buy-and-hold after costs and a 1-day implementation delay.
- Relevance: The standard example of walk-forward, adaptively estimated regime allocation.
- Status: VERIFIED.

**9. Nystrup, P., Madsen, H. & Lindström, E. (2017). "Long Memory of Financial Time Series and Hidden Markov Models with Time-Varying Parameters." *Journal of Forecasting* 36(8), 989–1002. doi:10.1002/for.2447**
- URL: https://ideas.repec.org/a/wly/jforec/v36y2017i8p989-1002.html
- Summary: Adaptive (exponentially forgetting) estimation of a 2-state Gaussian HMM reproduces the long memory of squared returns and improves one-step density forecasts.
- Relevance: Adaptive real-time estimation that is directly relevant to density, and therefore VaR, forecasting.
- Status: VERIFIED (bibliographic; IDEAS has no abstract, so the summary comes from the search result and DTU/Lund listings).

**10. Nystrup, P., Hansen, B.W., Madsen, H. & Lindström, E. (2016). "Detecting change points in VIX and S&P 500: A new approach to dynamic asset allocation." *Journal of Asset Management* 17(5), 361–374. doi:10.1057/jam.2016.12**
- URL: https://ideas.repec.org/a/pal/assmgt/v17y2016i5d10.1057_jam.2016.12.html
- Summary: An online change-point-detection allocation that needs no fixed number of regimes. It improves Sharpe and drawdown against a static benchmark.
- Relevance: A real-time alternative that sidesteps choosing the number of regimes. Entry 2 cites a Nystrup et al. paper for the 25-day median detection latency; I did not confirm which paper that is.
- Status: VERIFIED.

**11. Nystrup, P., Lindström, E. & Madsen, H. (2020). "Learning hidden Markov models with persistent states by penalizing jumps." *Expert Systems with Applications* 150, 113307.**
- URL: venue, volume and article number seen only in a DBLP search snippet (https://dblp.uni-trier.de/pid/204/8860.html); I opened no page.
- Summary (from memory): Introduces the jump-model estimator, which clusters temporal features with a jump penalty and is more robust to initialisation than EM/HMM.
- Relevance: The method base for entries 2, 3, 7 and 12.
- Status: PARTIALLY VERIFIED. The author list is UNVERIFIED (from memory).

**12. Aydınhan, A.O., Kolm, P.N., Mulvey, J.M. & Shu, Y. (2024). "Identifying patterns in financial markets: extending the statistical jump model for regime identification." *Annals of Operations Research*. doi:10.1007/s10479-024-06035-z**
- URL: https://collaborate.princeton.edu/en/publications/identifying-patterns-in-financial-markets-extending-the-statistic/
- Summary: A continuous jump model that outputs regime-probability vectors, with a "mode loss" penalty. It beats traditional regime-switching models, especially when regimes are imbalanced or data is short.
- Relevance: A modern ML regime model that would be a candidate in our horse race.
- Status: VERIFIED (volume and pages not listed).

**13. Kritzman, M., Page, S. & Turkington, D. (2012). "Regime Shifts: Implications for Dynamic Strategies (corrected)." *Financial Analysts Journal* 68(3), 22–39. doi:10.2469/faj.v68.n3.3**
- URL: https://ideas.repec.org/a/taf/ufajxx/v68y2012i3p22-39.html
- Summary: Markov-switching "normal" and "event" regimes for turbulence, inflation and growth. Out-of-sample regime forecasts beat static exposures for tactical allocation and for stock/bond/cash allocation, especially for investors trying to avoid large losses.
- Relevance: A heavily cited practitioner regime paper. Whether its out-of-sample design re-estimates parameters in real time could not be checked (paywalled). The "corrected" in the title is also worth noting.
- Status: VERIFIED (abstract).

**14. Bulla, J., Mergner, S., Bulla, I., Sesboüé, A. & Chesneau, C. (2011). "Markov-switching asset allocation: Do profitable strategies exist?" *Journal of Asset Management* 12(5), 310–321. doi:10.1057/jam.2010.27**
- URL: https://ideas.repec.org/a/pal/assmgt/v12y2011i5d10.1057_jam.2010.27.html
- Summary: An HMM volatility-regime de-risking strategy on US, Japanese and German indices over about 40 years. Out of sample, net of costs, volatility falls about 41% on average and annualised excess returns are 18.5–201.6 bp.
- Relevance: Early out-of-sample regime evidence and a baseline magnitude to compare against.
- Status: VERIFIED. Correction: the authors are not "Nyberg/Lindström", as one might assume.

**15. Guidolin, M. & Timmermann, A. (2007). "Asset allocation under multivariate regime switching." *Journal of Economic Dynamics and Control* 31(11), 3503–3544.**
- URL: https://ideas.repec.org/a/eee/dyncon/v31y2007i11p3503-3544.html
- Summary: Four regimes (crash, slow growth, bull, recovery) capture joint stock and bond returns. Allocations shift as investors update their filtered state probabilities, and out-of-sample experiments confirm the economic value of regimes.
- Relevance: Canonical regime asset-allocation paper; its investors learn from filtered probabilities.
- Status: VERIFIED.

**16. Ang, A. & Bekaert, G. (2002). "International Asset Allocation With Regime Shifts." *Review of Financial Studies* 15(4), 1137–1187.**
- URL: https://ideas.repec.org/a/oup/rfinst/v15y2002i4p1137-1187.html
- Summary: Regime-switching correlations and volatilities that rise in bear markets. International diversification still pays, and ignoring regimes is costly once a risk-free asset is available.
- Relevance: Canonical citation. Its value-of-regimes evidence is largely in-sample, model-implied welfare.
- Status: VERIFIED.

**17. Ang, A. & Timmermann, A. (2012). "Regime Changes and Financial Markets." *Annual Review of Financial Economics* 4(1), 313–337 (NBER WP 17182).**
- URL: https://www.nber.org/papers/w17182
- Summary: Survey of regime-switching models in finance: fat tails, time-varying correlations, and implications for portfolio choice.
- Relevance: Background survey.
- Status: VERIFIED.

**18. Dacco, R. & Satchell, S. (1999). "Why do regime-switching models forecast so badly?" *Journal of Forecasting* 18(1), 1–16.**
- URL: https://iaorifors.com/paper/30956
- Summary: Shows analytically that regime-switching models can lose to a random walk on MSE even when they are the true model, because a small misclassification of the future regime wipes out the gain.
- Relevance: The theoretical reason why regime value shrinks once regime inference is real-time and therefore misclassified. It is a key motivating citation.
- Status: VERIFIED. The IAOR record wrongly lists the venue as International Journal of Forecasting; the Wiley DOI and other listings point to *Journal of Forecasting*.

**19. Kim, C.-J. (1994). "Dynamic linear models with Markov-switching." *Journal of Econometrics* 60(1–2), 1–22.**
- URL: https://ideas.repec.org/a/eee/econom/v60y1994i1-2p1-22.html
- Summary (from knowledge; IDEAS has no abstract): Extends Hamilton's filter to state-space models and introduces the Kim smoother, which gives full-sample smoothed regime probabilities.
- Relevance: The technical source of the smoothed probabilities whose use we call look-ahead.
- Status: VERIFIED (existence); summary from knowledge.

## B. Regime models for VaR/ES and density forecasting (the setting our premium applies to)

**20. Ardia, D., Bluteau, K., Boudt, K. & Catania, L. (2018). "Forecasting risk with Markov-switching GARCH models: A large-scale performance study." *International Journal of Forecasting* 34(4), 733–747. doi:10.1016/j.ijforecast.2018.05.004**
- URL: https://ideas.repec.org/a/eee/intfor/v34y2018i4p733-747.html
- Summary: Large-scale comparison of single-regime GARCH and MSGARCH models. MSGARCH gives more accurate VaR, ES and left-tail forecasts at daily, weekly and 10-day horizons, and accounting for parameter uncertainty helps further.
- Relevance: The main benchmark claim that regimes help VaR/ES. It uses rolling, predictive (filtered) estimation, so it is a "clean" reference point. It does not separate out any look-ahead component.
- Status: VERIFIED.

**21. Marcucci, J. (2005). "Forecasting Stock Market Volatility with Regime-Switching GARCH Models." *Studies in Nonlinear Dynamics & Econometrics* 9(4), 1–55. doi:10.2202/1558-3708.1145**
- URL: https://ideas.repec.org/a/bpj/sndecm/v9y2005i4n6.html
- Summary: Regime-switching GARCH beats standard GARCH at horizons under one week on statistical and VaR-based losses; asymmetric GARCH wins beyond one week.
- Relevance: Prior evidence on regime VaR, with horizon-dependent results.
- Status: VERIFIED.

**22. Guidolin, M. & Timmermann, A. (2006). "Term structure of risk under alternative econometric specifications." *Journal of Econometrics* 131(1–2), 285–308.**
- URL: https://ideas.repec.org/a/eee/econom/v131y2006i1-2p285-308.html
- Summary: VaR and ES term structures across regime-switching, GARCH and bootstrap models. Out of sample, the bootstrap is best at 5% VaR and regime switching at 1% VaR.
- Relevance: A direct out-of-sample regime VaR/ES evaluation.
- Status: VERIFIED.

**23. Billio, M. & Pelizzon, L. (2000). "Value-at-Risk: a multivariate switching regime approach." *Journal of Empirical Finance* 7(5), 531–554.**
- URL: https://ideas.repec.org/a/eee/empfin/v7y2000i5p531-554.html
- Summary (from secondary sources and memory; IDEAS has no abstract): Switching-volatility models produce better VaR than variance-covariance and GARCH(1,1) for single assets and portfolios.
- Relevance: An early regime-VaR claim.
- Status: VERIFIED (existence); summary from secondary sources.

**24. Gatumel, M. & Ielpo, F. (2014). "The Number of Regimes Across Asset Returns: Identification and Economic Value." *International Journal of Theoretical and Applied Finance* 17(06), 1–25 (HAL halshs-00658540).**
- URL: https://ideas.repec.org/p/hal/cesptp/halshs-00658540.html
- Summary: Rejects the two-regime view for many assets: between 2 and 5 regimes are needed, and using the right number improves density forecasts and portfolio returns out of sample.
- Relevance: Shows that the number of regimes matters economically. This is exactly why choosing it on the full sample is a source of look-ahead we should measure.
- Status: VERIFIED.

## C. Real-time turning-point dating and data vintages

**25. Chauvet, M. & Piger, J. (2008). "A Comparison of the Real-Time Performance of Business Cycle Dating Methods." *Journal of Business & Economic Statistics* 26, 42–49.**
- URL: https://ideas.repec.org/a/bes/jnlbes/v26y2008p42-49.html
- Summary: Builds an unrevised real-time dataset and tests a nonparametric rule and a Markov-switching dynamic-factor model. Both match NBER turning points with no false positives and call troughs faster than the NBER, the Markov-switching model most of all.
- Relevance: The methodological template for "simulated real-time" regime evaluation, here for dating rather than forecast value.
- Status: VERIFIED.

**26. Hamilton, J.D. (2011). "Calling recessions in real time." *International Journal of Forecasting* 27(4), 1006–1026.**
- URL: https://ideas.repec.org/a/eee/intfor/v27y2011i4p1006-1026.html
- Summary: Surveys automated turning-point methods. Real-time out-of-sample dating is harder than academics assume because of data revisions and instability. Distinguishes simulated real-time evaluation from actual real-time evaluation.
- Relevance: An authoritative statement that ex-post regime inference overstates real-time ability. Quotable.
- Status: VERIFIED.

**27. Chauvet, M. & Hamilton, J.D. (2006). "Dating Business Cycle Turning Points." In Milas, Rothman & van Dijk (eds.), *Nonlinear Time Series Analysis of Business Cycles*, Elsevier (NBER WP 11422, 2005).**
- URL: https://www.nber.org/papers/w11422
- Summary: Real-time recession-probability indexes built from GDP and from multiple indicators, using data as first released. Waiting one more quarter or month before calling a turning point reduces misclassification.
- Relevance: The detection-lag versus accuracy trade-off, which is the cost of not using smoothed inference.
- Status: VERIFIED (chapter pages not found).

**28. Croushore, D. & Stark, T. (2001). "A real-time data set for macroeconomists." *Journal of Econometrics* 105(1), 111–130.**
- URL: https://ideas.repec.org/a/eee/econom/v105y2001i1p111-130.html
- Summary: Quarterly vintages of US macro data. Re-tests published results on different vintages and shows that revisions matter for forecasting and policy.
- Relevance: The analogue for data revisions of our look-ahead decomposition. It is relevant if macro features enter the regime models.
- Status: VERIFIED.

**29. Croushore, D. (2011). "Frontiers of Real-Time Data Analysis." *Journal of Economic Literature* 49(1), 72–100. doi:10.1257/jel.49.1.72**
- URL: https://ideas.repec.org/a/aea/jeclit/v49y2011i1p72-100.html
- Summary: Surveys real-time data research: revisions, forecasting, monetary policy, and current analysis.
- Relevance: Survey citation for real-time evaluation.
- Status: VERIFIED.

## D. Bull/bear dating used as labels (item 4)

**30. Pagan, A.R. & Sossounov, K.A. (2003). "A simple framework for analysing bull and bear markets." *Journal of Applied Econometrics* 18(1), 23–46. doi:10.1002/jae.664**
- URL: https://ideas.repec.org/a/jae/japmet/v18y2003i1p23-46.html
- Summary: A rule-based (Bry-Boschan-type) algorithm for dating bull and bear markets. A pure random walk explains bull/bear features about as well as more complex models.
- Relevance: A standard label generator. Its turning-point and censoring rules need future prices to confirm a peak or trough, so a label at time t is not observable at time t. That is the source of leakage when these labels train classifiers. The mechanism is my inference from how the algorithm works; I did not read the paper's text on it.
- Status: VERIFIED.

**31. Lunde, A. & Timmermann, A. (2004). "Duration Dependence in Stock Prices: An Analysis of Bull and Bear Markets." *Journal of Business & Economic Statistics* 22, 253–273.**
- URL: https://ideas.repec.org/a/bes/jnlbes/v22y2004p253-273.html
- Summary: Hazard models for when bull and bear markets end, by duration and interest rates. Rejects a random walk; rising rates lower the bear-market hazard rate, so declines tend to continue.
- Relevance: The other standard ex-post bull/bear labelling rule, which uses a threshold that is only confirmed after the fact.
- Status: VERIFIED.

**32. Nyberg, H. (2013). "Predicting bear and bull stock markets with dynamic binary time series models." *Journal of Banking & Finance* 37(9), 3351–3363. doi:10.1016/j.jbankfin.2013.05.008**
- URL: https://ideas.repec.org/a/eee/jbfina/v37y2013i9p3351-3363.html
- Summary: Dynamic probit models predict bear and bull states, defined by ex-post dating, in and out of sample. They beat buy-and-hold in a market-timing exercise.
- Relevance: An example of supervised prediction of ex-post-dated regimes. A key question for our leakage audit is how it handles the lag before a label is known. I could not check this (paywalled).
- Status: VERIFIED (abstract).

## E. Data snooping, backtest overfitting and leakage

**33. Lo, A.W. & MacKinlay, A.C. (1990). "Data-Snooping Biases in Tests of Financial Asset Pricing Models." *Review of Financial Studies* 3(3), 431–467.**
- URL: https://ideas.repec.org/a/oup/rfinst/v3y1990i3p431-67.html
- Summary: Forming test portfolios on characteristics chosen by looking at the data can badly distort asset-pricing tests. Shown analytically, by simulation and empirically.
- Relevance: The foundational data-snooping citation.
- Status: VERIFIED.

**34. White, H. (2000). "A Reality Check for Data Snooping." *Econometrica* 68(5), 1097–1126. doi:10.1111/1468-0262.00152**
- URL: https://www.econometricsociety.org/publications/econometrica/2000/09/01/reality-check-data-snooping
- Summary: A bootstrap test of whether the best model from a specification search beats a benchmark, controlling for data snooping.
- Relevance: Needed for testing many regime specifications against a no-regime benchmark.
- Status: VERIFIED.

**35. Hansen, P.R. (2005). "A Test for Superior Predictive Ability." *Journal of Business & Economic Statistics* 23, 365–380.**
- URL: https://ideas.repec.org/a/bes/jnlbes/v23y2005p365-380.html
- Summary (from knowledge; IDEAS has no abstract): The SPA test, a studentised and recentred refinement of White's Reality Check that is less sensitive to poor alternative models.
- Relevance: A multiple-comparison test for VaR/ES loss across many regime models.
- Status: VERIFIED (existence); summary from knowledge.

**36. Sullivan, R., Timmermann, A. & White, H. (1999). "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap." *Journal of Finance* 54(5), 1647–1691.**
- URL: https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1647-1691.html
- Summary: Applies the Reality Check to the full universe of technical rules on about 100 years of DJIA data, and quantifies how much data snooping inflates apparent performance.
- Relevance: Methodological precedent for measuring how much of reported performance is bias, which is the same logic as a look-ahead premium.
- Status: VERIFIED.

**37. Pesaran, M.H. & Timmermann, A. (1995). "Predictability of Stock Returns: Robustness and Economic Significance." *Journal of Finance* 50(4), 1201–1228.**
- URL: https://ideas.repec.org/a/bla/jfinan/v50y1995i4p1201-28.html
- Summary: Asks whether investors could have exploited predictability in real time. Predictive power varies over time and with volatility: weak in the 1960s, exploitable in the 1970s.
- Relevance: The classic "real-time recursive model selection" design (from my knowledge of the paper; the abstract does not describe it). Analogous to selecting the regime count and hyperparameters in real time.
- Status: VERIFIED.

**38. Cooper, M. & Gulen, H. (2006). "Is Time-Series-Based Predictability Evident in Real Time?" *Journal of Business* 79(3), 1263–1292. doi:10.1086/500676**
- URL: https://ideas.repec.org/a/ucp/jnlbus/v79y2006i3p1263-1292.html
- Summary: Fixing predictors, assets and in-sample periods in advance distorts the size of out-of-sample tests. Results are very sensitive to small specification changes, and much of the published out-of-sample evidence is consistent with data snooping.
- Relevance: Direct precedent that "out-of-sample" designs with choices made on the full sample are not real-time. This is our hyperparameter and regime-count channel.
- Status: VERIFIED.

**39. Bailey, D.H., Borwein, J.M., López de Prado, M. & Zhu, Q.J. (2017). "The probability of backtest overfitting." *Journal of Computational Finance* 20(4), 39–69. doi:10.21314/JCF.2016.322**
- URL: https://www.risk.net/journal-of-computational-finance/2471206/the-probability-of-backtest-overfitting
- Summary: Combinatorially symmetric cross-validation (CSCV) estimates the probability of backtest overfitting (PBO) from a matrix of backtest results without needing a model.
- Relevance: Can be applied to the grid of regime specifications.
- Status: VERIFIED.

**40. Bailey, D.H. & López de Prado, M. (2014). "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality." *Journal of Portfolio Management* 40(5), 94–107. doi:10.3905/jpm.2014.40.5.094**
- URL: https://papers.ssrn.com/abstract=2460551 (returned 403 when opened; details from search snippets)
- Summary: Adjusts Sharpe ratios for multiple testing and non-normal returns.
- Relevance: Multiple-testing correction for regime strategies.
- Status: PARTIALLY VERIFIED (search metadata only).

**41. Harvey, C.R., Liu, Y. & Zhu, H. (2016). "...and the Cross-Section of Expected Returns." *Review of Financial Studies* 29(1), 5–68. doi:10.1093/rfs/hhv059**
- URLs: https://sfs.org/?p=2432 ; https://academic.oup.com/rfs/article/29/1/5/1843824
- Summary: A multiple-testing framework for factor discovery. Recommends t > 3.0 for new factors.
- Relevance: Multiple-testing citation.
- Status: VERIFIED (journal, volume, issue and DOI). The page range 5–68 is from search; one CV lists 5–72.

**42. Arnott, R., Harvey, C.R. & Markowitz, H. (2019). "A Backtesting Protocol in the Era of Machine Learning." *Journal of Financial Data Science* 1(1), 64–74. doi:10.3905/jfds.2019.1.064**
- URL: https://scholars.duke.edu/publication/1518184
- Summary: A research protocol to curb backtest overfitting in ML-driven finance, with emphasis on the limited data available.
- Relevance: The protocol framing for our real-time pipeline.
- Status: VERIFIED (abstract content from SSRN and search snippets).

**43. López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. ISBN 978-1-119-48208-6.**
- URL: https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086
- Summary: Chapter 7 covers purged k-fold cross-validation and embargo, which remove training observations whose label windows overlap the test set. Later chapters cover combinatorial purged CV and backtest overfitting.
- Relevance: Purging and embargo are exactly the remedy when regime labels span forward windows.
- Status: VERIFIED (book). The chapter contents come from secondary sources.

**44. Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. (2012). "Leakage in data mining: Formulation, detection, and avoidance." *ACM Transactions on Knowledge Discovery from Data* 6(4), Article 15. doi:10.1145/2382577.2382579**
- URL: https://cris.iucc.ac.il/en/publications/leakage-in-data-mining-formulation-detection-and-avoidance-2/
- Summary: Formally defines leakage as target information that should not legitimately be available. Proposes a "learn-predict separation" plus detection methods. The KDD 2011 version had three authors.
- Relevance: Formal definition for our label-leakage channel.
- Status: VERIFIED.

**45. Kapoor, S. & Narayanan, A. (2023). "Leakage and the reproducibility crisis in machine-learning-based science." *Patterns* 4(9), 100804. doi:10.1016/j.patter.2023.100804**
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856
- Summary: Finds leakage in 17 fields affecting 294 papers, and gives an 8-type taxonomy. Two types map to our channels: L1.2, preprocessing on train and test together (full-sample standardisation), and L3.1, temporal leakage. In a civil-war prediction case study, the ML advantage over logistic regression disappears once leakage is fixed.
- Relevance: The best general citation for full-sample standardisation and temporal leakage. Its case study (an advantage that vanishes after correction) mirrors our hypothesis.
- Status: VERIFIED.

**46. Glasserman, P. & Lin, C. (2023). "Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis." arXiv:2309.17322.**
- URL: https://arxiv.org/abs/2309.17322
- Summary: Measures look-ahead bias, plus a "distraction effect", in LLM sentiment strategies by comparing anonymised and original headlines in and out of the training window. Distraction matters more than look-ahead in-sample.
- Relevance: A close methodological analogue: a paper whose main contribution is measuring look-ahead bias in a finance ML pipeline, with in-sample and out-of-sample contrasts. Not about regimes.
- Status: VERIFIED (arXiv; no journal reference shown).

## F. Non-academic precedents that already show the smoothed-vs-filtered gap (important for novelty)

**47. dmitridefreitas-dev, "regime-detection" (GitHub repository, 2026)**
- URL: https://github.com/dmitridefreitas-dev/regime-detection
- Summary: A "lookahead ladder" on SPY (fit 1993–2026, evaluation 2003–2026) with a 2-state Gaussian HMM:

  | Variant | Sharpe |
  |---|---|
  | Buy-and-hold | 0.67 |
  | Causal (filtered probabilities, annual expanding refit, 1-bar lag, 2 bp costs) | 0.78 |
  | Parameters fit on full sample, probabilities causal | 0.77 |
  | Smoothed probabilities | 1.74 |

- Relevance: Essentially a single-asset, single-strategy toy version of our decomposition. The full-sample-parameter channel barely matters; the smoothing channel more than doubles the Sharpe. Our paper should cite it or at least be aware of it, and generalise it: many assets, VaR/ES, ML regimes, more leakage channels, and formal tests.
- Status: VERIFIED (non-peer-reviewed).

**48. Ben-Graham-Wharton-Burry, "hmm-regime-detection" (GitHub repository)**
- URL: https://github.com/Ben-Graham-Wharton-Burry/hmm-regime-detection
- Summary: 3-state HMM on the OMX Copenhagen index, 2013–2024, with parameters frozen on 2013–2018. Over 2019–2024:

  | Variant | Sharpe | Max drawdown |
  |---|---|---|
  | Buy-and-hold | 0.74 | −27.4% |
  | Filtered, lagged, net of costs | 0.84 | −28.0% |
  | Smoothed | 1.39 | −15.2% |

- Relevance: A second informal measurement of the gap. It includes the drawdown (downside) dimension.
- Status: VERIFIED (non-peer-reviewed).

**49. "Halley" (halleytech Substack), "Regime switching and hidden Markov models: when the model itself changes" (21 Sep 2026)**
- URL: https://halleytech.substack.com/p/regime-switching-hidden-markov-math-for-quants
- Summary: Simulation of 2,000 ten-year paths from a stated 2-state Markov-switching model. Smoothed Sharpe is 0.689, filtered 0.539, and an oracle that knows the true regime gets 0.674. So smoothed beats the oracle, which shows that smoothing leaks future returns, not just regime identity.
- Relevance: The "beats the oracle" result is a useful diagnostic idea to borrow, with attribution.
- Status: VERIFIED (non-peer-reviewed; simulated).

**50. Fengler, A., Fonnesbeck, C. & Muia, F., "Bayesian Regime-Switching for Equity Returns" (PyMC Labs blog, Apr 2026)**
- URL: https://www.pymc-labs.com/blog-posts/bayesian-hmm-market-regime-detection-pymc
- Summary: States explicitly that smoothed probabilities "should not be used directly for back-testing" because they embed look-ahead bias, and uses filtered P(bear) at t−1 for allocation. Synthetic data; no smoothed-vs-filtered performance comparison.
- Relevance: Practitioner warning.
- Status: VERIFIED.

**51. Jalšovský, J. (Quantpedia), "Does More History Help? A Market-Regime HMM and the Trouble with Out-of-Sample Evaluation" (14 Oct 2026)**
- URL: https://quantpedia.com/does-more-history-help-a-market-regime-hmm-and-the-trouble-with-out-of-sample-evaluation/
- Summary: An HMM on Fama-French and FRED data that varies the training start date. It insists evaluation must use filtered estimates. Its timing edge over a static twin is slightly negative, and a permutation test fails to reject.
- Relevance: Very recent practitioner evidence that honest regime timing adds little.
- Status: VERIFIED. Its tables are images and could not be read, so no numbers are given here.

**Flagged:** Farzulla, M. & Maksakov, A. (2026), "ASRI: An Aggregated Systemic Risk Index for Cryptocurrency Markets", arXiv:2602.03874. A search snippet says it characterises regimes with smoothed probabilities and recommends filtered probabilities for real-time deployment. The abstract page I opened does not show that statement. The first author's name may be yours, so check whether this is your own paper before citing it as outside support.

---

## G. Novelty verdict on the look-ahead premium angle

**For VaR/ES specifically: not done.**
- I found no academic paper that measures how much of the benefit of regime models for VaR/ES comes from smoothed labels, full-sample hyperparameter or regime-count selection, full-sample standardisation, or label leakage.
- The regime-VaR literature (Ardia et al. 2018; Marcucci 2005; Guidolin & Timmermann 2006; Billio & Pelizzon 2000) reports out-of-sample gains. Where checkable, it uses predictive or filtered inference, but it never contrasts that with ex-post variants or separates out a look-ahead component.
- A search for the phrase "look-ahead premium" found nothing in finance.

**For regime-based forecasting or allocation generally: partially anticipated, but only informally or for one channel at a time.**
- Closest academic work:
  - Kole & van Dijk (2017): in-sample identification and out-of-sample forecasting favour different methods.
  - Shu, Yu & Mulvey (2024, JAM): acknowledges the gap between in-sample and online labels, tunes on online labels, and reports roughly half a month of detection latency.
  - Shu, Yu & Mulvey (2024, arXiv:2406.09578): explicitly flags that earlier work (Gu & Mulvey 2021; Uysal & Mulvey 2021) built ex-post trend-filter labels all at once.
  - Cooper & Gulen (2006): "out-of-sample" designs with choices fixed on the full sample are not real-time, though for return predictability rather than regimes.
  - Chauvet & Piger (2008) and Hamilton (2011): real-time versus ex-post turning-point dating, about dating accuracy rather than forecast or risk value.
- None of these runs a controlled, multi-channel decomposition.
- The only explicit smoothed-versus-filtered performance numbers are the 2026 GitHub "lookahead ladder" (Sharpe 1.74 vs 0.78 on SPY; full-sample parameter fitting changes almost nothing) and the Danish HMM repo (1.39 vs 0.84). Both are single-asset, return or Sharpe based, unpublished, and cover only the HMM smoothing and parameter channels. A referee may know them, so I suggest acknowledging them as anecdotal precedent.

**Conclusion:** The lead contribution looks novel as an academic contribution, provided it is framed as a formal, multi-asset, multi-model decomposition of the look-ahead premium in VaR/ES with proper backtests and multiple-testing control. It should be a decomposition into separate channels: smoothing, hyperparameter and regime-count selection, standardisation, and label leakage. A bare "smoothed vs filtered" comparison would not be novel, given the practitioner write-ups above. Dacco & Satchell (1999) gives the theory for why the premium should be large, since small regime misclassification erases the forecast gain. Kapoor & Narayanan (2023) gives an outside precedent where an ML advantage disappears once leakage is fixed.

**Remaining gaps:** Google Scholar was not queried directly, and SSRN pages returned 403. The SSRN-only literature could therefore still hide a recent working paper. One targeted SSRN title search before submission would be prudent.