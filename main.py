"""
Central script.

Set the file path and experiment name below and run this script.
It will ask which chart you want to generate:
    - Press Enter (leave it blank) to generate ALL charts.
    - Type a script name (e.g. "heatmap_delay" or "heatmap_delay.py")
      to generate only that one.

Each chart script saves its own file as:
    <chart_name>_<EXPERIMENT_NAME>.png
"""

from graph_scripts import (
    delay_comparison,
    grid_chart,
    heatmap_unfairness,
    heatmap_throughput,
    heatmap_delay,
    throughput_comparison,
)

# =============================================================================
# CONFIGURATION - edit these two lines for each experiment run
# =============================================================================
FILE_PATH = r"Experiment2\StressTest2.csv"
EXPERIMENT_NAME = "experiment3"

# maps the script name (without .py) to its module
AVAILABLE_CHARTS = {
    "grid_chart": grid_chart,
    "throughput_comparison": throughput_comparison,
    "delay_comparison": delay_comparison,
    "heatmap_throughput": heatmap_throughput,
    "heatmap_unfairness": heatmap_unfairness,
    "heatmap_delay": heatmap_delay,
}


def ask_which_chart():
    """Ask the user which chart to generate. Blank input means 'all'."""
    print("Available charts:")
    for name in AVAILABLE_CHARTS:
        print(f"  - {name}")

    choice = input("\nType a chart name to generate only that one, or press Enter to generate ALL: ").strip()

    # allow the user to type with or without the .py extension
    if choice.endswith(".py"):
        choice = choice[:-3]

    return choice


def main(file_path, experiment_name):
    choice = ask_which_chart()

    if choice == "":
        print(f"\nGenerating ALL charts for experiment '{experiment_name}' using '{file_path}'...")
        for module in AVAILABLE_CHARTS.values():
            module.generate(file_path, experiment_name)
        print("All charts generated successfully!")
        return

    module = AVAILABLE_CHARTS.get(choice)
    if module is None:
        print(f"\n'{choice}' is not a valid chart name. Please choose one of: {', '.join(AVAILABLE_CHARTS)}")
        return

    print(f"\nGenerating '{choice}' for experiment '{experiment_name}' using '{file_path}'...")
    module.generate(file_path, experiment_name)
    print(f"'{choice}' generated successfully!")


if __name__ == "__main__":
    main(FILE_PATH, EXPERIMENT_NAME)