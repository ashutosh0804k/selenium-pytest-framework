import numpy as np
import pandas as pd
import pytest


def make_prices(n_days=200, seed=0):
    """Synthetic daily closes for all four markets, shaped like the real loaded data."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-01", periods=n_days)
    df = pd.DataFrame({"Date": dates})
    start = {"spx": 3000.0, "dax": 13000.0, "ftse": 7000.0, "nikkei": 23000.0}
    for market, price in start.items():
        returns = rng.normal(0.0003, 0.01, n_days)
        df[market] = price * np.exp(np.cumsum(returns))
    return df


@pytest.fixture
def prices():
    return make_prices()
