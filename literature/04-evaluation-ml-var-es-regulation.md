# Strand: Evaluation methodology, ML VaR/ES, regulation

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I verified 49 entries: 25 in A, 19 in B, 5 in C. Bibliographic details were checked against Crossref records, arXiv abstract pages, IDEAS/RePEc, publisher PDFs, BIS pages and the Federal Reserve's FEDS page. Where the abstract was elided or paywalled, the summary comes from my own knowledge of the paper and is labelled "summary from memory". No entry is a fabricated reference.

Details that differ from your brief:
- **Omega "Learning about tail risk"** is vol. 133 (2025), not 2024.
- **Christensen, Siggaard & Veliyev** is JFEc 21(5), 2023 (online 2022).
- **Bayer & Dimitriadis** is JFEc 20(3), 2022 (online 2020).
- **Kılıç (FEDS 2025-061)** forecasts realized volatility, not VaR. It is still highly relevant because its regime-switching HAR models win.
- **"Gradient boosting quantile VaR"**: I found no standalone journal paper. The JRFM 2026 paper (B11) covers it directly, and I added Buse, Görgen & Schienle (IJF 2025) on generalized random forests as the nearest tree-based VaR study.

---

## A) Evaluation methodology

**A1. Kupiec, P. (1995).** "Techniques for Verifying the Accuracy of Risk Measurement Models." *Journal of Derivatives* 3(2), 73–84. doi:10.3905/jod.1995.407942
- URL: https://api.crossref.org/works?query.bibliographic=Kupiec... (record for doi:10.3905/jod.1995.407942); Semantic Scholar record
- Summary: Proposes the proportion-of-failures (POF) likelihood-ratio test of unconditional coverage: is the hit rate equal to the nominal alpha? It shows the test has low power in samples of about 250 days at the 99% level.
- Relevance: the baseline unconditional coverage test for every model and regime variant. Its low power at 1% argues for long out-of-sample windows.
- Status: VERIFIED (metadata); summary from memory, abstract elided.

**A2. Christoffersen, P. (1998).** "Evaluating Interval Forecasts." *International Economic Review* 39(4), 841–862. doi:10.2307/2527341
- URL: Crossref record
- Summary: Decomposes interval or VaR evaluation into unconditional coverage, independence (first-order Markov), and a joint conditional-coverage LR test (LRcc = LRuc + LRind).
- Relevance: tests whether regime-aware models reduce the clustering of violations, which is the core way regime misspecification shows up.
- Status: VERIFIED (metadata); summary from memory.

**A3. Christoffersen, P. & Pelletier, D. (2004).** "Backtesting Value-at-Risk: A Duration-Based Approach." *Journal of Financial Econometrics* 2(1), 84–108. doi:10.1093/jjfinec/nbh004
- URL: Crossref record
- Summary: Tests the memoryless (geometric/exponential) property of the durations between VaR violations. It has better power than Markov independence tests against higher-order dependence.
- Relevance: useful secondary independence test, because regime shifts create bursts of violations that a first-order Markov test can miss.
- Status: VERIFIED (metadata); summary from memory.

**A4. Engle, R.F. & Manganelli, S. (2004).** "CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles." *Journal of Business & Economic Statistics* 22(4), 367–381. doi:10.1198/073500104000000370
- URL: Crossref record (NBER w7341 version also listed)
- Summary: Introduces CAViaR models that estimate quantiles directly by regression quantiles. It also introduces the Dynamic Quantile (DQ) test, which regresses demeaned hits on lagged hits, the VaR forecast and other information-set variables.
- Relevance: DQ is the main conditional backtest. Regime probabilities and labels can go in as instruments to test whether violations are predictable from the regime state. CAViaR is also a key econometric benchmark.
- Status: VERIFIED (metadata); summary from memory.

**A5. Berkowitz, J. (2001).** "Testing Density Forecasts, With Applications to Risk Management." *JBES* 19(4), 465–474. doi:10.1198/07350010152596718
- URL: Crossref record
- Summary: Transforms PIT values to normality and applies LR tests, including a censored "tail-only" version focused on the region beyond the VaR level. It has good power in samples as small as about 100.
- Relevance: applies when the regime models produce full predictive densities (for example mixture or MDN models). The censored tail LR test targets downside calibration.
- Status: VERIFIED (metadata); summary from memory.

**A6. Diebold, F.X., Gunther, T.A. & Tay, A.S. (1998).** "Evaluating Density Forecasts with Applications to Financial Risk Management." *IER* 39(4), 863–883. doi:10.2307/2527342
- URL: Crossref record
- Summary: Establishes PIT-based evaluation of density forecasts: if the forecast is correct, the PITs are iid U(0,1).
- Relevance: diagnostic for density-producing regime models (PIT histograms by regime).
- Status: VERIFIED (metadata); summary from memory.

