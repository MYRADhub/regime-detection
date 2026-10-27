# Does Look-Ahead Bias Fake Good Risk Forecasts?

This is a student research project about how fair it is to test a risk model.

## The idea in one minute

Banks try to predict how much money they could lose tomorrow. This number is called
**Value-at-Risk (VaR)**. A "99% VaR" is a loss that should only be beaten on 1 day out of 100.

Markets have calm periods and stormy periods. A popular model, the **hidden Markov model (HMM)**,
tries to guess which period we are in. It then uses that guess to set the VaR.

When you test an HMM on old data, there is a trap: the model can look at the whole history at once,
including days that are "in the future" for the day it is predicting. That is like taking a test with
the answer key open. It is called **look-ahead bias**.

We built three versions of the same model:

| Version | What it can see | Fair? |
|---|---|---|
| **A, honest** | Only the past. It is retrained every month on the last 1,000 days. | Yes |
| **B, future-trained** | Its settings were learned from all the data, including the future. | No |
| **C, retrospective** | Its settings and its guess about calm vs stormy both use the future. | No |

B and C cheat on purpose. We measure how much better the cheating makes the model look. We also
compare against two simple models that many banks use: **historical simulation** and **GARCH-t**.

## What we found

- With the cheat, the model's forecast error goes down by about **15%** (95% VaR) and **20-27%**
  (99% VaR). This holds for all four stock markets we tested.
- Almost all of that gain comes from knowing **which period** the market was in. Learning the model's
  settings from future data adds only a little.
- The cheating model hits the 1% target almost exactly. The honest model is beaten on about 2% of days.
- Under the bank regulator's "traffic light" test, the cheating model gets a green light in 84-95% of
  years. The honest model gets green in only 60-68%.
- The honest HMM is **not** better than the simple GARCH-t model. With the cheat, it looks just as
  good. So a cheating test can make a weak model look strong.
- The honest model needs a few days to notice that a storm has started. Most of the cheat's
  advantage comes from the days just after the market changes from calm to stormy, or back.

All numbers are in `paper/tables.md`. The full story is in `paper/WORK_SUMMARY.md`.

## What is in this folder

| File or folder | What it is |
|---|---|
| `starter_notebook.ipynb` | A notebook that runs the main experiment on the S&P 500 and draws charts. Good place to start. |
| `regime_var.py` | All the model code: the three HMM versions, the two simple models and the scoring. |
| `run_robustness.py` | Repeats the test on 4 markets and with different settings. About 15 minutes. |
| `run_extras.py` | Bank traffic-light test and "how fast does the model notice a storm". About 5 minutes. |
| `run_improvements.py` | A model with fatter tails, results by time period, and a stricter significance check. About 10 minutes. |
| `crosscheck.py` | Rebuilds the main results with a different library to check we made no mistake. |
| `make_paper_results.py` | Makes every table and figure for the paper. |
| `tests/` | 25 automatic checks. One of them proves the honest model never sees the future. |
| `data/` | Saved daily prices for the S&P 500, FTSE 100, Nikkei 225 and DAX (1990-2025). Everyone uses the same data. |
| `results/` | Result files (CSV), logs and charts written by the scripts. `results/RESULTS.md` explains every experiment in plain words. |
| `paper/` | Tables, figures, the paper outline (`draft_outline.md`) and the work summary (`WORK_SUMMARY.md`). Both also come as PDF. |
| `literature/` | Notes on the research papers we read. |

## How to run it

You need **Python 3.10 or newer**. Check with `python --version` (on Mac or Linux it may be `python3`).

All commands below are run from inside this folder.

### Step 1. Make a private Python environment

This keeps the project's packages separate from the rest of your computer.

**Windows (PowerShell or Command Prompt):**

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

**Mac or Linux:**

```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Step 2. Check that everything works

**Windows:**

```
.venv\Scripts\python -m pytest
```

**Mac or Linux:**

```
.venv/bin/python -m pytest
```

You should see `25 passed`. It takes about 20 seconds.

### Step 3. Open the notebook

**Windows:**

```
.venv\Scripts\python -m notebook starter_notebook.ipynb
```

**Mac or Linux:**

```
.venv/bin/python -m notebook starter_notebook.ipynb
```

A browser tab opens. Run the cells from top to bottom.

### Step 4 (optional). Rebuild every result for the paper

Run these in this order. On Windows, write `.venv\Scripts\python`. On Mac or Linux, write
`.venv/bin/python`. Both are shown as `PY` below.

```
PY run_robustness.py
PY run_extras.py
PY run_improvements.py
PY crosscheck.py
PY make_paper_results.py
```

The last one writes all tables and figures into `paper/`. Never change numbers in `paper/` by hand.
Change the code and run the script again.

### Tip: shorter commands

If you "activate" the environment first, you can just type `python`.

- Windows (Command Prompt): `.venv\Scripts\activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`. If Windows blocks it, run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.
- Mac or Linux: `source .venv/bin/activate`

### Running on Google Colab

Upload `starter_notebook.ipynb`, `regime_var.py` and the `data/` folder. In the first cell run
`!pip install hmmlearn arch yfinance`, then run the notebook.

## Common problems

| Problem | Fix |
|---|---|
| `python` is not found on Windows | Install Python from python.org and tick "Add Python to PATH". Or use `py` instead of `python`. |
| `No module named ...` | You are using the wrong Python. Use the `.venv` commands above, or activate the environment. |
| Prices are downloaded again | The scripts read `data/*.csv` first. Run them from this folder so they can find it. |
| Numbers differ in the last decimal | Different computers can give tiny differences in the model fitting. Differences in the main results should be well under one percentage point. |

## Words used in this project

- **VaR (Value-at-Risk):** a loss level that should only be beaten on a small share of days, like 1%.
- **Breach:** a day when the real loss was worse than the VaR.
- **Regime:** a market mood, here "calm" or "stormy".
- **Filtered probability:** the chance of a stormy market using only data up to today. This is fair.
- **Smoothed probability:** the same chance, but using all data, even the future. This is the cheat.
- **Quantile loss:** a score for VaR forecasts. Lower is better.
- **Look-ahead premium:** how much lower the cheating model's quantile loss is, in percent.
- **Basel traffic light:** the bank regulator's test. It counts breaches in a year: green (0-4),
  yellow (5-9) or red (10 or more).

## About the paper

We plan to submit to NHSJS. The journal does not allow AI-written text, so the authors write all
sentences in the paper themselves. `paper/draft_outline.md` gives them the facts and numbers to work
from.
