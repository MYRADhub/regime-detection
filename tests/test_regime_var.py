import numpy as np
import pandas as pd
import pytest
from scipy import stats

import regime_var as rv


def synthetic_returns(n=900, seed=1):
    """Calm/stormy regime-switching returns, in percent."""
    rng = np.random.default_rng(seed)
    state, out = 0, []
    for _ in range(n):
        if rng.random() < (0.02 if state == 0 else 0.05):
            state = 1 - state
        out.append(rng.normal(0.05, 0.7) if state == 0 else rng.normal(-0.1, 2.5))
    index = pd.bdate_range("2000-01-03", periods=n)
    return pd.Series(out, index=index, name="return")


@pytest.fixture(scope="module")
def returns():
    return synthetic_returns()


# --- scoring ---------------------------------------------------------------


def test_kupiec_exact_rate_gives_p_value_one():
    hits = np.zeros(100, dtype=int)
    hits[:5] = 1
    lr, p = rv.kupiec_test(hits, 0.05)
    assert lr == pytest.approx(0.0, abs=1e-10)
    assert p == pytest.approx(1.0)


def test_kupiec_rejects_far_too_many_breaches():
    hits = np.zeros(500, dtype=int)
    hits[:100] = 1  # 20% breaches at a 5% target
    assert rv.kupiec_test(hits, 0.05)[1] < 0.001


def test_kupiec_handles_zero_breaches():
    lr, p = rv.kupiec_test(np.zeros(250, dtype=int), 0.01)
    assert np.isfinite(lr) and 0 <= p <= 1


def test_christoffersen_flags_clustered_breaches():
    spread = np.zeros(1000, dtype=int)
    spread[::20] = 1  # 5% breaches, evenly spaced
    clustered = np.zeros(1000, dtype=int)
    clustered[:50] = 1  # 5% breaches, all in a row
    assert rv.christoffersen_test(spread, 0.05)[1] > 0.05
    assert rv.christoffersen_test(clustered, 0.05)[1] < 0.001


def test_quantile_loss_values():
    # breach: (0.05 - 1) * (-3 - -2) = 0.95 ; no breach: 0.05 * (1 - -2) = 0.15
    assert rv.quantile_loss([-3.0, 1.0], [-2.0, -2.0], 0.05) == pytest.approx([0.95, 0.15])


def test_diebold_mariano_sign_and_identical_inputs():
    rng = np.random.default_rng(0)
    base = rng.random(500)
    stat, p = rv.diebold_mariano(base, base + 0.5)
    assert stat < 0 and p < 0.001
    assert np.isnan(rv.diebold_mariano(base, base)[0])


# --- HMM pieces --------------------------------------------------------------


def test_states_sorted_calm_first(returns):
    model = rv.fit_hmm(returns.to_numpy())
    sds = np.sqrt(model.covars_.ravel())
    assert sds[0] < sds[1]


def test_filter_matches_hmmlearn_on_last_day(returns):
    # On the last day, filtered and smoothed probabilities are the same thing.
    x = returns.to_numpy()
    model = rv.fit_hmm(x)
    alpha = rv.filtered_probs(x, *rv.hmm_params(model))
    assert alpha[-1] == pytest.approx(model.predict_proba(x.reshape(-1, 1))[-1], abs=1e-6)


def test_mixture_quantile_single_regime_is_normal_quantile():
    q = rv.mixture_quantile(0.01, np.array([1.0, 0.0]), np.array([0.1, 0.0]), np.array([1.5, 3.0]))
    assert q == pytest.approx(stats.norm.ppf(0.01, 0.1, 1.5), abs=1e-8)


# --- look-ahead: the most important tests -------------------------------------


def _scramble_after(returns, day):
    changed = returns.copy()
    rng = np.random.default_rng(99)
    after = changed.index > day
    changed[after] = rng.normal(0, 5, after.sum())
    return changed


def test_honest_version_ignores_the_future(returns):
    """Version A's forecast for a day must not change if later data changes."""
    start = returns.index[300]
    check_day = returns.index[450]
    original = rv.hmm_var_rolling(returns, start, window=300, refit_every=40)
    altered = rv.hmm_var_rolling(_scramble_after(returns, check_day), start, window=300, refit_every=40)
    pd.testing.assert_frame_equal(original.loc[:check_day], altered.loc[:check_day])


def test_honest_version_ignores_the_same_day_return(returns):
    """The forecast for day t may only use returns up to day t-1."""
    start = returns.index[300]
    check_day = returns.index[450]
    changed = returns.copy()
    changed[check_day] = -20.0
    original = rv.hmm_var_rolling(returns, start, window=300, refit_every=40)
    altered = rv.hmm_var_rolling(changed, start, window=300, refit_every=40)
    assert original.loc[check_day].equals(altered.loc[check_day])


@pytest.mark.parametrize("smoothed", [False, True])
def test_biased_versions_do_use_the_future(returns, smoothed):
    """Sanity check of the experiment itself: B and C are expected to leak."""
    start = returns.index[300]
    check_day = returns.index[450]
    original = rv.hmm_var_full_sample(returns, start, smoothed=smoothed)
    altered = rv.hmm_var_full_sample(_scramble_after(returns, check_day), start, smoothed=smoothed)
    assert not np.allclose(original.loc[check_day], altered.loc[check_day])


