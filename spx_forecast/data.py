"""Load and align the raw index data."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Column in indices.csv -> short name used everywhere else
CLOSE_COLUMNS = {
    "SPXClose": "spx",
    "DAXClose": "dax",
    "FTSEClose": "ftse",
    "NikkeiClose": "nikkei",
}


def load_indices(path=None):
    """Daily closes for S&P 500, DAX, FTSE 100 and Nikkei 225, one row per SPX trading day."""
    if path is None:
        path = DATA_DIR / "indices.csv"
    raw = pd.read_csv(path, parse_dates=["Date"])
    df = raw[["Date"] + list(CLOSE_COLUMNS)].rename(columns=CLOSE_COLUMNS)
    df = df.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)

    # Foreign markets have different holidays. Carry their last known close forward
    # (never backward, so no future value can leak into an earlier row).
    df[["dax", "ftse", "nikkei"]] = df[["dax", "ftse", "nikkei"]].ffill()
    df = df.dropna(subset=["spx"]).reset_index(drop=True)
    return df


def load_vix(path=None):
    """CBOE VIX daily close from FRED (series VIXCLS)."""
    if path is None:
        path = DATA_DIR / "vix.csv"
    vix = pd.read_csv(path)
    vix["Date"] = pd.to_datetime(vix["Date"])
    vix = vix.rename(columns={"VIXCLS": "vix"})
    vix["vix"] = pd.to_numeric(vix["vix"], errors="coerce")
    return vix.sort_values("Date").reset_index(drop=True)


def load_data(use_vix=False):
    """Indices, optionally joined with VIX. VIX only goes back to 2020, so it shortens the history."""
    df = load_indices()
    if use_vix:
        vix = load_vix()
        df = df.merge(vix, on="Date", how="inner")
        df["vix"] = df["vix"].ffill()
        df = df.dropna(subset=["vix"]).reset_index(drop=True)
    return df
