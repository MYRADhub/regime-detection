# Strand: ML / statistical-learning regime detection

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I found and checked 44 core entries plus 3 peripheral ones. I did not invent any citation. Bibliographic details for every entry were confirmed against at least one source page, Crossref or Semantic Scholar. Four items are only partly verified (metadata confirmed, findings not) and are marked as such. None of the papers you named is unverifiable. The IJCSAM paper turned out to be Staenly & Irsan 2026, entry 36. Some publisher pages (ScienceDirect, Springer, MDPI, SSRN, T&F) blocked fetching, so for those I worked from the Crossref or Semantic Scholar record or an open-access copy (arXiv, DTU Orbit, RePEc).

Status labels:
- **VERIFIED**: I read the abstract or full text.
- **VERIFIED (metadata)**: the citation is confirmed, but the summary comes from search snippets or secondary listings.

---

## A. Statistical jump models (JM)

**1. Bemporad, A., Breschi, V., Piga, D., & Boyd, S. P. (2018). Fitting jump models. *Automatica*, 96, 11–21. doi:10.1016/j.automatica.2018.06.022**
- URLs: arxiv.org/abs/1711.09220; Crossref; Semantic Scholar
- Summary: This is a general framework that alternates between two steps: fitting the parameters of K models by minimising a loss, and assigning each observation to the active model by minimising a discrete loss that includes a switching penalty. HMMs and piecewise affine models are special cases. It is a methods paper with no finance application.
- Relevance: This is the foundation of the JM literature. Estimation is batch and ex-post (dynamic programming over the whole sequence). No VaR/ES.
- VERIFIED

**2. Nystrup, P., Lindström, E., & Madsen, H. (2020). Learning hidden Markov models with persistent states by penalizing jumps. *Expert Systems with Applications*, 150, 113307. doi:10.1016/j.eswa.2020.113307**
- URLs: Crossref; Semantic Scholar (full abstract)
- Summary: The authors estimate HMMs by clustering temporal features with a jump penalty, and compare this with spectral clustering and maximum likelihood (ML) in simulations and on financial data. The jump estimator learns states and parameters faster, gives direct control over the transition rate, is less sensitive to initialisation, scales better in the number of states, and is robust to misspecified emission distributions. A simple trading strategy shows that better persistence estimates cut transaction costs a lot.
- Relevance: This is the main JM-vs-HMM reference. Estimation is in-sample/batch. No VaR/ES.
- VERIFIED

**3. Nystrup, P., Kolm, P. N., & Lindström, E. (2020). Greedy online classification of persistent market states using realized intraday volatility features. *Journal of Financial Data Science*, 2(3), 25–39. doi:10.3905/jfds.2020.2.3.025**
- URLs: orbit.dtu.dk publication page; Crossref
- Summary: An online JM classifier assigns each new observation to a state immediately, without re-parsing the past, using a fixed-cost jump penalty. In simulations it is often more accurate than the correctly specified ML estimator and more robust to misspecification. Its states are more persistent in and out of sample, and intraday realized-volatility features improve accuracy further. Applied to the S&P 500.
- Relevance: This is the key reference for real-time, no-lookahead JM regime assignment, which is exactly what our design needs. It does not evaluate VaR/ES.
- VERIFIED

**4. Nystrup, P., Kolm, P. N., & Lindström, E. (2021). Feature selection in jump models. *Expert Systems with Applications*, 184, 115558. doi:10.1016/j.eswa.2021.115558**
- URLs: Crossref; search results (DBLP, Fields Institute and NYU seminar abstracts)
- Summary: This is the sparse jump model. Coordinate descent alternates between feature weighting (lasso-type) and estimating the JM states and parameters, and it scales to many noisy features. Tested on simulations, financial returns, protein sequences and text, it outperformed the alternatives and was robust to noise.
- Relevance: The feature-selection machinery used by later Shu–Mulvey work. Batch, ex-post. No VaR/ES.
- VERIFIED (metadata). I did not open the publisher abstract; the summary comes from seminar abstracts.

**5. Aydınhan, A. O., Kolm, P. N., Mulvey, J. M., & Shu, Y. (2024). Identifying patterns in financial markets: extending the statistical jump model for regime identification. *Annals of Operations Research* (online 14 May 2024). doi:10.1007/s10479-024-06035-z**
- URLs: collaborate.princeton.edu publication page; Crossref; SSRN 4556048 (listed; fetch was blocked)
- Summary: The continuous jump model replaces discrete labels with probability vectors over regimes. A "mode loss" penalty pushes probabilities toward the vertices of the simplex. It beats traditional regime-switching models in simulations and on real data, especially when regimes are imbalanced and history is short.
- Relevance: Gives soft regime probabilities, which can be used for mixture-type VaR/ES like HMM filtered probabilities. Estimation is batch. No VaR/ES backtest.
- VERIFIED

