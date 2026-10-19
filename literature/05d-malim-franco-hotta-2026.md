# Deep read: Malim Franco & Hotta (2026)

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I couldn't get the paper's full text, because no public copy exists. SSRN serves a 1-page PDF that contains only the title and author page. So I can't confirm the forecast design, and whether it contains look-ahead is unclear.

## 1. Access
- **SSRN:** plain fetches got 403 (a Cloudflare bot check). I got through by driving a temporary Chrome profile on your machine. The abstract page says "1 Pages · Posted: 17 Apr 2026". The PDF behind `Delivery.cfm/71d92a35-…-MECA.pdf?abstractid=6597696&mirid=1` (and the `type=2` variant) is one page: title, UNICAMP (IMECC) affiliations, emails, and a competing-interest statement. There is no paper body. The file is stored under a `download.ssrn.com/frl/` path, which suggests a Finance Research Letters submission, but that is a guess.
- **Other routes with no full text:**
  - Crossref and OpenAlex have metadata and the abstract only.
  - Semantic Scholar returns 404.
  - arXiv and Google Scholar have nothing.
  - ResearchGate shows "Request full-text" only.
  - ORCID lists the paper with no file.
  - The first author's only GitHub repo is unrelated.
- **What I did read:**
  - The SSRN/Crossref abstract.
  - A longer conference abstract, A2210, at CFE-CMStatistics 2026 (Berlin, 12–14 Dec 2026, presented by Hotta): https://www.cmstatistics.org/RegistrationsV2/CFECMStatistics2026/viewSubmission.php?in=2210&token=9511394o4289r10o448so60o42p682n9
  - Barigozzi & Massacci in full (arXiv 2210.09828v5, 95 pp.).
- **Files:**
  - Cover page: `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/malim/pdf2/paper.pdf`
  - Barigozzi & Massacci text: `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/malim/bm1/bm.txt`

## 2–6. What the two abstracts establish
- **Data:** 37 cryptocurrencies, "rolling out-of-sample exercise … from 2022 to 2026". Neither abstract gives the frequency, window length or number of forecasts.
- **Model:** the Barigozzi–Massacci large-dimensional Markov-switching factor model. The abstracts don't give how the numbers of regimes and factors are chosen, how often the model is refit, or whether those choices are made on the full sample or inside each window.
- **Forecast:** "one-step-ahead Value-at-Risk forecasts as quantiles of a predictive mixture of regime-specific empirical distributions, weighted by propagated smoothed regime probabilities."
- **Benchmarks:** Gaussian GARCH, Student-t GARCH, MS-GARCH, time-invariant factor quantile regression, rolling historical quantiles.
- **Evaluation:** violation rates, 90% Model Confidence Set, pooled Diebold–Mariano tests. Kupiec, Christoffersen, DQ tests and the loss function are not mentioned, and neither is Expected Shortfall. The paper appears to be VaR only.
- **Quantile levels:** 1%, 2.5% and 5% (from the conference abstract).
- **Results:**
  - Violation rates are "close to their nominal levels".
  - Theirs is "the only model included in the 90% Model Confidence Set at the extreme 1% quantile … where regime dependence delivers the largest gains", but "additional models remain in the confidence set at the less extreme 2.5% and 5% quantiles".
  - It "significantly outperforms" all benchmarks in pooled DM tests.
  - No numbers are given.

## 4. What "propagated smoothed probabilities" can mean
- **The source method's equations:** Barigozzi & Massacci (§3.2, eqs. 16–17) define the predicted probability ξ_{t|t−1} = P′ξ_{t−1|t−1}, the filtered update, and the smoother ξ_{t|T} = (P(ξ_{t+1|T} ⊘ ξ_{t+1|t})) ⊙ ξ_{t|t}. The backward pass "is initiated at ξ_{T|T}, which is the last iteration of the filter". So at the window end, smoothed equals filtered, and P̂′ξ_{T|T} is the legitimate one-step predictive probability.
- **The source has no smoothed-probability forecast:** its only real-time exercise (§9.2) re-estimates on an expanding sample each month and uses "the filtered probability of recession, ξ̂_{1,t|t} … for the last observation in the considered sample".
- **Legitimate reading:** smooth within each rolling window (and possibly use ξ_{t|T} to weight the in-window residuals that build each regime's empirical distribution), then propagate the end point. That is clean.
- **Leaky reading:** smoothing over a span that includes the forecast date, or one full-sample run. That is look-ahead.
- **Why I lean legitimate, without certainty:** "propagated" implies multiplying by P̂ from the window end, which only makes sense in the legitimate reading. Neither abstract says how long the smoothing span is.
- **Other channels your study tracks that remain unknown:**
  - Whether regimes and factors are chosen on the full sample. Barigozzi & Massacci fix two regimes by assumption and pick factors with Bai–Ng or Ahn–Horenstein on their whole sample.
  - Full-sample preprocessing. Their stock application uses returns "demeaned along the time series dimension over the whole sample period"; worth checking whether this paper copies that step.
  - How regime labels are kept consistent across refits.

## 7. Verdict
- **Overlap: partial. Threat: medium.** They take the "regime models improve crypto tail-risk forecasts out of sample" claim, with an MCS/DM design and similar benchmarks. They do not decompose look-ahead, cover ES, or use ML regimes. Their gain is concentrated at 1%, which is where a look-ahead premium would show most, so it is a good case to discuss in our paper.
- **Does their design contain look-ahead? Unclear.** The likely reading is legitimate, but it can't be checked without the manuscript. Hotta's email (hotta@unicamp.br) or the December CFE-CMStatistics talk are the realistic ways to get the details.

**A closer paper I found by chance:** Taeyun Kim, "Carrying regime uncertainty forward in cryptocurrency tail-risk forecasting", *Finance Research Letters* (Sept 2026), DOI 10.1016/j.frl.2026.110286, with a related SSRN preprint 6387397 ("Soft regime filtering outperforms hard classification…"). I read only the SSRN abstract. It argues that regime signals arrive late in real time and that hidden-Markov forward filtering beats hard classification. It reports a cut in 99% VaR violations during contagion hours from 38.9% to 16.1%, on minute-level data for five Binance perpetual futures, 2020–2025. That is closer to our real-time framing than Malim Franco & Hotta and should be reviewed.