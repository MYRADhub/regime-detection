# Strand: Econometric regime-switching models for VaR/ES

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

## Strand B: Econometric regime-switching models for VaR, ES and tail-risk forecasting

**How I checked each entry.** I pulled citation details from the Crossref API (api.crossref.org) and abstracts from the Semantic Scholar API, IDEAS/RePEc, EconPapers and NBER. I read one full text, Ardia et al. (2018), and confirmed its design in the PDF.
- **V-full**: I read the full text.
- **V-abs**: I read the abstract.
- **V-meta**: Crossref confirms the citation, but the summary comes from my own knowledge and should be checked against the paper.
- **Partial**: the paper exists, but parts of the citation or summary come from memory or a secondary source.

Nothing on the list is unverified as to existence. ScienceDirect blocked direct access (403), so Elsevier abstracts came from secondary sources.

---

### A. Foundations

**1. Hamilton, J.D. (1989).** "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." *Econometrica* 57(2), 357–384. DOI 10.2307/1912559
- **URL:** api.crossref.org/works/10.2307/1912559
- **Summary:** Introduces the Markov-switching autoregression and the Hamilton filter, which gives the probability of each regime using only data up to time t. Applied to US real GNP growth, the two-state model's regimes line up with NBER recessions. The paper also introduces the smoothed probability, which uses the full sample.
- **Relevance:** This is the basic split our paper depends on. Filtered probabilities are available in real time; smoothed probabilities use future data. Every regime-based VaR forecast has to be built from filtered or predicted probabilities. Hamilton's well-known recession-dating results use smoothed ones.
- **Status:** V-meta. Crossref lists the start page only; 357–384 is from memory.

**2. Hamilton, J.D. & Susmel, R. (1994).** "Autoregressive Conditional Heteroskedasticity and Changes in Regime." *Journal of Econometrics* 64(1–2), 307–333. DOI 10.1016/0304-4076(94)90067-1
- **URLs:** Crossref; ideas.repec.org/a/eee/econom/v64y1994i1-2p307-333.html (IDEAS shows no abstract)
- **Summary:** Proposes SWARCH, in which an ARCH process is rescaled by a Markov regime. Applied to weekly NYSE returns (1962–1987, from memory), it fits better than GARCH and fixes GARCH's excessive volatility persistence. The high-volatility regime is linked to recessions and October 1987.
- **Relevance:** The origin of the idea that regimes cause apparent volatility persistence. Its forecast comparison is mostly short-horizon volatility, not VaR.
- **Status:** V-meta.

**3. Cai, J. (1994).** "A Markov Model of Switching-Regime ARCH." *Journal of Business & Economic Statistics* 12(3), 309–316. DOI 10.1080/07350015.1994.10524546
- **URL:** Crossref
- **Summary:** Lets the ARCH intercept switch between regimes. On US T-bill excess returns, ARCH persistence falls sharply once regime shifts are allowed (from memory).
- **Relevance:** Builds the argument that regimes explain apparent volatility persistence. It is an in-sample study.
- **Status:** V-meta.

**4. Gray, S.F. (1996).** "Modeling the Conditional Distribution of Interest Rates as a Regime-Switching Process." *Journal of Financial Economics* 42(1), 27–62. DOI 10.1016/0304-405X(96)00875-6
- **URLs:** Crossref; ideas.repec.org/a/eee/jfinec/v42y1996i1p27-62.html
- **Summary:** Builds the first workable regime-switching GARCH. It avoids path dependence by collapsing the conditional variance across regimes at each step. Applied to the short-term US interest rate, it beats single-regime GARCH out of sample (from memory).
- **Relevance:** The collapsing step is still used in Klaassen and in later VaR applications.
- **Status:** V-meta.

**5. Klaassen, F. (2002).** "Improving GARCH Volatility Forecasts with Regime-Switching GARCH." *Empirical Economics* 27(2), 363–394. DOI 10.1007/s001810100100
- **URL:** ideas.repec.org/a/spr/empeco/v27y2002i2p363-394.html
- **Summary:** Uses three US-dollar exchange rates. Single-regime GARCH forecasts are too high in volatile periods because shocks persist too long. A two-regime GARCH, with a collapsing scheme refined from Gray's, gives significantly better out-of-sample volatility forecasts.
- **Relevance:** A clean out-of-sample result in favour of regimes, but for volatility rather than VaR or ES. The over-forecasting mechanism matters for how VaR behaves after a crisis.
- **Status:** V-abs.