**6. Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. *Journal of Asset Management*, 25(5), 493–507. doi:10.1057/s41260-024-00376-x (arXiv:2402.05272)**
- URLs: arxiv.org/abs/2402.05272; Crossref
- Summary: A two-state JM on return-derived features, with the jump penalty tuned by time-series cross-validation on strategy performance, drives a 0/1 equity-exposure rule. Out-of-sample on US, German and Japanese equity indices, 1990–2023, with transaction costs and trading delay. The JM strategy cuts volatility and maximum drawdown and raises the Sharpe ratio relative to both an HMM-guided strategy and buy-and-hold. The abstract gives no figures.
- Relevance: This is the closest JM paper to "downside risk". It is genuinely out-of-sample, with online inference and a fixed penalty. But risk is judged through portfolio volatility and maximum drawdown, not VaR/ES forecasts or backtests.
- VERIFIED

**7. Shu, Y., Yu, C., & Mulvey, J. M. (2024). Dynamic asset allocation with asset-specific regime forecasts. arXiv:2406.09578.**
- URLs: arxiv.org/abs/2406.09578
- Summary: A JM labels each asset's history as bull or bear. A gradient-boosted tree classifier then forecasts those labels from asset-specific and cross-asset macro features, and the forecasts feed mean-variance optimisation. 12 risky assets, 1991–2023. It beats minimum-variance, mean-variance and naive diversified portfolios.
- Relevance: A hybrid unsupervised + supervised approach (JM labels, then XGBoost-style forecasting), which is a template for "ML regimes" that are forecast rather than merely filtered. No VaR/ES.
- VERIFIED

**8. Shu, Y., & Mulvey, J. M. (2025). Dynamic factor allocation leveraging regime-switching signals. *Journal of Portfolio Management*, 51(3), 50–72. doi:10.3905/jpm.2024.1.649 (arXiv:2410.14841)**
- URLs: arxiv.org/abs/2410.14841; collaborate.princeton.edu publication page
- Summary: A sparse JM gives bull/bear regimes for each of six US style factors' active returns, which feed Black–Litterman. The information ratio vs the market rises from about 0.05 (equal-weight benchmark) to about 0.4; the IR vs equal-weight is about 0.4–0.5. Sharpe ratio and maximum drawdown also improve.
- Relevance: Out-of-sample allocation use of sparse JM. No VaR/ES.
- VERIFIED

**9. Cortese, F. P., Kolm, P. N., & Lindström, E. (2026). Generalized information criteria for high-dimensional sparse statistical jump models. *AStA Advances in Statistical Analysis*, 110(2), 289–317. doi:10.1007/s10182-026-00554-9**
- URLs: lup.lub.lu.se record 64f7f7da…
- Summary: Derives generalised information criteria (fit plus complexity) to choose sparse-JM hyperparameters, meaning the number of states, the jump penalty and the sparsity level. Simulations recover the correct hyperparameters with high probability. A three-state model best describes MSCI developed and emerging market indices. An earlier 2023 working-paper version applied the method to crypto and found four states.
- Relevance: Gives a principled, non-performance-based way to tune JM hyperparameters, which matters for a real-time design that avoids tuning on the test period. No VaR/ES.
- VERIFIED

## B. HMM variants: adaptive, hierarchical, Bayesian nonparametric, ML hybrids

**10. Nystrup, P., Madsen, H., & Lindström, E. (2017). Long memory of financial time series and hidden Markov models with time-varying parameters. *Journal of Forecasting*, 36(8), 989–1002. doi:10.1002/for.2447 (online 2016)**
- URLs: Crossref; orbit.dtu.dk (conference version page)
- Summary: Adaptive estimation with exponential forgetting lets HMM parameters drift over time. A two-state Gaussian HMM with time-varying parameters reproduces the long memory of squared returns and improves one-step density forecasts.
- Relevance: The adaptive-HMM benchmark. Estimation is recursive and filtered, so it is real-time. It evaluates density forecasts, not VaR/ES specifically.
- VERIFIED

