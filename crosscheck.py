"""Independent cross-check of the main numbers. Run: python crosscheck.py

1. GARCH-t: checks the t quantile, re-computes the volatility forecasts with a
   hand-written GARCH recursion, and re-runs GARCH-t with refits every 5 days.
2. HMM: re-builds Versions A, B and C with a different library
   (statsmodels MarkovRegression, fitted by maximum likelihood instead of EM).

Writes results/crosscheck.csv.
"""

import warnings

import numpy as np
import pandas as pd
from arch import arch_model
from scipy import stats
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

import regime_var as rv

warnings.filterwarnings("ignore")

START = "2005-01-03"
ALPHAS = (0.05, 0.01)
WINDOW, REFIT = 1000, 21


def garch_quantile_check():
    worst = 0.0
    for nu in (3.5, 5.0, 8.0, 30.0):
        dist = arch_model(np.zeros(10), dist="t").distribution
        for a in ALPHAS:
            arch_q = dist.ppf(a, [nu])
            manual = stats.t.ppf(a, nu) * np.sqrt((nu - 2) / nu)
            worst = max(worst, abs(arch_q - manual))
    return worst


def garch_recursion_check(r):
    """Hand-written GARCH(1,1) one-step volatility vs the arch package, one block."""
    first = int(np.searchsorted(r.index, pd.Timestamp(START)))
    train = r.iloc[first - WINDOW : first]
    res = arch_model(train, mean="Constant", vol="GARCH", p=1, q=1, dist="t").fit(disp="off")
    mu, omega, alpha, beta = res.params[["mu", "omega", "alpha[1]", "beta[1]"]]
    seen = r.iloc[first - WINDOW : first + REFIT - 1]
    fixed = arch_model(seen, mean="Constant", vol="GARCH", p=1, q=1, dist="t").fix(res.params)
    arch_sigma = np.sqrt(fixed.forecast(horizon=1, start=WINDOW - 1, reindex=False).variance.to_numpy().ravel())

    eps = seen.to_numpy() - mu
    backcast = np.sum(eps[:75] ** 2 * 0.94 ** np.arange(75)) / np.sum(0.94 ** np.arange(75))  # arch's default
    s2 = np.empty(len(eps) + 1)
    s2[0] = backcast
    for t in range(len(eps)):
        s2[t + 1] = omega + alpha * eps[t] ** 2 + beta * s2[t]
    manual_sigma = np.sqrt(s2[WINDOW:])
    return np.max(np.abs(arch_sigma - manual_sigma))


def statsmodels_fit(x, seed=0):
    mod = MarkovRegression(x, k_regimes=2, trend="c", switching_variance=True)
    np.random.seed(seed)
    res = mod.fit(search_reps=10, disp=False)
    return mod, res


def sm_params(res):
    """Means, sds, transition matrix P[i, j] = P(next = j | now = i), calm regime first."""
    p = dict(zip(res.model.param_names, res.params))
    means = np.array([p["const[0]"], p["const[1]"]])
    sds = np.sqrt(np.array([p["sigma2[0]"], p["sigma2[1]"]]))
    trans = res.model.regime_transition_matrix(res.params)[:, :, 0].T  # statsmodels stores [to, from]
    order = np.argsort(sds)
    return means[order], sds[order], trans[np.ix_(order, order)], order


def quantiles(weights, means, sds):
    return np.array([[rv.mixture_quantile(a, w, means, sds) for a in ALPHAS] for w in weights])


def statsmodels_versions(r):
    x = r.to_numpy()
    index = r.index
    first = int(np.searchsorted(index, pd.Timestamp(START)))

    # Version A: rolling refit, filtered probabilities with fixed parameters
    q_a = []
    for b in range(first, len(x), REFIT):
        e = min(b + REFIT, len(x))
        _, res = statsmodels_fit(x[b - WINDOW : b])
        means, sds, trans, order = sm_params(res)
        seen = x[b - WINDOW : e - 1]
        filt = MarkovRegression(seen, k_regimes=2, trend="c", switching_variance=True).filter(res.params)
        probs = filt.filtered_marginal_probabilities[:, order]
        q_a.append(quantiles((probs @ trans)[WINDOW - 1 :], means, sds))
    a = pd.DataFrame(np.vstack(q_a), index=index[first:], columns=["q5", "q1"])

    # Versions B and C: one fit on all data
    mod, res = statsmodels_fit(x)
    means, sds, trans, order = sm_params(res)
    filt = res.filtered_marginal_probabilities[:, order]
    smooth = res.smoothed_marginal_probabilities[:, order]
    pred = np.vstack([np.full(2, 0.5), (filt @ trans)[:-1]])
    b_ = pd.DataFrame(quantiles(pred[first:], means, sds), index=index[first:], columns=["q5", "q1"])
    c_ = pd.DataFrame(quantiles(smooth[first:], means, sds), index=index[first:], columns=["q5", "q1"])
    return {"A honest": a, "B future-trained": b_, "C retrospective": c_}


def main():
    r = rv.load_returns(cache_path="data/sp500.csv")
    print("GARCH t-quantile max difference:", garch_quantile_check())
    print("GARCH volatility recursion max difference:", garch_recursion_check(r))

    ours = {
        "A honest": rv.hmm_var_rolling(r, START, ALPHAS),
        "B future-trained": rv.hmm_var_full_sample(r, START, ALPHAS),
        "C retrospective": rv.hmm_var_full_sample(r, START, ALPHAS, smoothed=True),
        "GARCH-t": rv.garch_var(r, START, ALPHAS),
    }
    other = statsmodels_versions(r)
    other["GARCH-t"] = rv.garch_var(r, START, ALPHAS, refit_every=5)

    e1 = rv.evaluate(r, ours, ALPHAS).assign(implementation="ours (hmmlearn EM; GARCH refit 21d)")
    e2 = rv.evaluate(r, other, ALPHAS).assign(implementation="independent (statsmodels MLE; GARCH refit 5d)")
    out = pd.concat([e1, e2])[["implementation", "method", "VaR level", "breach rate %", "Kupiec p", "quantile loss"]]
    out.to_csv("results/crosscheck.csv", index=False)

    for impl, frames in [("ours", ours), ("independent", other)]:
        x = r.loc[frames["A honest"].index]
        for a, col in [(0.05, "q5"), (0.01, "q1")]:
            la = rv.quantile_loss(x, frames["A honest"][col], a)
            lc = rv.quantile_loss(x, frames["C retrospective"][col], a)
            lb = rv.quantile_loss(x, frames["B future-trained"][col], a)
            print(f"{impl:12s} {col}: C vs A {100 * (1 - lc.mean() / la.mean()):.1f}%   B vs A {100 * (1 - lb.mean() / la.mean()):.1f}%")
    pd.set_option("display.width", 200)
    print(out.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
