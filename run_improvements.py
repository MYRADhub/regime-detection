"""Further checks for the paper. Run: python run_improvements.py  (about 10 minutes)

1. Fat-tailed HMM: each regime uses the actual distribution of returns instead
   of a normal curve. Does the look-ahead premium survive a better model?
2. Stability over time: the premium in four sub-periods.
3. Holm correction for the main Diebold-Mariano tests.

Writes results/fat_tail_evaluation.csv, results/fat_tail_premium.csv,
results/subperiod_premium.csv and results/dm_holm.csv.
"""

import warnings

import numpy as np
import pandas as pd

import regime_var as rv

warnings.filterwarnings("ignore")

START = "2005-01-03"
ALPHAS = (0.05, 0.01)
INDICES = {
    "S&P 500": ("^GSPC", "data/sp500.csv"),
    "FTSE 100": ("^FTSE", "data/ftse.csv"),
    "Nikkei 225": ("^N225", "data/n225.csv"),
    "DAX": ("^GDAXI", "data/gdaxi.csv"),
}
PERIODS = {
    "2005-2009": ("2005-01-01", "2009-12-31"),
    "2010-2014": ("2010-01-01", "2014-12-31"),
    "2015-2019": ("2015-01-01", "2019-12-31"),
    "2020-2025": ("2020-01-01", "2025-12-31"),
}


def holm(pvalues):
    """Holm step-down adjusted p-values."""
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adj[i] = min(running, 1.0)
    return adj


def level(a):
    return f"{int(round(100 * (1 - a)))}%"


def main():
    eval_frames, prem_rows, sub_rows, dm_rows = [], [], [], []

    for name, (ticker, cache) in INDICES.items():
        r = rv.load_returns(ticker, cache_path=cache)
        f = {
            "A honest": rv.hmm_var_rolling(r, START, ALPHAS),
            "B future-trained": rv.hmm_var_full_sample(r, START, ALPHAS),
            "C retrospective": rv.hmm_var_full_sample(r, START, ALPHAS, smoothed=True),
            "A honest (fat-tailed)": rv.hmm_var_rolling(r, START, ALPHAS, emission="empirical"),
            "B future-trained (fat-tailed)": rv.hmm_var_full_sample(r, START, ALPHAS, emission="empirical"),
            "C retrospective (fat-tailed)": rv.hmm_var_full_sample(r, START, ALPHAS, smoothed=True, emission="empirical"),
            "Historical sim": rv.historical_var(r, START, ALPHAS),
            "GARCH-t": rv.garch_var(r, START, ALPHAS),
        }
        idx = f["A honest"].index
        x = r.loc[idx]
        eval_frames.append(rv.evaluate(r, f, ALPHAS).assign(index=name))

        for a in ALPHAS:
            col = f"q{int(round(100 * a))}"
            loss = {m: rv.quantile_loss(x, fr.loc[idx, col], a) for m, fr in f.items()}

            # 1. premium for the fat-tailed model, and fat-tailed vs normal honest
            for biased, honest in [
                ("C retrospective (fat-tailed)", "A honest (fat-tailed)"),
                ("B future-trained (fat-tailed)", "A honest (fat-tailed)"),
                ("A honest (fat-tailed)", "A honest"),
                ("GARCH-t", "A honest (fat-tailed)"),
            ]:
                est, lo, hi = rv.premium_with_ci(loss[honest], loss[biased])
                prem_rows.append({"index": name, "VaR level": level(a), "comparison": f"{biased} vs {honest}",
                                  "loss reduction %": est, "95% CI low": lo, "95% CI high": hi,
                                  "DM p-value": rv.diebold_mariano(loss[biased], loss[honest])[1]})

            # 2. premium by sub-period (normal and fat-tailed)
            for period, (s, e) in PERIODS.items():
                m = (idx >= s) & (idx <= e)
                for biased, honest in [("C retrospective", "A honest"), ("C retrospective (fat-tailed)", "A honest (fat-tailed)")]:
                    est, lo, hi = rv.premium_with_ci(loss[honest][m], loss[biased][m])
                    sub_rows.append({"index": name, "period": period, "VaR level": level(a),
                                     "model": "fat-tailed" if "fat" in biased else "normal",
                                     "C vs A loss reduction %": est, "95% CI low": lo, "95% CI high": hi})

            # 3. main DM tests, S&P 500 only (Holm-corrected below)
            if name == "S&P 500":
                for first, second in [("C retrospective", "A honest"), ("B future-trained", "A honest"),
                                      ("A honest", "Historical sim"), ("A honest", "GARCH-t")]:
                    s_, p_ = rv.diebold_mariano(loss[first], loss[second])
                    dm_rows.append({"VaR level": level(a), "comparison": f"{first} vs {second}",
                                    "DM statistic": s_, "p-value": p_})
        print("done:", name, flush=True)

    dm = pd.DataFrame(dm_rows)
    dm["Holm-adjusted p"] = holm(dm["p-value"])
    dm.round(4).to_csv("results/dm_holm.csv", index=False)
    pd.concat(eval_frames).round(4).to_csv("results/fat_tail_evaluation.csv", index=False)
    pd.DataFrame(prem_rows).round(4).to_csv("results/fat_tail_premium.csv", index=False)
    pd.DataFrame(sub_rows).round(3).to_csv("results/subperiod_premium.csv", index=False)

    pd.set_option("display.width", 230)
    print(dm.round(4).to_string(index=False))
    ev = pd.concat(eval_frames)
    print(ev[ev["method"].str.contains("fat|GARCH|A honest$", regex=True)][["index", "method", "VaR level", "breach rate %", "Kupiec p", "quantile loss"]].round(3).to_string(index=False))
    print(pd.DataFrame(prem_rows).round(2).to_string(index=False))
    print(pd.DataFrame(sub_rows).round(1).pivot_table(index=["index", "model", "VaR level"], columns="period", values="C vs A loss reduction %").to_string())


if __name__ == "__main__":
    main()