**6. Haas, M., Mittnik, S. & Paolella, M.S. (2004a).** "A New Approach to Markov-Switching GARCH Models." *Journal of Financial Econometrics* 2(4), 493–530. DOI 10.1093/jjfinec/nbh020
- **URLs:** Crossref (lists only Haas); Semantic Scholar
- **Summary:** Each regime runs its own GARCH process, so the variance path does not depend on the history of regimes and likelihood estimation is tractable. The abstract favours independent switching GARCH with a possibly skewed conditional mixture density.
- **Relevance:** This is the specification MSGARCH implements and the one used in most later VaR/ES studies, including Ardia et al. (2018).
- **Status:** V-abs. Co-authors confirmed from memory.

**7. Haas, M., Mittnik, S. & Paolella, M.S. (2004b).** "Mixed Normal Conditional Heteroskedasticity." *Journal of Financial Econometrics* 2(2), 211–250. DOI 10.1093/jjfinec/nbh009
- **URL:** Crossref
- **Summary:** The mixed-normal GARCH model, a regime model where the mixing is i.i.d. rather than Markov.
- **Relevance:** A natural "regime without persistence" benchmark. It lets you test whether gains come from the regime dynamics or just from the mixture shape.
- **Status:** V-meta.

**8. Ang, A. & Timmermann, A. (2012).** "Regime Changes and Financial Markets." *Annual Review of Financial Economics* 4(1), 313–337. DOI 10.1146/annurev-financial-110311-101808 (NBER WP 17182)
- **URLs:** Crossref; nber.org/papers/w17182
- **Summary:** A review. Regimes capture fat tails, heteroskedasticity, skewness and time-varying correlations. They often coincide with changes in policy or regulation, and they matter for asset pricing and portfolio choice.
- **Relevance:** The standard citation for why regimes should help tail-risk forecasting. Out-of-sample risk forecasting is not its main focus.
- **Status:** V-abs.

**9. Guidolin, M. (2011).** "Markov Switching Models in Empirical Finance." In *Missing Data Methods: Time-Series Methods and Applications*, Advances in Econometrics 27B, 1–86. Emerald. DOI 10.1108/S0731-9053(2011)000027B004
- **URL:** ideas.repec.org/h/eme/aecozz/s0731-9053(2011)000027b004.html
- **Summary:** A survey covering fit, inference on regimes, hypothesis testing, and point and density forecasting. Applications span stock returns, the term structure, exchange rates and stock–bond co-movement.
- **Relevance:** Its forecasting section collects mixed out-of-sample evidence, which is useful framing.
- **Status:** V-abs.

**10. Guidolin, M. & Timmermann, A. (2007).** "Asset Allocation under Multivariate Regime Switching." *Journal of Economic Dynamics and Control* 31(11), 3503–3544. DOI 10.1016/j.jedc.2006.12.004
- **URL:** Crossref
- **Summary:** A four-state multivariate regime model (crash, slow growth, bull, recovery) for stocks and bonds. Optimal allocations depend strongly on the current regime. They report real-time out-of-sample portfolio gains (from memory).
- **Relevance:** Uses filtered probabilities for real-time allocation. Not a VaR paper.
- **Status:** V-meta.

**11. Guidolin, M. & Timmermann, A. (2008).** "International Asset Allocation under Regime Switching, Skew, and Kurtosis Preferences." *Review of Financial Studies* 21(2), 889–935. DOI 10.1093/rfs/hhn006
- **URL:** Crossref
- **Summary:** Regime-dependent higher moments of international equity returns create time-varying home bias once investors care about skewness and kurtosis (from memory).
- **Relevance:** Regimes as a source of time-varying higher moments, which is what drives tail risk.
- **Status:** V-meta.

**12. Kim, C.-J. (1994).** "Dynamic Linear Models with Markov-Switching." *Journal of Econometrics* 60(1–2), 1–22. DOI 10.1016/0304-4076(94)90036-1
- **URL:** Crossref
- **Summary:** The Kim filter and smoother for state-space models with Markov switching.
- **Relevance:** The standard reference for the smoothing algorithm. Cite it when explaining why smoothed probabilities are look-ahead.
- **Status:** V-meta.

### B. Regime-switching GARCH for VaR and ES

**13. Billio, M. & Pelizzon, L. (2000).** "Value-at-Risk: A Multivariate Switching Regime Approach." *Journal of Empirical Finance* 7(5), 531–554. DOI 10.1016/S0927-5398(00)00022-0
- **URLs:** ideas.repec.org/a/eee/empfin/v7y2000i5p531-554.html (no abstract); secondary summary in Taamouti WP (eco.uc3m.es/temp/09-24-14.pdf)
- **Summary:** A switching-volatility model gives return distributions and VaR for single assets and linear portfolios. Backtests favour the regime model over variance-covariance VaR and GARCH(1,1).
- **Relevance:** The earliest regime-switching VaR paper. I could not confirm the dataset or whether probabilities were filtered.
- **Status:** Partial. Citation verified; summary from a secondary source.

