"""Forecast the next 1-4 trading days from the latest close in the data.

Run from the repo root:
    python -m spx_forecast.forecast
    python -m spx_forecast.forecast --model Ridge
"""

import argparse

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay

from spx_forecast.data import load_data
from spx_forecast.features import HORIZONS, feature_columns, make_dataset
from spx_forecast.models import make_models


def forecast(model_name="GradientBoosting", use_vix=False):
    """One model per horizon (direct forecasting), each trained on all history.

    Direct forecasting avoids feeding a predicted price back in as a lag, which is how
    errors compound in recursive forecasts.
    """
    data = make_dataset(load_data(use_vix), use_vix)
    cols = feature_columns(data)
    latest = data.iloc[[-1]]
    last_date = latest["Date"].iloc[0]
    last_price = latest["spx"].iloc[0]

    rows = []
    for h in HORIZONS:
        target = f"target_{h}"
        train = data.dropna(subset=[target])
        model = make_models()[model_name]
        model.fit(train[cols], train[target])
        pred_return = model.predict(latest[cols])[0]
        rows.append({
            # Business days only. Exchange holidays are not modeled, so check the calendar.
            "date": (last_date + BDay(h)).date(),
            "horizon_days": h,
            "predicted_spx": round(last_price * np.exp(pred_return), 2),
            "predicted_change_pct": round((np.exp(pred_return) - 1) * 100, 3),
        })

    return last_date, last_price, pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Forecast the S&P 500 close 1-4 trading days ahead.")
    parser.add_argument("--model", default="GradientBoosting", choices=list(make_models()))
    parser.add_argument("--vix", action="store_true", help="add VIX features (shortens history to 2020+)")
    args = parser.parse_args()

    last_date, last_price, result = forecast(args.model, args.vix)
    print(f"Last close in data: {last_date:%Y-%m-%d}  SPX {last_price:,.2f}  (model: {args.model})\n")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
