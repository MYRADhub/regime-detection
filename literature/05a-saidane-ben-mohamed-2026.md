# Deep read: Saidane & Ben Mohamed (2026)

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I could not get the full text of Saidane & Ben Mohamed (2026). Only the abstract and bibliographic metadata are readable, so most of items 2–9 cannot be answered from the paper itself. As a stand-in I read the methods, data and conclusion sections of the first author's 2024 precursor paper; I did not read all of it. Anything below drawn from that precursor is an inference about the 2026 paper, not something it states.

## 1. Access
- **Wiley** (`/doi/abs`, `/full`, `/pdf`, `/pdfdirect`, `/epdf`, `/full-xml`): every request returned HTTP 403, a bot block.
- **Unpaywall**: returned 422 because it rejects placeholder emails. I did not substitute a real email.
- **Semantic Scholar**: `openAccessPdf.url` is empty. The abstract is available.
- **OpenAlex**: `is_oa: False, oa_status: "closed", any_repository_has_fulltext: False`.
- **Crossref**: Wiley's standard VoR licence (not open access) plus a text-and-data-mining link that needs a Wiley token. Published 2026-04-16 in vol. 45, issue 6, pp. 2735–2759.
- **arXiv, SSRN, scholar.archive.org, web search**: no preprint or working-paper version. The ResearchGate profile of Ben Mohamed lists the paper but returned 403.
- **RePEc/IDEAS**: the abstract only, which restores a symbol the Semantic Scholar version drops: "strong Basel III compliance at **α=2.5%**".

**What the abstract establishes:**
- The model is "the mixture of hidden Markov factor analyzers (MHMFA)" for "jointly forecasting VaR and ES". It has a hidden Markov chain, latent factors, and "regime-specific Gaussian mixtures" in both the common and idiosyncratic components.
- Estimation is by EM. Forecasts come from "Monte Carlo simulation under a probabilistic soft-assignment scheme", which points to probability-weighted regimes rather than picking the single most likely regime.
- The evaluation is "large-scale out-of-sample" on a "six-cryptocurrency portfolio" across "multiple portfolio strategies and confidence levels". MHMFA "consistently outperforms all competing models" on the Patton–Ziegel–Chen (PZC) joint loss.
- Other claims: Basel III compliance at α=2.5%, a time-varying ES/VaR ratio, and "robust performance after transaction costs" for a risk-averse strategy.

## Proxy evidence: the precursor paper
Saidane, M. (2024), "Risk Assessment in Cryptocurrency Portfolios: a Composite Hidden Markov Factor Analysis Framework", *Stat. Optim. Inf. Comput.* 12, 463–487. Text: `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/saidane/precursor/p.txt`

- **Data (Sec. 4):** six cryptocurrencies (BTC, LTC, DASH, ETH, XRP, XLM) from Yahoo Finance, 2018-10-01 to 2022-09-30, 1,460 daily log-returns. "Six cryptocurrencies" matches the 2026 abstract, but I can't confirm the 2026 sample period.
- **Refit scheme (Sec. 4):** a one-day rolling window of 365 days, re-estimated every day. Training data is 2018-10-01 to 2019-09-30, and there are 1,095 out-of-sample VaR/ES forecasts (2019-10-01 to 2022-09-30).
- **Choosing regimes and factors (Sec. 4):** the number of factors and HMM states is picked by minimum BIC, "using the maximum likelihood principle on the rolling-window data sample (a window size of 365 trading days)". It is ambiguous whether BIC is re-run in every window or once. The paper then refers to a single "BIC-optimal CHMFA model" (Sec. 4.4), which suggests one fixed choice.
- **Regime inference:** in the E-step, the regime weights ξt come from "forward-backward recursions", so they are smoothed within the window. Monte Carlo forecasts use the regime "with the highest variational parameter, ξt" (Sec. 3.2, Steps 2–3), which is hard assignment, unlike the 2026 "soft-assignment". At the last observation in a window, smoothed and filtered probabilities coincide, so there is no future leakage. But I found no explicit statement that the transition matrix is applied to get a one-step-ahead predictive regime.
- **Look-ahead or real-time discussion:** none. A grep for "look-ahead", "bias", "smooth" and "real-time" found nothing relevant.
- **Preprocessing:** nothing about standardization. The descriptive statistics in Table 1 use the full sample.
- **Benchmarks:** only the author's own models (FAHMM, SSSM, CHFM, MFHMM). There are no GARCH, filtered historical simulation (FHS), CAViaR or ML benchmarks.
- **Evaluation (Sec. 4.5):** α = 1%, 2%, 5% and 10%, one-day horizon. VaR is tested with Kupiec UC, Christoffersen IND and CC, Engle–Manganelli DQ, Gaglianone VQ, the average quantile loss and the model confidence set (MCS). ES is tested with McF, NF and BD tests (Table 7). The precursor has no PZC/FZ0 loss and no Basel traffic light; the 2026 paper adds both.
- **Limitations stated (Sec. 5):** these are about extensions, namely time-varying idiosyncratic risk and non-homogeneous transition probabilities. Nothing about bias or leakage.