**14. Guidolin, M. & Timmermann, A. (2006).** "Term Structure of Risk under Alternative Econometric Specifications." *Journal of Econometrics* 131(1–2), 285–308. DOI 10.1016/j.jeconom.2005.01.033. Working-paper version: "Value at Risk and Expected Shortfall under Regime Switching," SSRN 557091 (2004).
- **URLs:** ideas.repec.org/a/eee/econom/v131y2006i1-2p285-308.html; SSRN abstract via Crossref
- **Summary:** VaR and ES across horizons from a four-state multivariate Markov-switching model, GARCH-M with t errors, component GARCH, and a bootstrap, for stock, bond and cash portfolios. Out of sample, the best model depends on asset and horizon. The bootstrap wins at 5% VaR and regime switching wins at 1% VaR. The working paper says it studies "real-time measures of risk."
- **Relevance:** Very close to our question. The gain appears only deep in the tail, and the authors explicitly use real-time (filtered) state probabilities.
- **Status:** V-abs.

**15. Marcucci, J. (2005).** "Forecasting Stock Market Volatility with Regime-Switching GARCH Models." *Studies in Nonlinear Dynamics & Econometrics* 9(4), Article 6. DOI 10.2202/1558-3708.1145
- **URL:** ideas.repec.org/a/bpj/sndecm/v9y2005i4n6.html
- **Summary:** MRS-GARCH with all parameters switching, and Gaussian, t or GED errors with regime-specific degrees of freedom, on S&P 100 volatility. It is evaluated with statistical losses and VaR-based loss. MRS-GARCH clearly beats standard GARCH at horizons under one week. Asymmetric single-regime GARCH is better beyond one week.
- **Relevance:** The gain depends on horizon, and it is a true out-of-sample, filtered-probability design. Useful evidence that the benefit fades at longer horizons.
- **Status:** V-abs.

**16. Sajjad, R., Coakley, J. & Nankervis, J.C. (2008).** "Markov-Switching GARCH Modelling of Value-at-Risk." *Studies in Nonlinear Dynamics & Econometrics* 12(3), Article 7. DOI 10.2202/1558-3708.1522
- **URLs:** Crossref; repository.essex.ac.uk/4770 (via search); ideas.repec.org/a/bpj/sndecm/v12y2008i3n7.html
- **Summary:** Asymmetric MS-GARCH (with skewness and leverage) for VaR on long and short positions in daily FTSE 100 and S&P 500 returns. MS-GARCH is best for FTSE positions and reasonable for S&P. Ignoring regimes and skewness produces overly conservative capital requirements.
- **Relevance:** A direct VaR backtest. The result differs by market, so there is no universal gain.
- **Status:** V-abs (via repository/search summary).

**17. Ardia, D., Bluteau, K., Boudt, K. & Catania, L. (2018).** "Forecasting Risk with Markov-Switching GARCH Models: A Large-Scale Performance Study." *International Journal of Forecasting* 34(4), 733–747. DOI 10.1016/j.ijforecast.2018.05.004
- **URL:** pure.au.dk/ws/files/137371173/Forecasting_risk_with_markov_switching_garch_models_VOR18.pdf (full text read)
- **Data and design:** 426 S&P 500 stocks, 11 equity indices and 8 FX rates. Rolling estimation window of 1,500 days; 2,000 out-of-sample days from Oct 2008 to Nov 2016. Horizons of 1, 5 and 10 days; 1% and 5% VaR and ES.
- **Models and tests:** Models compared on UC, CC and DQ backtests, quantile loss, FZ loss and weighted CRPS, with Diebold–Mariano tests. Specifications are GARCH/GJR, normal/t/skewed variants, MS vs single-regime, and Bayesian vs ML.
- **Results:** MS clearly beats single-regime for stocks. For indices, MS helps only when the conditional distribution is not fat-tailed. For FX, single-regime wins on 1% quantile loss at 5- and 10-day horizons. Gains from MS concentrate in the first half of the out-of-sample period (2008–2012). Accounting for parameter uncertainty helps independently of regimes.
- **Relevance:** The key benchmark for us. The one-step predictive density weights each regime by the filtered probability (Hamilton filter) multiplied through the transition matrix, so it is fully real-time. Fat tails absorb much of the regime gain for indices, and the gains depend on the period.
- **Status:** V-full.

**18. Ardia, D., Bluteau, K., Boudt, K., Catania, L. & Trottier, D.-A. (2019).** "Markov-Switching GARCH Models in R: The MSGARCH Package." *Journal of Statistical Software* 91(4). DOI 10.18637/jss.v091.i04
- **URL:** Crossref
- **Summary:** Software for MS-GARCH (Haas et al. 2004a) with ML and Bayesian estimation. Supports VaR and ES forecasts from filtered-probability predictive mixtures (from memory).
- **Relevance:** The likely implementation for our econometric benchmark.
- **Status:** V-meta.