**11. Nystrup, P., Madsen, H., & Lindström, E. (2018). Dynamic portfolio optimization across hidden market regimes. *Quantitative Finance*, 18(1), 83–95. doi:10.1080/14697688.2017.1342857**
- URLs: DTU Orbit accepted-version PDF (abstract read); Crossref
- Summary: Model predictive control uses mean and variance forecasts from a time-varying-parameter HMM that is updated with every new observation. With transaction costs and a one-day implementation delay, it beats a static decision rule and buy-and-hold on several major indices, with higher return and significantly lower risk. A trading penalty makes it more robust.
- Relevance: Real-time filtered HMM forecasts used for risk control. No VaR/ES backtest.
- VERIFIED

**12. Nystrup, P., Hansen, B. W., Madsen, H., & Lindström, E. (2016). Detecting change points in VIX and S&P 500: A new approach to dynamic asset allocation. *Journal of Asset Management*, 17(5), 361–374. doi:10.1057/jam.2016.12**
- URLs: Crossref; Semantic Scholar (abstract withheld by the publisher)
- Summary: Change-point detection on VIX and S&P 500 is used for dynamic allocation. I could not read the abstract.
- Relevance: An early change-point-detection application to allocation.
- VERIFIED (metadata only)

**13. Oelschläger, L., & Adam, T. (2023). Detecting bearish and bullish markets in financial time series using hierarchical hidden Markov models. *Statistical Modelling*, 23(2), 107–126. doi:10.1177/1471082X211034048 (arXiv:2007.14874)**
- URLs: Crossref; Semantic Scholar abstract
- Summary: A hierarchical HMM separates long-term bull/bear trends from short-term fluctuations, applied to the DAX and Deutsche Bank stock. Implemented in the R package fHMM (CRAN; JSS 2024).
- Relevance: Ex-post decoding. No VaR/ES.
- VERIFIED

**14. Tampouris, A., & Dritsaki, C. (2026). Adaptive hierarchical hidden Markov models for structural market change. *Journal of Risk and Financial Management*, 19(1), 15. doi:10.3390/jrfm19010015 (online Dec 2025)**
- URLs: Crossref; Semantic Scholar abstract
- Summary: In this AH-HMM, transition matrices depend on a latent meta-regime, approximated empirically by low- and high-uncertainty VIX environments. Weekly data on major equity indices plus macro-uncertainty indicators. It identifies the GFC, COVID and the 2022 tightening, has a higher in-sample likelihood, and gives competitive out-of-sample forecasts and VaR coverage vs standard and time-varying-transition HMMs.
- Relevance: One of the few HMM-variant papers with an out-of-sample VaR coverage evaluation. Weekly frequency, no ES.
- VERIFIED

**15. Fox, E. B., Sudderth, E. B., Jordan, M. I., & Willsky, A. S. (2011). A sticky HDP-HMM with application to speaker diarization. *Annals of Applied Statistics*, 5(2A), 1020–1056. doi:10.1214/10-AOAS395**
- URLs: Crossref (Project Euclid page came back empty); search results (Fox et al. IEEE SPM 2010 tutorial, NeurIPS 2008 SLDS paper with an IBOVESPA application)
- Summary: A Bayesian nonparametric HMM with a self-transition ("sticky") bias, which lets the data choose the number of states while avoiding rapid redundant switching. The companion SLDS work applies it to IBOVESPA volatility regimes.
- Relevance: The method reference for nonparametric regime counts. Inference is MCMC/smoothed. No VaR/ES.
- VERIFIED (metadata). Summary from search results.

**16. Dufays, A. (2016). Infinite-state Markov-switching for dynamic volatility. *Journal of Financial Econometrics*, 14(2), 418–460. doi:10.1093/jjfinec/nbv017**
- URLs: Semantic Scholar record; search results (CORE discussion paper abstract, author CV)
- Summary: GARCH and DCC models whose parameters switch under a sticky infinite HMM. Bayesian inference selects the number of regimes and whether the structure is Markov-switching or change-point.
- Relevance: This is where the sticky HDP-HMM meets volatility in finance. Volatility only. I could not confirm any VaR/ES content.
- VERIFIED (metadata). Summary from the working-paper abstract.

**17. Gupta, R., Kapoor, S., Gupta, H., & Natesan, S. (2025). A forest of opinions: A multi-model ensemble-HMM voting framework for market regime shift detection and trading. *Data Science in Finance and Economics*, 5(4), 466–501. doi:10.3934/DSFE.2025019**
- URLs: aimspress.com article page
- Summary: Bagging and boosting tree ensembles (XGBoost, BaggingClassifier) vote with an HMM to classify bull, neutral and bear regimes from macro and technical indicators. S&P 500 and Russell 3000 ETFs, two-fold walk-forward (train 2010–15, test 2015–20; train to 2020, test 2020–25).
- Relevance: The RF/XGBoost-plus-HMM regime-classification strand. Walk-forward. No VaR/ES.
- VERIFIED

