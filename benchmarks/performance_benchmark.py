import json
import os
import subprocess
import time

BENCHMARK_RESULTS_PATH = os.path.join("benchmarks", "benchmark_results.json")

# Define target scripts and their associated output assets
PIPELINES = [
    {
        "framework": "Matplotlib",
        "type": "Python (Imperative)",
        "script": "python/matplotlib_analytics.py",
        "asset": "assets/matplotlib_ev_trend.png",
    },
    {
        "framework": "Seaborn",
        "type": "Python (Statistical)",
        "script": "python/seaborn_analytics.py",
        "asset": "assets/seaborn_ev_distribution.png",
    },
    {
        "framework": "plotnine",
        "type": "Python (Grammar of Graphics)",
        "script": "python/plotnine_analytics.py",
        "asset": "assets/plotnine_ev_density_facet.png",
    },
    {
        "framework": "ggplot2",
        "type": "R (Grammar of Graphics)",
        "script": "r/ggplot2_analytics.R",
        "asset": "assets/ggplot2_ev_density_facet.png",
    },
]


def count_lines_of_code(filepath):
    """Counts non-empty, non-comment lines of code in a file."""
    if not os.path.exists(filepath):
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return len(
        [
            l
            for l in lines
            if l.strip() and not l.strip().startswith(("#", "//"))
        ]
    )


def run_benchmarks():
    """Executes all analytics scripts, records execution times and file sizes,

    and prints a structured comparison matrix.
    """
    print("[INFO] Starting Framework Performance & Brevity Benchmarks...\n")

    results = []

    for pipe in PIPELINES:
        script = pipe["script"]
        framework = pipe["framework"]
        framework_type = pipe["type"]
        asset = pipe["asset"]

        if not os.path.exists(script):
            print(f"[WARN] Script {script} missing. Skipping benchmark.")
            continue

        loc = count_lines_of_code(script)

        # Benchmark execution duration
        start_time = time.perf_counter()

        if script.endswith(".py"):
            cmd = ["python", script]
        elif script.endswith(".R"):
            cmd = ["Rscript", script]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            elapsed_time = time.perf_counter() - start_time
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Execution failed for {framework}: {e}")
            elapsed_time = 0.0

        # Calculate output asset file size in KB
        asset_size_kb = (
            os.path.getsize(asset) / 1024.0 if os.path.exists(asset) else 0.0
        )

        results.append(
            {
                "framework": framework,
                "type": framework_type,
                "loc": loc,
                "execution_time_sec": round(elapsed_time, 3),
                "asset_size_kb": round(asset_size_kb, 2),
            }
        )

    # Save metrics to JSON
    os.makedirs(os.path.dirname(BENCHMARK_RESULTS_PATH), exist_ok=True)
    with open(BENCHMARK_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Display clean ASCII performance table
    print("=" * 75)
    print(
        f"{'Framework':<12} | {'Paradigm / Type':<26} | {'LOC':<5} | {'Time (s)':<8} | {'Asset Size'}"
    )
    print("=" * 75)

    for r in results:
        print(
            f"{r['framework']:<12} | {r['type']:<26} | {r['loc']:<5} | {r['execution_time_sec']:<8.3f} | {r['asset_size_kb']} KB"
        )

    print("=" * 75)
    print(
        f"[SUCCESS] Benchmark results stored at {BENCHMARK_RESULTS_PATH}\n"
    )


if __name__ == "__main__":
    run_benchmarks()