**19. Ardia, D., Bluteau, K. & Rüede, M. (2019).** "Regime Changes in Bitcoin GARCH Volatility Dynamics." *Finance Research Letters* 29, 266–271. DOI 10.1016/j.frl.2018.08.009
- **URL:** Crossref
- **Summary:** Finds regime changes in Bitcoin's GARCH dynamics. MS-GARCH improves VaR forecasts over single-regime GARCH (from memory).
- **Relevance:** Shows the result extends to crypto.
- **Status:** V-meta.

**20. Caporale, G.M. & Zekokh, T. (2019).** "Modelling Volatility of Cryptocurrencies Using Markov-Switching GARCH Models." *Research in International Business and Finance* 48, 143–155. DOI 10.1016/j.ribaf.2018.12.009
- **URLs:** Crossref; summary via search
- **Summary:** More than 1,000 GARCH and MS-GARCH specifications for BTC, ETH, XRP and LTC. Standard GARCH can give poor VaR and ES. Asymmetric and regime-switching specifications do better, judged by Model Confidence Set.
- **Relevance:** Large-scale out-of-sample VaR and ES testing.
- **Status:** V-abs (secondary).

**21. Maciel, L. (2021).** "Cryptocurrencies Value-at-Risk and Expected Shortfall: Do Regime-Switching Volatility Models Improve Forecasting?" *International Journal of Finance & Economics* 26(3), 4840–4855. DOI 10.1002/ijfe.2043
- **URL:** ideas.repec.org/a/wly/ijfiec/v26y2021i3p4840-4855.html
- **Summary:** 54 Bayesian MS-GARCH specifications per coin across six coins, at 1-, 5- and 10-step horizons. MS-GARCH gives more accurate VaR and ES than single-regime models.
- **Relevance:** A direct VaR and ES test. The rolling design is not described in the abstract.
- **Status:** V-abs.

**22. Hotta, L.K., Trucíos, C., Valls Pereira, P. & Zevallos, M. (2024).** "Forecasting VaR and ES through Markov-Switching GARCH Models: Does the Specification Matter?" FGV EESP Textos para discussão No. 567.
- **URL:** econpapers.repec.org/paper/fgveesptd/567.htm
- **Summary:** EUR, JPY, CAD and DKK against the USD, plus Monte Carlo experiments. Out-of-sample VaR and ES are robust to misspecifying the MS volatility structure. Performance improves with sample size.
- **Relevance:** The exact choice of regime structure matters less than having enough data.
- **Status:** V-abs. Working paper, not peer-reviewed.

**23. Malim Franco, J.P. & Hotta, L.K. (2026).** "Regime Dependence, Not Dimensionality: Forecasting Cryptocurrency Value-at-Risk." SSRN, DOI 10.2139/ssrn.6597696
- **URL:** Crossref/SSRN abstract
- **Summary:** A Markov-switching factor model (Barigozzi & Massacci 2025) on 37 cryptocurrencies, rolling out of sample 2022–2026. It is the only model in the 90% Model Confidence Set at 1% VaR. It beats GARCH-N, GARCH-t, MS-GARCH, factor quantile regression and historical simulation.
- **Relevance:** Important caveat: the abstract says it weights regimes by "propagated smoothed regime probabilities." If those are smoothed within each rolling window and only the end-point is used, that equals the filtered probability. But this is exactly the issue we need to check.
- **Status:** V-abs. Very recent preprint.

**24. Bauwens, L., Preminger, A. & Rombouts, J.V.K. (2010).** "Theory and Inference for a Markov Switching GARCH Model." *Econometrics Journal* 13(2), 218–244. DOI 10.1111/j.1368-423X.2009.00307.x
- **URL:** Crossref
- **Summary:** Gives stationarity conditions and Bayesian (Gibbs) inference for the path-dependent MS-GARCH (from memory).
- **Relevance:** Methodological background on estimating MS-GARCH.
- **Status:** V-meta.

**25. Augustyniak, M. (2014).** "Maximum Likelihood Estimation of the Markov-Switching GARCH Model." *Computational Statistics & Data Analysis* 76, 61–75. DOI 10.1016/j.csda.2013.01.026
- **URL:** Semantic Scholar
- **Summary:** Monte Carlo EM with importance sampling gives exact ML estimation of the path-dependent MS-GARCH.
- **Relevance:** Estimation fragility is one practical reason regime models can disappoint out of sample.
- **Status:** V-abs.

