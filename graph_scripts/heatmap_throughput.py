"""
Heatmap: Throughput dominance zones (Stop Sign vs Traffic Light).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

SKIP_ROWS = 6


def generate(file_path, experiment_name):
    df = pd.read_csv(file_path, skiprows=SKIP_ROWS)
    df["total_throughput"] = df["fluxo-vermelhos"] + df["fluxo-azuis"]

    df_agg = df.groupby(["red-spawn", "blue-spawn", "method"])["total_throughput"].mean().reset_index()
    df_pivot = df_agg.pivot(index=["red-spawn", "blue-spawn"], columns="method", values="total_throughput").reset_index()

    # positive: stop sign moves more cars | negative: traffic light moves more cars
    df_pivot["throughput_difference"] = df_pivot["stop sign"] - df_pivot["red light"]

    heat_matrix = df_pivot.pivot(index="blue-spawn", columns="red-spawn", values="throughput_difference")
    heat_matrix = heat_matrix.sort_index(ascending=False)

    fig = plt.figure(figsize=(12, 8))
    ax = sns.heatmap(heat_matrix, cmap="RdBu", center=0, annot=False)

    plt.title("Throughput Dominance Zones: Stop Sign vs. Traffic Light", fontsize=16, fontweight="bold")
    plt.xlabel("Arterial Road Flow (red-spawn %)", fontsize=12)
    plt.ylabel("Secondary Road Flow (blue-spawn %)", fontsize=12)

    cbar = ax.collections[0].colorbar
    cbar.set_label("Throughput Advantage (Total Cars)", fontsize=12)

    # indicates which method each end of the scale represents
    cbar.ax.set_title("Stop Sign", fontweight="bold", color="#2980b9", pad=10)
    cbar.ax.text(
        0.5, -0.02, "Traffic Light", transform=cbar.ax.transAxes,
        ha="center", va="top", fontweight="bold", color="#e74c3c",
    )

    plt.tight_layout()

    output_name = f"heatmap_throughput_{experiment_name}.png"
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved as '{output_name}'")


if __name__ == "__main__":
    generate("StressTest3_Semaforo_Pare-table.csv", "experiment3")