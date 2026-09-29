"""Leakage tests: nothing known after day t may show up in day t's features."""

import numpy as np
import pandas as pd
import pytest

from spx_forecast.data import load_indices
from spx_forecast.features import HORIZONS, add_targets, build_features, feature_columns, make_dataset


def test_features_do_not_change_when_future_prices_change(prices):
    cutoff = 120
    original = build_features(prices)

    shocked = prices.copy()
    # Crash every market after the cutoff. If any feature peeks ahead, rows <= cutoff will move.
    shocked.loc[cutoff + 1:, ["spx", "dax", "ftse", "nikkei"]] *= 0.5
    after_shock = build_features(shocked)

    cols = feature_columns(original)
    pd.testing.assert_frame_equal(original.loc[:cutoff, cols], after_shock.loc[:cutoff, cols])


def test_features_do_change_when_past_prices_change(prices):
    """Sanity check for the test above: the shock must be visible from its own row onward."""
    cutoff = 120
    shocked = prices.copy()
    shocked.loc[cutoff + 1:, "spx"] *= 0.5
    before = build_features(prices).loc[cutoff + 1, "spx_ret_lag0"]
    after = build_features(shocked).loc[cutoff + 1, "spx_ret_lag0"]
    assert before != after


@pytest.mark.parametrize("h", HORIZONS)
def test_target_is_log_return_h_days_ahead(prices, h):
    data = add_targets(build_features(prices))
    i = 50
    expected = np.log(prices.loc[i + h, "spx"] / prices.loc[i, "spx"])
    assert data.loc[i, f"target_{h}"] == pytest.approx(expected)


def test_targets_are_never_used_as_features(prices):
    cols = feature_columns(make_dataset(prices))
    assert not any(c.startswith("target_") for c in cols)
    assert "spx" not in cols  # raw price level is not stationary, only returns go in


def test_latest_day_is_kept_for_forecasting(prices):
    data = make_dataset(prices)
    assert data["Date"].iloc[-1] == prices["Date"].iloc[-1]
    assert data["target_1"].isna().iloc[-1]
    assert not data[feature_columns(data)].iloc[-1].isna().any()


def test_foreign_holidays_are_filled_forward_not_backward(tmp_path):
    csv = tmp_path / "indices.csv"
    csv.write_text(
        "Date,SPXClose,DAXClose,FTSEClose,NikkeiClose\n"
        "2024-01-02,100,200,300,400\n"
        "2024-01-03,101,,301,401\n"
        "2024-01-04,102,999,302,402\n"
    )
    df = load_indices(csv)
    # The missing DAX day must reuse the previous close (200), never the next one (999).
    assert df.loc[1, "dax"] == 200