**26. Kuester, K., Mittnik, S. & Paolella, M.S. (2006).** "Value-at-Risk Prediction: A Comparison of Alternative Strategies." *Journal of Financial Econometrics* 4(1), 53–89. DOI 10.1093/jjfinec/nbj002
- **URL:** Crossref (Crossref lists only Kuester; co-authors confirmed from memory)
- **Summary:** NASDAQ returns over about 30 years. Compares historical simulation, GARCH variants, EVT, CAViaR and mixed-normal GARCH. Hybrid GARCH-EVT/skew-t and MixN-GARCH do well. CAViaR is less reliable (from memory).
- **Relevance:** The canonical "horse race" design, with a regime-mixture model included.
- **Status:** V-meta.

### C. Regime-switching EVT, copulas and GAS

**27. Ze-To, S.Y.M. (2008).** "Value at Risk and Conditional Extreme Value Theory via Markov Regime Switching Models." *Journal of Futures Markets* 28(2), 155–181. DOI 10.1002/fut.20293
- **URL:** Crossref (abstract read)
- **Summary:** SWARCH filtering followed by EVT on the residuals. Tested on the S&P 500, Hang Seng and HSCEI. EVT-SWARCH beats GARCH, SWARCH and EVT-GARCH in both in-sample and out-of-sample VaR.
- **Relevance:** Regimes combined with EVT tails. Shows the benefit of regimes can complement better tail modelling.
- **Status:** V-abs. Crossref records the author as "Yau Man Ze-to Samuel."

**28. Sampid, M.G., Hasim, H.M. & Dai, H. (2018).** "Refining Value-at-Risk Estimates Using a Bayesian Markov-Switching GJR-GARCH Copula-EVT Model." *PLOS ONE* 13(6), e0198753. DOI 10.1371/journal.pone.0198753
- **URL:** Semantic Scholar
- **Summary:** Combines Bayesian MS-GJR-GARCH with skewed-t errors, copulas and EVT (with a hybrid method for choosing the EVT threshold). Backtests show adequate VaR in both calm and crisis periods.
- **Relevance:** Portfolio VaR with regimes. The evaluation is weaker than in the IJF studies.
- **Status:** V-abs.

**29. Elliott, R.J. & Miao, H. (2009).** "VaR and Expected Shortfall: A Non-Normal Regime Switching Framework." *Quantitative Finance* 9(6), 747–755. DOI 10.1080/14697680902849320
- **URL:** ideas.repec.org/a/taf/quantf/v9y2009i6p747-755.html
- **Summary:** VaR and ES under regime switching with Student-t returns, for single assets and portfolios.
- **Relevance:** Mainly methodological. Limited out-of-sample evidence.
- **Status:** V-abs.

**30. Taamouti, A. (2009).** "Analytical Value-at-Risk and Expected Shortfall under Regime-Switching." *Finance Research Letters* 6(3), 138–151. DOI 10.1016/j.frl.2009.03.004
- **URL:** Semantic Scholar
- **Summary:** An analytical approximation for multi-horizon conditional VaR and a closed-form conditional ES under regime switching. Results match simulation at much lower computing cost.
- **Relevance:** Computational tool for multi-horizon VaR and ES from a regime mixture.
- **Status:** V-abs.

**31. Makatjane, K. (2024).** "Forecasting Time-Varying Value-at-Risk and Expected Shortfall Dependence: A Markov-Switching Generalized Autoregressive Score Copula Approach." *Austrian Journal of Statistics* 53(2), 81–98. DOI 10.17713/ajs.v53i2.1710
- **URL:** Semantic Scholar
- **Summary:** An MS(2)-GAS(1) copula estimated by EM, combined with six extreme-value distributions. Applied to the Botswana market.
- **Relevance:** An example of MS-GAS. Minor journal, single market.
- **Status:** V-abs.

**32. Paolella, M.S., Polak, P. & Walker, P.S. (2019).** "Regime Switching Dynamic Correlations for Asymmetric and Fat-Tailed Conditional Returns." *Journal of Econometrics* 213(2), 493–515. DOI 10.1016/j.jeconom.2019.07.002
- **URL:** Semantic Scholar
- **Summary:** A multivariate generalized-hyperbolic regime-switching dynamic correlation model, estimated with a two-stage EM. Gives accurate risk forecasts and lower capital requirements during distress. Regime forecasts drive a risk-control strategy that avoids most GFC losses.
- **Relevance:** Strong evidence for multivariate regimes in portfolio tail risk, using regime forecasts.
- **Status:** V-abs.

### D. Regime-switching and threshold quantile (CAViaR) models and joint VaR/ES frameworks

**33. Engle, R.F. & Manganelli, S. (2004).** "CAViaR: Conditional Autoregressive Value at Risk by Regression Quantiles." *Journal of Business & Economic Statistics* 22(4), 367–381. DOI 10.1198/073500104000000370
- **URL:** Crossref
- **Summary:** Models the quantile directly as an autoregressive process (SAV, AS, IGARCH forms) estimated by quantile regression, and introduces the Dynamic Quantile (DQ) backtest.
- **Relevance:** The base for all regime and threshold CAViaR models. The DQ test is a standard evaluation tool for us.
- **Status:** V-meta.