def test_benchmarks_ignore_the_future(returns):
    start = returns.index[300]
    check_day = returns.index[450]
    changed = _scramble_after(returns, check_day)
    changed[check_day] = -20.0
    for fn, kwargs in [(rv.historical_var, {}), (rv.garch_var, {"window": 300, "refit_every": 40})]:
        original = fn(returns, start, **kwargs)
        altered = fn(changed, start, **kwargs)
        pd.testing.assert_frame_equal(original.loc[:check_day], altered.loc[:check_day])


def test_milder_retrospective_version_also_leaks(returns):
    start = returns.index[300]
    check_day = returns.index[450]
    original = rv.hmm_var_full_sample(returns, start, smoothed=True, smoothed_lag=True)
    altered = rv.hmm_var_full_sample(_scramble_after(returns, check_day), start, smoothed=True, smoothed_lag=True)
    assert not np.allclose(original.loc[check_day], altered.loc[check_day])


# --- bootstrap confidence interval ---------------------------------------------


def test_premium_ci_contains_estimate_and_detects_a_real_gap():
    rng = np.random.default_rng(3)
    honest = rng.exponential(1.0, 3000)
    biased = honest * 0.8  # biased model has 20% lower loss on every day
    est, lo, hi = rv.premium_with_ci(honest, biased)
    assert est == pytest.approx(20.0)
    assert lo <= est <= hi
    assert lo == pytest.approx(20.0) and hi == pytest.approx(20.0)


def test_premium_ci_covers_zero_when_there_is_no_gap():
    rng = np.random.default_rng(4)
    honest = rng.exponential(1.0, 3000)
    biased = rng.exponential(1.0, 3000)
    est, lo, hi = rv.premium_with_ci(honest, biased)
    assert lo < 0 < hi


# --- fat-tailed (empirical) regime distributions --------------------------------


def test_weighted_quantile_matches_plain_quantile_with_equal_weights():
    rng = np.random.default_rng(5)
    x = rng.normal(size=1000)
    q = rv.weighted_quantile(x, np.ones(1000), 0.05)
    assert q == np.sort(x)[49]


def test_empirical_honest_version_ignores_the_future(returns):
    start, check_day = returns.index[300], returns.index[450]
    kw = dict(window=300, refit_every=40, emission="empirical")
    original = rv.hmm_var_rolling(returns, start, **kw)
    altered = rv.hmm_var_rolling(_scramble_after(returns, check_day), start, **kw)
    pd.testing.assert_frame_equal(original.loc[:check_day], altered.loc[:check_day])
    changed = returns.copy()
    changed[check_day] = -20.0
    assert rv.hmm_var_rolling(changed, start, **kw).loc[check_day].equals(original.loc[check_day])


def test_empirical_versions_produce_valid_var(returns):
    start = returns.index[300]
    normal = rv.hmm_var_full_sample(returns, start)
    empirical = rv.hmm_var_full_sample(returns, start, emission="empirical")
    assert empirical.notna().all().all()
    assert (empirical["q1"] < empirical["q5"]).all()


# --- Basel traffic light and detection delay -----------------------------------


def test_basel_zones_boundaries():
    hits = np.zeros(260, dtype=int)
    hits[:4] = 1  # 4 breaches in the first window -> green
    z = rv.basel_zones(hits)
    assert z.loc[0, "zone"] == "green" and z.loc[0, "multiplier"] == 3.0
    hits[4:6] = 1  # 6 breaches -> yellow, plus factor 0.5
    z = rv.basel_zones(hits)
    assert z.loc[0, "zone"] == "yellow" and z.loc[0, "multiplier"] == pytest.approx(3.5)
    hits[6:12] = 1  # 12 breaches -> red, multiplier 4
    z = rv.basel_zones(hits)
    assert z.loc[0, "zone"] == "red" and z.loc[0, "multiplier"] == 4.0
    assert len(z) == 260 - 250 + 1


def test_detection_delay_counts_days_until_realtime_catches_up():
    ref = np.zeros(200)
    ref[100:150] = 1.0  # hindsight says the storm starts on day 100
    rt = np.zeros(200)
    rt[107:150] = 1.0  # real time only notices on day 107
    assert rv.stormy_onsets(ref) == [100]
    assert rv.detection_delays(ref, rt) == [7]
    assert rv.detection_delays(ref, np.zeros(200), max_delay=60) == [60]


def test_rolling_can_return_stormy_probabilities(returns):
    q, p = rv.hmm_var_rolling(returns, returns.index[300], window=300, refit_every=40, return_probs=True)
    assert p.index.equals(q.index)
    assert ((p >= 0) & (p <= 1)).all()


# --- shapes ------------------------------------------------------------------


def test_every_method_forecasts_every_day(returns):
    start = returns.index[300]
    expected = returns.index[300:]
    frames = [
        rv.hmm_var_rolling(returns, start, window=300, refit_every=40),
        rv.hmm_var_full_sample(returns, start),
        rv.hmm_var_full_sample(returns, start, smoothed=True),
        rv.historical_var(returns, start),
        rv.garch_var(returns, start, window=300, refit_every=40),
    ]
    for frame in frames:
        assert frame.index.equals(expected)
        assert list(frame.columns) == ["q5", "q1"]
        assert frame.notna().all().all()
        assert (frame["q1"] < frame["q5"]).all()  # 99% VaR is the bigger loss


def test_rolling_rejects_too_little_history(returns):
    with pytest.raises(ValueError):
        rv.hmm_var_rolling(returns, returns.index[100], window=300)