## 10. Overlap verdict: low to medium for the core contribution
**What they cover:**
- A regime model (HMM plus factors) producing out-of-sample joint VaR/ES forecasts for crypto.
- PZC joint loss, Basel compliance, multiple confidence levels, an economic evaluation.

This overlaps our "do regime models improve VaR/ES?" framing for crypto and HMM-type models.

**What they do not cover, as far as the abstract and precursor show:**
- **Look-ahead decomposition:** no sign of any. Neither text discusses look-ahead at all, which makes our "look-ahead premium" contribution look new relative to this line of work.
- **ML regime detectors:** none. No jump models, clustering, or supervised labels.
- **Assets:** crypto only, no multi-asset universe.
- **Benchmarks:** if the 2026 paper follows the precursor, it compares against the author's own family of models only, with no GARCH-family or FHS.

**Why not "low":**
- It is a 2026 *Journal of Forecasting* paper on regime-dependent joint VaR/ES forecasting with PZC. Referees will expect us to cite it and set ourselves apart.
- Its headline claim ("consistently outperforms all competing models") is exactly the kind of gain our paper asks whether leakage inflates.

**Possible look-ahead red flags to cite (unconfirmed for the 2026 paper):**
- **Possibly fixed model selection:** BIC picks the number of states and factors, and the precursor's reference to a single "BIC-optimal" model suggests the choice may have been made once rather than inside each window.
- **No stated filtered-versus-smoothed convention:** the authors never say whether forecasts use filtered or smoothed regime probabilities or how the transition matrix enters the forecast.
- **No statement on data timing or standardization.**

Cite these as "insufficiently documented real-time protocol", not as confirmed leakage. Their daily rolling 365-day re-estimation is actually a reasonably clean design.

**To close the gap:** get the PDF through institutional Wiley access (or interlibrary loan or the authors) and drop it into a new folder under `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/saidane/`. I can then answer items 2–9 exactly. The sections to check first are the soft-assignment forecasting step, how the number of regimes and factors is chosen, and the out-of-sample design.

Sources:
- [Wiley article page](https://onlinelibrary.wiley.com/doi/10.1002/for.70159)
- [RePEc/IDEAS listing](https://ideas.repec.org/a/wly/jforec/v45y2026i6p2735-2759.html)
- [Precursor PDF (Semantic Scholar)](https://pdfs.semanticscholar.org/50e3/0cd1efdf33d9a3f13a4ee68f6921d07b943e.pdf)
- [Ben Mohamed ResearchGate profile](https://www.researchgate.net/profile/Ben-Mohamed-Ezzeddine-2)
- [Precursor on ResearchGate](https://www.researchgate.net/publication/378382106_Risk_assessment_in_cryptocurrency_portfolios_a_composite_hidden_Markov_factor_analysis_framework)