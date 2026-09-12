"""
Grid chart: Average Delay and Total Throughput across scenario ratios (1:1 and 2:1).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

SKIP_ROWS = 6
COLORS = {"red light": "#e74c3c", "stop sign": "#2980b9"}


def generate(file_path, experiment_name):
    df = pd.read_csv(file_path, skiprows=SKIP_ROWS)

    df["total_throughput"] = df["fluxo-vermelhos"] + df["fluxo-azuis"]
    df["global_avg_delay"] = np.where(
        df["total_throughput"] > 0,
        (df["tempo-total-vermelhos"] + df["tempo-total-azuis"]) / df["total_throughput"],
        0,
    )

    scenarios = [
        {"name": "1:1 (Symmetric Flow)", "filter": df["red-spawn"] == df["blue-spawn"]},
        {"name": "2:1 (Main Avenue)", "filter": df["red-spawn"] == 2 * df["blue-spawn"]},
    ]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    fig.suptitle(
        "Intersection Analysis Across Different Ratios: Delay and Throughput",
        fontsize=18, fontweight="bold",
    )

    for i, scenario in enumerate(scenarios):
        df_filtered = df[scenario["filter"]]
        df_agg = (
            df_filtered.groupby(["red-spawn", "method"])[["global_avg_delay", "total_throughput"]]
            .mean()
            .reset_index()
        )

        sns.lineplot(
            data=df_agg, x="red-spawn", y="global_avg_delay", hue="method",
            ax=axes[i, 0], marker="o", linewidth=2.5, markersize=8, palette=COLORS,
        )
        axes[i, 0].set_title(f"Average Delay | {scenario['name']}")
        axes[i, 0].set_ylabel("Delay (Ticks)")
        axes[i, 0].set_xlabel("Main Road Density (Spawn %)")
        axes[i, 0].grid(True, linestyle="--", alpha=0.7)

        sns.lineplot(
            data=df_agg, x="red-spawn", y="total_throughput", hue="method",
            ax=axes[i, 1], marker="s", linewidth=2.5, markersize=8, palette=COLORS, legend=False,
        )
        axes[i, 1].set_title(f"Total Throughput | {scenario['name']}")
        axes[i, 1].set_ylabel("Total Cars Crossed")
        axes[i, 1].set_xlabel("Main Road Density (Spawn %)")
        axes[i, 1].grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.4)

    output_name = f"grid_chart_{experiment_name}.png"
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved as '{output_name}'")


if __name__ == "__main__":
    generate("StressTest3_Semaforo_Pare-table.csv", "experiment3")