**18. Pomorski, P., & Gorse, D. (2023). Improving portfolio performance using a novel method for predicting financial regimes. arXiv:2310.04536.**
- URLs: arxiv.org/abs/2310.04536
- Summary: Regime labels from KAMA plus a Markov-switching regression train a random forest to predict regimes ahead of time. Tested on equities, commodities and FX over a four-year test period, benchmarked against an HMM. For commodities, the cost-adjusted cumulative return was "over four times higher" than the index.
- Relevance: Supervised random-forest regime forecasting. Out-of-sample trading only.
- VERIFIED

**19. De Mel, W. A. R. (2026). Value at risk of stock market returns using a hidden Markov–LSTM hybrid model. *Sri Lankan Journal of Applied Statistics*, 27(1), 118–131. doi:10.4038/sljas.v27i1.8231**
- URLs: sljastats.sljol.info/articles/10.4038/sljas.v27i1.8231
- Summary: A Gaussian HMM regime sequence is fed into an LSTM that forecasts a realized-volatility proxy. Student-t residuals give 1% VaR and ES. MSFT daily data, train 2016–19, test 2020–22. Kupiec unconditional coverage is not rejected.
- Relevance: A direct ML-regime VaR/ES paper, but weak evidence: a single stock, only Kupiec, no ES backtest. The abstract does not say whether test-period regimes are filtered or smoothed.
- VERIFIED

**20. Verma, A. K., Putri, N. S., & Lesupi, N. P. (2026). Regime-based portfolio allocation using hidden Markov models and reinforcement learning. arXiv:2605.27848.**
- URLs: econpapers.repec.org/paper/arxpapers/2605.27848.htm
- Summary: A three-state Gaussian HMM (chosen by BIC) on SPY, TLT and GLD daily data, 2004–2025. Rule-based and reinforcement-learning rotation strategies are tested on a 30% out-of-sample window with a one-day lag. Both beat SPY, and the reinforcement-learning policy has the best risk-adjusted return and the smallest drawdowns.
- Relevance: Allocation and drawdown only. No VaR/ES.
- VERIFIED

**21. Boukardagha, A. (2026). Explainable regime aware investing. arXiv:2603.04441.**
- URLs: econpapers.repec.org/paper/arxpapers/2603.04441.htm
- Summary: A "causal Wasserstein HMM": rolling Gaussian HMM inference, predictive choice of model order, and regime identity tracked across refits by the 2-Wasserstein distance between components. Sharpe 2.18 vs 1.59 (equal-weight) and 1.18 (SPX); maximum drawdown −5.43% vs −14.62% (SPX).
- Relevance: Explicitly causal/real-time, and it addresses label switching across rolling refits, a practical problem we will face too. No VaR/ES.
- VERIFIED

## C. Clustering, signature, change-point and other unsupervised regime detection

**22. Horvath, B., Issa, Z., & Muguruza, A. (2024). Clustering market regimes using the Wasserstein distance. *Journal of Computational Finance*. doi:10.21314/JCF.2024.005 (arXiv:2110.11848; SSRN 3947905)**
- URLs: arxiv.org/abs/2110.11848; Crossref
- Summary: Wasserstein k-means clusters empirical return distributions over rolling windows in Wasserstein space, with no parametric assumptions. Judged by within- and between-cluster MMD scores, it "vastly outperforms" competing clustering methods on synthetic and real data.
- Relevance: The leading distributional clustering method. Evaluated by cluster quality, not risk forecasts; batch/ex-post. No VaR/ES.
- VERIFIED

**23. Issa, Z., & Horvath, B. (2023). Non-parametric online market regime detection and regime clustering for multidimensional and path-dependent data structures. arXiv:2306.15835.**
- URLs: arxiv.org/abs/2306.15835
- Summary: An online two-sample MMD test with rough-path signature kernels, tuned for small incoming batches, plus path-wise regime clustering. Tested on synthetic data, equity baskets and crypto; it "swiftly and accurately" flags past turmoil.
- Relevance: An explicitly online signature-based detector, usable in real time. No VaR/ES.
- VERIFIED