**A7. Acerbi, C. & Székely, B. (2014).** "Back-testing Expected Shortfall." *Risk*, December 2014.
- URLs: https://www.msci.com/documents/10199/22aa9922-f874-4060-b77a-0f0e267a489b (MSCI PDF, text extracted); https://www.risk.net/risk-magazine/technical-paper/2381658/back-testing-expected-shortfall (located via search, not opened)
- Summary: Three model-independent, non-parametric ES backtests (Z1, Z2, Z3), tested at ES 2.5% against the Basel VaR 1% test. Z2 is most powerful against volatility misspecification, and Z1/Z3 against tail-index misspecification. The VaR exceptions test is "generally significantly less powerful." Z2's critical values are stable enough for a traffic light with fixed thresholds of −0.7 and −1.8.
- Relevance: a standard ES backtest that requires the predictive distribution, or at least the tail, to be stored. Z2 maps naturally onto a Basel-style ES traffic light.
- Status: VERIFIED (PDF text).

**A8. Costanzino, N. & Curran, M. (2015).** "Backtesting General Spectral Risk Measures with Application to Expected Shortfall." *Journal of Risk Model Validation* 9(1), 21–31. doi:10.21314/jrmv.2015.131
- URL: Crossref record (SSRN 2514403 version also listed)
- Summary: Builds a coverage-type test for spectral risk measures, ES included, by integrating VaR violation indicators across levels. It gives an asymptotically normal "failure rate" test for ES.
- Relevance: a simple Z-test for ES calibration that needs only the PITs or the tail, and complements A7.
- Status: VERIFIED (metadata); summary from memory.

**A9. Du, Z. & Escanciano, J.C. (2017).** "Backtesting Expected Shortfall: Accounting for Tail Risk." *Management Science* 63(4), 940–958. doi:10.1287/mnsc.2015.2342
- URLs: Crossref record; https://caepr.indiana.edu/RePEc/inu/caeprp/caepr2015-001.pdf (abstract extracted)
- Summary: Defines "cumulative violations" (integrating violations over the tail below alpha) and builds unconditional (U) and conditional, Box-Pierce-type (C) ES backtests, the natural analogues of the Kupiec and Christoffersen tests. It accounts for estimation risk. In the empirical application VaR is "unresponsive to extreme events" during the crisis, while ES describes the risk more accurately.
- Relevance: the conditional ES backtest that pairs most naturally with DQ for VaR. Use it to test serial dependence of ES failures across regime transitions.
- Status: VERIFIED.

**A10. Kratz, M., Lok, Y.H. & McNeil, A.J. (2018).** "Multinomial VaR Backtests: A Simple Implicit Approach to Backtesting Expected Shortfall." *Journal of Banking & Finance* 88, 393–407. doi:10.1016/j.jbankfin.2018.01.002
- URL: https://ideas.repec.org/a/eee/jbfina/v88y2018icp393-407.html
- Summary: Backtests ES implicitly through a multinomial test of VaR exceptions at several levels. At least four VaR levels are needed to beat single- and two-level binomial tests in power. It proposes a traffic-light approval system and illustrates it with data spanning 2008.
- Relevance: a cheap, regulator-friendly ES backtest that needs only a few quantile forecasts. Ideal for quantile-only ML models such as QRF or QRNN.
- Status: VERIFIED.

**A11. Gneiting, T. (2011).** "Making and Evaluating Point Forecasts." *JASA* 106(494), 746–762. doi:10.1198/jasa.2011.r10138
- URLs: Crossref record; https://arxiv.org/abs/0912.0902
- Summary: Forecasts must be judged with a scoring function consistent for the target functional. Quantiles and expectiles are elicitable, but "conditional value-at-risk", that is ES, is not.
- Relevance: justifies the tick loss for VaR and the need for a joint VaR–ES loss for ES rankings. It also rules out ad hoc ES losses such as the MSE of ES.
- Status: VERIFIED.

**A12. Fissler, T. & Ziegel, J.F. (2016).** "Higher Order Elicitability and Osband's Principle." *Annals of Statistics* 44(4), 1680–1707. doi:10.1214/16-aos1439
- URLs: Crossref record; https://arxiv.org/abs/1503.08123
- Summary: Characterizes strictly consistent scoring functions for vector-valued functionals. It shows that (VaR, ES) is jointly elicitable under mild conditions, which gives the FZ class of losses.
- Relevance: the theoretical basis for every joint VaR/ES loss used in the comparative tests.
- Status: VERIFIED.

