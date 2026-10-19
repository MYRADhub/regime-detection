"""Regime-based Value-at-Risk with and without look-ahead bias.

All forecasts are one day ahead. A VaR forecast for day t is stored as the
return quantile q_t (a negative number, in percent). A "breach" happens when
the actual return r_t falls below q_t.

Three HMM versions differ only in how much future information they can see:
  A  honest          rolling refit on past data only, filtered probabilities
  B  future-trained  fit once on ALL data, filtered probabilities
  C  retrospective   fit once on ALL data, smoothed probabilities
B and C are deliberately biased. They exist only to measure the bias.
"""

import warnings

import numpy as np
import pandas as pd
from arch import arch_model
from hmmlearn.hmm import GaussianHMM
from scipy import optimize, stats

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------


def load_returns(ticker="^GSPC", start="1990-01-01", end="2026-01-01", cache_path=None):
    """Daily log returns in percent. Uses a CSV cache so Yahoo is hit only once."""
    if cache_path is not None:
        try:
            prices = pd.read_csv(cache_path, index_col=0, parse_dates=True).iloc[:, 0]
            return _to_returns(prices)
        except FileNotFoundError:
            pass

    import yfinance as yf

    data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    prices = data["Close"].squeeze().dropna()
    prices.name = "close"
    if cache_path is not None:
        prices.to_csv(cache_path)
    return _to_returns(prices)


def _to_returns(prices):
    returns = 100 * np.log(prices / prices.shift(1))
    returns = returns.dropna()
    returns.name = "return"
    return returns


# ---------------------------------------------------------------------------
# HMM helpers
# ---------------------------------------------------------------------------