**24. Bilokon, P., Jacquier, A., & McIndoe, C. (2021). Market regime classification with signatures. arXiv:2107.00066.**
- URLs: arxiv.org/abs/2107.00066
- Summary: Data-driven regime clustering using path signatures, plus a metric linking regime separation to cluster tightness.
- Relevance: Signature-based regimes. No risk evaluation.
- VERIFIED

**25. Mc Greevy, J., Muguruza, A., Issa, Z., Salvi, C., Chan, J., & Zuric, Z. (2024). Detecting multivariate market regimes via clustering algorithms. SSRN 4758243. doi:10.2139/ssrn.4758243**
- URLs: Crossref; Semantic Scholar; search snippet of the related Imperial College MSc thesis
- Summary: According to the thesis snippet, multivariate non-parametric k-means regime detection comparing Wasserstein and MMD distances, with a two-step clustering method.
- Relevance: The multivariate extension of entry 22.
- VERIFIED (metadata only). I could not read the SSRN abstract.

**26. Botte, A., & Bao, D. (2021). A machine learning approach to regime modeling. Two Sigma Street View, 6 Oct 2021.**
- URLs: twosigma.com/articles/a-machine-learning-approach-to-regime-modeling
- Summary: A Gaussian mixture model on the 17 factors of the Two Sigma Factor Lens, 1971–2020, with the number of clusters chosen by cross-validated log-likelihood. Four conditions: Crisis, Steady State, Inflation, and "Walking on Ice". The authors say the model is not predictive, and the classification switches abruptly.
- Relevance: The industry reference for GMM regimes. In-sample. Tail risk is mentioned only through stress testing; no VaR/ES.
- VERIFIED

**27. Ung, D. (2025). Decoding market regimes: Machine-learning insights into US asset performance over the last 30 years. State Street Global Advisors, Insights, Feb 2025 (reprinted 2026).**
- URLs: ssga.com PDF (2025 path; text extracted)
- Summary: 23 features (17 return factors, following Two Sigma, plus 6 uncertainty measures such as CDS spreads, option skews and an economic-uncertainty index), modelled with a t-distributed mixture with GARCH. Four regimes over 30 years, with the assets that outperform in each.
- Relevance: Practitioner GMM/t-mixture regimes, contemporaneous and in-sample. No VaR/ES.
- VERIFIED

**28. Kritzman, M., Page, S., & Turkington, D. (2012). Regime shifts: Implications for dynamic strategies (corrected). *Financial Analysts Journal*, 68(3), 22–39. doi:10.2469/faj.v68.n3.3**
- URLs: ideas.repec.org/a/taf/ufajxx/v68y2012i3p22-39.html; Crossref
- Summary: Two-state Markov-switching models on Mahalanobis turbulence, inflation and growth series, each with a "normal" and an "event" regime. Out-of-sample backtests show dynamic allocation beats static allocation, especially for investors who want to avoid large losses.
- Relevance: The classic turbulence-regime paper with out-of-sample tests aimed at large losses. Not ML in the modern sense, and no VaR/ES backtest.
- VERIFIED

**29. Bucci, A., & Ciciretti, V. (2022). Market regime detection via realized covariances. *Economic Modelling*, 111, 105832. doi:10.1016/j.econmod.2022.105832 (arXiv:2104.03667)**
- URLs: arxiv.org/abs/2104.03667; Crossref
- Summary: Detects regimes from monthly realized covariance matrices, comparing agglomerative hierarchical clustering with nonlinear vector logistic smooth-transition autoregressive (VLSTAR) and regime-switching models. Validated on simulated data with known regimes and with a regime-filtered trading rule. VLSTAR is the best labeller, especially in stress periods.
- Relevance: One of the few papers that benchmarks unsupervised clustering directly against an econometric regime model, and the econometric model wins. The motivation is tail-risk hedging, but there is no VaR/ES.
- VERIFIED

**30. Akioyamen, P., Tang, Y. Z., & Hussien, H. (2020). A hybrid learning approach to detecting regime switches in financial markets. *Proc. ICAIF 2020*. doi:10.1145/3383455.3422521 (arXiv:2108.05801)**
- URLs: arxiv.org/abs/2108.05801
- Summary: PCA then k-means gives regimes, and classifiers then predict the regime from public economic data. Two trading strategies are built and evaluated. The abstract reports no numbers.
- Relevance: An early clustering-plus-classification design. Partly in-sample. No VaR/ES.
- VERIFIED