**34. Gerlach, R.H., Chen, C.W.S. & Chan, N.Y.C. (2011).** "Bayesian Time-Varying Quantile Forecasting for Value-at-Risk in Financial Markets." *Journal of Business & Economic Statistics* 29(4), 481–492. DOI 10.1198/jbes.2010.08203
- **URLs:** ideas.repec.org/a/bes/jnlbes/v29i4y2011p481-492.html; ses.library.usyd.edu.au/handle/2123/8159
- **Summary:** A fully nonlinear CAViaR family estimated by adaptive MCMC with a Skewed-Laplace likelihood. On 10 stock indices it finds significant nonlinearity in quantile dynamics. It forecasts 2-year out-of-sample VaR better than alternatives, especially at lower quantiles.
- **Relevance:** Nonlinear, threshold-type quantile dynamics. The regime is an observable threshold, not a latent Markov state.
- **Status:** V-abs.

**35. Chen, C.W.S., Gerlach, R., Hwang, B.B.K. & McAleer, M. (2012).** "Forecasting Value-at-Risk Using Nonlinear Regression Quantiles and the Intra-day Range." *International Journal of Forecasting* 28(3), 557–574. DOI 10.1016/j.ijforecast.2011.12.004
- **URLs:** Crossref; eprints.ucm.es/12755/1/1116.pdf; repub.eur.nl/pub/23795
- **Summary:** Threshold CAViaR models using the intraday range, estimated by Bayesian methods (Skewed-Laplace). Tested on 5 APEC indices and 2 FX series. Threshold CAViaR with range information forecasts VaR most efficiently.
- **Relevance:** The regime is an observable threshold, so there is no look-ahead problem. A natural benchmark for ML regime labels.
- **Status:** V-abs.

**36. Chen, C.W.S., Weng, M.M.C. & Watanabe, T. (2017).** "Bayesian Forecasting of Value-at-Risk Based on Variant Smooth Transition Heteroskedastic Models." *Statistics and Its Interface* 10(3), 451–470. DOI 10.4310/SII.2017.v10.n3.a9
- **URLs:** Crossref; hias.hit-u.ac.jp/?p=1796 (likely the HIAS working-paper version)
- **Summary:** Smooth-transition GARCH with first-order logistic, second-order logistic and exponential transition functions, estimated by MCMC. VaR is compared with skewed and fat-tailed models and realized-volatility models.
- **Relevance:** Smooth-transition regimes for VaR.
- **Status:** Partial. The link between the working paper and the journal article is inferred.

**37. Liu, X. (2016).** "Markov Switching Quantile Autoregression." *Statistica Neerlandica* 70(4), 356–395. DOI 10.1111/stan.12091
- **URL:** Crossref (abstract read)
- **Summary:** A location-scale quantile autoregression whose parameters switch with a latent Markov regime, estimated by Bayesian methods using a three-parameter asymmetric Laplace likelihood. Marginal likelihood is used to choose the number of regimes. Ignoring quantile-dependent AR coefficients biases both regime inference and quantile prediction. Applications include S&P 500 risk assessment.
- **Relevance:** The closest latent-regime analogue of CAViaR. The abstract does not make clear how strict its out-of-sample design is.
- **Status:** V-abs.

**38. Gao, L., Ye, W. & Guo, R. (2022).** "Jointly Forecasting the Value-at-Risk and Expected Shortfall of Bitcoin with a Regime-Switching CAViaR Model." *Finance Research Letters* 48, 102826. DOI 10.1016/j.frl.2022.102826
- **URL:** Crossref (ScienceDirect returned 403)
- **Summary:** I could not access the abstract. From the title, it is a regime-switching CAViaR extended to joint VaR/ES on Bitcoin.
- **Relevance:** The only regime-switching joint VaR/ES CAViaR I found. You need to read it before claiming novelty for anything in that space.
- **Status:** Citation verified; content unverified.

**39. Taylor, J.W. (2019).** "Forecasting Value at Risk and Expected Shortfall Using a Semiparametric Approach Based on the Asymmetric Laplace Distribution." *Journal of Business & Economic Statistics* 37(1), 121–133. DOI 10.1080/07350015.2017.1281815
- **URL:** Semantic Scholar (abstract read)
- **Summary:** An asymmetric Laplace (AL) likelihood with a time-varying scale gives a joint CAViaR model for VaR and ES. The AL score is strictly consistent for joint evaluation of VaR and ES. Illustrated on stock indices.
- **Relevance:** Provides the ES-CAViaR benchmark and the AL scoring rule for our evaluation.
- **Status:** V-abs.