def fit_hmm(x, n_regimes=2, n_starts=5, seed=0):
    """Fit a Gaussian HMM, trying several random starts and keeping the best.

    States are sorted by variance so that state 0 is always the calm regime.
    This keeps labels consistent across refits.
    """
    x = np.asarray(x, dtype=float).reshape(-1, 1)
    best, best_score = None, -np.inf
    for k in range(n_starts):
        model = GaussianHMM(
            n_components=n_regimes,
            covariance_type="diag",
            n_iter=200,
            tol=1e-4,
            random_state=seed + k,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(x)
            score = model.score(x)
        if np.isfinite(score) and score > best_score:
            best, best_score = model, score
    return _sort_states_by_variance(best)


def _sort_states_by_variance(model):
    order = np.argsort(model.covars_.ravel())
    model.startprob_ = model.startprob_[order]
    model.transmat_ = model.transmat_[np.ix_(order, order)]
    model.means_ = model.means_[order]
    model.covars_ = model.covars_.reshape(len(order), -1)[order]
    return model


def hmm_params(model):
    """Plain arrays: means, standard deviations, transition matrix, start probs."""
    means = model.means_.ravel()
    sds = np.sqrt(model.covars_.ravel())
    return means, sds, model.transmat_.copy(), model.startprob_.copy()


def filtered_probs(x, means, sds, transmat, startprob):
    """Forward filter: P(regime at day t | returns up to and including day t).

    Row t only uses x[0..t], so this never looks into the future.
    """
    x = np.asarray(x, dtype=float)
    dens = stats.norm.pdf(x[:, None], loc=means[None, :], scale=sds[None, :])
    alpha = np.empty_like(dens)
    prior = startprob
    for t in range(len(x)):
        a = prior * dens[t]
        total = a.sum()
        alpha[t] = a / total if total > 0 else np.full_like(a, 1 / len(a))
        prior = alpha[t] @ transmat
    return alpha


def mixture_quantile(alpha_level, weights, means, sds):
    """Return quantile q such that P(r < q) = alpha_level under the regime mixture."""

    def cdf_gap(q):
        return np.dot(weights, stats.norm.cdf((q - means) / sds)) - alpha_level

    lo = np.min(means - 12 * sds)
    hi = np.max(means + 12 * sds)
    return optimize.brentq(cdf_gap, lo, hi)


def _quantiles_from_weights(weights, means, sds, alphas):
    out = np.empty((len(weights), len(alphas)))
    for i, w in enumerate(weights):
        for j, a in enumerate(alphas):
            out[i, j] = mixture_quantile(a, w, means, sds)
    return out


# ---------------------------------------------------------------------------
# The three HMM versions
# ---------------------------------------------------------------------------


def hmm_var_full_sample(returns, forecast_start, alphas=(0.05, 0.01), smoothed=False, n_regimes=2, seed=0, smoothed_lag=False):
    """Versions B and C: fit the HMM once on ALL data (deliberately biased).

    smoothed=False -> Version B: the regime weights for day t are the filtered
                      probabilities up to day t-1, pushed one step forward.
    smoothed=True  -> Version C: the regime weights for day t are the smoothed
                      probabilities for day t itself, which use day t's return
                      and every later return (hindsight regime labels).
    smoothed_lag   -> milder Version C (robustness check): smoothed
                      probabilities for day t-1, pushed one step forward. Still
                      uses future returns, but not the hindsight label of day t.
    """
    x = returns.to_numpy()
    model = fit_hmm(x, n_regimes=n_regimes, seed=seed)
    means, sds, transmat, startprob = hmm_params(model)

    if smoothed and smoothed_lag:
        gamma = model.predict_proba(x.reshape(-1, 1))
        weights_all = np.vstack([startprob, (gamma @ transmat)[:-1]])
    elif smoothed:
        weights_all = model.predict_proba(x.reshape(-1, 1))
    else:
        alpha = filtered_probs(x, means, sds, transmat, startprob)
        predictive = alpha @ transmat
        weights_all = np.vstack([startprob, predictive[:-1]])

    mask = returns.index >= pd.Timestamp(forecast_start)
    q = _quantiles_from_weights(weights_all[mask], means, sds, alphas)
    return _as_frame(q, returns.index[mask], alphas)


def hmm_var_rolling(returns, forecast_start, alphas=(0.05, 0.01), window=1000, refit_every=21, n_regimes=2, seed=0):
    """Version A (honest): only past data is ever used.

    Every `refit_every` days the HMM is refit on the last `window` returns.
    Between refits the parameters stay fixed, and each day's regime weights
    come from the forward filter run up to the day before.
    """
    x = returns.to_numpy()
    index = returns.index
    first = int(np.searchsorted(index, pd.Timestamp(forecast_start)))
    if first < window:
        raise ValueError("forecast_start leaves fewer than `window` days of history")

    q_all = []
    for block_start in range(first, len(x), refit_every):
        block_end = min(block_start + refit_every, len(x))
        train = x[block_start - window : block_start]
        model = fit_hmm(train, n_regimes=n_regimes, seed=seed)
        means, sds, transmat, startprob = hmm_params(model)

        # Filter from the start of the training window up to the day before
        # the last forecast day of this block. Nothing at or after the
        # forecast day is used.
        seen = x[block_start - window : block_end - 1]
        alpha = filtered_probs(seen, means, sds, transmat, startprob)
        predictive = alpha @ transmat
        weights = predictive[window - 1 :]  # one row per forecast day in the block
        q_all.append(_quantiles_from_weights(weights, means, sds, alphas))

    q = np.vstack(q_all)
    return _as_frame(q, index[first:], alphas)


def _as_frame(q, index, alphas):
    return pd.DataFrame(q, index=index, columns=[f"q{int(round(100 * a))}" for a in alphas])


# ---------------------------------------------------------------------------
# Benchmarks
# ---------------------------------------------------------------------------


def historical_var(returns, forecast_start, alphas=(0.05, 0.01), window=250):
    """VaR = empirical quantile of the previous `window` returns."""
    out = {}
    for a in alphas:
        out[f"q{int(round(100 * a))}"] = returns.rolling(window).quantile(a).shift(1)
    frame = pd.DataFrame(out)
    return frame.loc[frame.index >= pd.Timestamp(forecast_start)]


def garch_var(returns, forecast_start, alphas=(0.05, 0.01), window=1000, refit_every=21):
    """GARCH(1,1) with Student-t errors, refit on the same schedule as Version A."""
    x = returns
    first = int(np.searchsorted(x.index, pd.Timestamp(forecast_start)))
    rows = []
    for block_start in range(first, len(x), refit_every):
        block_end = min(block_start + refit_every, len(x))
        train = x.iloc[block_start - window : block_start]
        res = arch_model(train, mean="Constant", vol="GARCH", p=1, q=1, dist="t").fit(disp="off")

        # Re-use the fitted parameters on data that runs to the day before the
        # block's last forecast day, then read off one-step-ahead forecasts.
        seen = x.iloc[block_start - window : block_end - 1]
        fixed = arch_model(seen, mean="Constant", vol="GARCH", p=1, q=1, dist="t").fix(res.params)
        fc = fixed.forecast(horizon=1, start=window - 1, reindex=False)
        mu = fc.mean.to_numpy().ravel()
        sigma = np.sqrt(fc.variance.to_numpy().ravel())
        nu = res.params["nu"]
        z = [fixed.model.distribution.ppf(a, [nu]) for a in alphas]
        rows.append(np.column_stack([mu + sigma * zj for zj in z]))

    q = np.vstack(rows)
    return _as_frame(q, x.index[first:], alphas)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def breaches(r, q):
    return (np.asarray(r) < np.asarray(q)).astype(int)


def quantile_loss(r, q, alpha):
    """Tick loss: lower is better. Penalises VaR that is too high or too low."""
    r, q = np.asarray(r), np.asarray(q)
    hit = (r < q).astype(float)
    return (alpha - hit) * (r - q)


def kupiec_test(hits, alpha):
    """Unconditional coverage: is the breach rate equal to alpha?"""
    hits = np.asarray(hits)
    n, x = len(hits), hits.sum()
    p_hat = x / n
    log_null = (n - x) * np.log(1 - alpha) + x * np.log(alpha)
    log_alt = _xlogy(n - x, 1 - p_hat) + _xlogy(x, p_hat)
    lr = -2 * (log_null - log_alt)
    return lr, 1 - stats.chi2.cdf(lr, df=1)


def christoffersen_test(hits, alpha):
    """Conditional coverage = correct breach rate AND no breach clustering."""
    hits = np.asarray(hits)
    lr_uc, _ = kupiec_test(hits, alpha)
    prev, curr = hits[:-1], hits[1:]
    n00 = np.sum((prev == 0) & (curr == 0))
    n01 = np.sum((prev == 0) & (curr == 1))
    n10 = np.sum((prev == 1) & (curr == 0))
    n11 = np.sum((prev == 1) & (curr == 1))
    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p = (n01 + n11) / max(n00 + n01 + n10 + n11, 1)
    log_null = _xlogy(n00 + n10, 1 - p) + _xlogy(n01 + n11, p)
    log_alt = _xlogy(n00, 1 - p01) + _xlogy(n01, p01) + _xlogy(n10, 1 - p11) + _xlogy(n11, p11)
    lr_ind = -2 * (log_null - log_alt)
    lr_cc = lr_uc + lr_ind
    return lr_cc, 1 - stats.chi2.cdf(lr_cc, df=2)


def diebold_mariano(loss_a, loss_b, lags=None):
    """Is model A's average loss different from model B's?

    Returns (statistic, two-sided p-value). Negative statistic = A is better.
    Uses Newey-West standard errors to allow for autocorrelation.
    """
    d = np.asarray(loss_a) - np.asarray(loss_b)
    n = len(d)
    if lags is None:
        lags = int(np.floor(n ** (1 / 3)))
    d_c = d - d.mean()
    var = np.dot(d_c, d_c) / n
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1)
        var += 2 * w * np.dot(d_c[k:], d_c[:-k]) / n
    stat = d.mean() / np.sqrt(var / n)
    return stat, 2 * (1 - stats.norm.cdf(abs(stat)))


