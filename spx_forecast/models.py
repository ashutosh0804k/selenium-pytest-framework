"""Models, the naive baseline, and a leakage-safe train/test split."""

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_models():
    """Every model predicts a log return. Prices are rebuilt from the return afterwards."""
    gbr = GradientBoostingRegressor(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.8,
        random_state=42,
    )
    ridge = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    return {"GradientBoosting": gbr, "Ridge": ridge}


def chronological_split(data, horizon, test_fraction=0.2):
    """Oldest rows train, newest rows test, never shuffled.

    A gap of `horizon` rows is dropped between the two sets. Without it, the last training
    targets (which look `horizon` days ahead) would overlap prices inside the test period.
    """
    target = f"target_{horizon}"
    usable = data.dropna(subset=[target]).reset_index(drop=True)

    test_start = int(len(usable) * (1 - test_fraction))
    train_end = test_start - horizon

    train = usable.iloc[:train_end]
    test = usable.iloc[test_start:]
    return train, test