**A13. Fissler, T., Ziegel, J.F. & Gneiting, T. (2016).** "Expected Shortfall is Jointly Elicitable with Value at Risk – Implications for Backtesting." *Risk*, January 2016, 58–61.
- URL: https://arxiv.org/abs/1507.00244
- Summary: A practitioner-facing note proposing Diebold–Mariano comparative backtests for ES based on joint VaR–ES scoring functions.
- Relevance: the direct template for DM-type pairwise tests of regime models against benchmarks.
- Status: VERIFIED.

**A14. Nolde, N. & Ziegel, J.F. (2017).** "Elicitability and Backtesting: Perspectives for Banking Regulation." *Annals of Applied Statistics* 11(4), 1833–1874. doi:10.1214/17-aoas1041
- URLs: Crossref record; https://arxiv.org/abs/1608.05498
- Summary: Distinguishes traditional backtests (H0: the forecast is correct) from comparative backtests (H0: the internal model is at least as good as a standard model). It proposes a three-zone comparative traffic light and covers VaR, ES and expectiles.
- Relevance: frames the RQ as a comparative backtest. The null should be "the regime model is no better than the benchmark", not just "the regime model passes coverage".
- Status: VERIFIED.

**A15. Patton, A.J., Ziegel, J.F. & Chen, R. (2019).** "Dynamic Semiparametric Models for Expected Shortfall (and Value-at-Risk)." *Journal of Econometrics* 211(2), 388–413. doi:10.1016/j.jeconom.2018.10.008
- URLs: Crossref record; https://arxiv.org/abs/1707.05108
- Summary: Introduces the FZ0 loss (the zero-homogeneous FZ member) and GAS-driven semiparametric ES/VaR models estimated by M-estimation. On four equity indices the new models outperform GARCH and rolling-window forecasts.
- Relevance: FZ0 is the recommended primary loss for joint VaR/ES ranking, and the FZ-GAS models are strong econometric benchmarks.
- Status: VERIFIED. The arXiv abstract does not name "FZ0"; that detail is from my knowledge of the paper.

**A16. Dimitriadis, T. & Bayer, S. (2019).** "A Joint Quantile and Expected Shortfall Regression Framework." *Electronic Journal of Statistics* 13(1), 1823–1871. doi:10.1214/19-ejs1560
- URL: Crossref record (also lists the CRAN `esreg` package, doi:10.32614/cran.package.esreg)
- Summary: M-estimation of linear quantile and ES regressions using FZ losses, with asymptotic theory. Implemented in R `esreg`.
- Relevance: the engine behind the ES regression backtest (A17). It can also run ES-on-regime-probability regressions directly.
- Status: VERIFIED (metadata); summary from memory.

**A17. Bayer, S. & Dimitriadis, T. (2022).** "Regression-Based Expected Shortfall Backtesting." *Journal of Financial Econometrics* 20(3), 437–471. doi:10.1093/jjfinec/nbaa013
- URLs: Crossref record (CRAN `esback`); https://arxiv.org/abs/1801.04112
- Summary: A Mincer–Zarnowitz-style ES backtest that regresses returns jointly on the ES forecast. It needs only ES forecasts and uses a misspecification-robust covariance. It "outperform[s] the competitors throughout all considered simulations."
- Relevance: the preferred ES backtest for ML models that output only (VaR, ES) point pairs. Available in R `esback`.
- Status: VERIFIED.

**A18. Ehm, W., Gneiting, T., Jordan, A. & Krüger, F. (2016).** "Of Quantiles and Expectiles: Consistent Scoring Functions, Choquet Representations and Forecast Rankings." *JRSS-B* 78(3), 505–562. doi:10.1111/rssb.12154
- URLs: Crossref record; https://arxiv.org/abs/1503.08195
- Summary: Every consistent scoring function for a quantile is a mixture of elementary scores, and Murphy diagrams check forecast dominance across all of them.
- Relevance: a robustness check that the regime model's VaR ranking does not depend on the choice of tick loss.
- Status: VERIFIED.

**A19. Ziegel, J.F., Krüger, F., Jordan, A. & Fasciati, F. (2020).** "Robust Forecast Evaluation of Expected Shortfall." *JFEc* 18(1), 95–120. doi:10.1093/jjfinec/nby035. Preprint title: "Murphy Diagrams: Forecast Evaluation of Expected Shortfall."
- URLs: Crossref record; https://arxiv.org/abs/1705.04537v1 (via search)
- Summary: Extends Murphy diagrams and dominance tests to the joint (VaR, ES) elicitable pair.
- Relevance: shows whether ES improvements from regimes hold across all consistent joint losses, not just FZ0.
- Status: VERIFIED.

