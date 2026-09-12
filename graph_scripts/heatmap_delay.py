"""
Heatmap: Delay dominance zones (Stop Sign vs Traffic Light).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

SKIP_ROWS = 6


def generate(file_path, experiment_name):
    df = pd.read_csv(file_path, skiprows=SKIP_ROWS)
    df["total_delay"] = (df["red-delay"] + df["blue-delay"]) / (
        df["red-throughput"] + df["blue-throughput"] + 0.0001
    )

    df_agg = df.groupby(["red-spawn", "blue-spawn", "method"])["total_delay"].mean().reset_index()
    df_pivot = df_agg.pivot(index=["red-spawn", "blue-spawn"], columns="method", values="total_delay").reset_index()

    # positive: advantage to stop sign | negative: advantage to traffic light
    df_pivot["delay_difference"] = df_pivot["red light"] - df_pivot["stop sign"]

    heat_matrix = df_pivot.pivot(index="blue-spawn", columns="red-spawn", values="delay_difference")
    heat_matrix = heat_matrix.sort_index(ascending=False)

    fig = plt.figure(figsize=(12, 8))

    vmin_lock, vmax_lock = -15, 50
    ax = sns.heatmap(heat_matrix, cmap="RdBu", center=0, annot=False, vmin=vmin_lock, vmax=vmax_lock)

    plt.title("Delay Dominance Zones: Stop Sign vs. Traffic Light", fontsize=16, fontweight="bold", pad=15)
    plt.xlabel("Arterial Road Flow (red-spawn %)", fontsize=12)
    plt.ylabel("Secondary Road Flow (blue-spawn %)", fontsize=12)

    cbar = ax.collections[0].colorbar
    cbar.set_label("Advantage (Ticks Saved)", fontsize=12)

    exact_ticks = [-10, 0, 10, 20, 30, 40, 50]
    cbar.set_ticks(exact_ticks)
    cbar.set_ticklabels([str(abs(t)) for t in exact_ticks])

    cbar.ax.set_title("Stop", fontweight="bold", color="#1e5b8e", pad=10)
    cbar.ax.text(
        0.5, -0.02, "Traffic Light", transform=cbar.ax.transAxes,
        ha="center", va="top", fontweight="bold", color="#d35400",
    )

    plt.tight_layout()

    output_name = f"heatmap_delay_{experiment_name}.png"
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved as '{output_name}'")


if __name__ == "__main__":
    generate("StressTest3_Semaforo_Pare-table.csv", "experiment3")
