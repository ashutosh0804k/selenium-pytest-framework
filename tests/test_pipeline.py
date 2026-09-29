"""End-to-end checks against the real dataset in data/."""

import pandas as pd

from spx_forecast.data import load_data
from spx_forecast.features import feature_columns, make_dataset
from spx_forecast.forecast import forecast


def test_real_data_has_no_gaps_in_features():
    data = make_dataset(load_data())
    assert len(data) > 6000
    assert not data[feature_columns(data)].isna().any().any()
    assert data["Date"].is_monotonic_increasing
    assert data["Date"].is_unique


def test_forecast_starts_after_last_real_close():
    last_date, last_price, result = forecast("Ridge")
    assert len(result) == 4
    dates = pd.to_datetime(result["date"])
    assert dates.min() > last_date
    assert dates.is_monotonic_increasing
    assert (dates.dt.dayofweek < 5).all()
    # A 1-4 day forecast should stay within a sane band of the last close.
    assert result["predicted_spx"].between(last_price * 0.8, last_price * 1.2).all()