def premium_with_ci(loss_honest, loss_biased, block=20, n_boot=2000, level=0.95, seed=0):
    """Look-ahead premium = % by which the biased model's average loss is lower.

    Returns (premium %, lower %, upper %). The confidence interval comes from a
    moving-block bootstrap: we resample blocks of `block` consecutive days, so
    that calm and stormy stretches stay together.
    """
    a, b = np.asarray(loss_honest, dtype=float), np.asarray(loss_biased, dtype=float)
    n = len(a)
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(n_boot, n_blocks))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n_boot, -1)[:, :n]
    boot = 100 * (1 - b[idx].mean(axis=1) / a[idx].mean(axis=1))
    tail = (1 - level) / 2
    lo, hi = np.quantile(boot, [tail, 1 - tail])
    return 100 * (1 - b.mean() / a.mean()), lo, hi


def _xlogy(x, y):
    return 0.0 if x == 0 else x * np.log(y)


def evaluate(returns, forecasts, alphas=(0.05, 0.01)):
    """One row per (method, VaR level) with every score."""
    rows = []
    for name, frame in forecasts.items():
        r = returns.loc[frame.index]
        for a in alphas:
            q = frame[f"q{int(round(100 * a))}"]
            ok = q.notna()
            hits = breaches(r[ok], q[ok])
            rows.append(
                {
                    "method": name,
                    "VaR level": f"{int(round(100 * (1 - a)))}%",
                    "days": int(ok.sum()),
                    "breach rate %": 100 * hits.mean(),
                    "target %": 100 * a,
                    "Kupiec p": kupiec_test(hits, a)[1],
                    "Christoffersen p": christoffersen_test(hits, a)[1],
                    "quantile loss": quantile_loss(r[ok], q[ok], a).mean(),
                }
            )
    return pd.DataFrame(rows)