**40. Patton, A.J., Ziegel, J.F. & Chen, R. (2019).** "Dynamic Semiparametric Models for Expected Shortfall (and Value-at-Risk)." *Journal of Econometrics* 211(2), 388–413. DOI 10.1016/j.jeconom.2018.10.008
- **URL:** Crossref
- **Summary:** GAS-type dynamic models for VaR and ES estimated by minimizing the FZ0 loss, with asymptotic theory. On daily equity indices (from memory), the semiparametric models outperform GARCH-based alternatives out of sample.
- **Relevance:** The FZ0 loss is the standard tool for comparing ES forecasts. A strong single-regime benchmark.
- **Status:** V-meta.

**41. Fissler, T. & Ziegel, J.F. (2016).** "Higher Order Elicitability and Osband's Principle." *Annals of Statistics* 44(4), 1680–1707. DOI 10.1214/16-AOS1439
- **URL:** Crossref
- **Summary:** Shows VaR and ES are jointly elicitable and characterizes the consistent scoring functions.
- **Relevance:** The theoretical basis for evaluating ES forecasts.
- **Status:** V-meta.

### E. Realized-volatility regime models (MS-HAR, smooth-transition HAR)

**42. McAleer, M. & Medeiros, M.C. (2008).** "A Multiple Regime Smooth Transition Heterogeneous Autoregressive Model for Long Memory and Asymmetries." *Journal of Econometrics* 147(1), 104–119. DOI 10.1016/j.jeconom.2008.09.032
- **URL:** ideas.repec.org/a/eee/econom/v147y2008i1p104-119.html
- **Summary:** A multiple-regime smooth-transition HAR with sequential tests for the number of regimes. Applied to TAQ data on Dow Jones stocks over about 10 years. Finds long memory plus sign and size asymmetries. Combining it with linear HAR improves forecasts.
- **Relevance:** Regimes driven by observable variables. Its keywords include risk management.
- **Status:** V-abs.

**43. Raggi, D. & Bordignon, S. (2012).** "Long Memory and Nonlinearities in Realized Volatility: A Markov Switching Approach." *Computational Statistics & Data Analysis* 56(11), 3730–3742. DOI 10.1016/j.csda.2010.12.008
- **URL:** Semantic Scholar
- **Summary:** A Markov-switching long-memory realized-volatility model with shifting level and persistence. Forecasts better than nested models.
- **Relevance:** MS on realized volatility. Its evaluation is volatility-focused.
- **Status:** V-abs.

**44. Ma, F., Wahab, M.I.M., Huang, D. & Xu, W. (2017).** "Forecasting the Realized Volatility of the Oil Futures Market: A Regime Switching Approach." *Energy Economics* 67, 136–145. DOI 10.1016/j.eneco.2017.08.004
- **URL:** ideas.repec.org/a/eee/eneeco/v67y2017icp136-145.html
- **Summary:** MRS-HAR-RV models for crude oil futures. The high-volatility regime is short-lived. Out-of-sample forecasts beat non-switching HAR, robust across benchmarks and windows.
- **Relevance:** Out-of-sample evidence for MS-HAR. Volatility only, not VaR.
- **Status:** V-abs.

**45. Ding, Y., Kambouroudis, D. & McMillan, D.G. (2025).** "Forecasting Realised Volatility Using Regime-Switching Models." *International Review of Economics & Finance* 101, 104171. DOI 10.1016/j.iref.2025.104171
- **URLs:** Crossref; storre.stir.ac.uk/handle/1893/37126 (via search)
- **Summary:** AR and HAR realized-volatility models with smooth-transition and Markov-switching regimes, for 8 international indices, 2007–2021. Evaluated statistically and on VaR and ES. Regime models win in sample and out of sample, but the daily-horizon gain is weaker. Abrupt MS switching is preferred to smooth transition.
- **Relevance:** Very recent. Combines a realized-volatility regime model with VaR/ES evaluation and finds weak 1-day gains. Directly relevant.
- **Status:** V-abs. Open access.

### F. Evidence against regime models out of sample

**46. Engel, C. (1994).** "Can the Markov Switching Model Forecast Exchange Rates?" *Journal of International Economics* 36(1–2), 151–165.
- **URLs:** nber.org/papers/w4210; ideas.repec.org/p/fip/fedkrw/91-04.html (via search)
- **Summary:** 18 exchange rates at monthly and quarterly frequency. Good in-sample fit, but it does not beat a random walk or the forward rate on mean squared or mean absolute error. Some advantage in predicting the direction of change.
- **Relevance:** The classic "fits in sample, fails out of sample" result.
- **Status:** V-abs. Issue number from memory; DOI not fetched.

