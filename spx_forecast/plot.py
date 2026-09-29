"""Chart the backtest: MAE by forecast horizon, each model next to the naive baseline.

Run after evaluate:
    python -m spx_forecast.plot
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

# Baseline is a neutral reference; the two models take categorical slots 1 and 2.
COLORS = {
    "Naive (no change)": "#9c9b94",
    "GradientBoosting": "#2a78d6",
    "Ridge": "#eb6834",
}
SURFACE = "#fcfcfb"
TEXT = "#1a1a19"
MUTED = "#6b6a63"


def plot_backtest(csv_name="backtest.csv", png_name="mae_by_horizon.png"):
    results = pd.read_csv(RESULTS_DIR / csv_name)
    horizons = sorted(results["horizon_days"].unique())
    models = list(COLORS)
    bar_width = 0.26

    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for i, model in enumerate(models):
        subset = results[results["model"] == model].set_index("horizon_days").loc[horizons]
        positions = [h + (i - 1) * bar_width for h in horizons]
        bars = ax.bar(
            positions,
            subset["mae_points"],
            width=bar_width,
            color=COLORS[model],
            edgecolor=SURFACE,
            linewidth=2,
            label=model,
            zorder=3,
        )
        if model == "Naive (no change)":
            for bar, value in zip(bars, subset["mae_points"]):
                ax.text(bar.get_x() + bar.get_width() / 2, value + 1, f"{value:.0f}",
                        ha="center", va="bottom", fontsize=8, color=MUTED)

    ax.set_xticks(horizons)
    ax.set_xticklabels([f"{h} day" if h == 1 else f"{h} days" for h in horizons])
    ax.set_ylabel("Mean absolute error (index points)", color=MUTED, fontsize=9)
    fig.text(0.015, 0.965, "Neither model meaningfully beats \"tomorrow = today\"",
             color=TEXT, fontsize=12, fontweight="bold", va="top")
    fig.text(0.015, 0.905, "S&P 500 test period Aug 2019 to Apr 2025, lower is better",
             color=MUTED, fontsize=9, va="top")

    ax.grid(axis="y", color="#e4e3dd", linewidth=0.8, zorder=0)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c0")
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=TEXT)

    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(RESULTS_DIR / png_name, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved results/{png_name}")


if __name__ == "__main__":
    plot_backtest()
