"""Backtest every model against the naive baseline on a held-out, most-recent test period.

Run from the repo root:
    python -m spx_forecast.evaluate           # indices only, 1997-2025
    python -m spx_forecast.evaluate --vix     # adds VIX, 2020-2025 only
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_absolute_error

from spx_forecast.data import load_data
from spx_forecast.features import HORIZONS, feature_columns, make_dataset
from spx_forecast.models import chronological_split, make_models

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def to_price(today_price, log_return):
    return today_price * np.exp(log_return)


def score(today_price, true_return, pred_return):
    """MAE in index points plus how often the predicted direction was right."""
    actual = to_price(today_price, true_return)
    predicted = to_price(today_price, pred_return)
    mae = mean_absolute_error(actual, predicted)
    direction = float(np.mean(np.sign(pred_return) == np.sign(true_return)))
    return mae, direction


def p_value_vs_naive(today_price, true_return, pred_return, horizon):
    """Paired t-test: are the model's absolute errors really smaller than the naive baseline's?

    h-day targets overlap day to day, so only every h-th row is used to keep samples independent.
    """
    actual = to_price(today_price, true_return)
    model_err = np.abs(actual - to_price(today_price, pred_return))
    naive_err = np.abs(actual - today_price)
    diff = (model_err - naive_err)[::horizon]
    return float(stats.ttest_1samp(diff, 0.0).pvalue)


def run_backtest(use_vix=False, test_fraction=0.2):
    data = make_dataset(load_data(use_vix), use_vix)
    cols = feature_columns(data)
    rows = []

    for h in HORIZONS:
        target = f"target_{h}"
        train, test = chronological_split(data, h, test_fraction)
        today = test["spx"].to_numpy()
        truth = test[target].to_numpy()

        # Naive baseline: the price in h days equals today's price (a predicted return of 0).
        naive_mae, _ = score(today, truth, np.zeros_like(truth))
        always_up = float(np.mean(truth > 0))
        rows.append(result_row("Naive (no change)", h, train, test, naive_mae, naive_mae, always_up, None))

        for name, model in make_models().items():
            model.fit(train[cols], train[target])
            pred = model.predict(test[cols])
            mae, direction = score(today, truth, pred)
            p_value = p_value_vs_naive(today, truth, pred, h)
            rows.append(result_row(name, h, train, test, mae, naive_mae, direction, p_value))

    return pd.DataFrame(rows)


def result_row(model, horizon, train, test, mae, naive_mae, direction, p_value):
    return {
        "model": model,
        "horizon_days": horizon,
        "train_period": f"{train['Date'].min():%Y-%m-%d} to {train['Date'].max():%Y-%m-%d}",
        "test_period": f"{test['Date'].min():%Y-%m-%d} to {test['Date'].max():%Y-%m-%d}",
        "test_rows": len(test),
        "mae_points": round(mae, 2),
        "vs_naive_pct": round((mae / naive_mae - 1) * 100, 2),
        "direction_acc": round(direction, 3),
        "p_value_vs_naive": None if p_value is None else round(p_value, 3),
    }


def main():
    parser = argparse.ArgumentParser(description="Backtest S&P 500 forecasting models.")
    parser.add_argument("--vix", action="store_true", help="add VIX features (shortens history to 2020+)")
    args = parser.parse_args()

    results = run_backtest(use_vix=args.vix)
    RESULTS_DIR.mkdir(exist_ok=True)
    name = "backtest_vix" if args.vix else "backtest"
    results.to_csv(RESULTS_DIR / f"{name}.csv", index=False)

    with pd.option_context("display.width", 160, "display.max_columns", 20):
        print(results.drop(columns=["train_period"]).to_string(index=False))
    print(f"\nSaved results/{name}.csv")


if __name__ == "__main__":
    main()
