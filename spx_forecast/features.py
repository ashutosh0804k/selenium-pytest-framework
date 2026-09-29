"""Feature engineering and targets.

Rule for every feature: the value on row t may only use prices from day t or earlier.
Targets are the only columns allowed to look forward, and they are never used as inputs.
"""

import numpy as np
import pandas as pd

MARKETS = ["spx", "dax", "ftse", "nikkei"]
N_LAGS = 5
HORIZONS = [1, 2, 3, 4]


def log_return(prices):
    return np.log(prices).diff()


def add_lagged_returns(features, df, column, n_lags):
    """Returns for day t, t-1, ..., t-(n_lags-1)."""
    ret = log_return(df[column])
    for lag in range(n_lags):
        features[f"{column}_ret_lag{lag}"] = ret.shift(lag)


def build_features(df, use_vix=False):
    """One row per trading day with everything known at that day's close."""
    features = pd.DataFrame({"Date": df["Date"], "spx": df["spx"]})

    for market in MARKETS:
        add_lagged_returns(features, df, market, N_LAGS)

    spx_ret = log_return(df["spx"])
    features["spx_vol_10d"] = spx_ret.rolling(10).std()
    features["spx_vol_30d"] = spx_ret.rolling(30).std()
    features["spx_vs_ma20"] = df["spx"] / df["spx"].rolling(20).mean() - 1
    features["spx_vs_ma50"] = df["spx"] / df["spx"].rolling(50).mean() - 1

    if use_vix:
        features["vix"] = df["vix"]
        features["vix_change"] = log_return(df["vix"])

    return features


def add_targets(features, horizons=HORIZONS):
    """target_h = log(SPX close h trading days ahead / SPX close today)."""
    out = features.copy()
    log_price = np.log(out["spx"])
    for h in horizons:
        out[f"target_{h}"] = log_price.shift(-h) - log_price
    return out


def feature_columns(frame):
    skip = {"Date", "spx"}
    return [c for c in frame.columns if c not in skip and not c.startswith("target_")]


def make_dataset(df, use_vix=False, horizons=HORIZONS):
    """Features plus targets, with warm-up rows (rolling windows not full yet) removed.

    Rows at the very end have no future price, so their targets are NaN. They are kept
    here and dropped per horizon at training time, so the latest day is still available
    for forecasting.
    """
    data = add_targets(build_features(df, use_vix), horizons)
    cols = feature_columns(data)
    data = data.dropna(subset=cols).reset_index(drop=True)
    return data
