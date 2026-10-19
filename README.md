# Does Look-Ahead Bias Fake Good Risk Forecasts?

Student research project: how much does look-ahead bias inflate the apparent performance of
machine-learning market regime models (a 2-regime hidden Markov model) in Value-at-Risk forecasting?

## Files

| File | What it is |
|---|---|
| `starter_notebook.ipynb` | Runs the whole experiment and draws the charts. Start here. |
| `regime_var.py` | All model code: the three HMM versions, the benchmarks and the scoring tests. |
| `tests/test_regime_var.py` | Checks, including proof that the honest version never uses future data. |
| `data/sp500.csv` | Cached S&P 500 prices (1990-2025), so everyone uses the same data. |
| `results/` | Tables (CSV) and charts (PNG) written by the notebook. |
| `literature/` | Literature-review notes. |

## Run it

Locally:

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest          # 16 tests, about 20 seconds
.venv/bin/jupyter notebook starter_notebook.ipynb
```

On Google Colab: upload `starter_notebook.ipynb`, `regime_var.py` and `data/sp500.csv`,
then run `!pip install hmmlearn arch yfinance` in the first cell.
