"""
Throughput comparison: Main road vs secondary road in the 2:1 scenario.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

SKIP_ROWS = 6
COLORS = {"red light": "#e74c3c", "stop sign": "#2980b9"}


def generate(file_path, experiment_name):
    df = pd.read_csv(file_path, skiprows=SKIP_ROWS)

    df_21 = df[df["red-spawn"] == 2 * df["blue-spawn"]]
    df_agg = (
        df_21.groupby(["red-spawn", "method"])[["red-throughput", "blue-throughput"]]
        .mean()
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Throughput Analysis: Starvation in the 2:1 Scenario", fontsize=16, fontweight="bold", y=1.05)

    sns.lineplot(
        data=df_agg, x="red-spawn", y="fluxo-vermelhos", hue="method", ax=axes[0],
        marker="o", linewidth=2.5, palette=COLORS,
    )
    axes[0].set_title("Main Road (Privileged)", fontsize=14)
    axes[0].set_ylabel("Cars Crossed")
    axes[0].set_xlabel("Main Road Density (Spawn %)")
    axes[0].grid(True, linestyle="--", alpha=0.7)

    sns.lineplot(
        data=df_agg, x="red-spawn", y="fluxo-azuis", hue="method", ax=axes[1],
        marker="s", linewidth=2.5, palette=COLORS, legend=False,
    )
    axes[1].set_title("Secondary Road (Penalized)", fontsize=14)
    axes[1].set_ylabel("Cars Crossed")
    axes[1].set_xlabel("Main Road Density (Spawn %)")
    axes[1].grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()

    output_name = f"throughput_comparison_{experiment_name}.png"
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved as '{output_name}'")


if __name__ == "__main__":
    generate("StressTest3_Semaforo_Pare-table.csv", "experiment3")
