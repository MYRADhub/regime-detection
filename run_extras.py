"""Two extra analyses for the paper. Run: .venv/bin/python run_extras.py  (about 5 minutes)

1. Regulatory consequence: the Basel traffic light for 99% VaR on every rolling
   250-day window. Would hindsight change a regulator's verdict?
2. Mechanism: how many days the honest model needs to notice a stormy regime
   that hindsight sees immediately, and how much of the look-ahead premium comes
   from the days right after a regime switch.

Writes results/basel_traffic_light.csv, results/detection_delay.csv,
results/premium_near_switches.csv and paper/figure5_basel_zones.png/.pdf.
"""

import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
NEAR_SWITCH_DAYS = 20
ZONE_COLORS = {"green": "#0ca30c", "yellow": "#fab219", "red": "#d03b3b"}
INK, INK_2 = "#0b0b0b", "#52514e"


def main():
    basel_rows, delay_rows, near_rows = [], [], []
    sp_zones = {}

    for name, (ticker, cache) in INDICES.items():
        r = rv.load_returns(ticker, cache_path=cache)
        a, p_honest = rv.hmm_var_rolling(r, START, ALPHAS, return_probs=True)
        forecasts = {
            "A honest": a,
            "B future-trained": rv.hmm_var_full_sample(r, START, ALPHAS),
            "C retrospective": rv.hmm_var_full_sample(r, START, ALPHAS, smoothed=True),
            "Historical sim": rv.historical_var(r, START, ALPHAS),
            "GARCH-t": rv.garch_var(r, START, ALPHAS),
        }
        idx = a.index
        x = r.loc[idx]

        # 1. Basel traffic light (99% VaR)
        for m, f in forecasts.items():
            z = rv.basel_zones(rv.breaches(x, f["q1"]))
            if name == "S&P 500":
                sp_zones[m] = z
            share = z["zone"].value_counts(normalize=True)
            basel_rows.append(
                {
                    "index": name,
                    "method": m,
                    "windows": len(z),
                    "green %": 100 * share.get("green", 0),
                    "yellow %": 100 * share.get("yellow", 0),
                    "red %": 100 * share.get("red", 0),
                    "mean multiplier": z["multiplier"].mean(),
                }
            )

        # 2. Detection delay: hindsight (full-sample smoothed) vs real time
        model = rv.fit_hmm(r.to_numpy())
        means, sds, transmat, startprob = rv.hmm_params(model)
        smooth = pd.Series(model.predict_proba(r.to_numpy().reshape(-1, 1))[:, 1], index=r.index).loc[idx]
        filt = rv.filtered_probs(r.to_numpy(), means, sds, transmat, startprob)
        p_future = pd.Series(np.vstack([startprob, (filt @ transmat)[:-1]])[:, 1], index=r.index).loc[idx]
        for label, rt in [("A honest", p_honest), ("B future-trained", p_future)]:
            d = rv.detection_delays(smooth.to_numpy(), rt.to_numpy())
            delay_rows.append(
                {
                    "index": name,
                    "real-time model": label,
                    "stormy onsets (hindsight)": len(d),
                    "median delay (days)": float(np.median(d)) if d else np.nan,
                    "mean delay (days)": float(np.mean(d)) if d else np.nan,
                    "share caught within 5 days %": 100 * np.mean(np.array(d) <= 5) if d else np.nan,
                }
            )

        # 3. How much of the premium sits right after a regime switch?
        near = np.zeros(len(idx), dtype=bool)
        sm = smooth.to_numpy()
        switches = np.flatnonzero((sm[1:] >= 0.5) != (sm[:-1] >= 0.5)) + 1
        for t in switches:
            near[t : t + NEAR_SWITCH_DAYS] = True
        for a_lvl, col in [(0.05, "q5"), (0.01, "q1")]:
            la = rv.quantile_loss(x, forecasts["A honest"][col], a_lvl)
            lc = rv.quantile_loss(x, forecasts["C retrospective"][col], a_lvl)
            gap = la - lc
            near_rows.append(
                {
                    "index": name,
                    "VaR level": f"{int(round(100 * (1 - a_lvl)))}%",
                    "switches (hindsight)": len(switches),
                    "days near a switch %": 100 * near.mean(),
                    "share of premium from those days %": 100 * gap[near].sum() / gap.sum(),
                    "premium near switches %": 100 * (1 - lc[near].mean() / la[near].mean()),
                    "premium elsewhere %": 100 * (1 - lc[~near].mean() / la[~near].mean()),
                }
            )
        print("done:", name, flush=True)

    pd.DataFrame(basel_rows).round(2).to_csv("results/basel_traffic_light.csv", index=False)
    pd.DataFrame(delay_rows).round(2).to_csv("results/detection_delay.csv", index=False)
    pd.DataFrame(near_rows).round(2).to_csv("results/premium_near_switches.csv", index=False)

    # Figure 5: share of rolling 250-day windows in each Basel zone, S&P 500
    methods = list(sp_zones)
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    for i, m in enumerate(methods):
        share = sp_zones[m]["zone"].value_counts(normalize=True)
        left = 0.0
        for zone in ("green", "yellow", "red"):
            w = 100 * share.get(zone, 0)
            ax.barh(i, w, left=left, color=ZONE_COLORS[zone], edgecolor="white", linewidth=1.5, height=0.62,
                    label=zone.capitalize() if i == 0 else None)
            if w >= 7:
                ax.text(left + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=8, color=INK)
            left += w
    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods, color=INK_2)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of rolling 250-day windows", color=INK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(title="Basel zone (99% VaR breaches: green 0-4, yellow 5-9, red 10+)", loc="upper center",
              bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8, title_fontsize=8)
    fig.savefig("paper/figure5_basel_zones.png", dpi=300, bbox_inches="tight")
    fig.savefig("paper/figure5_basel_zones.pdf", bbox_inches="tight")

    pd.set_option("display.width", 220)
    for f in ("basel_traffic_light", "detection_delay", "premium_near_switches"):
        print(f"\n{f}\n", pd.read_csv(f"results/{f}.csv").to_string(index=False))


if __name__ == "__main__":
    main()
