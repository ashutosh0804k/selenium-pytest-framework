import numpy as np
import pytest

from spx_forecast.evaluate import p_value_vs_naive, score
from spx_forecast.features import HORIZONS, make_dataset
from spx_forecast.models import chronological_split


@pytest.mark.parametrize("h", HORIZONS)
def test_split_is_chronological_with_purge_gap(prices, h):
    data = make_dataset(prices)
    train, test = chronological_split(data, h)

    assert train["Date"].max() < test["Date"].min()
    # Positions in the usable (non-NaN target) frame: at least h rows must sit between the sets
    gap = test.index.min() - train.index.max() - 1
    assert gap >= h


@pytest.mark.parametrize("h", HORIZONS)
def test_training_targets_never_reach_into_test_period(prices, h):
    data = make_dataset(prices)
    usable = data.dropna(subset=[f"target_{h}"]).reset_index(drop=True)
    train, test = chronological_split(data, h)
    # The last training target looks h rows ahead. That price must be before the first test day.
    last_train_target_date = usable.loc[train.index.max() + h, "Date"]
    assert last_train_target_date < test["Date"].min()


def test_split_is_never_shuffled(prices):
    train, test = chronological_split(make_dataset(prices), 1)
    assert train["Date"].is_monotonic_increasing
    assert test["Date"].is_monotonic_increasing


def test_naive_mae_is_mean_absolute_price_move():
    today = np.array([100.0, 200.0])
    true_return = np.log(np.array([110.0 / 100.0, 190.0 / 200.0]))
    mae, _ = score(today, true_return, np.zeros(2))
    assert mae == pytest.approx(10.0)


def test_perfect_model_scores_zero_error_and_full_direction():
    today = np.array([100.0, 100.0, 100.0])
    true_return = np.array([0.01, -0.02, 0.005])
    mae, direction = score(today, true_return, true_return)
    assert mae == pytest.approx(0.0)
    assert direction == 1.0


def test_identical_model_to_naive_is_not_significant():
    rng = np.random.default_rng(1)
    today = np.full(100, 100.0)
    true_return = rng.normal(0, 0.01, 100)
    tiny_noise = rng.normal(0, 1e-6, 100)
    assert p_value_vs_naive(today, true_return, tiny_noise, 1) > 0.05