**31. Adams, R. P., & MacKay, D. J. C. (2007). Bayesian online changepoint detection. arXiv:0710.3742.**
- URLs: arxiv.org/abs/0710.3742
- Summary: Exact online inference of the posterior over run length (time since the last change point) by message passing, with a modular choice of observation model.
- Relevance: The standard real-time change-point method, a natural "online regime" competitor.
- VERIFIED

**32. Tsaknaki, I.-Y., Lillo, F., & Mazzarisi, P. (2025). Online learning of order flow and market impact with Bayesian change-point detection methods. *Quantitative Finance*, 25(2), 307–322. doi:10.1080/14697688.2024.2337300 (arXiv:2307.02375)**
- URLs: ideas.repec.org/a/taf/quantf/v25y2025i2p307-322.html
- Summary: A score-driven BOCPD (online change-point detection) variant with correlation and time-varying parameters within regimes. On NASDAQ order flow it beats i.i.d.-within-regime models out of sample and improves online impact forecasts.
- Relevance: A recent finance application of real-time BOCPD. Microstructure focus, no VaR/ES.
- VERIFIED

## D. Regime models applied to VaR/ES and tail risk, mostly 2016–2026

**33. Salhi, K., Deaconu, M., Lejay, A., Champagnat, N., & Navet, N. (2016). Regime switching model for financial data: Empirical risk analysis. *Physica A*, 461, 148–157. doi:10.1016/j.physa.2016.05.002**
- URLs: Crossref; Semantic Scholar; search results (Physica A preprint and HAL abstract; direct fetches failed)
- Summary: HMM classification into crisis and steady states, then extreme value theory (EVT) fitted within each regime. NYSE Euronext Paris stocks, 2001–2011. VaR backtests (the related thesis uses 56 assets) show better predictive performance.
- Relevance: An early HMM-regime + EVT VaR paper. I could not confirm whether the regimes are filtered.
- VERIFIED (metadata)

**34. Saidane, M. (2019). Forecasting portfolio-Value-at-Risk with mixed factorial hidden Markov models. *Croatian Operational Research Review*, 10(2). (Published 13 Dec 2019)**
- URLs: ojs.srce.hr/crorr/article/view/9278
- Summary: HMM plus mixture-of-factor-analyzers, estimated by EM, with Monte Carlo VaR for a Tunisian public-debt FX portfolio. Backtesting shows better VaR accuracy and no severe breaches in crises.
- Relevance: HMM-mixture VaR with backtests. Niche data.
- VERIFIED

**35. Saidane, M., & Ben Mohamed, E. (2026). Forecasting regime-dependent tail risk in digital asset portfolios with a mixture of hidden Markov factor analyzers. *Journal of Forecasting*. doi:10.1002/for.70159**
- URLs: Semantic Scholar abstract; Wiley listing in search results
- Summary: The mixture of hidden Markov factor analyzers combines an HMM, latent factors and regime-specific Gaussian mixtures, estimated by EM, and produces joint VaR–ES by Monte Carlo with soft regime assignment. In a large out-of-sample test on six cryptocurrencies it beats all competitors under the Patton–Ziegel–Chen joint VaR–ES loss and achieves strong Basel III compliance. The ES/VaR ratio varies over time and rises in turbulence.
- Relevance: The closest published analogue to our RQ: regime-mixture joint VaR–ES with an out-of-sample FZ-type loss. The regimes are HMM-family rather than clustering or JM, and the sample is crypto only.
- VERIFIED

**36. Staenly, S., & Irsan, M. Y. T. (2026). Regime-switching Value-at-Risk using hidden Markov models: A cross-market analysis of emerging and developed equity indices. *International Journal of Computing Science and Applied Mathematics (IJCSAM)*, 12(2), 50–62. doi:10.12962/j24775401.ijcsam.v12i2.9691**
- URLs: journal.its.ac.id/index.php/ijcsam/article/view/9691
- Summary: Gaussian HMMs with 2, 3 or 4 states (BIC picks 3 for JCI and Nikkei, 4 for S&P 500), daily 2008–2024. Regime-conditional VaR vs historical simulation (HS) and t-GARCH, with Kupiec and Christoffersen tests. In crises HS violations reach 11.88% (JCI) and 13.55% (S&P 500) at a nominal 5%. In normal periods HMM-VaR is the only method that passes both tests in all three markets, with violation rates of 4.90–5.61%.
- Relevance: A direct HMM-VaR comparison. Filtered vs smoothed is not stated, which is a lookahead red flag. No ES.
- VERIFIED

