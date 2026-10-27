"""Every table and figure for the paper. Run: python make_paper_results.py

Needs results/robustness_premium.csv and results/robustness_evaluation.csv
(run run_robustness.py first). Writes everything to paper/.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import regime_var as rv

warnings.filterwarnings("ignore")

FORECAST_START = "2005-01-03"
ALPHAS = (0.05, 0.01)
CRISES = {
    "2008 crisis": ("2008-09-01", "2009-06-30"),
    "COVID 2020": ("2020-02-15", "2020-06-30"),
    "2022 sell-off": ("2022-01-01", "2022-12-31"),
}
INDICES = {
    "S&P 500": ("^GSPC", "data/sp500.csv"),
    "FTSE 100": ("^FTSE", "data/ftse.csv"),
    "Nikkei 225": ("^N225", "data/n225.csv"),
    "DAX": ("^GDAXI", "data/gdaxi.csv"),
}
OUT = "paper"

# Validated categorical palette (dataviz reference, light mode), fixed order.
BLUE, ORANGE, AQUA, YELLOW, MAGENTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"
INK, INK_2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
METHOD_COLORS = {
    "A honest": BLUE,
    "B future-trained": AQUA,
    "C retrospective": ORANGE,
    "Historical sim": YELLOW,
    "GARCH-t": MAGENTA,
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": INK_2,
        "axes.labelcolor": INK,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "legend.frameon": False,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    }
)

tables_md = []


def save_table(df, name, title, note=""):
    df.to_csv(f"{OUT}/{name}.csv", index=False)
    tables_md.append(f"## {title}\n\n{df.to_markdown(index=False)}\n\n{note}\n")


def save_fig(fig, name):
    fig.savefig(f"{OUT}/{name}.png")
    fig.savefig(f"{OUT}/{name}.pdf")
    plt.close(fig)


def fmt_ci(est, lo, hi):
    return f"{est:.1f} [{lo:.1f}, {hi:.1f}]"


def main():
    os.makedirs(OUT, exist_ok=True)
    prem = pd.read_csv("results/robustness_premium.csv")
    rob_eval = pd.read_csv("results/robustness_evaluation.csv")

    # ---- Table 1: data summary -------------------------------------------------
    rows = []
    all_returns = {}
    for name, (ticker, cache) in INDICES.items():
        r = rv.load_returns(ticker, cache_path=cache)
        all_returns[name] = r
        oos = r.loc[FORECAST_START:]
        rows.append(
            {
                "Index": name,
                "First day": r.index[0].date(),
                "Last day": r.index[-1].date(),
                "Days (total)": len(r),
                "Days forecast": len(oos),
                "Mean %": r.mean(),
                "Std. dev. %": r.std(),
                "Min %": r.min(),
                "Max %": r.max(),
                "Skewness": stats.skew(r),
                "Excess kurtosis": stats.kurtosis(r),
            }
        )
    save_table(
        pd.DataFrame(rows).round(3),
        "table1_data_summary",
        "Table 1. Daily log returns (%), 1990-2025",
        "Forecast period starts 3 Jan 2005. Excess kurtosis > 0 means fatter tails than a normal distribution.",
    )

    # ---- S&P 500 forecasts (re-run, needed for the figures and splits) -----------
    r = all_returns["S&P 500"]
    forecasts = {
        "A honest": rv.hmm_var_rolling(r, FORECAST_START, ALPHAS),
        "B future-trained": rv.hmm_var_full_sample(r, FORECAST_START, ALPHAS),
        "C retrospective": rv.hmm_var_full_sample(r, FORECAST_START, ALPHAS, smoothed=True),
        "Historical sim": rv.historical_var(r, FORECAST_START, ALPHAS),
        "GARCH-t": rv.garch_var(r, FORECAST_START, ALPHAS),
    }
    idx = forecasts["A honest"].index
    ro = r.loc[idx]

    # ---- Table 2: fitted regimes (full sample, for description only) ------------
    model = rv.fit_hmm(r.to_numpy())
    means, sds, transmat, startprob = rv.hmm_params(model)
    smoothed = model.predict_proba(r.to_numpy().reshape(-1, 1))
    share = smoothed.mean(axis=0)
    save_table(
        pd.DataFrame(
            {
                "Regime": ["Calm", "Stormy"],
                "Mean daily return %": means.round(3),
                "Daily volatility %": sds.round(3),
                "Prob. of staying": np.diag(transmat).round(4),
                "Avg. length (days)": (1 / (1 - np.diag(transmat))).round(0),
                "Share of days %": (100 * share).round(1),
            }
        ),
        "table2_regimes",
        "Table 2. Two-regime HMM fitted on the full S&P 500 sample (description only)",
        "Fitted on all data, so it is used only to describe the regimes, never to forecast.",
    )

    # ---- Table 3: main results, S&P 500 ----------------------------------------
    ev = rv.evaluate(r, forecasts, ALPHAS)
    t3 = ev.rename(columns={"breach rate %": "Breach rate %", "quantile loss": "Quantile loss"})
    t3 = t3[["method", "VaR level", "Breach rate %", "target %", "Kupiec p", "Christoffersen p", "Quantile loss"]]
    t3.columns = ["Method", "VaR level", "Breach rate %", "Target %", "Kupiec p", "Christoffersen p", "Quantile loss"]
    save_table(
        t3.round(4),
        "table3_main_results",
        "Table 3. VaR forecasts for the S&P 500, 2005-2025 (5,283 days)",
        "B and C are deliberately biased. Lower quantile loss is better; Kupiec/Christoffersen p > 0.05 means the test does not reject.",
    )

    # ---- Table 4: look-ahead premium across indices ------------------------------
    p = prem[prem["experiment"] == "indices"].copy()
    keep = {
        "C retrospective vs A honest": "C vs A (total)",
        "C mild (lagged smoothed) vs A honest": "C mild vs A",
        "B future-trained vs A honest": "B vs A (parameters)",
    }
    p = p[p["comparison"].isin(keep)]
    p["cell"] = [
        fmt_ci(e, lo, hi) + ("*" if dm < 0.05 else "")
        for e, lo, hi, dm in zip(p["loss reduction vs A %"], p["95% CI low"], p["95% CI high"], p["DM p-value"])
    ]
    p["comparison"] = p["comparison"].map(keep)
    t4 = p.pivot_table(index="setting", columns=["comparison", "VaR level"], values="cell", aggfunc="first")
    t4 = t4.reindex(list(INDICES))
    t4.columns = [f"{c} {v}" for c, v in t4.columns]
    t4 = t4.reset_index().rename(columns={"setting": "Index"})
    order = ["Index"] + [f"{c} {v}" for c in keep.values() for v in ("95%", "99%")]
    save_table(
        t4[order],
        "table4_look_ahead_premium",
        "Table 4. Look-ahead premium: % lower quantile loss than the honest version, with 95% bootstrap CI",
        "Moving-block bootstrap, 20-day blocks, 2,000 resamples. * = Diebold-Mariano p < 0.05.",
    )

    # ---- Table 5: honest HMM vs benchmarks across indices ------------------------
    b = prem[(prem["experiment"] == "indices") & prem["comparison"].isin(["Historical sim vs A honest", "GARCH-t vs A honest"])].copy()
    b["Benchmark"] = b["comparison"].str.replace(" vs A honest", "", regex=False)
    b["Benchmark loss vs honest HMM %"] = [
        fmt_ci(-e, -hi, -lo) for e, lo, hi in zip(b["loss reduction vs A %"], b["95% CI low"], b["95% CI high"])
    ]
    b["DM p"] = b["DM p-value"].round(4)
    t5 = b.rename(columns={"setting": "Index"})[["Index", "Benchmark", "VaR level", "Benchmark loss vs honest HMM %", "DM p"]]
    save_table(
        t5.sort_values(["Benchmark", "VaR level", "Index"]),
        "table5_benchmarks",
        "Table 5. Benchmarks vs the honest HMM: % difference in quantile loss (positive = benchmark worse)",
        "Negative numbers mean the benchmark beats the honest HMM.",
    )

    # ---- Table 6: Diebold-Mariano tests, S&P 500 ---------------------------------
    pairs = [("C retrospective", "A honest"), ("B future-trained", "A honest"), ("A honest", "Historical sim"), ("A honest", "GARCH-t")]
    rows = []
    for a in ALPHAS:
        col = f"q{int(round(100 * a))}"
        for first, second in pairs:
            s, pv = rv.diebold_mariano(rv.quantile_loss(ro, forecasts[first][col], a), rv.quantile_loss(ro, forecasts[second][col], a))
            rows.append({"VaR level": f"{int(round(100 * (1 - a)))}%", "Comparison": f"{first} vs {second}", "DM statistic": round(s, 2), "p-value": round(pv, 4)})
    save_table(pd.DataFrame(rows), "table6_diebold_mariano", "Table 6. Diebold-Mariano tests on quantile loss, S&P 500", "Negative statistic = the first model has lower loss.")

    # ---- Table 7: crisis vs calm, S&P 500 -----------------------------------------
    crisis = pd.Series(False, index=idx)
    for s, e in CRISES.values():
        crisis.loc[s:e] = True
    rows = []
    for period, mask in [("Crisis", crisis), ("Calm", ~crisis)]:
        for a in ALPHAS:
            col = f"q{int(round(100 * a))}"
            losses = {m: rv.quantile_loss(ro[mask], f.loc[mask, col], a).mean() for m, f in forecasts.items()}
            for m, v in losses.items():
                rows.append(
                    {
                        "Period": period,
                        "Days": int(mask.sum()),
                        "VaR level": f"{int(round(100 * (1 - a)))}%",
                        "Method": m,
                        "Quantile loss": round(v, 4),
                        "% lower than A": round(100 * (1 - v / losses["A honest"]), 1),
                    }
                )
    save_table(
        pd.DataFrame(rows),
        "table7_crisis_vs_calm",
        "Table 7. Crisis vs calm periods, S&P 500",
        "Crisis = Sep 2008-Jun 2009, mid-Feb-Jun 2020, all of 2022.",
    )

    # ---- Table 8: robustness, S&P 500 ---------------------------------------------
    rr = prem[(prem["experiment"].isin(["window", "seed", "regimes"])) & (prem["comparison"].isin(["C retrospective vs A honest", "B future-trained vs A honest"]))].copy()
    base = prem[(prem["experiment"] == "indices") & (prem["setting"] == "S&P 500") & prem["comparison"].isin(["C retrospective vs A honest", "B future-trained vs A honest"])].copy()
    base["setting"] = "Main (1,000 days, seed 0, 2 regimes)"
    rr = pd.concat([base, rr])
    rr["cell"] = [fmt_ci(e, lo, hi) for e, lo, hi in zip(rr["loss reduction vs A %"], rr["95% CI low"], rr["95% CI high"])]
    rr["comparison"] = rr["comparison"].str.replace(" vs A honest", "", regex=False).str.split().str[0].map({"C": "C vs A", "B": "B vs A"})
    t8 = rr.pivot_table(index="setting", columns=["comparison", "VaR level"], values="cell", aggfunc="first")
    t8.columns = [f"{c} {v}" for c, v in t8.columns]
    t8 = t8.reindex(["Main (1,000 days, seed 0, 2 regimes)", "500 days", "1500 days", "seed 10", "seed 20", "seed 30", "seed 40", "3 regimes"])
    save_table(t8.reset_index().rename(columns={"setting": "Setting"}), "table8_robustness", "Table 8. Robustness of the look-ahead premium, S&P 500 (% lower loss, 95% CI)")

    # ---- Figure 1: returns and regime probabilities, 2007-2010 -------------------
    x = r.to_numpy()
    filt = pd.Series(rv.filtered_probs(x, means, sds, transmat, startprob)[:, 1], index=r.index)
    smth = pd.Series(smoothed[:, 1], index=r.index)
    win = slice("2007-01-01", "2010-12-31")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 4.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.1]})
    ax1.plot(r.loc[win], lw=0.5, color=INK_2)
    ax1.set_ylabel("Daily return (%)")
    ax1.set_title("S&P 500 daily returns", loc="left")
    ax2.plot(filt.loc[win], lw=0.9, color=BLUE, label="Filtered (real time)")
    ax2.plot(smth.loc[win], lw=1.6, color=ORANGE, label="Smoothed (hindsight)")
    ax2.set_ylim(-0.03, 1.03)
    ax2.set_ylabel("P(stormy regime)")
    ax2.set_title("Probability of the stormy regime", loc="left")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    fig.tight_layout()
    save_fig(fig, "figure1_regime_probabilities")

    # ---- Figure 2: VaR lines around 2008 ------------------------------------------
    win = slice("2007-06-01", "2009-12-31")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.plot(ro.loc[win], lw=0.5, color="#b3b2ad", label="Daily return")
    ax.plot(forecasts["A honest"].loc[win, "q1"], lw=1.4, color=BLUE, label="99% VaR, A honest")
    ax.plot(forecasts["C retrospective"].loc[win, "q1"], lw=1.4, color=ORANGE, label="99% VaR, C retrospective")
    ax.set_ylabel("%")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
    ax.set_ylim(-11, 12)
    save_fig(fig, "figure2_var_2008")

    # ---- Figure 3: look-ahead premium by index (point + 95% CI) -------------------
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True)
    names = list(INDICES)
    for ax, level in zip(axes, ["95%", "99%"]):
        for k, (comp, label, color) in enumerate(
            [("C retrospective vs A honest", "C vs A (total)", ORANGE), ("B future-trained vs A honest", "B vs A (parameters)", BLUE)]
        ):
            sub = prem[(prem["experiment"] == "indices") & (prem["comparison"] == comp) & (prem["VaR level"] == level)].set_index("setting").loc[names]
            y = np.arange(len(names)) + (0.15 if k == 0 else -0.15)
            ax.errorbar(
                sub["loss reduction vs A %"], y,
                xerr=[sub["loss reduction vs A %"] - sub["95% CI low"], sub["95% CI high"] - sub["loss reduction vs A %"]],
                fmt="o", ms=5, color=color, ecolor=color, elinewidth=1.4, capsize=0, label=label,
            )
        ax.axvline(0, color=INK_2, lw=0.8)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.set_title(f"{level} VaR", loc="left")
        ax.set_xlabel("% lower loss than honest version")
        ax.grid(axis="y", visible=False)
    axes[0].invert_yaxis()
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save_fig(fig, "figure3_premium_by_index")

    # ---- Figure 4: breach timeline, 99% VaR ----------------------------------------
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    order_m = list(forecasts)
    for i, m in enumerate(order_m):
        hits = rv.breaches(ro, forecasts[m]["q1"]).astype(bool)
        ax.scatter(idx[hits], np.full(hits.sum(), i), marker="|", s=60, color=METHOD_COLORS[m], linewidths=1.2)
        ax.text(idx[-1] + pd.Timedelta(days=60), i, f"{100 * hits.mean():.2f}%", va="center", fontsize=8, color=INK)
    ax.set_yticks(range(len(order_m)))
    ax.set_yticklabels(order_m)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.text(idx[-1] + pd.Timedelta(days=60), -0.45, "Breach rate", fontsize=8, color=INK_2, va="bottom")
    save_fig(fig, "figure4_breach_timeline")

    with open(f"{OUT}/tables.md", "w", encoding="utf-8") as fh:
        fh.write("# Paper tables\n\nGenerated by make_paper_results.py. Do not edit by hand; rerun the script.\n\n" + "\n".join(tables_md))
    print("wrote", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()