**A20. González-Rivera, G., Lee, T.-H. & Mishra, S. (2004).** "Forecasting Volatility: A Reality Check Based on Option Pricing, Utility Function, Value-at-Risk, and Predictive Likelihood." *International Journal of Forecasting* 20(4), 629–645. doi:10.1016/j.ijforecast.2003.10.003
- URL: Crossref record
- Summary: Evaluates many volatility models with Reality-Check/SPA tests under economic losses, including the asymmetric "check" (tick) loss for VaR. The model ranking depends on the loss function.
- Relevance: the early, canonical use of tick loss for VaR model comparison, and a caution that rankings depend on the loss.
- Status: VERIFIED (metadata); summary from memory.

**A21. Diebold, F.X. & Mariano, R.S. (1995).** "Comparing Predictive Accuracy." *JBES* 13(3), 253–263. doi:10.1080/07350015.1995.10524599
- URL: Crossref record
- Summary: A test of equal expected loss between two forecasts using the loss differential and a HAC variance. It is valid for general loss functions.
- Relevance: pairwise unconditional comparison of regime model versus benchmark under tick and FZ0 losses.
- Status: VERIFIED (metadata); summary from memory.

**A22. Giacomini, R. & White, H. (2006).** "Tests of Conditional Predictive Ability." *Econometrica* 74(6), 1545–1578. doi:10.1111/j.1468-0262.2006.00718.x
- URL: https://ideas.repec.org/a/ecm/emetrp/v74y2006i6p1545-1578.html
- Summary: Tests conditional equal predictive ability under rolling-window estimation and allows nested models. It also gives a two-step decision rule to predict which forecast will be better given current information.
- Relevance: the most directly relevant test for the RQ. Using regime indicators or probabilities as test functions asks whether ML regimes help in specific states, for example stress, rather than on average.
- Status: VERIFIED.

**A23. Hansen, P.R., Lunde, A. & Nason, J.M. (2011).** "The Model Confidence Set." *Econometrica* 79(2), 453–497. Econometrica DOI per my memory: 10.3982/ECTA5771; Crossref returned the SSRN version, doi:10.2139/ssrn.522382.
- URL: https://ideas.repec.org/a/ecm/emetrp/v79y2011i2p453-497.html
- Summary: A sequential equal-predictive-ability elimination procedure that yields a set containing the best model with a given confidence. Uninformative data produce a larger set.
- Relevance: multi-model comparison across the whole zoo (GARCH, CAViaR, FZ-GAS, ML ± regimes) under tick and FZ0 losses, avoiding pairwise multiple-testing problems.
- Status: VERIFIED.

**A24. Bernardi, M. & Catania, L. (2016).** "Comparison of Value-at-Risk Models Using the MCS Approach." *Computational Statistics* 31(2), 579–608. doi:10.1007/s00180-016-0646-6. Companion: "The Model Confidence Set package for R," arXiv:1410.8504.
- URLs: Crossref record; https://arxiv.org/abs/1410.8504
- Summary: Applies the MCS with an asymmetric VaR loss to a large set of VaR models, and the R `MCS` package implements it. Per my memory, the paper also combines the surviving models.
- Relevance: the direct precedent and implementation (R `MCS`) for MCS-based VaR ranking.
- Status: VERIFIED (metadata and arXiv companion); CompStat summary from memory.

**A25. Clark, T.E. & West, K.D. (2007).** "Approximately Normal Tests for Equal Predictive Accuracy in Nested Models." *Journal of Econometrics* 138(1), 291–311. doi:10.1016/j.jeconom.2006.05.023
- URL: Crossref record
- Summary: An adjusted-MSPE statistic that corrects the bias in nested comparisons under the null, with approximately normal critical values.
- Relevance: limited. A regime-augmented model nests its base model, but CW is built for MSE of point forecasts. For tick or FZ0 losses with rolling windows, use GW instead. Cite CW only to motivate that choice.
- Status: VERIFIED (metadata); summary from memory.

---

## B) ML / deep learning for VaR/ES and related volatility forecasting

**B1. Taylor, J.W. (2000).** "A Quantile Regression Neural Network Approach to Estimating the Conditional Density of Multiperiod Returns." *Journal of Forecasting* 19(4), 299–311. doi:10.1002/1099-131X(200007)19:4<299::AID-FOR775>3.0.CO;2-V
- URL: Crossref record
- Summary: The original QRNN: a neural network trained on the pinball loss to estimate conditional quantiles of multiperiod returns, without distributional assumptions.
- Relevance: the foundational ML quantile benchmark. A regime-augmented QRNN is a natural treatment arm.
- Status: VERIFIED (metadata); summary from memory.

**B2. Xu, Q., Liu, X., Jiang, C. & Yu, K. (2016).** "Quantile Autoregression Neural Network Model with Applications to Evaluating Value at Risk." *Applied Soft Computing* 49, 1–12. doi:10.1016/j.asoc.2016.08.003
- URL: Crossref record
- Summary: QARNN, a nonlinear quantile autoregression by neural network applied to VaR. Per my memory it beats linear QAR and GARCH-type benchmarks on equity data.
- Relevance: a nonlinear quantile-autoregressive ML baseline without explicit regimes.
- Status: VERIFIED (metadata); summary from memory.