**47. Dacco, R. & Satchell, S. (1999).** "Why Do Regime-Switching Models Forecast So Badly?" *Journal of Forecasting* 18(1), 1–16. DOI 10.1002/(SICI)1099-131X(199901)18:1<1::AID-FOR685>3.0.CO;2-B
- **URLs:** Crossref; iaorifors.com/paper/30956 (via search)
- **Summary:** Even a correctly specified regime model can lose to a random walk on mean squared error. A small error in classifying the future regime wipes out the advantage of knowing the true model. It also argues MSE may be the wrong loss for nonlinear models. Applied to DM/USD.
- **Relevance:** This is the theoretical mechanism our paper tests. The value of regimes depends on how accurately they are classified in real time, and tail losses such as FZ or quantile loss may reward regimes differently from MSE.
- **Status:** V-abs. Note: one secondary source mislabels the venue as IJF; Crossref confirms *Journal of Forecasting*.

**48. Clements, M.P. & Krolzig, H.-M. (1998).** "A Comparison of the Forecast Performance of Markov-Switching and Threshold Autoregressive Models of US GNP." *Econometrics Journal* 1(1), C47–C75. DOI 10.1111/1368-423X.11004
- **URL:** Crossref
- **Summary:** MS and SETAR models capture business-cycle nonlinearity in sample. Out of sample they barely improve on linear AR models (from memory).
- **Relevance:** Fitting nonlinearity in sample does not mean it will help forecasts.
- **Status:** V-meta.

**49. Bessec, M. & Bouabdallah, O. (2005).** "What Causes the Forecasting Failure of Markov-Switching Models? A Monte Carlo Study." *Studies in Nonlinear Dynamics & Econometrics* 9(2). DOI 10.2202/1558-3708.1171
- **URL:** Semantic Scholar
- **Summary:** MS models fit better in sample than linear models but improve prediction only slightly. The main source of error is misclassifying future regimes.
- **Relevance:** Confirms Dacco and Satchell by simulation. Strong motivation for comparing how well regimes are classified in real time across ML and econometric methods.
- **Status:** V-abs.

---

### Synthesis

The literature agrees that regime switching captures the fat tails, volatility clustering, too-persistent GARCH volatility and time-varying higher moments that drive downside risk. It is also clear that the gain shows up mostly deep in the tail and at short horizons:
- Regime switching wins only at 1% VaR in Guidolin and Timmermann (2006).
- MRS-GARCH wins only under one week in Marcucci (2005).
- In Ardia et al. (2018), the clearest out-of-sample evidence, MS-GARCH beats single-regime models for individual stocks. For indices and FX the gain is weak or reversed once fat tails are allowed, and it is concentrated in 2008–2012.

Most rigorous MS-GARCH VaR/ES studies are properly real-time. They build the predictive mixture from Hamilton-filtered probabilities multiplied through the transition matrix, inside a rolling re-estimation window. Smoothed-probability leakage is therefore mainly a risk for papers that label regimes on the full sample, and for some recent preprints whose wording is ambiguous (Malim Franco & Hotta 2026).

The forecast-failure literature (Engel 1994; Dacco & Satchell 1999; Clements & Krolzig 1998; Bessec & Bouabdallah 2005) gives the mechanism: the value of regimes is destroyed by misclassifying regimes in real time. That makes the accuracy of real-time regime classification, rather than in-sample fit, the variable that matters.

**What the strand leaves open:**
- **No regime-switching joint VaR/ES framework that is evaluated against single-regime and ML-label alternatives under FZ/AL scoring.** ES-CAViaR (Taylor 2019) and FZ-based models (Patton, Ziegel & Chen 2019) have essentially no regime-switching versions. Gao et al. (2022) is the only one I found, and I could not read it.
- **No direct test of whether regimes estimated outside the risk model (e.g., HMMs, clustering, ML classifiers) add value over regimes built into the model (MS-GARCH) or observable thresholds (threshold CAViaR, smooth-transition HAR).**
- **No accounting for how quickly regimes are detected, or how they behave around breaks, as the driver of tail-forecast gains.**

Those are the gaps our paper can fill.

**Caveats:** These items should be checked against full text before you cite specifics:
- The V-meta summaries (Hamilton 1989, Hamilton & Susmel, Cai, Gray, Guidolin & Timmermann 2007/2008, Kim 1994, Kuester et al., Patton et al., Clements & Krolzig, MSGARCH JSS, Ardia et al. 2019 Bitcoin, Bauwens et al. 2010).
- Billio & Pelizzon (2000), whose summary comes from a secondary source.
- Gao et al. (2022), whose content I could not see at all.

I did not find verifiable sources for a regime-switching EVT ES-CAViaR or a threshold-HAR VaR paper beyond those listed above.