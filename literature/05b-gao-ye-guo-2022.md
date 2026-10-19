# Deep read: Gao, Ye & Guo (2022)

Research agent output, retrieved 2026-10-15. Verification status is stated per entry.

I could not get the full text of Gao, Ye & Guo (2022), so I can't give you quoted sentences, page numbers, equations or result numbers. Everything below comes from the abstract, ScienceDirect's indexed summary as returned by web search, the paper's reference list, and how later papers describe it. Anything I inferred is labelled as such.

## 1. Access
- **Every legal open-access route is closed.** OpenAlex says `is_oa: False, oa_status: closed, any_repository_has_fulltext: False`. Semantic Scholar has no open-access PDF. ScienceDirect's full-text and abstract pages return 403, and the Elsevier text-mining API returns 400 without a key. ResearchGate returns 403. Google Scholar shows "All 3 versions", but every link leads to ScienceDirect or RePEc. I found no SSRN, arXiv or Chinese repository version, and no Chinese-language precursor.
- **Unpaywall refused the placeholder email** (HTTP 422, "Please use your own email address"). I did not substitute any other email.
- **What I did read:**
  - The abstract, verbatim, from RePEc/IDEAS: https://ideas.repec.org/a/eee/finlet/v48y2022ics1544612322001258.html
  - Fragments of ScienceDirect's summary that came back through web search.
  - The full reference list (26 entries) from the Crossref API.
  - How two later papers describe it: Wang & Xu (Research Square preprint rs-9287691), and the PLOS ONE 2025 paper 10.1371/journal.pone.0319008.
- I found no earlier working paper by the same authors on a regime-switching CAViaR. It looks like this letter introduced the model.

Key abstract sentences: "we construct a Markov regime-switching (MS) model in which the time-varying transition probability is driven by the information contained in asset price bubbles… Using daily Bitcoin data from 2013 to 2021, the results provide strong evidence of a form of regime change in Bitcoin's VaR and ES. Furthermore, the bubble index has a significant impact on tail risk and improves the model's ability to estimate and predict VaR and ES."

## 2. Data
- Daily Bitcoin data, 2013–2021.
- Price source, exact dates, the in-sample/out-of-sample split and the number of out-of-sample forecasts are all unknown (not in the abstract).

## 3. Model
- **Regimes are latent (a hidden Markov chain), not an observable threshold.** Transition probabilities vary over time, driven by a bubble index. The search summary says this setup follows Bauwens & Otranto (2016), and the bubble index comes from Wong (2011) "Market BuVaR".
- **Quantile level:** 5% according to the summary. I could not confirm whether other levels were used.
- **Number of regimes:** unstated in what I could see. Two is the likely default, but that is unconfirmed.
- **Estimation and ES form (inferred from the references):** the paper cites Taylor (2019), the asymmetric-Laplace approach to joint VaR/ES, and Fissler & Ziegel (2016). Wang & Xu put it in the "CAViaR-FZ literature". So the likely set-up is ES-CAViaR as in Taylor 2019, estimated by an asymmetric-Laplace likelihood, with ES tied to VaR through a multiplicative factor. I could not verify the exact ES form.
- It also cites Kim & Nelson (1999), which suggests a Hamilton/Kim filtering approach with maximum likelihood. Nothing points to MCMC.

## 4. Regime inference at forecast time, refitting, look-ahead
**Unknown on all three counts.** I found no wording on filtered, predictive or smoothed probabilities, on refitting, or on look-ahead. There are indirect signals:
- Kim & Nelson (1999) is cited. That book covers both the filter and the Kim smoother, so the citation doesn't settle which one they used.
- Nothing on forecast evaluation or data snooping is cited: no Diebold-Mariano, Hansen MCS or White reality check.
- Wong's BuVaR bubble index is built from price relative to a trailing average. If they computed it, or any detrending, over the full sample, that would be a preprocessing leak. This is unverified.

## 5. Benchmarks
From the summary: a single-regime ES-CAViaR, and a regime-switching CAViaR without the bubble index (constant transition probabilities). Nothing in the references points to GARCH or machine-learning benchmarks in the comparison.

## 6. Evaluation
Inferred from the references, not confirmed in the text:
- Christoffersen (1998) coverage tests for VaR.
- Acerbi & Szekely (2014) ES backtests.
- Fissler-Ziegel scoring, and possibly asymmetric-Laplace or FZ loss.
- Nolde & Ziegel (2017) on elicitability.

No DM, MCS or Patton-Ziegel-Chen (2019) is cited, so there was probably no formal test of predictive superiority. The horizon is probably one day ahead (unconfirmed).

## 7. Main results
Qualitative only. The bubble-driven model reportedly beats both benchmarks in-sample and out-of-sample. There is "strong evidence of… regime change in Bitcoin's VaR and ES", and the bubble index significantly affects tail risk. I could not get any numbers.

## 8. Limitations, judged from what's visible
- Bitcoin only, in a short letter format.
- Probably one quantile (5%).
- No sign of a formal predictive-ability testing framework.
- No visible discussion of real-time regime inference.
- The bubble covariate's real-time construction is unclear.
- The regimes are econometric (Markov switching), not machine-learning regimes.

## 9. Overlap verdict
**Low-to-medium threat. A regime-switching joint VaR/ES CAViaR for Bitcoin has already been done**, so we can't claim a regime-switching ES-CAViaR as new. Cite it as the closest econometric precedent.

It does not touch our lead contribution. Nothing visible decomposes forecast gains into look-ahead channels, compares real-time and ex-post regime inference, or uses machine-learning regimes or supervised labels.

**I would not cite look-ahead red flags against it from what we have.** The filtered-vs-smoothed choice, the refit scheme and the full-sample bubble index are all unverified. Citing them as flaws without the full text would be speculative. The defensible line is: "Prior regime-switching ES-CAViaR evidence (Gao et al., 2022) does not report whether regime probabilities and covariates are constructed in real time." Even that needs checking against the PDF.

To settle points 2–7, someone with institutional ScienceDirect access needs to pull the PDF (PII S1544612322001258). Put it in its own new folder under `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/gao/` and I can extract and answer the open items.

**One paper to check that may matter more than this one:** Lou, Zhang & Tian (2026), "Auditing weakly supervised cryptocurrency risk-state learning: when label fit, stability, and semantics disagree", Applied Intelligence, DOI 10.1007/s10489-026-07467-9. It cites Gao et al., and from the title alone it overlaps our "ex-post labels as supervised targets" and "label alignment across refits" channels. It is closed access and I couldn't read its abstract.

Sources:
- [IDEAS/RePEc abstract](https://ideas.repec.org/a/eee/finlet/v48y2022ics1544612322001258.html)
- [ScienceDirect (403)](https://www.sciencedirect.com/science/article/abs/pii/S1544612322001258)
- [PLOS ONE citing paper](https://doi.org/10.1371/journal.pone.0319008)
- [Wang & Xu preprint, Research Square](https://www.researchsquare.com/article/rs-9287691/latest.pdf)
- [Lou et al. 2026, Applied Intelligence](https://link.springer.com/article/10.1007/s10489-026-07467-9)

Local files are in `/private/tmp/claude-501/-Users-Murad-Projects-regime-detection/0f844751-cf40-4cd7-89b0-cbf2f9ffad7f/scratchpad/papers/gao/`, one subfolder per citing-paper download. None of them is the target paper.