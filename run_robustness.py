"""Robustness experiments. Run: python run_robustness.py  (about 15 minutes)

Writes:
  results/robustness_premium.csv     look-ahead premium with 95% bootstrap CIs
  results/robustness_evaluation.csv  every score for every experiment
"""

import os
import warnings

import pandas as pd

import regime_var as rv

warnings.filterwarnings("ignore")

FORECAST_START = "2005-01-03"
ALPHAS = (0.05, 0.01)
INDICES = {"S&P 500": "^GSPC", "FTSE 100": "^FTSE", "Nikkei 225": "^N225", "DAX": "^GDAXI"}

COMPARISONS = [
    ("C retrospective", "A honest"),
    ("C mild (lagged smoothed)", "A honest"),
    ("B future-trained", "A honest"),
    ("Historical sim", "A honest"),
    ("GARCH-t", "A honest"),
]


def hmm_versions(returns, window=1000, n_regimes=2, seed=0):
    return {
        "A honest": rv.hmm_var_rolling(returns, FORECAST_START, ALPHAS, window=window, n_regimes=n_regimes, seed=seed),
        "B future-trained": rv.hmm_var_full_sample(returns, FORECAST_START, ALPHAS, n_regimes=n_regimes, seed=seed),
        "C retrospective": rv.hmm_var_full_sample(returns, FORECAST_START, ALPHAS, smoothed=True, n_regimes=n_regimes, seed=seed),
        "C mild (lagged smoothed)": rv.hmm_var_full_sample(
            returns, FORECAST_START, ALPHAS, smoothed=True, smoothed_lag=True, n_regimes=n_regimes, seed=seed
        ),
    }


def premiums(returns, forecasts, experiment, setting):
    """Premium of each method over the honest HMM. Positive = lower loss than A."""
    rows = []
    honest = forecasts["A honest"]
    r = returns.loc[honest.index]
    for a in ALPHAS:
        col = f"q{int(round(100 * a))}"
        loss_a = rv.quantile_loss(r, honest[col], a)
        for other, _ in COMPARISONS:
            if other not in forecasts:
                continue
            loss_o = rv.quantile_loss(r, forecasts[other].loc[honest.index, col], a)
            est, lo, hi = rv.premium_with_ci(loss_a, loss_o)
            dm_stat, dm_p = rv.diebold_mariano(loss_o, loss_a)
            rows.append(
                {
                    "experiment": experiment,
                    "setting": setting,
                    "comparison": f"{other} vs A honest",
                    "VaR level": f"{int(round(100 * (1 - a)))}%",
                    "loss reduction vs A %": est,
                    "95% CI low": lo,
                    "95% CI high": hi,
                    "DM p-value": dm_p,
                }
            )
    return rows


def main():
    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    prem_rows, eval_frames = [], []

    def record(experiment, setting, returns, forecasts):
        prem_rows.extend(premiums(returns, forecasts, experiment, setting))
        ev = rv.evaluate(returns, forecasts, ALPHAS)
        ev.insert(0, "setting", setting)
        ev.insert(0, "experiment", experiment)
        eval_frames.append(ev)
        print(f"done: {experiment} / {setting}", flush=True)

    # 1. Same design on four stock indices
    sp500 = None
    for name, ticker in INDICES.items():
        cache = "data/sp500.csv" if ticker == "^GSPC" else f"data/{ticker.strip('^').lower()}.csv"
        returns = rv.load_returns(ticker, cache_path=cache)
        if ticker == "^GSPC":
            sp500 = returns
        forecasts = hmm_versions(returns)
        forecasts["Historical sim"] = rv.historical_var(returns, FORECAST_START, ALPHAS)
        forecasts["GARCH-t"] = rv.garch_var(returns, FORECAST_START, ALPHAS)
        record("indices", name, returns, forecasts)

    # 2. Honest version with a shorter and a longer training window (S&P 500)
    for window in (500, 1500):
        forecasts = hmm_versions(sp500, window=window)
        record("window", f"{window} days", sp500, forecasts)

    # 3. Different random starting points for the HMM fits (S&P 500)
    for seed in (10, 20, 30, 40):
        forecasts = hmm_versions(sp500, seed=seed)
        record("seed", f"seed {seed}", sp500, forecasts)

    # 4. Three regimes instead of two (S&P 500)
    forecasts = hmm_versions(sp500, n_regimes=3)
    record("regimes", "3 regimes", sp500, forecasts)

    prem = pd.DataFrame(prem_rows)
    prem.to_csv("results/robustness_premium.csv", index=False)
    pd.concat(eval_frames).to_csv("results/robustness_evaluation.csv", index=False)

    pd.set_option("display.width", 220)
    view = prem[prem["comparison"].str.startswith(("C retrospective", "B future", "GARCH"))]
    print(view.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