**37. Alswaidan, A., Jin, C., & Varner, J. D. (2026). Continuous hidden Markov models for equity returns: Heavy-tail emission families and regime-conditional Value-at-Risk. arXiv:2606.23492.**
- URLs: arxiv.org/abs/2606.23492; arxiv.org/html/2606.23492v1
- Summary: Continuous HMMs with Gaussian, Student-t, Laplace and GED emissions. Heavy-tailed marginals, not extra states, close most of the fit gap. SPY in-sample 2014–2024, out-of-sample Jan 2024–Apr 2026. At 5%, all CHMM rows pass Christoffersen conditional coverage (p_cc 0.49–0.68), with 26–35 breaches. At 1%, only CHMM-N with K = 3 avoids rejection by the Engle–Manganelli dynamic-quantile (DQ) test. Walk-forward conditional coverage passes on 19 of 24 rows. ES is reported only as a simulated band, with no ES backtest.
- Relevance: Uses one-step-ahead predictive (past-only) state probabilities, so the design is real-time. Strong on VaR methodology, weak on ES.
- VERIFIED

**38. Martín-Lunas, J. G., Lazcano, A., & Sandubete, J. E. (2026). From regime detection to decision rules: A data-driven macro-financial CVaR framework for European multi-asset portfolios. *Economies*, 14(7), 268. doi:10.3390/economies14070268**
- URLs: Crossref; Semantic Scholar full abstract (MDPI page returned 403)
- Summary: A four-state Gaussian HMM on eight weekly macro-financial features drives CVaR (ES) portfolio optimisation, Jan 2000–Apr 2026, strictly out-of-sample walk-forward. The naive regime-conditional CVaR allocation has about 226% annual turnover and underperforms the benchmark net of costs. Regime-constrained weight bands bring the net Sharpe to within 0.009 of the static benchmark at about 29% turnover. Their conclusion is that "the bottleneck is not regime detection" but the decision rule.
- Relevance: Out-of-sample HMM with CVaR as the optimisation objective, not as a forecast being evaluated. A useful cautionary result for our paper.
- VERIFIED

**39. Blake, A. C., Gandhi, N. A., & Jakkula, A. R. (2025). Improving S&P 500 volatility forecasting through regime-switching methods. arXiv:2510.03236.**
- URLs: arxiv.org/abs/2510.03236
- Summary: SPX 5-minute realized volatility, May 2014–May 2025. Compares soft Markov switching, spectral clustering with XGBoost, and a coefficient-based soft-regime method (HAR coefficients, Mood-test segmentation, Bayesian GMM). Recursive 5- and 10-day forecasts before, during and after COVID. The coefficient-clustering method beats everything else, including autoregressive baselines. The abstract gives no error figures.
- Relevance: ML regimes for volatility forecasting. No VaR/ES.
- VERIFIED

**40. Fang, X., & Ślepaczuk, R. (2026). Volatility forecasting and return prediction under market regimes: Evidence from high-frequency Chinese equity data. arXiv:2606.09478.**
- URLs: arxiv.org/abs/2606.09478
- Summary: CSI 300 high-frequency data, 2005–2023. Regime-augmented HARQ and Markov-switching GJR-GARCH filtering, then XGBoost on regime indicators, walk-forward. Regime-aware volatility forecasts generally beat HARQ in formal tests. Return predictability is weak and concentrated in low-volatility regimes.
- Relevance: Filtered regimes, out-of-sample volatility. The abstract does not mention VaR/ES.
- VERIFIED

**41. Kijkarncharoensin, A. (2025). Identifying risk regimes in a sectoral stock index through a multivariate hidden Markov framework. *Risks*, 13(7), 135. doi:10.3390/risks13070135**
- URLs: Semantic Scholar full abstract
- Summary: A multivariate Gaussian-mixture HMM on open-to-close, open-to-high and low-to-open returns of a Thai sector index. Three regimes (bull, sideways, bear), with ES, maximum drawdown and coefficient of variation reported by regime; the bear regime is riskiest.
- Relevance: In-sample, descriptive ES by regime, not forecasting.
- VERIFIED

**42. Alzahrani, A. A. (2025). Multi-agent regime-conditioned diffusion (MARCD) for CVaR-constrained portfolio decisions. arXiv:2510.10807.**
- URLs: arxiv.org/abs/2510.10807
- Summary: Gaussian HMM regimes condition a diffusion-model scenario generator with a tail-weighted objective, feeding a CVaR-constrained quadratic program. Multi-asset ETFs 2005–2025, walk-forward. Out-of-sample 2020–25 maximum drawdown is 9.3% vs 14.1% for BL (likely Black–Litterman), a 34% reduction.
- Relevance: CVaR used as a constraint. No VaR/ES forecast evaluation.
- VERIFIED