**B3. Li, Z., Tran, M.-N., Wang, C., Gerlach, R. & Gao, J. (2020/2021).** "A Bayesian Long Short-Term Memory Model for Value at Risk and Expected Shortfall Joint Forecasting." arXiv:2001.08374 (v2 May 2021).
- URL: https://arxiv.org/abs/2001.08374
- Summary: LSTM-AL couples an LSTM with the asymmetric-Laplace quasi-likelihood, which is equivalent to an FZ-type joint score, and is estimated by adaptive MCMC. It improves VaR/ES accuracy over established competitors.
- Relevance: a deep joint VaR/ES model already in the elicitable-loss framework, and a strong ML comparator.
- Status: VERIFIED. No journal reference listed on arXiv.

**B4. Qiu, Z., Lazar, E. & Nakata, K. (2024).** "VaR and ES Forecasting via Recurrent Neural Network-Based Stateful Models." *International Review of Financial Analysis* 92, 103102. doi:10.1016/j.irfa.2024.103102
- URLs: Crossref record; https://ideas.repec.org/a/eee/finana/v92y2024ics1057521924000346.html
- Summary: Three stateful RNN+FNN models for joint VaR/ES on six return series spanning more than 20 years. Stateful RNNs generally beat non-stateful RNNs and rolling-window, GARCH and GAS benchmarks.
- Relevance: "stateful" hidden memory is an implicit, learned regime. This is the key comparator for explicit ML-regime features versus implicit latent state.
- Status: VERIFIED.

**B5. Herrig, N. (2025).** "Risk Forecasting Using Long Short-Term Memory Mixture Density Networks." arXiv:2501.01278 (MSc thesis).
- URL: https://arxiv.org/abs/2501.01278
- Summary: LSTM-MDN VaR (including a 3-component mixture) on FTSE 100, S&P 500 and EURO STOXX 50, compared with historical simulation, CMM and GARCH. The networks were poor in calm 2017–18 but outperformed in turbulent 2021–22.
- Relevance: mixture components act as soft regimes. The calm-versus-turbulent asymmetry suggests the RQ should report results by sub-period or regime. It is a thesis, so cite cautiously.
- Status: VERIFIED.

**B6. Goel, A., Pasricha, P. & Kanniainen, J. (2024/2025).** "Time-Series Foundation AI Model for Value-at-Risk Forecasting." arXiv:2410.11773 (v7 May 2025).
- URL: https://arxiv.org/abs/2410.11773
- Summary: Uses TimesFM, zero-shot and fine-tuned, on S&P 100 and its constituents over 19 years, with more than 8.5 years out of sample. The fine-tuned version beats GARCH and GAS on actual-over-expected ratios and matches GAS on quantile loss at α = 0.01, 0.025, 0.05 and 0.10.
- Relevance: a frontier ML benchmark. It shows that improvements on quantile loss over GAS are hard to obtain.
- Status: VERIFIED.

**B7. Wang, D.-Y., Liang, G., Zhang, K. & Zhu, Q. (2026).** "Reliable Real-Time Value at Risk Estimation via Quantile Regression Forest with Conformal Calibration." arXiv:2602.01912.
- URL: https://arxiv.org/abs/2602.01912
- Summary: Trains a quantile regression forest offline on risk factors, applies it online, and adds conformal calibration with consistency and coverage-validity guarantees. Numerical experiments only, with no headline numbers in the abstract.
- Relevance: conformal calibration is a practical fix for ML under-coverage (see B11) and should be considered as a design arm.
- Status: VERIFIED.

**B8. Zhang, Y., Zhu, K. & Zhu, Z. (2026).** "ReSGA: A Large Tail Risk Model for Learning Value-at-Risk and Expected Shortfall." arXiv:2606.04576.
- URL: https://arxiv.org/abs/2606.04576
- Summary: A retrieval-enhanced self-grouping autoencoder for joint VaR/ES on monthly US equities (1926–2023, 153 characteristics). It beats 12 econometric and ML competitors on out-of-sample loss and backtests, and gains come mainly from data complexity rather than model complexity.
- Relevance: cross-sectional, monthly frequency, so only a loose comparator for a daily time-series design. Its "self-grouping" mechanism is regime-like.
- Status: VERIFIED.

