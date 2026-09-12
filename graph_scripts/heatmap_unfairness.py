"""
Heatmap pair: Fairness index (demand ratio vs throughput ratio) for both methods.

Unfairness Index explanation:
    demand_ratio = red-spawn / blue-spawn
        How many times more cars are being spawned on the main road
        compared to the secondary road (the "expected" ratio).

    throughput_ratio = red-throughput / blue-throughput
        How many times more cars actually crossed on the main road
        compared to the secondary road (the "real" ratio).

    unfairness_index = throughput_ratio - demand_ratio
        The gap between what actually happened and what was expected
        given the input demand.
            0   -> perfectly fair: cars crossed in the same proportion
                   they were spawned in.
            > 0 -> the secondary road is being unfairly treated: the main
                   road is crossing proportionally more cars than its
                   demand alone would justify (secondary road starvation).
            < 0 -> the main road is being unfairly treated: it is crossing
                   proportionally fewer cars than its demand would justify
                   (main road waiting around for no good reason).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

SKIP_ROWS = 6


def generate(file_path, experiment_name):
    df = pd.read_csv(file_path, skiprows=SKIP_ROWS)
    epsilon = 0.0001  # avoids division by zero when blue-spawn or fluxo-azuis is 0

    # ratio of how many cars were spawned on the main road vs the secondary road
    df["demand_ratio"] = df["red-spawn"] / (df["blue-spawn"] + epsilon)

    # ratio of how many cars actually crossed on the main road vs the secondary road
    df["throughput_ratio"] = df["red-throughput"] / (df["blue-throughput"] + epsilon)

    # gap between the real crossing ratio and the expected demand ratio
    # positive: secondary road is penalized | negative: main road is penalized
    df["unfairness_index"] = df["throughput_ratio"] - df["demand_ratio"]

    df_agg = df.groupby(["red-spawn", "blue-spawn", "method"])["unfairness_index"].mean().reset_index()

    df_stop = df_agg[df_agg["method"] == "stop sign"].pivot(
        index="blue-spawn", columns="red-spawn", values="unfairness_index"
    ).sort_index(ascending=False)
    df_light = df_agg[df_agg["method"] == "red light"].pivot(
        index="blue-spawn", columns="red-spawn", values="unfairness_index"
    ).sort_index(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(18, 9))

    # main title
    fig.suptitle(
        "Unfairness: Demand Ratio vs. Throughput Ratio", fontsize=18, fontweight="bold", y=0.985
    )

    # short explanation of what the index measures, shown below the title
    fig.text(
        0.5, 0.945,
        "Unfairness Index = (crossing ratio between roads) − (spawn ratio between roads).\n"
        "It shows whether cars cross in the same proportion they were spawned in, or whether one road is favored beyond its actual demand.",
        ha="center", va="top", fontsize=11, style="italic", color="#444444",
    )

    # fixed color scale limits so both heatmaps are directly comparable
    vmin_lock, vmax_lock = -3, 3

    sns.heatmap(
        df_stop, cmap="RdBu_r", center=0, ax=axes[0], vmin=vmin_lock, vmax=vmax_lock,
        cbar_kws={"label": "Unfairness Index"},
    )
    axes[0].set_title("Stop Sign", fontsize=16, fontweight="bold", pad=15)
    axes[0].set_xlabel("Main Road Density (red-spawn %)", fontsize=12)
    axes[0].set_ylabel("Secondary Road Density (blue-spawn %)", fontsize=12)

    sns.heatmap(
        df_light, cmap="RdBu_r", center=0, ax=axes[1], vmin=vmin_lock, vmax=vmax_lock,
        cbar_kws={"label": "Unfairness Index"},
    )
    axes[1].set_title("Static Traffic Light", fontsize=16, fontweight="bold", pad=15)
    axes[1].set_xlabel("Main Road Density (red-spawn %)", fontsize=12)
    axes[1].set_ylabel("")

    # legend explaining what each color means
    plt.figtext(
        0.5, -0.05,
        "Red: Secondary Road is being unfairly treated (Starvation)  |  White: Perfect Balance  |  "
        "Blue: Main Road is being unfairly treated (Wasted Waiting)",
        ha="center", fontsize=13, fontweight="bold", bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    plt.tight_layout(rect=[0, 0, 1, 0.90])

    output_name = f"heatmap_unfairness_{experiment_name}.png"
    plt.savefig(output_name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved as '{output_name}'")


if __name__ == "__main__":
    generate("StressTest3_Semaforo_Pare-table.csv", "experiment3")