**43. Oprea, S., & Bâra, A. (2026). Regime-aware adaptive forecasting framework for Bitcoin prices using probabilistic generative models. *Computational Economics* (online 28 Mar 2026). doi:10.1007/s10614-026-11338-3**
- URLs: Crossref; Semantic Scholar record (Springer page redirected to login)
- Summary (from a search snippet only): a regime-switching CAViaR for joint VaR/ES on Bitcoin, with an XGBoost meta-learner choosing the model for each regime.
- Relevance: Possibly ML regimes plus VaR/ES, but unconfirmed.
- VERIFIED (metadata only); content unverified

**44. Morkūnaitė, I., Celov, D., & Leipus, R. (2024). Evaluation of Value-at-Risk (VaR) using the Gaussian mixture models. *Research in Statistics*, 2(1). doi:10.1080/27684520.2024.2346075**
- URLs: Crossref; Semantic Scholar (T&F page returned 403)
- Summary: GMM-based VaR. I could not read the abstract.
- Relevance: GMM as a return distribution for VaR, not necessarily as regimes.
- VERIFIED (metadata only)

**Peripheral, for context only:**
- **González Cortés et al. (2024), IEEE Access 12, 16999–17009, doi:10.1109/ACCESS.2024.3359413.** Autoencoder-enhanced clustering of financial series. It clusters series rather than time regimes. VERIFIED.
- **Zhang, Zhu & Zhu (2026), "ReSGA", arXiv:2606.04576.** A large autoencoder for joint VaR–ES, with no regimes. VERIFIED. Useful as a non-regime ML VaR/ES benchmark.
- **Ding, Kambouroudis & McMillan (2025), "Forecasting realised volatility using regime-switching models", *International Review of Economics & Finance* 101, 104171.** Markov-switching realized-volatility models, with VaR/ES as the economic evaluation according to a snippet. Metadata verified only.

**Not found:** I found no verifiable paper that uses spectral clustering specifically for return regimes, apart from its use inside entry 39 and as a comparator in entry 2. I also found no "Chen/Pagnoncelli" paper matching your note, so I left both out.

---

## Synthesis

**Most established ML regime methods:**
1. **Statistical jump models.** The Nystrup–Kolm–Lindström and Mulvey–Shu lines, entries 1–9. This is the most coherent and fastest-growing strand. Its persistence and robustness advantages over ML-estimated HMMs are well documented, and an online, no-lookahead variant exists (entry 3).
2. **Adaptive, hierarchical and nonparametric HMMs.** Entries 10–16. This is the mature statistical-learning baseline.
3. **Distributional and signature clustering.** Wasserstein k-means and signature MMD, entries 22–25. Methodologically strong, but judged on clustering quality, not forecasting.
4. **GMM / t-mixture.** Entries 26–27. Mostly practitioner work and in-sample.
5. **Tree ensembles on top of regime labels.** Entries 7, 17, 18. Increasingly used to turn ex-post labels into forecastable signals.

**Applied to VaR/ES:**
- Almost only HMM-family models: entries 14, 19, 33–37.
- Only entry 35 (crypto) evaluates joint VaR–ES out of sample with a strictly consistent scoring function.
- Entry 37 is the only one I found that explicitly uses past-only predictive state probabilities with a full VaR backtest battery (Kupiec, Christoffersen, DQ), and it does not backtest ES.
- Entries 19 and 36 do not say whether regimes are filtered or smoothed, which leaves possible look-ahead bias.
- JM, Wasserstein k-means, signature, GMM and BOCPD regimes have so far only been evaluated through portfolio outcomes (drawdown, volatility, Sharpe) or clustering quality, never through VaR/ES forecast accuracy.

**The gap:**
No study I found does all of the following:
- compares ML regime detectors (JM, continuous JM, Wasserstein k-means, GMM, BOCPD) against Markov-switching HMMs and regime-free GARCH/FHS benchmarks;
- forecasts VaR and ES;
- infers regimes strictly in real time, with no smoothed labels and no hyperparameters tuned on the test period;
- evaluates with modern ES backtests and FZ loss / Diebold–Mariano or model confidence set comparisons.

Two pieces of evidence argue against assuming ML regimes help:
- Entry 29 finds that an econometric regime model beats clustering at labelling regimes.
- Entry 38 finds that, net of costs, detecting the regime is not where the value lies.

So "do they improve VaR/ES?" is an open and well-posed question.