**B9. Wang, S., Wang, Q., Lu, H., Zhang, D., Xing, Q. & Wang, J. (2025).** "Learning About Tail Risk: Machine Learning and Combination with Regularization in Market Risk Management." *Omega* 133, 103249. doi:10.1016/j.omega.2024.103249
- URL: Crossref record (https://ideas.repec.org/a/eee/jomega/v133y2025ics0305048324002135.html shows no abstract)
- Summary: Per the title, ML tail-risk forecasts combined with regularized combination weights. I could not retrieve the abstract.
- Relevance: a combination benchmark. If regimes help, does a regularized combination of non-regime models capture the same gains?
- Status: PARTIALLY VERIFIED (title, authors and venue confirmed; content UNVERIFIED).

**B10. Spilak, B. & Härdle, W.K. (2020/2021).** "Tail-Risk Protection: Machine Learning Meets Modern Econometrics." arXiv:2010.03315 (v4 Aug 2021).
- URL: https://arxiv.org/abs/2010.03315
- Summary: Weak classifiers, parametric and non-parametric, estimate the probability of exceeding a VaR level and drive a hedging strategy that limits participation in bull regimes. An ensemble improves generalization and trading performance.
- Relevance: an exceedance-classification view of tail risk with an economic evaluation angle, useful if the paper adds a "value of regime signals" section.
- Status: VERIFIED.

**B11. Zherlitsyn, D., Kuzheliev, M., Mandra, V. & Mandra, N. (2026).** "Benchmarking Machine Learning and Econometric Models for Joint Value-at-Risk and Expected Shortfall in Mixed Equity and Cryptocurrency Portfolios." *JRFM* 19(9), 720. doi:10.3390/jrfm19090720
- URL: Crossref record with abstract (mdpi.com returned 403)
- Summary: Ten models on equity, crypto and mixed portfolios over 1,397 out-of-sample days. Uncalibrated gradient boosting under-covers, with violation rates up to 10.81% against a nominal 5%. Split-conformal calibration keeps forecasts in the traffic-light green zone, yet 47 of 49 significant loss comparisons still favour a classical benchmark.
- Relevance: the most direct prior evidence against the RQ. ML needs calibration to pass backtests, and econometric models still win on consistent losses. The design must separate calibration from accuracy.
- Status: VERIFIED.

**B12. Buse, R., Görgen, K. & Schienle, M. (2025).** "Predicting Value at Risk for Cryptocurrencies with Generalized Random Forests." *International Journal of Forecasting* 41(3), 1199–1222. doi:10.1016/j.ijforecast.2024.12.002
- URLs: Crossref record; https://arxiv.org/abs/2203.08224
- Summary: Generalized random forests adapted to quantile prediction for 105 cryptocurrencies, beating QR, GARCH and CAViaR. The advantage is largest in unstable periods, and the method shows time-varying predictor importance. Backtests per the search snippet: DQ, Kupiec, Christoffersen and actual-over-expected.
- Relevance: tree-based quantile ML whose gains concentrate in unstable periods, which supports conditional (GW, regime-sliced) evaluation. It fills the "gradient boosting / tree quantile VaR" slot.
- Status: VERIFIED.

**B13. Gu, S., Kelly, B. & Xiu, D. (2020).** "Empirical Asset Pricing via Machine Learning." *Review of Financial Studies* 33(5), 2223–2273. doi:10.1093/rfs/hhaa009
- URL: Crossref record
- Summary: A large-scale comparison of ML methods for return prediction. Trees and neural networks win because they capture nonlinear interactions, and the paper sets norms for out-of-sample design and tuning.
- Relevance: general ML-in-finance context and a methodological template (rolling or expanding refits, validation splits).
- Status: VERIFIED (metadata); summary from memory.

**B14. Christensen, K., Siggaard, M. & Veliyev, B. (2023).** "A Machine Learning Approach to Volatility Forecasting." *JFEc* 21(5), 1680–1727. doi:10.1093/jjfinec/nbac020
- URLs: Crossref record; https://ideas.repec.org/a/oup/jfinec/v21y2023i5p1680-1727..html (via search)
- Summary: For DJIA constituents' realized variance, regularization, trees and neural networks with minimal tuning beat the HAR family, even with only HAR lags as inputs. Gains grow with the horizon because the ML models are more persistent.
- Relevance: pro-ML evidence for volatility inputs. It should be contrasted with B15 and B16.
- Status: VERIFIED.

**B15. Branco, R.R., Rubesam, A. & Zevallos, M. (2024).** "Forecasting Realized Volatility: Does Anything Beat Linear Models?" *Journal of Empirical Finance* 78, 101524. doi:10.1016/j.jempfin.2024.101524
- URL: https://econpapers.repec.org/article/eeeempfin/v_3a78_3ay_3a2024_3ai_3ac_3as0927539824000598.htm
- Summary: Ten global indices, 2000–2021. Extra predictors help at daily and weekly horizons, but there is no evidence that nonlinear ML statistically beats linear models, and simpler models give more economic value monthly.
- Relevance: a sobering prior that the null of "no improvement" is plausible. It supports MCS-based reporting.
- Status: VERIFIED.

**B16. Kılıç, R. (2025, rev. 2026).** "Linear and Nonlinear Econometric Models versus Machine-Learning Models: Evidence from Realized-Volatility Forecasting." FEDS 2025-061r1. doi:10.17016/FEDS.2025.061r1
- URL: https://www.federalreserve.gov/econres/feds/linear-and-nonlinear-econometric-models-against-machine-learning-models.htm
- Summary: HAR, ARFIMA and regime-based HAR variants against XGBoost and neural networks on the S&P 500 and 40 US equities. Markov-switching HAR is best at short horizons and ARFIMA at monthly. ML sometimes beats HAR but not the broader econometric set.
- Relevance: direct evidence that econometric regime models, not ML, deliver the gains in volatility. A Markov-switching benchmark is therefore mandatory for an "ML regimes" claim.
- Status: VERIFIED. The topic is realized volatility, not VaR.

**B17. Amendola, A., Candila, V., Naimoli, A. & Storti, G. (2024/2026).** "Combining Value-at-Risk and Expected Shortfall Forecasts via the Model Confidence Set." arXiv:2406.06235 (v2 Feb 2026).
- URL: https://arxiv.org/abs/2406.06235
- Summary: Uses an MCS with a strictly consistent joint VaR–ES loss to select a set of superior models, then combines their forecasts. On nine indices at 2.5% and 1%, the combinations pass backtests and consistently enter the superior set.
- Relevance: a combination benchmark and a ready-made MCS-plus-joint-loss pipeline to copy.
- Status: VERIFIED.

**B18. Le, T.H. (2020).** "Forecasting Value at Risk and Expected Shortfall with Mixed Data Sampling." *International Journal of Forecasting* 36(4), 1362–1379. doi:10.1016/j.ijforecast.2020.01.008
- URL: https://ideas.repec.org/a/eee/intfor/v36y2020i4p1362-1379.html
- Summary: MIDAS models forecast VaR/ES directly at the target horizon and "significantly outperform traditional GARCH-based forecasts," especially at multi-day horizons. It recommends asymmetric quantile models with an AL density for joint estimation.
- Relevance: a strong econometric benchmark for multi-day (10-day, FRTB-relevant) horizons.
- Status: VERIFIED.

**B19. Taylor, J.W. (2019).** "Forecasting Value at Risk and Expected Shortfall Using a Semiparametric Approach Based on the Asymmetric Laplace Distribution." *JBES* 37(1), 121–133. doi:10.1080/07350015.2017.1281815
- URL: Crossref record
- Summary: Joint CAViaR-type VaR/ES estimation through an AL likelihood, linking to the FZ score.
- Relevance: the econometric joint VaR/ES benchmark that B3 builds on.
- Status: VERIFIED (metadata); summary from memory.

---

## C) Regulatory context (BIS)

**C1. BCBS (1996).** "Supervisory Framework for the Use of 'Backtesting' in Conjunction with the Internal Models Approach to Market Risk Capital Requirements." 4 January 1996.
- URL: https://www.bis.org/publ/bcbs22.htm
- Summary: The original traffic-light backtesting framework, which compares actual trading outcomes with model risk measures. Now superseded.
- Relevance: the historical origin of the green/amber/red zones used to label backtest outcomes.
- Status: VERIFIED.

**C2. BCBS (2016).** "Minimum Capital Requirements for Market Risk" (FRTB), d352, 14 January 2016.
- URL: https://www.bis.org/bcbs/publ/d352.htm
- Summary: The FRTB standard: a revised trading/banking book boundary, IMA and SA, a shift from VaR to ES under stress, and market-illiquidity horizons. Marked superseded.
- Relevance: cite for the regulatory shift from VaR to ES that motivates joint VaR/ES evaluation.
- Status: VERIFIED.

**C3. BCBS (2019).** "Minimum Capital Requirements for Market Risk," d457, 14 January 2019 (corrected 25 February 2019), effective 1 January 2022.
- URL: https://www.bis.org/bcbs/publ/d457.htm
- Summary: Replaces d352. It revises the simplified SA, scope, FX and index treatments, risk weights, the desk-level internal-model assessment (PLA), and risk-factor eligibility.
- Relevance: the current FRTB text to cite.
- Status: VERIFIED. The landing page does not state the ES 97.5% or PLA numbers; those come from the consolidated MAR in C4 and C5.

**C4. Basel Framework MAR32.** "Internal Models Approach: Backtesting and Profit and Loss Attribution Test Requirements" (in force 1 January 2023).
- URL: https://www.bis.org/basel_framework/chapter/MAR/32.htm?inforce=20230101&published=20200327
- Summary:
  - Bank-wide backtest: 1-day 99% VaR over 250 days. Green is 0–4 exceptions (multiplier 1.50), amber 5–9 (1.70, 1.76, 1.83, 1.88, 1.92), red 10 or more (2.00) (MAR32.9).
  - Desk level: VaR at 97.5% and 99%. A desk with more than 12 exceptions at 99% or more than 30 at 97.5% goes to the standardised approach (MAR32.18–19).
  - PLA: Spearman correlation and KS test. Green needs Spearman > 0.80 and KS < 0.09; red is Spearman < 0.70 or KS > 0.12 (MAR32.42).
- Relevance: report the traffic-light zone over every 250-day window at 99% and 97.5%. This converts statistical results into regulatory consequences.
- Status: VERIFIED.

**C5. Basel Framework MAR33.** "Internal Models Approach: Capital Requirements Calculation."
- URL: https://www.bis.org/basel_framework/chapter/MAR/33.htm?inforce=20230101&published=20200327
- Summary:
  - ES at 97.5% one-tailed (MAR33.3), with a 10-day base horizon and liquidity horizons of 10/20/40/60/120 days (MAR33.4, 33.12).
  - Stressed ES is calibrated to the worst 12-month period since 2007, using a reduced factor set that explains at least 75% of full ES (MAR33.5–33.7).
  - IMCC uses ρ = 0.5 (MAR33.15). The multiplier m_c = 1.5 plus a 0–0.5 add-on from the 99% VaR backtest (MAR33.42).
- Relevance: fixes the evaluation levels (ES 97.5%, VaR 99%), motivates a 10-day horizon check, and motivates a stress-period sub-sample analysis.
- Status: VERIFIED. The plus-factor table itself was not in the extracted text.

---

## Recommended evaluation toolkit

- **Use the regulatory levels.** Evaluate VaR at 99% and 97.5% and ES at 97.5% (MAR32/33), with 1-day as the primary horizon and a 10-day robustness check (MIDAS benchmark, B18). Report the Basel traffic-light zone over rolling 250-day windows so results have regulatory meaning.
- **VaR calibration (absolute backtests):**
  - Kupiec POF for unconditional coverage.
  - Christoffersen conditional coverage.
  - Engle–Manganelli DQ test, with regime probabilities and labels added as DQ instruments. That checks whether non-regime models leave violations predictable from the regime state, which is the cleanest single test of the RQ's mechanism.
  - Christoffersen–Pelletier duration test as a check for clustering.
- **ES calibration:**
  - Bayer–Dimitriadis ESR backtest (`esback`) as the primary test, because it needs only (VaR, ES) point forecasts.
  - Du–Escanciano conditional test for tail-failure dependence.
  - Kratz–Lok–McNeil multinomial test (at least 4 levels) for quantile-only ML models.
  - Acerbi–Székely Z2 where full predictive distributions exist.
- **Accuracy (comparative backtests):** rank with the tick loss for VaR and the FZ0 loss for joint VaR/ES; this follows the consistency requirement of Gneiting (2011) and Fissler & Ziegel (2016). Never use the MSE of ES. Run pairwise DM tests, framed as comparative backtests per Nolde & Ziegel, of each ML-regime model against its own no-regime twin and against the best econometric benchmark.
- **Conditional comparison: the GW test.** Rolling-window GW handles nested comparisons (regime-augmented versus base) under tick and FZ0 losses, where Clark–West does not apply. Use regime state or VIX level as the test function to show where any gain arises. Prior work (B5, B12) suggests ML gains concentrate in turbulent periods.
- **Model zoo:** apply the MCS (Hansen–Lunde–Nason; R `MCS`) at 75% and 90% under tick and FZ0 losses. The zoo should include:
  - Non-regime econometric models: GARCH-t/FHS, CAViaR, FZ-GAS, AL-joint.
  - An explicit Markov-switching benchmark. Kılıç (B16) shows econometric regimes are the bar ML regimes must clear.
  - ML models with and without regime features.
  - An MCS-based forecast combination (B17).
- **Separate calibration from discrimination:** report every ML model both raw and conformally calibrated (B7, B11). The JRFM 2026 study shows calibration can fix coverage while classical models still win 47 of 49 loss comparisons. Add Murphy diagrams (Ehm et al.; Ziegel et al.) to show that the rankings do not depend on the choice of loss.
- **Sample design:** use strictly real-time, rolling or expanding refits with the regime classifier re-estimated only on past data. Analyze sub-samples separately: GFC, COVID-2020, 2022, and the MAR33-style worst 12-month stress window. Use a long out-of-sample span, because coverage tests at 1% have little power at 250 observations.